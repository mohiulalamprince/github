#!/usr/bin/env python

import os
import sys

class GetHostNameFromDirectoryList:
    
    def __init__(self, thisDirectoryList, outputFolder = ""):
        
        self.thisDirectoryList = thisDirectoryList
        self.outputFolder = os.path.join(outputFolder, "RecentHostList.txt")
        self.outFile = open(self.outputFolder, "w")
        self.MAX_NUMBER = 100
        
    def getTagContent(self, thisData, stTag, enTag):
        
        idxLB = thisData.find(stTag)
        
        if idxLB != -1:            
            idxUB = thisData.find(enTag, idxLB + len(stTag))
            
            if idxUB != -1 :                
                return [True, thisData[idxLB + len(stTag) : idxUB]]
        
        return [False, ""]
        
    def formatHostName(self, thisHostName):
        
        if not thisHostName.startswith("http"):
            thisHostName = "http://" + thisHostName
            
        if not thisHostName.endswith("/"):
            thisHostName += "/"
            
        return thisHostName
    
    def parse(self):
        
        for fileName in os.listdir(self.thisDirectoryList):
            
            if fileName.endswith(".xml"):
                fileName = os.path.join(self.thisDirectoryList, fileName)
                self.parseHost(fileName)            
    
    def parseHost(self, cFileLoc):
        
        print 'Now Processing File: ', cFileLoc
        
        try:
        
            inFile = open(cFileLoc, "r")
            #outFile = open(self.outputFolder, "w")
            hostName = ""
            phoneNo = 0            
            
            for line in inFile.readlines():
                
                data = self.getTagContent(line, "<URL>", "</URL>")
                
                if data[0]:
                    hostName = data[1]
                else:
                    data = self.getTagContent(line, "<PHONE>", "</PHONE>")
                    
                    if data[0]:
                        phoneNo = int(data[1])
                        
                        if phoneNo >= self.MAX_NUMBER:
                            hostName = self.formatHostName(hostName)
                            self.outFile.write(hostName+"\n")
                            self.outFile.flush()
                            print "HostName: %s , PhoneNo: %d" % (hostName, phoneNo)
                        else:
                            print "[IGNORED] HostName: %s , PhoneNo: %d" % (hostName, phoneNo)
                            
        except:
            print "[EXCEPTION]: ", str(sys.exc_info())
            
        finally:
            inFile.close()
            #outFile.close()
            
            
if __name__ == "__main__":
    
    location = "D:\\OfficeWork\\Development\\WebCrawler\\BusinessSearch\\Data\\Output\\HostLargest\\Business Data\\"
    getHostNameFromDirectoryList = GetHostNameFromDirectoryList(location + "DirectoryListSortedByPHONE.xml", location)
    getHostNameFromDirectoryList.parseHost()     
