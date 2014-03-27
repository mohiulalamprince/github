import os
import sys
import urlparse

class UniqueHostExtractor:
    
    def __init__(self, inDirectory=""):
        
        self.inDirectory = inDirectory
        self.allHosts = {}
        
    def getHostName(self, strLine):
        
        hostName = urlparse.urlparse(strLine)[1].strip()
                
        if len(hostName) == 0:
            return ''
        
        lbIDX = hostName.find('www.')
        
        if lbIDX != -1:
            hostName = hostName[lbIDX+4:]
            
        return hostName        
        
    def extract():
        
        outFile = open(os.path.join(self.inDirectory, "allUniqueHosts.txt"), "wb")
        
        for fileName in os.listdir(self.inDirectory):
            
            fileName = os.path.join(self.inDirectory, fileName)
            
            print 'Now Processing File: ', fileName
            
            inFile = open(fileName, 'rb')
            
            strLine = ''
            
            while True:
                
                strLine = inFile.readline().strip()
                
                if len(strLine) == 0 and inFile.tell() == os.path.getsize(fileName):
                    break
                
                hostName = self.getHostName(strLine)
                
                if not self.allHost.has_key(hostName):
                    
                    self.allHost[hostName] = True
                    outFile.write(strLine+"\n")
                    outFile.flush()
            
            inFile.close()
            
        outFile.close()
                    
                
if __name__ == '__main__':
    
     uniqueHostExtractors = UniqueHostExtractor('')
     uniqueHostExtractors.extract()

                
                
            
            
        