import os
import sys

class ReIndexDirectoryList:
    
    def __init__(self, thisDir = os.getcwd()):
        
        self.workingDirectory = thisDir
        self.data = ""
        self.profiles = {}
    
    def getTagContent(self, thisContent, startTag, endTag):
        
        lbIDX = thisContent.find(startTag)
        
        if lbIDX == -1:
            return ""
        
        ubIDX = thisContent.find(endTag, len(startTag) + lbIDX)
        
        if ubIDX == -1:
            return ""
        
        return thisContent[lbIDX+len(startTag) : ubIDX].strip()
            
    def index(self):
        
        fileBusinessDirList = open(os.path.join(self.workingDirectory, "BusinessDirectoryList.xml"), "r")
        fileDataFoundURL = open(os.path.join(self.workingDirectory, "DataFoundURL.xml"), "r")
        
        fileDataFoundURLReIndex = open(os.path.join(self.workingDirectory, "DataFoundURL.xml.tmp"), "w")
        
        self.data = fileBusinessDirList.read()
        fileBusinessDirList.close()       

        
        lb = 0
        ub = 0
        
        while True:
            
            ub = self.data.find("</PROFILE>", lb)
            
            if ub == -1:
                break
            
            hostName = self.getTagContent(self.data[lb:ub+10], "<URL>", "</URL>")
            tempProfile = Profile(lb, ub+10)
            self.profiles[hostName] = tempProfile
            print self.data[tempProfile.lb:tempProfile.ub]
            
            lb = ub + 10
            
        fileBusinessDirList = open(os.path.join(self.workingDirectory, "BusinessDirectoryList.xml"), "w")
        fileBusinessDirListIndex = open(os.path.join(self.workingDirectory, "BusinessDirectoryList.index"), "w")
            
        line = ""
        strContent = ""
        
        szDataFoundURL = os.path.getsize(fileDataFoundURL.name)
        startByte = 0
        endByte = 0
            
        while True:
            
            line = fileDataFoundURL.readline()
            
            if len(line) == 0 and szDataFoundURL <= fileDataFoundURL.tell():
                break            
                        
            if line.strip().startswith("<PROFILE>") and len(strContent) > 0:
                                
                strContent += "\n\t</URL_LIST>\n</PROFILE>\n"
                hostName = self.getTagContent(strContent, "<HOST>", "</HOST>")               
                
                print "Host Name: ", hostName
                print strContent
                
                fileName = os.path.join(self.workingDirectory, "DataFoundURL.xml.tmp")
                
                startByte = os.path.getsize(fileName)
                fileDataFoundURLReIndex.write(strContent)
                fileDataFoundURLReIndex.flush()                
                endByte = os.path.getsize(fileName)
                
                tempProfile = self.profiles[hostName]
                strContent = self.data[tempProfile.lb:tempProfile.ub]
                strContent = strContent.replace("<START_BYTE>" + self.getTagContent(strContent, "<START_BYTE>", "</START_BYTE>") + "</START_BYTE>", "<START_BYTE>" + str(startByte) + "</START_BYTE>")
                strContent = strContent.replace("<END_BYTE>" + self.getTagContent(strContent, "<END_BYTE>", "</END_BYTE>") + "</END_BYTE>", "<END_BYTE>" + str(endByte) + "</END_BYTE>")
                
                startByte = os.path.getsize(fileBusinessDirList.name)
                fileBusinessDirList.write(strContent)
                fileBusinessDirList.flush()
                endByte = os.path.getsize(fileBusinessDirList.name)
                
                fileBusinessDirListIndex.write(hostName + " " + str(startByte) + " " + str(endByte) + "\n")
                fileBusinessDirListIndex.flush()
                
                strContent = ""
                
            strContent += line
            
        fileBusinessDirList.close()
        fileDataFoundURL.close()
        fileDataFoundURLReIndex.close()
        fileBusinessDirListIndex.close()
        
class Profile:
    
    def __init__(self, lb, ub):
        
        self.lb = lb
        self.ub = ub
        
if __name__ == "__main__":
    
    reIndexDirectoryList = ReIndexDirectoryList("E:\\ReCrawlHostDataLargest\\HostData\\Script\\DirectoryDetector\\BusinessData\\Recover")
    reIndexDirectoryList.index()
