import os
import sys


class BusinessProfileParser:
    
    def __init__(self):
        
        self.profileStTag = "<PROFILE"
        self.profileEnTag = "</PROFILE>"
        
    def getTagData(self, thisContent, stTag, enTag):
        
        lbIDX = thisContent.find(stTag)
        
        if lbIDX == -1:
            return ""
        
        lbIDX += len(stTag)
        ubIDX = thisContent.find(enTag, lbIDX)
        
        if ubIDX == -1:
            return ""
        
        return thisContent[lbIDX:ubIDX].strip()
        
    """    
    return True if need to extract more profiles otherwise False indicate no more profile parsing
    """
    def processProfile(self, thisProfile):
        pass
    
    def parse(self, thisFile):
        
        inFile = None
        tempProfile = ""
        line = ""
        
        if not os.path.exists(thisFile):
            print "File Not Found: ", thisFile
            return        
        
        try:
            
            print "Now Parsing: ", thisFile
            
            inFile = open(thisFile, "r")
            
            for line in inFile.readlines():
                
                line = line.strip()
                
                tempProfile += line
                
                if line.startswith(self.profileEnTag):
                    if not self.processProfile(tempProfile):
                        print "No More Profile Needed."
                        break
                    
                    tempProfile = ""
                    
            print "Parsing Completed: ", thisFile
            
        except:
            
            print "Exception in parse()"
            print "Exception: ", str(sys.exc_info())
            
        finally:
            
            if inFile != None:
                inFile.close()


class BusinessProfileAttributeParser(BusinessProfileParser):
    
    def __init__(self):
        
        BusinessProfileParser.__init__(self)
        self.allHostName = {}
        
    def processProfile(self, thisProfile):
        
        hostName = self.getTagData(thisProfile, "<URL>", "</URL>")
        totalPhone = int(self.getTagData(thisProfile, "<PHONE>", "</PHONE>"))
        
        if totalPhone >= 100:
            
            if not hostName.startswith("http"):
                hostName = "http://" + hostName
            
            if not hostName.endswith("/"):
                hostName += "/"
                
            if not self.allHostName.has_key(hostName):                
                self.outFile.write(hostName+"\n")
                self.outFile.flush()
                self.allHostName[hostName] = True
            else:
                print "Duplicate Host: ", hostName
            
        return True
            
    def start(self, folderLoc = ""):
        
        self.outFile = open(os.path.join(folderLoc, "HostName.txt"), "w")
        
        for fileName in os.listdir(folderLoc):            
            if fileName.endswith(".xml"):                
                self.parse(os.path.join(folderLoc, fileName))
            
        self.outFile.close()        

if __name__ == "__main__":
    
    businessProfileAttributeParser = BusinessProfileAttributeParser()
    businessProfileAttributeParser.start("F:\\OfficeWork\\Development\\BusinessSearch\\Data\\HostFromDirectoryList")
        