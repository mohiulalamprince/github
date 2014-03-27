# -*- coding: utf-8 -*-
import os
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
from socket import timeout
import socket
import logging
import os

class Reader:

    def __init__(self, inDirectory, blockSize= 1024*1024*200):
        self.enable_downloader = False
        self.url_imageID_file_fp = None
        self.default_dir = "H:\\pic\\"
        self.image_counter = 0
        self.initilizeVariables()
        self.inputDirectory = inDirectory
        self.SZ = blockSize
        self.dataReadSize = blockSize                
        self.allHosts = {}
        self.allHostsName = []        
        self.loadHosts()
        self.contentFile = None

    def initilizeVariables(self):
        
        self.contentFile = None
        self.currentContentBlockNo = 0
        self.currentDataBlock = None
        self.currentDataBlockSize = 0
        self.lastSeekPosition = 0
        
    def parseLine(self, thisLine):
        
        wTokens =  thisLine.split(" ")
        return filter(lambda x: len(x) > 0, wTokens)

    def normalizeHostName(self, hostName):
        
        lbIDX = hostName.find("http://")
        ubIDX = hostName.find("/", lbIDX+7)

        if lbIDX < ubIDX :
            return hostName[lbIDX+7:ubIDX].strip()
        else:
            return ""

    def loadContentBlock(self, urlInfo):
        
        #inputFile = None
        isLoaded = False
        seekPosition = 0
        self.currentDataBlock = None
        self.currentContentBlockNo = urlInfo.contentNo
        contentFileName = os.path.join(self.inputDirectory, "WebSite/Content", str(urlInfo.contentNo) + ".CONTENT")

        if urlInfo.urlStartByte == 0:
            seekPosition = 0
        else:
            seekPosition = urlInfo.urlStartByte - 1

        contentFileSize = os.path.getsize(contentFileName)

        if contentFileSize > (seekPosition + self.dataReadSize):
            self.currentDataBlockSize = self.dataReadSize
        else:
            self.currentDataBlockSize = long(contentFileSize - seekPosition)

        if self.currentDataBlockSize < 0:
            self.currentDataBlockSize = self.dataReadSize

        print "ContentFileLocation: ", contentFileName
        print "ContentFileSize: ", contentFileSize
        print "CurrentDataBlockSize: ", self.currentDataBlockSize
        print "currentContentBlockNo: ",self.currentContentBlockNo
        print "SeekPosition: ", seekPosition        

        try:
            #inputFile = open(contentFileName, "rb")
            #inputFile.seek(seekPosition)
            #self.currentDataBlock = inputFile.read(self.currentDataBlockSize)
            self.contentFile.seek(seekPosition)
            print "file seeked"
            self.currentDataBlock = self.contentFile.read(self.currentDataBlockSize)
            print "file read"
            self.lastSeekPosition = seekPosition
            isLoaded = True            
        except:
            print "[Exception] ", sys.exc_info()        
            r = raw_input('')
            isLoaded = False
        finally:
            #self.closeFile(inputFile)
            return isLoaded                         

    def getURLAndContent(self, urlInfo):

        if urlInfo.contentNo != self.currentContentBlockNo:
            
            print "This URL Not in Current Content Block. Need to Switch Block."
            print "URLInfo: ", urlInfo.contentNo
            print "currentContentBlockNo: ", self.currentContentBlockNo

            contentFileName = os.path.join(self.inputDirectory, "WebSite/Content", str(urlInfo.contentNo) + ".CONTENT")
            self.closeFile(self.contentFile)

            if not os.path.exists(contentFileName):
                print "File Not Found"
                print "Path: ", contentFileName
                self.initilizeVariables()
                return "", ""
            
            self.contentFile = open(contentFileName, "rb")                        
            
            if not self.loadContentBlock(urlInfo):
                print "Unable to Load Content"
                self.initilizeVariables()
                return "", ""
            else:
                print "Block Loading Completed."

        if urlInfo.contentEndByte > (self.lastSeekPosition + len(self.currentDataBlock)):
            print "This URL Not in Current Content Block. Need to Load More Content."
            if not self.loadContentBlock(urlInfo):
                print "Unable to Load Content"
                self.initilizeVariables()
                return "", ""
            else:
                print "Block Loading Completed."
        
        strURL = self.read(urlInfo.urlStartByte, urlInfo.urlEndByte)
        strContent = self.read(urlInfo.contentStartByte, urlInfo.contentEndByte)
        return strURL, strContent
    
    def read(self, startByte, endByte):

        if startByte > endByte:
            print "Invalid Byte Info:"
            print "StartByte: ", startByte, " EndByte: ", endByte
            return ""       
        
        lb = startByte - self.lastSeekPosition - 1
        ub = endByte - self.lastSeekPosition

        return self.currentDataBlock[lb:ub]        
        
    def processHost(self, hostName = None, seekPosition = -1):

        if hostName == None:
            for hostName in self.allHostsName:
                self.getHostData(hostName, self.allHosts[hostName])
        elif seekPosition == -1:
            hostName = self.normalizeHostName(hostName)
            if self.allHosts.has_key(hostName):
                self.getHostData(hostName, self.allHosts[hostName])
            else:
                print "Host Not Found: ", hostName
        else:
            hostName = self.normalizeHostName(hostName)
            self.getHostData(hostName, seekPosition)
            
    def readHostData(self, hostURLsInfo):
        
        self.dataReadSize = self.SZ

        for urlInfo in hostURLsInfo:
           strURL, strContent = self.getURLAndContent(urlInfo)
           self.processData(strURL, strContent)

    def processData(self, thisURL, thisContent):

        self.enable_downloader = True

        if (self.enable_downloader == True):            
            content = thisContent
            
            soup = BeautifulSoup(content)
            imgs = soup.findAll("img",{"alt":True, "src":True})
            cnt = self.image_counter
            
            print "URL : " + thisURL
            self.url_imageID_file_fp = open(self.default_dir + "log.txt", "a+b")
            
            for img in imgs:
                img_url = img["src"]
                filename = os.path.join(self.default_dir, str(cnt))
                cnt = cnt +  1
                
                if (cnt <= 1291989):
                    self.image_counter = cnt
                    continue
                try:
                    print img_url

                    default_timeout = 30

                    socket.setdefaulttimeout(default_timeout)                    
                    img_data = urllib.urlopen(img_url).read()
                    
                    self.url_imageID_file_fp.write("<URL>" + str(thisURL) + "<URL><IMG_URL>" +
                                                   str(img_url) + "</IMG_URL>" + "<IMG_CNT>" + str(cnt) + "</IMG_CNT>\n")
                    
                    print "<URL>" + str(thisURL) + "<URL><IMG_URL>" + str(img_url) + "</IMG_URL>" + "<IMG_CNT>" + str(cnt) + "</IMG_CNT>"

                    f = open(filename,"wb")
                    f.write(img_data)
                    f.close()
                    print "Saved : " + img_url
                except Exception, e:
                    print "exception" + str(logging.exception(e))
                    pass
                self.image_counter = cnt
            self.url_imageID_file_fp.close()
        
    def getHostData(self, hostName, seekPosition):
        
        print "Now Processing: ", hostName
        print "Seek Position: ", seekPosition
        self.initilizeVariables()

        indexFileName = os.path.join(self.inputDirectory, "WebSite/Content/1.INDEX")
        inputFile = None
        urlsInfo = []

        if not os.path.exists(indexFileName):
            print "File Not Found"
            print "Path: ", finishedFileName
            return
        
        try:
            inputFile = open(indexFileName, "r")
            inputFile.seek(seekPosition)

            while True:
                line = inputFile.readline().strip()
                
                if len(line) == 0 or line == "</" + hostName + ">":
                    break
                            
                wTokens = self.parseLine(line)

                if len(wTokens) >= 6 and wTokens[5] == "1":
