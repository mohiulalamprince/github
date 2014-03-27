
from BusinessProfileParser import BusinessProfileParser

class ProfileLatLngOmitor(BusinessProfileParser):
    
    def __init__(self):
        
        BusinessProfileParser.__init__(self)
        self.outputFile = None
        
    def getTagContent(self, thisContent, startTag, endTag):
        
        lbIDX = thisContent.find(startTag)
        
        if lbIDX == -1:
            return ""
        
        ubIDX = thisContent.find(endTag, len(startTag) + lbIDX)
        
        if ubIDX == -1:
            return ""
        
        return thisContent[lbIDX+len(startTag) : ubIDX].strip()
        
    def processProfile(self, thisProfile):
        
        strPostLatLng = self.getTagContent(thisProfile, "<POSSIBLE_LOTLAN>", "</POSSIBLE_LOTLAN>")
        strLng = "<LONGITUDE>\n\t\t" + self.getTagContent(strPostLatLng, "<LONGITUDE>", "</LONGITUDE>") + "\n\t</LONGITUDE>"
        strLat = "<LATITUDE>\n\t\t" + self.getTagContent(strPostLatLng, "<LATITUDE>", "</LATITUDE>") + "\n\t</LATITUDE>"
        
        thisProfile = thisProfile.replace(strPostLatLng, "")
        
        if thisProfile.find("<LONGITUDE>") == -1:        
            thisProfile = thisProfile.replace("<POSSIBLE_LOTLAN>\n", strLng)
            thisProfile = thisProfile.replace("</POSSIBLE_LOTLAN>", strLat)
                
        #print thisProfile
        
        self.outputFile.write(thisProfile)
        self.outputFile.flush()
        return True
        
        
    def omit(self, fileLocation):
        
        self.outputFile = open(fileLocation + "converted", "w")
        self.parse(fileLocation)
        
        
if __name__ == "__main__":
    
    profileLatLngOmitor = ProfileLatLngOmitor()
    profileLatLngOmitor.omit("F:\\OfficeWork\\Development\\BusinessSearch\\Data\\Profiles\\Release 04-05-2011\\LatLngFind\\BusinessProfiles.xml")
    
    
        
        
        
        
        
        
        
        
        
        