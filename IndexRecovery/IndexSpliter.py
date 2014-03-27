import os
import sys

class IndexSpliter:
    
    def __init__(self, inputDirectory, outputDirectory = ""):
        
        self.inputDirectory = inputDirectory
        self.outputDirectory = outputDirectory
        self.totalContentBlock = 0
        self.fileContentIndexBlock = []
        self.isPrintLog = True
        self.lastContentIndexBlock = 0
        self.totalIndexedByte = long(0)
        
    def printLog(self, strLog):
        
        if self.isPrintLog:
            print strLog
            
    def closeFile(self, thisFile):
        
        if thisFile != None:
            thisFile.close()

    def openFile(self, thisLocation, mode):
        
        filePointer = None
        
        try:
            filePointer = open(thisLocation, mode)
        except:
            print "Exception In openFile: ", thisLocation
            print "Exception: ", sys.exc_info()
        finally:
            return filePointer
    
    def saveURLInfo(self, strURLInfo, fileBlockNo):

        self.fileContentIndexBlock[fileBlockNo].write(strURLInfo)
        self.fileContentIndexBlock[fileBlockNo].flush()
    
    def dumpHostURLs(self, strURLsInfo, hostName):
        
        if len(strURLsInfo) == 0:
            self.printLog("No URL Found For Host: " + hostName)
        else:
            self.saveURLInfo(hostName +" "+ strURLsInfo[0] + " start\n", int(strURLsInfo[0].split(" ")[0]) - 1)
            
            for i in range(1, len(strURLsInfo)-1):
                self.saveURLInfo(hostName +" "+ strURLsInfo[i] + " continue\n", int(strURLsInfo[i].split(" ")[0]) - 1)
                
            self.saveURLInfo(hostName +" "+ strURLsInfo[-1] + " end\n", int(strURLsInfo[-1].split(" ")[0]) - 1)
                
    def processIndexFile(self, thisIndexFile):
        
        self.printLog("Now Processing Index File: " + thisIndexFile)
        
        inFile = None
        line = ""
        currentHostName = ""
        urlsInfo = ""
        self.lastContentIndexBlock = 0
        strHostURLsInfo = []
        
        try:            
            inFile = open(thisIndexFile, "r")
            
            while True:
                
                line = inFile.readline().strip()
                
                if len(line) == 0:
                    break
                
                if line.startswith("<"):                    
                    if line.startswith("</"):
                        self.dumpHostURLs(strHostURLsInfo, currentHostName)
                        self.printLog("Host Indexed: " + currentHostName)  
                        strHostURLsInfo = []
                        currentHostName = ""                       
                    else:
                        strHostURLsInfo = []
                        currentHostName = ""  
                        currentHostName = line[1:len(line)-1]                        
                        self.printLog("Host Indexing... : " + currentHostName)
                else:
                    strHostURLsInfo.append(line)
           
        except:
            print "Exception in processIndexFile."
            print "[Exception] ", sys.exc_info()
        finally:
            self.closeFile(inFile)
            self.printLog("Index File Processed: " + thisIndexFile)

    def split(self):
        
        self.printLog("Index Spliting ... ")
        
        if not os.path.exists(self.inputDirectory):
            print "Invalid Directory: ", self.inputDirectory
            return
        
        fileName = os.path.join(self.inputDirectory, "WebSite/Content/CurrentContentBlock.CM")
        
        if not os.path.exists(fileName):
            print "File Not Found: ", fileName
            return
        
        inFile = open(fileName, "r")        
        self.totalContentBlock = int(inFile.read().strip())
        inFile.close()
        
        self.totalContentBlock = 2 # HARD_CODED
        
        self.printLog("Total Content Block: "+ str(self.totalContentBlock))
        
        for i in range(1, self.totalContentBlock + 1):
            fileName = os.path.join(self.outputDirectory, str(i) + ".ContentIndex")
            self.fileContentIndexBlock.append(self.openFile(fileName, "w"))
            
        folderName = os.path.join(self.inputDirectory, "WebSite/Content/")
        
        folderName  = "E:\\ReCrawlHostDataLargest\\HostData\\WebSite\\Content"  # HARD_CODED
        
        for fileName in os.listdir(folderName):            
            if fileName.endswith(".INDEX"):
                self.processIndexFile(os.path.join(folderName, fileName))
        
        for i in range(len(self.fileContentIndexBlock)):
            self.closeFile(self.fileContentIndexBlock[i])
            
        self.sortContentIndexBlocks()
            
        self.printLog("Index Splitied.")
        
    def parseLine(self, thisLine):
        
        wTokens =  thisLine.split(" ")
        return filter(lambda x: len(x) > 0, wTokens)
        
    def sortContentIndexBlocks(self):
        
        for i in range(1, self.totalContentBlock + 1):
            
            urlsInfo = self.getURLInfo(i)
                        
            if len(urlsInfo) > 0:
                
                fileName = os.path.join(self.outputDirectory, str(i) + ".ContentIndex")
                
                self.printLog("Now Sorting : "+ fileName)
                urlsInfo.sort(compare)              
                self.printLog("File Sorted. :"+ fileName)
                
                try:
                    inFile = open(fileName, "w")
                    
                    for urlInfo in urlsInfo:
                        inFile.write(urlInfo.get()+"\n")
                        inFile.flush()                        
                except:
                    print "Exception in sortContentIndexBlocks()"
                    print "Exception: ", sys.exc_info()
                finally:
                    self.closeFile(inFile)
                    
    def getURLInfo(self, thisContentIndex, seekPosition = 0):
        
        urlsInfo = []
        inFile = None
        line = ""
        fileName = os.path.join(self.outputDirectory, str(thisContentIndex) + ".ContentIndex")
        
        print "File Name: ", fileName
        print "Seek: ", seekPosition
        countLine = 0        
        
        try:
            
            inFile = open(fileName, "rb")
            #inFile.seek(seekPosition)
            
            while True:
                
                line = inFile.readline().strip()
                
                if len(line) == 0:
                    break
                
                countLine += 1
                
                if countLine <= seekPosition:
                    continue                    
                
                wTokens = self.parseLine(line)

                if len(wTokens) >= 8: #and wTokens[6] == "1":
                    tempURLInfo = URLInfo()
                    tempURLInfo.setValues(wTokens)
                    self.totalIndexedByte += tempURLInfo.indexedByte
                    urlsInfo.append(tempURLInfo)
        except:
            print "Exception in getURLInfo()"
            print "Exception: ", sys.exc_info()
        finally:
            self.closeFile(inFile)            
            return urlsInfo  
        
