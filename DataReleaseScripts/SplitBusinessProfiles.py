
from BusinessProfileParser import BusinessProfileParser

# split business profiles file with n profiles

class SplitBusinessProfiles(BusinessProfileParser):
    
    def __init__(self):
        
        BusinessProfileParser.__init__(self)
        self.outputFile = None
        self.profileFound = 0
        self.currentFileNo = 1
        self.profilePerFile = 0
        self.inputFileLocation = None
        
    def processProfile(self, thisProfile):
        
        self.profileFound += 1
        
        self.outputFile.write(thisProfile)
        self.outputFile.flush()
        
        if self.profilePerFile!= 0 and self.profileFound % self.profilePerFile == 0:
            self.currentFileNo += 1
            self.outputFile.close()
            self.outputFile = open(self.inputFileLocation +"."+ str(self.currentFileNo), "w")
            
        return True      
        
    def split(self, fileLocation, profilePerFile):        
        
        self.inputFileLocation = fileLocation 
        self.profilePerFile = profilePerFile
        self.outputFile = open(self.inputFileLocation +"."+ str(self.currentFileNo), "w")
        self.parse(self.inputFileLocation)
        
if __name__ == '__main__':
    
    splitBusinessProfiles = SplitBusinessProfiles()
    splitBusinessProfiles.split(r"F:\OfficeWork\Development\BusinessSearch\Data\Profiles\Release 29-06-2011\BusinessProileWithLatLon_29-06-2011(part 03).xml", 33113)
        
        
        
