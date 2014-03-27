import os
import sys

class GetUniqueProfiles:
    
    def __init__(self):
        
        #self.outputLocation = os.path.join(outputDirectory, "BusinessProfiles.xml")
        self.companyNames = {}
        self.baseStartTag = "<COMPANY>"
        self.baseEndTag = "</COMPANY>"
        self.profileStartTag = "<BUSINESS_PROFILE"
        self.profileEndTag = "</BUSINESS_PROFILE>"
        
    def getTagContent(self, thisContent, startTag, endTag):
        
        lbIDX = thisContent.find(startTag)
        
        if lbIDX == -1:
            return ""
        
        ubIDX = thisContent.find(endTag, len(startTag) + lbIDX)
        
        if ubIDX == -1:
            return ""
        
        return thisContent[lbIDX+len(startTag) : ubIDX]
        
    def isUnique(self, thisProfile):
        
        thisCompany = self.getTagContent(thisProfile, self.baseStartTag, self.baseEndTag)
        thisCompany += "#" + self.getTagContent(thisProfile, "<PHONE>", "</PHONE>")
        
        if not self.companyNames.has_key(thisCompany):
            self.companyNames[thisCompany] = ""
            return True
        else:
            return False
        
    def getOutputLocation(self, inputLocation):
                
        pathIDX = inputLocation.rfind("\\")
        
        if pathIDX == -1:
            pathIDX = inputLocation.rfind("/")
            
        fileName = inputLocation[pathIDX+1:]    
        fileIDX = fileName.rfind(".")
        fileExtension =  fileName[fileIDX:]
        fileName = fileName[0:fileIDX] + "Unique"        
        
        return inputLocation[0:pathIDX+1] + fileName + fileExtension
        
    def getOutputLocationCommon(self, inputLocation):
                
        pathIDX = inputLocation.rfind("\\")
        
        if pathIDX == -1:
            pathIDX = inputLocation.rfind("/")
            
        fileName = inputLocation[pathIDX+1:]    
        fileIDX = fileName.rfind(".")
        fileExtension =  fileName[fileIDX:]
        fileName = fileName[0:fileIDX] + "Common"        
        
        return inputLocation[0:pathIDX+1] + fileName + fileExtension
        
    def doUnique(self, thisFileLocation):
        
        self.outputLocation = self.getOutputLocation(thisFileLocation);
        commonProfileLocation = self.getOutputLocationCommon(thisFileLocation)
        print "Output File Location: ", self.outputLocation
        print "Input File Location: ", thisFileLocation
        
        if not os.path.exists(thisFileLocation):
            
            print "No Such File : ", thisFileLocation
            return
                
        try:
            
            inputFile = open(thisFileLocation, "r")
            outputFile = open(self.outputLocation, "w")
            outputFileCommon = open(commonProfileLocation, "w")
            tempProfile = ""

            print "Processing ... "
                    
            for line in inputFile.readlines():
                
                tempProfile += line
                
                if line.find(self.profileEndTag) != -1:
                    if self.isUnique(tempProfile):                        
                        outputFile.write(tempProfile)
                        outputFile.flush()
                        #print tempProfile
                    else:
                        outputFileCommon.write(tempProfile)
                        outputFileCommon.flush()
                    tempProfile = ""
                        
                        
            print "Total Unique Profiles: ", len(self.companyNames)
            
        except:
            
            print "Exception During Processing"
            print "Exception: ", sys.exc_info()
            
        finally:
            
            if inputFile != None:
                inputFile.close()
                
            if outputFile != None:
                outputFile.close()
                
            if outputFileCommon != None:
                outputFileCommon.close()

if __name__ == "__main__":
    
    path = r"F:\OfficeWork\Development\BusinessSearch\Release\DataRelease 29-06-2011\Part with lat lng"
    getUniqueProfiles = GetUniqueProfiles()
    
    for fileName in os.listdir(path):
        if fileName.endswith(".xml"):
            getUniqueProfiles.companyNames = {}
            getUniqueProfiles.doUnique(os.path.join(path, fileName))
