import os
import sys

class UniqueProfilesExtractor:
    
    def __init__(self, outputDirectory = ""):
        
        self.outputLocation = os.path.join(outputDirectory, "BusinessProfiles.xml")
        self.companyNames = {}
        self.baseStartTag = "<COMPANY>"
        self.baseEndTag = "</COMPANY>"
        self.profileStartTag = "<BUSINESS_PROFILE"
        self.profileEndTag = "</BUSINESS_PROFILE>"
        
        
        
    def doUnique(self, inputFileLocation):
        
        if not os.path.exists(inputFileLocation):
            print "No Such File: ", inputFileLocation
            return
        
        try:
            inputFile = open(inputFileLocation, "r")
            outputFile = open(self.outputLocation, "w")
        except:
            
            
            print "Exception: ", sys.exc_info()
        finally:
            
            if inputFile != None:
                inputFile.close()
            
            if outputFile != None:
                outputFile.close()

if __name__ == "__main__":
    
    getUniqueProfiles = UniqueProfilesExtractor("D:/New Folder")
    getUniqueProfiles.doUnique("D:/New Folder/www.albertonpropertyforsale.co.zaOut.xml")
