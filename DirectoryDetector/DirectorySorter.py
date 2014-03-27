import os
import sys
import FindOutSingleProfileInformation

class DirectorySorter:
    
    def __init__(self):
        
        self.data = ""
        self.isPrintLog = True
        self.totalDataFoundPages = 0
        self.totalPhones = 0
        self.totalPages = 0
        self.totalDataFoundPagesFor100 = 0
        self.totalPagesFor100 = 0
        self.totalPhonesFor100 = 0
        self.totalProfileFor100 = 0        
        
    def closeFile(self, thisFile):
        
        if thisFile != None:
            thisFile.close()
    
    def printLog(self, logMsg):
        
        if self.isPrintLog:
            print logMsg    
            
    def getTagData(self, lbIDX, ubIDX, stTag, endTag):
        
        lb = 0
        ub = 0
        
        lb = self.data.find(stTag, lbIDX, ubIDX)
        
        if lb == -1:
            return 0
        
        ub = self.data.find(endTag, lb + len(stTag), ubIDX)
        
        if ub == -1:
            return 0
        
        return int(self.data[lb + len(stTag):ub])    
            
    def getPhone(self, lbIDX, ubIDX):
        
        lb = 0
        ub = 0
        
        lb = self.data.find("<PHONE>", lbIDX, ubIDX)
        
        if lb == -1:
            return 0
        
        ub = self.data.find("</PHONE>", lb + 7, ubIDX)
        
        if ub == -1:
            return 0
        
        return int(self.data[lb + 7:ub])        
    
    def getProfile(self, lbIDX, ubIDX):
        
        profile = ProfileInfo()
        
        profile.lb = lbIDX
        profile.ub = ubIDX
        profile.totalPhones = self.getTagData(lbIDX, ubIDX, "<PHONE>", "</PHONE>")
        profile.totalPages = self.getTagData(lbIDX, ubIDX, "<TOTAL_PAGES>", "</TOTAL_PAGES>")
        profile.totalDataFoundPages = self.getTagData(lbIDX, ubIDX, "<TOTAL_PAGES_DATA_FOUND>", "</TOTAL_PAGES_DATA_FOUND>")
        #self.printLog("Phone: " + str(profile.phone))
        
        return profile        
        
    def sort(self, thisFileLoc):
        
        cDir = thisFileLoc
        thisFileLoc = os.path.join(thisFileLoc, "BusinessDirectoryList.xml")
        
        if not os.path.exists(thisFileLoc):
            print "File Not Found: ", thisFileLoc
            return
        
        inFile = None
        outFile = None
        profileList = None
        
        self.printLog("Now Sorting ... :" + thisFileLoc)
        
        #try:
    #    
        inFile = open(thisFileLoc, "r")
        dataSize = 32*1024*1024
        
        while True:
            
            dataBuffer = inFile.read(dataSize)
            
            if len(dataBuffer) == 0:
                break
            
            self.data += dataBuffer
            
        #print self.data
        
        self.printLog("Profile Loaded.")
            
        profileList = self.processData()
        
        self.printLog("Total Profile Found: " + str(len(profileList)))
        
        profileList.sort(cmp=compare)
        
        #fileName = thisFileLoc[0:thisFileLoc.rfind(".")] + "Sorted.xml"
        #fileName = "DirectoryListSortedByPHONE.xml"
        fileName = os.path.join(cDir, "DirectoryListSortedByPHONE.xml")
        
        outFile = open(fileName, "w")
        
        strData = "<STATISTIC>"
        strData += "\n\t<TOTAL_PAGES>" + str(self.totalPages) + "</TOTAL_PAGES>"
        strData += "\n\t<TOTAL_DATA_FOUND_PAGES>" + str(self.totalDataFoundPages) + "</TOTAL_DATA_FOUND_PAGES>"
        strData += "\n\t<TOTAL_PHONES>" + str(self.totalPhones) + "</TOTAL_PHONES>"
        strData += "\n</STATISTIC>\n"
        
        strData += "<STATISTIC_FOR_100>"
        strData + "\n\t<PROFILE>" + str(self.totalProfileFor100) +"</PROFILE>"
        strData += "\n\t<TOTAL_PAGES>" + str(self.totalPagesFor100) + "</TOTAL_PAGES>"
        strData += "\n\t<TOTAL_DATA_FOUND_PAGES>" + str(self.totalDataFoundPagesFor100) + "</TOTAL_DATA_FOUND_PAGES>"
        strData += "\n\t<TOTAL_PHONES>" + str(self.totalPhonesFor100) + "</TOTAL_PHONES>"
        strData += "\n</STATISTIC_FOR_100>\n"
                    
        outFile.write(strData)
        outFile.flush()
        
#            for profile in profileList:
#                outFile.write(self.data[profile.lb:profile.ub]+"\n")
#                outFile.flush()

        for i in range(len(profileList)):

            profile = profileList[i]
            strProfile = self.data[profile.lb:profile.ub]
            strProfile = strProfile.replace("<PROFILE>", "<PROFILE NO: "+ str(i+1) +" >")
            outFile.write(strProfile + "\n")
            outFile.flush()
            
        print os.path.dirname(thisFileLoc)
        FindOutSingleProfileInformation.findOutTheNumberOfSingleProfile(os.path.dirname(thisFileLoc), self.totalProfileFor100)
            
        #except:
        #    print "Exception in sort()"
        #    print "Exception: ", sys.exc_info()
        #finally:
        #    self.closeFile(inFile)
        #    self.closeFile(outFile)
            
        self.printLog("File Sorted:" + thisFileLoc)            
            
    def processData(self):
        
        lbIDX = 0
        ubIDX = 0
        profileList = []
        
        while True:   
                        
            lbIDX = self.data.find("<PROFILE>", ubIDX)
            
            if lbIDX == -1:
                break
            
            ubIDX = self.data.find("</PROFILE>", lbIDX + 9)
            
            if ubIDX == -1:
                break
            
            tempProfile = self.getProfile(lbIDX, ubIDX+10)
            self.totalDataFoundPages += tempProfile.totalDataFoundPages
            self.totalPages += tempProfile.totalPages
            self.totalPhones += tempProfile.totalPhones
            
            if tempProfile.totalPhones >= 100:
                
                self.totalDataFoundPagesFor100 += tempProfile.totalDataFoundPages
                self.totalPagesFor100 += tempProfile.totalPages
                self.totalPhonesFor100 += tempProfile.totalPhones
                self.totalProfileFor100 += 1
            
            profileList.append(tempProfile)
            ubIDX += 10
            
        return profileList
    
def compare(xProfile, yProfile):    
    return yProfile.totalPhones - xProfile.totalPhones      
            
class ProfileInfo:
    
    def __init__(self):
        
        self.lb = 0
        self.ub = 0
        self.totalPages = 0
        self.totalDataFounds = 0
        self.totalPhones = 0
        
        
if __name__ == "__main__":
    
    directorySorter = DirectorySorter()
    #directorySorter.sort("E:/ReCrawlHostDataLargest/HostData/Script/DirectoryDetector/BusinessData/BusinessDirectoryList.xml")
    directorySorter.sort("DirectoryDetectorData")    
