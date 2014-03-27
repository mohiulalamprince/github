import os
import sys

class BusinessProfileParser:
    
    def __init__(self):
        
        self.profileStTag = "<profile"
        self.profileEnTag = "</profile"
    """    
    return True if need to extract more profiles otherwise False indicate no more profile parsing
    """
    def processProfile(self, thisProfile):
        pass
    
    def getTagContent(self, content, stTag, enTag):

        tagContent = ""

        lb = content.find(stTag)

        if lb==-1:
            return ""

        ub = content.find(enTag)
        
        if ub == -1:
            return ""
        
        return content[lb+len(stTag):ub].strip()
    
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
                
                #line = line.strip()
                #print line
                
                tempProfile += line
                line = line.lower()
                
                if line.startswith(self.profileEnTag):
                    if not self.processProfile(tempProfile):
                        print "No More Profile Needed."
                        break
                    else:
                        print "Continue"
                    
                    tempProfile = ""
                    
            print "Parsing Completed: ", thisFile
            
        except:
            
            print "Exception in parse()"
            print "Exception: ", str(sys.exc_info())
            
        finally:
            
            if inFile != None:
                inFile.close()
        
        
        