import time
import sys
import os

class SequentialDataReader:
    
    def __init__(self, crawledDataLoc, dataSZ = 1024*1024*32):
        
        self.crawledDirectory = crawledDataLoc
        self.dataSZ = dataSZ
        
    def read(self):
        
        inFile = open(os.path.join(self.crawledDirectory, "WebSite\Content\CurrentContentBlock.CM"), "r")
        totalContentBlock = int(inFile.read().strip())
        inFile.close()
        
        readSZ = 0
        contentBlock = 1
        
        fileName = os.path.join(self.crawledDirectory, "WebSite/Content/" + str(contentBlock) + ".CONTENT")
        inFile = open(fileName, "r")
                
                                
        for i in range(1000):            
            
            if readSZ + self.dataSZ > os.path.getsize(fileName):
                print "Block Changing ... "
                inFile.close()
                contentBlock += 1
                readSZ = 0
                
                if contentBlock > totalContentBlock:
                    break
                
                fileName = os.path.join(self.crawledDirectory, "WebSite/Content/" + str(contentBlock) + ".CONTENT")
                inFile = open(fileName, "r")
            
            startTime = time.clock()
            inFile.read(self.dataSZ)
            print "Time to Read: ", (time.clock()-startTime)
            readSZ += self.dataSZ
            
                
                
if __name__ == "__main__":

    sequentialDataReader = SequentialDataReader("E:/ReCrawlHostDataLargest/HostData")
    sequentialDataReader.read()
    
        
        