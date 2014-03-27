import os
from BusinessProfileParser import BusinessProfileParser

class TopHost(BusinessProfileParser):
    
    def __init__(self):
        
        BusinessProfileParser.__init__(self)
        self.outputFile = open("TopHostList.txt", "w")
        self.hostNames = {}
        
    def processProfile(self, thisProfile):
        
        phone = self.getTagContent(thisProfile, "<PHONE>", "</PHONE>")
        print phone
        cntPhone = int(phone)
        
        if cntPhone >= 100:
            
            hName = self.getTagContent(thisProfile, "<URL>", "</URL>")
            
            print hName
            
            if not self.hostNames.has_key(hName):
            
                self.hostNames[hName] = True
                self.outputFile.write(hName + "\n")
                self.outputFile.flush()
                
            return True
        else:
            return False
        
            
    def getTopHost(self, inDir):
        
        for fileName in os.listdir(inDir):
            self.parse(os.path.join(inDir, fileName))
                        
            
if __name__ == "__main__":
    
    topHost = TopHost()
    topHost.getTopHost("E:/topHost/")
    