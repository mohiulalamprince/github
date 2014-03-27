import os
import sys

class GetRepeatedData:
    
    def __init__(self, crawlerDir=""):
        
        self.crawlerDir = crawlerDir        
        
        
    def getStatus(self, hostName):
        
        print "Now Processing Host: ", hostName
        
        #cFolder = os.path.join(self.crawlerDir, "WebSite\LinkDB" , hostName, "DownloadedLinkPath")
        cFolder = hostName
        pDiff = 0
        pDiffURL = 0
        sameByte = 0
        totalPage = 0
        rangeLB = ""
        rangeUB = ""
        dataInContent = {}
        
        for fileName in os.listdir(cFolder):
            
            if fileName.endswith(".linkPath"):
                
                pDiff = 0
                pDiffURL = 0
                sameByte = 0
                totalPage = 0
                
                cFile = open(os.path.join(cFolder, fileName), "r")
                strLine = ""
                
                print "Now Processing File: ", cFile.name
                
                while True:
                    
                    strLine = cFile.readline()
                    
                    if len(strLine) == 0:
                        break
                    
                    wTokens = strLine.split(" ")
                    
                    stContentByte = long(wTokens[5])
                    enContentByte = long(wTokens[6])
                    
                    stURLByte = long(wTokens[3])
                    enURLByte = long(wTokens[4])
                    
                    #cDiff = enURLByte - stURLByte
                    cDiff = enContentByte - stContentByte
                    #pDiffURL = enURLByte - stURLByte
                    
                    if cDiff == pDiff:                            
                        
                        sameByte += cDiff
                        totalPage += 1
                        
                        rangeUB = strLine
                        
                    else:
                        
                        if sameByte != 0 and totalPage > 1:
                            
                            print "\nSame Byte In: ", cFile.name, "\nSize: ", float(sameByte / (1024*1024*8.0)), " MB \nPage: ", totalPage
                            print "Difference: ", pDiff
                            print "From: ", rangeLB.strip()
                            print "To: ", rangeUB
                            
                            cNo = rangeUB.split(" ")[2]
                            if dataInContent.has_key(cNo):
                                dataInContent[cNo] += sameByte
                            else:
                                dataInContent[cNo] = sameByte
                            
                            
                        sameByte = cDiff
                        totalPage = 1
                        rangeLB = strLine
                
                    pDiff = cDiff
                
                if sameByte != 0 and totalPage > 1:
                    
                    print "\nSame Byte In: ", cFile.name, "\nSize: ", float(sameByte / (1024*1024*8.0)), " MB \nPage: ", totalPage
                    print "Difference: ", pDiff
                    print "From: ", rangeLB.strip()
                    print "To: ", rangeUB
                    
                    cNo = rangeUB.split(" ")[2]
                    if dataInContent.has_key(cNo):
                        dataInContent[cNo] += sameByte
                    else:
                        dataInContent[cNo] = sameByte
                    
                cFile.close()
                
        for key in dataInContent.keys():            
            print "Repeated Data in Content: ", key ," is : ", float(dataInContent[key] / (1024*1024*8.0)) , " MB"
        
        print "Host Processed:  ", hostName
                    
    def start(self):
        
        linkDBDir = os.path.join(self.crawlerDir, "WebSite/LindDB")
        
        for fileName in os.listdir(linkDBDir):            
            if os.path.isdir(fileName):                
                self.getStatus(fileName)
                
if __name__ == "__main__":
    
    getRepeatedData = GetRepeatedData("E:\\www.numatic.co.za\\HostData\\")
    getRepeatedData.getStatus("E:\\www.numatic.co.za_\\HostData\\WebSite\\LinkDB\\www.numatic.co.za\\DownloadedLinkPath\\")
                
                
