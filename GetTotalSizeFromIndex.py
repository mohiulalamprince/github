import os
import sys


class GetTotalSizeFromIndex:
    
    def __init__(self, inputDir, outputDir=os.getcwd()):
        
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.totalContentBlock = 0
        self.indexWiseContentSize = 0
        
        
    def getSize(self):
        
        outFile = open(os.path.join(self.outputDir, "CrawlerDataStatus.txt"), "wb")
        
        folderName = os.path.join(self.inputDir, "WebSite/Content")
        fileName = os.path.join(folderName, "CurrentContentBlock.CM")
        
        inFile = open(fileName, "r")        
        self.totalContentBlock = int(inFile.read().strip())
        inFile.close()
        
        self.indexWiseContentSize = []
        
        for i in range(self.totalContentBlock):
            self.indexWiseContentSize.append(long(0))
            
        for fileName in os.listdir(folderName):
            
            if fileName.endswith(".INDEX"):
                
                indexFileName = os.path.join(folderName, fileName)
                
                inFile = open(indexFileName, "rb")
                
                strLine = ""
                
                while True:
                    
                    strLine = inFile.readline().strip()
                    
                    if len(strLine) == 0:
                        break
                    
                    wTokens = strLine.split(" ")
                    
                    if len(wTokens) == 6:
                        
                        self.indexWiseContentSize[int(wTokens[0])-1] += long(wTokens[2]) - long(wTokens[1])
                        self.indexWiseContentSize[int(wTokens[0])-1] += long(wTokens[4]) - long(wTokens[3])
                    
        
        for i in range(self.totalContentBlock):
            
            fileName = os.path.join(folderName, str(i+1)+".CONTENT")
            
            contentSZ = os.path.getsize(fileName)
            strOut = "%s"%("Content No: " + str(i+1))
            strOut += "%40s"%("Content Size: " + str((contentSZ /(1024*1024))))
            strOut += "%40s"%("Index Wise Content Size: " + str((self.indexWiseContentSize[i-1] / (1024*1024))))
            strOut += "%40s"%("Missing Content Size: " + str(((contentSZ - self.indexWiseContentSize[i-1]) / (1024*1024))))
            print strOut
            outFile.write(strOut + "\n")
            outFile.flush()
            
        outFile.close()
            
        
if __name__ == "__main__":
    
    getTotalSizeFromIndex = GetTotalSizeFromIndex(r"E:\ReCrawlHostDataLargest\HostData")
    getTotalSizeFromIndex.getSize()
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
            