#                    print wTokens
                    tempURLInfo = URLInfo()
                    tempURLInfo.setValues(wTokens)
                    urlsInfo.append(tempURLInfo)                    
                    
        except:
            print "[Exception] ", sys.exc_info()
            print "Line: ", line
        finally:
            self.closeFile(inputFile)

        if len(urlsInfo) > 0:
            urlsInfo.sort(compare)
            self.readHostData(urlsInfo)            
                
        print "Host Processing Finished: ", hostName

    def loadHosts(self):

        print "Loading Hosts..."
        finishedFileName = os.path.join(self.inputDirectory, "HostConf/finishHostList.txt")
        inputFile = None

        if not os.path.exists(finishedFileName):
            print "File Not Found"
            print "Path: ", finishedFileName
            return

        try:
            inputFile = open(finishedFileName, "r")

            for line in inputFile.readlines():                
                wTokens = self.parseLine(line)
                if len(wTokens) >= 14:
                    #self.processHost(wTokens[1], long(wTokens[13]))
                    hostName = self.normalizeHostName(wTokens[1])
                    if not self.allHosts.has_key(hostName):
                        print "Host Loaded: ", hostName
                        self.allHostsName.append(hostName)
                        self.allHosts[hostName] = long(wTokens[13])
                    else:
                        print "Duplicate Host Found: ", hostName
                else:
                    print "Invalid Host Info: ", line
        except:
            print "[Exception] ", sys.exc_info()
        finally:
            self.closeFile(inputFile)
            
    def closeFile(self, thisFile):
        if thisFile != None:
            thisFile.close()            


class URLInfo:

    def __init__(self):
        
        self.contentNo = 0
        self.urlStartByte = 0
        self.urlEndByte = 0
        self.contentStartByte = 0
        self.contentEndByte = 0

    def setValues(self, thisValues):
        
        self.contentNo = int(thisValues[0])
        self.urlStartByte = long(thisValues[1])
        self.urlEndByte = long(thisValues[2])
        self.contentStartByte = long(thisValues[3])
        self.contentEndByte = long(thisValues[4])        

def compareValue(xValue, yValue):

    if xValue == yValue:
        return 0
    elif xValue > yValue:
        return 1
    else:
        return -1       
        
def compare(xURLInfo, yURLInfo):

    if xURLInfo.contentNo == yURLInfo.contentNo:
        return compareValue(xURLInfo.urlStartByte, yURLInfo.urlStartByte)
    else:
        return compareValue(xURLInfo.contentNo , yURLInfo.contentNo)

if __name__ == "__main__":

    reader = Reader("H:/nelly/HostData/")
    reader.processHost("http://www.nelly.com/")

    print "DONE"