class URLInfo:

    def __init__(self):
        
        self.contentNo = 0
        self.urlStartByte = 0
        self.urlEndByte = 0
        self.contentStartByte = 0
        self.contentEndByte = 0
        self.hostName = ""
        self.status = ""
        self.isValid = ""
        self.indexedByte = long(0)

    def setValues(self, thisValues):
        
        self.hostName = thisValues[0]
        self.contentNo = int(thisValues[1])
        self.urlStartByte = long(thisValues[2])
        self.urlEndByte = long(thisValues[3])
        self.contentStartByte = long(thisValues[4])
        self.contentEndByte = long(thisValues[5])
        self.isValid = thisValues[6]
        self.status = thisValues[7]
        
        self.indexedByte += long(self.contentEndByte-self.urlStartByte+1)
        
    def get(self):
        return self.hostName + " " + str(self.contentNo) + " " + str(self.urlStartByte) + " " + str(self.urlEndByte) + " " + str(self.contentStartByte) + " " + str(self.contentEndByte) + " " + str(self.isValid) + " " + str(self.status)

def compareValue(xValue, yValue):

    if xValue == yValue:
        return 0
    elif xValue > yValue:
        return 1
    else:
        return -1       
        
def compare(xURLInfo, yURLInfo):
    return compareValue(xURLInfo.urlStartByte, yURLInfo.urlStartByte)

if __name__ == "__main__":
    
    indexSpliter = IndexSpliter("\\\\192.168.1.68\\NewLargestData\\HostData")
    indexSpliter.split()
        
    #urlInfo = [URLInfo(), URLInfo(), URLInfo(), URLInfo()]
    #
    #urlInfo[0].contentNo = 3
    #urlInfo[1].contentNo = 1
    #urlInfo[2].contentNo = 0
    #urlInfo[3].contentNo = 1
    #
    #urlInfo[0].urlStartByte = 5
    #urlInfo[1].urlStartByte = 9
    #urlInfo[2].urlStartByte = -8
    #urlInfo[3].urlStartByte = -7
    #
    #urlInfo.sort(compare)
    #
    #for info in urlInfo:
    #    print info.contentNo
    #    print info.urlStartByte
    #    print ""
    #        
            
        
