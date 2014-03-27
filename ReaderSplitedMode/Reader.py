#!/usr/bin/env python

import os
import sys
import time
from IndexSpliter import IndexSpliter
from IndexSpliter import URLInfo
from Robustness import Robustness

class Reader:
    
    def __init__(self, inputDirectory, outputDirectoy = "", readSZ = 32):
        
        self.inputDirectory = inputDirectory
        self.outputDirectoy = outputDirectoy
        self.indexSpliter = IndexSpliter(self.inputDirectory)
        self.configFileName = None
        self.currentContentIndexBlockNo = 0
        self.lastIndexSeekPosition = 0
        self.lastContentSeek = 0
        self.contentFileSZ = 0
        self.isPrintLog = True
        self.contentFile = None
        self.readSZ = readSZ * 1024 *1024
        self.cahcheData = []        
        self.data = []
        self.robustWrite = Robustness()
        
        self.totalURLsInLastBlock = 0
        self.stTotalURLsTime = time.clock()
        self.totalRuningTime = 0
        self.totalDataProcessed = long(0)
        self.totalContentSize = long(0)
        self.totalDocs = long(0)
        self.stTotalRunningTime = time.clock()
        
    def printLog(self, strLog):
        
        if self.isPrintLog:
            print strLog
            
    def closeFile(self, thisFile):
        
        if thisFile != None:
            thisFile.close()
            
    def getLastProcessedIndex(self):
        
        self.configFileName = os.path.join(self.outputDirectoy, "lastProcessed.config")
        
        self.currentContentIndexBlockNo = 1
        self.lastIndexSeekPosition = 0

        robustFile = Robustness()
        robustFile.setPath(self.configFileName)
        data = robustFile.read()
        data = robustFile.getNthValue(data)
        
        if len(data) > 0:

            wTokens = data.split("#")
                
            if len(wTokens) > 1:
                self.currentContentIndexBlockNo = int(wTokens[0])
                self.lastIndexSeekPosition = long(wTokens[1])
                
    def processData(self, thisHostName, thisURL, thisContent):
        #print "URL: ", thisURL
        self.totalURLsInLastBlock += 1
        #pass
    
    def startHost(self, thisHostName):
        pass

    def endHost(self, thisHostName):
        pass
    
    def printStatus(self):
               
        pTime = (time.clock()-self.stTotalURLsTime)/60
        dataLeft = self.totalContentSize - (self.totalDataProcessed/(1024*1024))
        self.totalDocs += self.totalURLsInLastBlock
        self.totalRuningTime += (time.clock()-self.stTotalRunningTime)/60
        self.stTotalRunningTime = time.clock()
        
        if self.totalDataProcessed != 0:
            tLeft = ((self.totalRuningTime * dataLeft)/(self.totalDataProcessed/(1024*1024)))
        else:
            tLeft = 0.0            
        
        self.printLog("\nCurrent Content Block          : " + ("%10ld")%self.currentContentIndexBlockNo + " CONTENT") 
        self.printLog("Total Content Size             : " + ("%10.0lf")%self.totalContentSize + " MB")
        self.printLog("Total Data Processed           : " + ("%10.0lf")%(self.totalDataProcessed/(1024*1024)) + " MB")
        self.printLog("Data Remaining                 : " +  ("%10.0lf")%dataLeft + " MB")
        self.printLog("Total Running Time             : " + ("%10.4lf")%self.totalRuningTime + " Min(s)")              
        self.printLog("Time Remaining                 : " + ("%10.4lf")%tLeft + " Min(s)")
        self.printLog("Total Documents Processed      : " + ("%10ld")%(self.totalDocs) + " DOCUMENTS")
        self.printLog("Total Documents in Last Block  : " + ("%10ld")%(self.totalURLsInLastBlock) + " DOCUMENTS")
        self.printLog("Process Time for Last Block    : " + ("%10.4lf")%pTime + " Sec(s)")
        
        strStaus = str(self.totalDataProcessed) + "#" + str(self.totalDocs) + "#" + str(self.totalRuningTime)
        self.dumpStatus(strStaus)
        
    def dumpStatus(self, thisStatus):
        
        outFile = None
        
        try:
            fileName = os.path.join(self.outputDirectoy, "lastStatus.config")
            outFile = open(fileName, "w")
            outFile.write(thisStatus)
        except:
            print "Exception in dumpStatus()"
            print "Exception: ", sys.exc_info()
        finally:
            self.closeFile(outFile)
            
    def readStatus(self):
        
        inFile = None
        fileName = os.path.join(self.outputDirectoy, "lastStatus.config")
        
        if not os.path.exists(fileName):           
            self.totalDataProcessed = long(0)
            self.totalDocs = long(0)
            self.totalRuningTime = 0
            return
        
        try:            
            inFile = open(fileName, "r")
            data = inFile.read().strip()
            wTokens = data.split("#")
            
            self.totalDataProcessed = long(wTokens[0])
            self.totalDocs = int(wTokens[1])
            self.totalRuningTime = float(wTokens[2])
            
        except:
            print "Exception in readStatus()"
            print "Exception: ", sys.exc_info()
        finally:
            self.closeFile(inFile)
            self.printStatus()
            
    def loadContent(self, seekPosition):
        
        if seekPosition <= 0:
            seekPosition = 1
            
        sz = self.readSZ
            
        if self.contentFileSZ < seekPosition + self.readSZ:
            sz = long(self.contentFileSZ - seekPosition)
                        
        self.robustWrite.setPath(self.configFileName)
        self.robustWrite.write(str(self.currentContentIndexBlockNo) + "#" + str(self.lastIndexSeekPosition)) 

        self.printStatus()

        self.totalDataProcessed += sz
        
        self.printLog("\nContent Loading ...")
        startTime = time.clock()
                
        self.contentFile.seek(seekPosition - 1)
        self.data = self.contentFile.read(sz)
        self.lastContentSeek = seekPosition - 1      
        
        rTime = (time.clock()-startTime)
        self.printLog("Content Loaded")
        self.printLog("Reading Time                   : " + ("10%.4lf")%(rTime) + " Sec(s)\n")
        
        self.totalURLsInLastBlock = 0
        self.stTotalURLsTime = time.clock()
                
    def read(self, startByte, endByte):
        
        if startByte > endByte:
            print "Invalid Byte Info, Start: ", startByte, " End: ", endByte
            return ""
        
        if (startByte > self.lastContentSeek + len(self.data))or (endByte > self.lastContentSeek + len(self.data)):
            self.loadContent(startByte)           
        
        lb = startByte - self.lastContentSeek -1
        ub = endByte - self.lastContentSeek

        return self.data[lb:ub]
        
    def readData(self, strURLInfo):
        
        urlInfo = strURLInfo
        
        strURL = self.read(urlInfo.urlStartByte, urlInfo.urlEndByte)
        strContent = self.read(urlInfo.contentStartByte, urlInfo.contentEndByte)        
        
        if urlInfo.status == "start":
            self.startHost(urlInfo.hostName)
            self.processData(urlInfo.hostName, strURL, strContent)
        elif urlInfo.status == "end":
            self.processData(urlInfo.hostName, strURL, strContent)
            self.endHost(urlInfo.hostName)
        else:
            self.processData(urlInfo.hostName, strURL, strContent)
                                    
    def processContentIndexBlock(self, indexNo):
        
        robustFile = Robustness()
        indexFileName = os.path.join(self.outputDirectoy, str(indexNo) + ".ContentIndex")
        contentFileName = os.path.join(self.inputDirectory, "WebSite/Content/" + str(indexNo) + ".CONTENT")
        inFile = None
        line = ""
        self.currentContentIndexBlockNo = indexNo
        
        self.printLog("Now Processing : " + indexFileName)
        startTime = time.clock()
        
        try:           
            self.contentFile = open(contentFileName, "rb")
            self.contentFileSZ = os.path.getsize(contentFileName)
            self.lastContentSeek = 0
            self.loadContent(0)
                         
            urlsInfo = self.indexSpliter.getURLInfo(indexNo, self.lastIndexSeekPosition)
            print "Len: ", len(urlsInfo)
            
            for urlInfo in urlsInfo:
                self.lastIndexSeekPosition += 1
                self.readData(urlInfo)            
        except:
            print "Exception in getLastProcessedIndex()"
            print "Exception: ", sys.exc_info()
        finally:
            self.closeFile(self.contentFile)
            self.lastIndexSeekPosition = 0
            self.printLog("ContentIndexBlock Processed. : " + indexFileName)
            self.printLog("Time Elpased For This Block: " + str((time.clock()-startTime)/60) + " Min(s)")
            self.printStatus()

    def start(self):
        
        self.getLastProcessedIndex()
        
        fileName = os.path.join(self.inputDirectory, "WebSite/Content/CurrentContentBlock.CM")
        
        if not os.path.exists(fileName):
            print "File Not Found: ", fileName
            return
        
        inFile = open(fileName, "r")        
        self.indexSpliter.totalContentBlock = int(inFile.read().strip())
        inFile.close()        
        
        self.printLog("CurrentContentIndexBlock: " + str(self.currentContentIndexBlockNo))
        self.printLog("Last Seek Position: " + str(self.lastIndexSeekPosition))
        self.printLog("Total Block: " + str(self.indexSpliter.totalContentBlock))
        
        if self.currentContentIndexBlockNo == 1 and self.lastIndexSeekPosition == 0:
            self.indexSpliter.split()

            
        tempLBIdex = self.currentContentIndexBlockNo
        self.getTotalContentSize();
        self.readStatus();
                    
        for indexNo in range(tempLBIdex, self.indexSpliter.totalContentBlock+1):
            self.processContentIndexBlock(indexNo)
            
        self.printLog("Data Reading Completed.")
        
    def getTotalContentSize(self):
        
        self.totalContentSize = 0
        
        for blockNo in range(1, self.indexSpliter.totalContentBlock + 1):
            fileName = os.path.join(self.inputDirectory, "WebSite/Content/" + str(blockNo) + ".CONTENT")
            self.totalContentSize += os.path.getsize(fileName)
            
        self.totalContentSize /= (1024 * 1024)
        
        self.printLog("Total Content Size: " + str(self.totalContentSize) + " MB")
        
if __name__  == "__main__":
    
    reader = Reader("E:/ReCrawlHostDataLargest/HostData")
    reader.start()
        
    
