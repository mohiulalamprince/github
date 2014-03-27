import os
import sys

class Robustness():
    
    filePth =   None
    logFile=None
    
    def __init__(self, filePath=""):
        self.filePth=filePath
        self.logFile=filePath+".log"

    def getNthValue(self, data, n=-1):

        if type(data) == list:
            if len(data) > 0:
                if len(data[0]) > 0:
                    return self.getNthValue(data[0], n)
                
                if len(data[1]) > 0:
                    return self.getNthValue(data[1], n)
                
            return ""
        
        elif len(data) > 0:
            dataTokens = data.split(" ")
            #print len(dataTokens)

            if n == -1:
                return data
            else:
                if len(dataTokens) >= n:
                    return dataTokens[n-1]

            return ""

        return ""       
        
                    
    def getPath(self):
        return self.filePth
    
    def setPath(self,filePath):
        #print "File Pointer Set to : ", filePath
        self.filePth=filePath
        self.logFile=filePath+".log"

    def checkPart(self):
        partFile=self.getPath()+".part"
        if os.path.exists(partFile):
            if os.path.exists(self.getPath()):
                os.remove(self.getPath())
            os.rename(partFile,self.getPath())

    def __readFileContent(self, thisFilePath):

        fileData = ""
        
        if os.path.exists(thisFilePath):
            
            try:
                inFile = open(thisFilePath, 'r')
                fileData = inFile.read()
            except:
                print "Unable to Process File. ", str(thisFilePath)
                print "[Exception] ", str(sys.exc_info())
                self.createLog("Unable to Process File. " + str(thisFilePath) + " [Exception] "+ str(sys.exc_info()))
            finally:
                inFile.close()

        return fileData
        

    def __readConfigFile(self):
        
        thisFilePath = self.getPath()
        thisFilePathPart = thisFilePath + ".part"
        fileDataList = []

        fileDataList.append(self.__readFileContent(thisFilePath))
        fileDataList.append(self.__readFileContent(thisFilePathPart))

        return fileDataList

    def __isValidDataPresent(self, configData, countValue):

        configValues = configData.split(" ")
        
        if len(configValues) == countValue:
            
            for value in configValues:
                if not self.__isNumericalData(value.strip()):
#                    print "Not", value
                    return False
        
            return True
        
        return False
        
    def __isNumericalData(self, value):        
        return value.isdigit()

    def __parseConfigFile(self, countValue):

        fileDataList = self.__readConfigFile()
        
        if len(fileDataList) > 0:

            if len(fileDataList[0]) > 0:
                if self.__isValidDataPresent(fileDataList[0], countValue):
                    return fileDataList[0]

            if len(fileDataList[1]) > 0:
                if self.__isValidDataPresent(fileDataList[1], countValue):
                    return fileDataList[1]
                
        return ""

    # Send list or string    
    def read(self, countValue = -1):

        #print "Data Reading Using Robustness ... "    

        if countValue == -1:
            return self.__readConfigFile()
        else:
            return self.__parseConfigFile(countValue)

    def write(self,content):
        
        #print "Data Writing Using Robustness : ", content
        
        filePath=self.getPath()
        
        if filePath==None or len(filePath)<2:
            print "Robustness.......[",filePath,"] Invalid filepath"
            return

        isFileRenamed=False
        tempFileName=filePath+".part"

        if os.path.exists(tempFileName):
            if os.path.exists(filePath):
                os.remove(filePath)
            os.renames(tempFileName, filePath)
        
        if os.path.exists(filePath):
            try:
                os.rename(filePath,tempFileName)                
                fc=open(filePath,"w")
                fc.write(str(content))                
                fc.close()
                isFileRenamed=True

            except IOError,strErr:
                self.createLog("IO ERROR["+str(strErr.code)+"] reason:"+str(strErr.reason) + "\n")
            except:
                self.createLog("ERROR saving "+filePath+" file.\n")
                print sys.exc_info()
        else:
            try:
                fc=open(filePath,"w")
                fc.write(content)
                fc.close()

            except IOError:
                self.createLog("IO ERROR")
            except:
                self.createLog("ERROR saving "+filePath+" file.")
                print sys.exc_info()
        try:
            if isFileRenamed:
                os.remove(tempFileName)
        except:
               self.createLog("ERROR removing temporary file "+tempFileName+" file.") 

    def  createLog(self,content):
        logPath=self.logFile
        fc=open(logPath,"a")
        fc.write(content)
        fc.close()

if __name__ == "__main__":

    robustness = Robustness("D:/bangladesh.config")
    robustness.write("10#5")
    rtnValue = robustness.read()
    print rtnValue
    value = robustness.getNthValue(rtnValue, 1)
    print "Value: ", value, "Type: ", type(value)
    
