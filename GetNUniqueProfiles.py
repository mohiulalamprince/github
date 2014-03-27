import os
import sys
from BusinessProfileParser import BusinessProfileParser

"""

GetNUniqueProfiles class is use for extract N profiles from  xBusinessProfile file.

input:
xBusinessProfile.xml
yBusinessProfile.xml

output:
ResultBusinessProfile.xml = N  profiles from (xBusinessProfile.xml-yBusinessProfile.xml

n(yBusinessProfiles) = number of profiles in yBusinessProfiles

"""

class GetNUniqueProfiles(BusinessProfileParser):
    
    def __init__(self,profileNeeded, outputFile=""):
        
        BusinessProfileParser.__init__(self)
        self.outputFile = open(os.path.join(outputFile, "ResutlBusinessProfile.xml"), "w")
        self.profileMap = {}
        self.isSave = True
        self.profileNeeded = profileNeeded
        self.profileFound = 0
        
    def getTagContent(self, thisContent, startTag, endTag):
        
        lbIDX = thisContent.find(startTag)
        
        if lbIDX == -1:
            return ""
        
        ubIDX = thisContent.find(endTag, len(startTag) + lbIDX)
        
        if ubIDX == -1:
            return ""
        
        return thisContent[lbIDX+len(startTag) : ubIDX].strip()
        
    def processProfile(self, thisProfile):

        strProfileInfo = self.getTagContent(thisProfile, "<COMPANY>", "</COMPANY>")
        strProfileInfo += "#" + self.getTagContent(thisProfile, "<PHONE>", "</PHONE>")
        
        #print strProfileInfo
        
        if self.isSave:           

            if not self.profileMap.has_key(strProfileInfo):
                self.profileMap[strProfileInfo] = True
            
            return True
        
        else:
            
            if not self.profileMap.has_key(strProfileInfo):
                
                self.profileFound += 1
                                
                self.outputFile.write(thisProfile)
                self.outputFile.flush()
                
                if self.profileFound >= self.profileNeeded:
                    return False
        
            return True            
            
    
    def get(self, xProfileLoc, yProfileLoc):        
                
        self.isSave = True
        
        self.parse(yProfileLoc)
        
        self.isSave = False
        self.profileFound = 0
        
        self.parse(xProfileLoc)
        
if __name__ == "__main__":
    
    folderName = "F:/OfficeWork/Development/BusinessSearch/Data/Profiles/Release 04-05-2011/"
    
    getNUniqueProfiles = GetNUniqueProfiles(34000, folderName)
    getNUniqueProfiles.get(folderName+"BusinessProfiles.xml", folderName+"BusinessProfileTotal3Release.xml")
    
    
        
            
            
            
        
        
        
        
