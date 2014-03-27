import os
import sys
import time
from Reader import Reader
from Parser import Parser
from Hash2D import Hash2D
from DirectorySorter import DirectorySorter
from tkCommonDialog import Dialog
import tkFileDialog
from FileDialog import FileDialog
from LinkDb import LinkDb
from TypeDetector import TypeDetector

class DirectoryDetector(Reader):
    
    def __init__(self, inDirectory="../../", outDirectory=os.getcwd(), ramSize=32):
        
        Reader.__init__(self, inDirectory, os.path.join(outDirectory, 'DirectoryDetectorData'), ramSize)

        print "Input: ", inDirectory
        print "Output: ", os.path.join(outDirectory, 'DirectoryDetectorData')
        
        self.inputDirectory = inDirectory
        self.outputDirectory = os.path.join(outDirectory, 'DirectoryDetectorData')
        self.hostDataProcessor = {}
        self.mainDBFile = None
        self.mainDBIndex = None
        self.dataFoundURLFile = None
        #self.dataFoundURLIndex = None
                
        self.isPrintLog = True
        
        self.errorFile = open(os.path.join(outDirectory, "Error.log"), "w")
        sys.stderr = self.errorFile
        
    def closeFile(self, thisFile):
        
        if thisFile != None:
            thisFile.close()
        
    def printLog(self, logMsg):
        
        if self.isPrintLog:
            print logMsg

    def processData(self, thisHostName, thisURL, thisContent, urlInfo):
                
        if not self.hostDataProcessor.has_key(thisHostName):
            
            print "No Such Host Found in Data Processor : " + thisHostName
            dataProcessor = DataProcessor(thisHostName, self)
            self.hostDataProcessor[thisHostName] = dataProcessor
        else:
            self.hostDataProcessor[thisHostName].process(thisHostName, thisURL, thisContent, urlInfo)        
    
    def startHost(self, thisHostName):
        
        self.printLog("New Host Found: " + thisHostName)       
        
        if not self.hostDataProcessor.has_key(thisHostName):
            
            dataProcessor = DataProcessor(thisHostName, self)
            self.hostDataProcessor[thisHostName] = dataProcessor
            
        else:
            print "Host Already Under Processing : ", thisHostName        
    
    def endHost(self, thisHostName):        
        self.processEndofHost(thisHostName)
    
    def deleteFile(self, thisFile):
        
        if not os.path.exists(thisFile):
            print "No Such File Found For Delete: ", thisFile
            return
        
        try:        
            curFile = open(thisFile, "w")
            curFile.close()       
        
            os.remove(thisFile)            
        except:
            print "Exception in deleteFile()"
            print "Exception: ", sys.exc_info()       
    
    def processEndofHost(self, thisHostName):
        
        self.printLog("Data Dumping Host: " + thisHostName)
        startTime = time.clock()
        currentHostTotalPhones = 0
        
        if not self.hostDataProcessor.has_key(thisHostName):
            print "Invalid Host Name : ", thisHostName
            
        else:
            
            inFile = None
            
            try:
                #dataProcessor = self.hostDataProcessor.pop(thisHostName)
                dataProcessor = self.hostDataProcessor[thisHostName]
                
                #startByte = os.path.getsize(self.mainDBFile.name)
                #
                #strData = dataProcessor.getStatus()
                #self.mainDBFile.write(strData)
                #self.mainDBFile.flush()
                #
                #endByte = os.path.getsize(self.mainDBFile.name)
                #
                #strData = thisHostName +" "+ str(startByte) +" "+ str(endByte) + "\n"
                #self.mainDBIndex.write(strData)
                #self.mainDBIndex.flush()
                                                
                dataProcessor.file.write("\n\t<URL_LIST>\n</PROFILE>\n")
                dataProcessor.file.close()
                
                fileName = os.path.join(self.outputDirectory, thisHostName + ".db")
                inFile = open(fileName, "r")
                startByte = os.path.getsize(self.dataFoundURLFile.name)
                     
                self.printLog("Now Moving Data Found URL For Host: " + thisHostName)
                
                while True:
                    
                    data = inFile.read(32*1024*1024)
                    
                    if len(data) == 0:
                        break
                    
                    self.dataFoundURLFile.write(data)
                    self.dataFoundURLFile.flush()
                
                self.printLog("Data Found URL Moved For Host: " + thisHostName)
                
                endByte = os.path.getsize(self.dataFoundURLFile.name)
                        
                       
                strData = dataProcessor.getStatus(startByte, endByte)
                currentHostTotalPhones = dataProcessor.totalPhones 
                self.printLog("Total Phones: "+ str(currentHostTotalPhones))
                
                startByte = os.path.getsize(self.mainDBFile.name)
                
                self.mainDBFile.write(strData)
                self.mainDBFile.flush()
                
                endByte = os.path.getsize(self.mainDBFile.name)
                
                strData = thisHostName +" "+ str(startByte) +" "+ str(endByte) + "\n"
                self.mainDBIndex.write(strData)
                self.mainDBIndex.flush()                
                
                #strData = "<PROFILE>"
                #strData += "\n\t<HOST>" + thisHostName + "</HOST>"
                #strData += "\n\t<START>" + str(startByte) + "</START>"
                #strData += "\n\t<END>" + str(endByte) + "</END>"
                #strData += "\n</PROFILE>\n"
                #
                #self.dataFoundURLIndex.write(strData)
                #self.dataFoundURLIndex.flush()
                
                self.closeFile(inFile)
                                
                fileName = os.path.join(self.outputDirectory, thisHostName + ".db")  
                self.deleteFile(fileName)
                self.hostDataProcessor.pop(thisHostName)
            
            except:                
                print "Exception in processEndofHost()"
                print "Exception: " + sys.exc_info()              
                
        self.printLog("Data Dumped. Host: " + thisHostName)
        self.printLog("Time For Dumping: " + str(time.clock()-startTime))
        
        if currentHostTotalPhones < 100:
            self.printLog("Host Ingnored: "+ str(thisHostName))
            self.printLog("Total Phones: "+ str(currentHostTotalPhones))
            return
        
        self.printLog("LinkDB Writer Started For Host: "+ thisHostName)
        
##        cDir = os.path.join(self.inputDirectory, "WebSite/LinkDB/")        
##        configFileLocation = self.outputDirectory + "/config.txt"
##        
##        #print "InputDirectory: ", self.inputDirectory
##        #print "cDir: ", cDir
##        #print "configFileLocation: ", configFileLocation
##        
##        if os.path.exists(configFileLocation):            
##            configRead=open(configFileLocation,'r')
##        else:
##            configRead=open(configFileLocation,'w')
##            
##        configRead.close()
##        tempHostName = thisHostName
##        
##        hostFileLoc = os.path.join(cDir, tempHostName)
##        
##        if not os.path.exists(hostFileLoc):
##            tempHostName += ".tar"          
##        
##        if os.path.exists(os.path.join(cDir, tempHostName)):
##            
##            try:
##                linkDB = LinkDb()        
##                linkDB.doCrawl(tempHostName, cDir, self.outputDirectory, "RESTART")
##                self.printLog("LinkDB Writer Finished For Host: "+ tempHostName)
##            except:
##                print "Error: in LinkDB: ", tempHostName
        
    def getTagData(self, thisData, stTag, endTag):
        
        lb = thisData.find(stTag)
        
        if lb < 0:
            return ""
        
        ub = thisData.find(endTag, lb + len(stTag))
        
        if ub < 0:
            return ""
        
        return thisData[lb + len(stTag):ub].strip()
    
    def getDataProcessor(self, thisHostName):
        
        fileName = os.path.join(self.outputDirectory, thisHostName + ".db")
        inFile = None
        dataProcessor = DataProcessor(thisHostName, self)
        line = ""
        cPhone = 0
        
        try:
            
            inFile = open(fileName, "r")
            
            while True:
                
                line = inFile.readline().strip()
                
                if len(line) == 0:
                    break
                
                if line.startswith("<PHONE>"):
                    
                    tagData = self.getTagData(line, "<PHONE>", "</PHONE>")
                    
                    if len(tagData) == 0:
                        cPhone = 0
                    else:
                        cPhone = int(tagData)
                        
                    if cPhone != 0:
                        dataProcessor.totalPhones += cPhone
                        dataProcessor.totalDataFoundPages += 1
                    
                    dataProcessor.totalPages += 1                      
        except:
            print "Exception in getDataProcessor()"
            print "Exception: ", sys.exc_info()
        finally:
            self.closeFile(inFile)
            return dataProcessor
        
    def loadPreviousHosts(self):
        
        self.printLog("Loading Previous Host ... ")
        
        for fileName in os.listdir(self.outputDirectory):
            
            if fileName.endswith(".db"):
                
                hostName = fileName[0:fileName.rfind(".")]
                
                self.printLog("Loading Host: " + hostName)
                
                if not self.hostDataProcessor.has_key(hostName):
                    
                    dataProcessor = self.getDataProcessor(hostName)
                    self.hostDataProcessor[hostName] = dataProcessor                    
                
                self.printLog("Host Loaded: " + hostName)
                
        self.printLog("Previous Hosts Loaded")
        
    def checkUnFinishedHosts(self):
        
        self.printLog("Checking UnFinished Host")
                
        for fileName in os.listdir(self.outputDirectory):
            
            if fileName.endswith(".db"):
                
                hostName = fileName[0:fileName.rfind(".")]
                
                self.printLog("Finishing UnFinished Host: " + hostName)
                
                if not self.hostDataProcessor.has_key(hostName):
                    print "Host Not Found in Host Data Processor: ", hostName
                    dataProcessor = self.getDataProcessor(hostName)
                    self.hostDataProcessor[hostName] = dataProcessor
                                
                self.processEndofHost(hostName)
                    
                self.printLog("Host Finished: " + hostName)
        
        self.printLog("UnFinished Hosts Check Completed")
    
    def detect(self):
        
        if not os.path.exists(self.outputDirectory):
            os.mkdir(self.outputDirectory)            
                
        try:
            
            self.printLog("Directory Detection Started")
            
            fileName = os.path.join(self.outputDirectory, "BusinessDirectoryList.xml")
            
            if not os.path.exists(fileName):
                self.mainDBFile = open(fileName, "w")
            else:
                self.mainDBFile = open(fileName, "a")
            
            fileName = os.path.join(self.outputDirectory, "BusinessDirectoryList.index")
            
            if not os.path.exists(fileName):
                self.mainDBIndex = open(fileName, "w")
            else:
                self.mainDBIndex = open(fileName, "a")            
            
            fileName = os.path.join(self.outputDirectory, "DataFoundURL.xml")
            
            if not os.path.exists(fileName):
                self.dataFoundURLFile = open(fileName, "w")
            else:
                self.dataFoundURLFile = open(fileName, "a")
            
            fileName = os.path.join(self.outputDirectory, "DataFoundURL.index")
            
            #if not os.path.exists(fileName):
            #    self.dataFoundURLIndex = open(fileName, "w")
            #else:
            #    self.dataFoundURLIndex = open(fileName, "a")
                
            self.loadPreviousHosts()            
            self.start()
            self.checkUnFinishedHosts()
            directorySorter = DirectorySorter()
            #directorySorter.sort(os.path.join(self.outputDirectory, "BusinessDirectoryList.xml"))
            directorySorter.sort(self.outputDirectory)

            self.printLog("Type Detector Started");

            typeDetector = TypeDetector(self.inputDirectory, self.outputDirectory)
            typeDetector.detect()

            self.printLog("Type Detector Finished");
            
            self.printLog("Directory Detection Finished")
            
        except:
            
            print "Exception in detect()"
            print "Exception: ", sys.exc_info()
            
        finally:
            
            self.closeFile(self.mainDBFile)
            self.closeFile(self.mainDBIndex)
            self.closeFile(self.dataFoundURLFile)
            #self.closeFile(self.dataFoundURLIndex)

        
class DataProcessor:
    
    def __init__(self, hostName, directoryDetector):
        
        self.directoryDetector = directoryDetector
        self.hostName = hostName
        self.keywordFrePhone = Hash2D()
        self.keywordFreTag = Hash2D()
        self.parser = Parser()
        
        self.totalPages = 0        
        self.totalDataFoundPages = 0
        self.totalPhones = 0        
        
        self.file = open(os.path.join(self.directoryDetector.outputDirectory, self.hostName + ".db"), "w")
        self.file.write("<PROFILE>\n\t<HOST>" + self.hostName + "</HOST>\n\t<URL_LIST>\n")
        self.file.flush()
        
        self.isPrintLog = True
    
    def printLog(self, logMsg):
        
        if self.isPrintLog:
            print logMsg

    def getStatus(self, dataFoundURLStByte, dataFoundURLEnByte):
                       
        strData = ""

        strKeyPhone, strFrePhone = self.keywordFrePhone.get()
        strKeyTag, strFreTag = self.keywordFreTag.get()
        
        self.totalPhones += self.keywordFrePhone.size() + self.keywordFreTag.size()
        
        strData = "<PROFILE>"
        strData += "\n\t<URL>" + self.hostName + "</URL>"
        strData += "\n\t<INPUT_DIRECTORY>" + self.directoryDetector.inputDirectory + "</INPUT_DIRECTORY>"
        strData += "\n\t<OUTPUT_DIRECTORY>" + self.directoryDetector.outputDirectory + "</OUTPUT_DIRECTORY>"
        strData += "\n\t<TOTAL_PAGES>" + str(self.totalPages) + "</TOTAL_PAGES>"
        strData += "\n\t<TOTAL_PAGES_DATA_FOUND>" + str(self.totalDataFoundPages) + "</TOTAL_PAGES_DATA_FOUND>"
        strData += "\n\t<START_BYTE>" + str(dataFoundURLStByte) + "</START_BYTE>"
        strData += "\n\t<END_BYTE>" + str(dataFoundURLEnByte) + "</END_BYTE>"
        strData += "\n\t<KEYWORD_INFO>"
        strData += "\n\t\t<KEYWORDS>" + strKeyPhone + "</KEYWORDS>"
        strData += "\n\t\t<FREQUENCIES>" + strFrePhone + "</FREQUENCIES>"
        strData += "\n\t</KEYWORD_INFO>"
        strData += "\n\t<KEYWORDS_IN_TAG>"
        strData += "\n\t\t<TAG_KEYWORDS>" + strKeyTag + "</TAG_KEYWORDS>"
        strData += "\n\t\t<FREQUENCIES_TAG_KEY>" + strFreTag + "</FREQUENCIES_TAG_KEY>"
        strData += "\n\t</KEYWORDS_IN_TAG>"
        strData += "\n\t<PHONE>" + str(self.totalPhones) + "</PHONE>"
        strData += "\n</PROFILE>\n"
        
        return strData        
        
    def process(self, thisHostName, thisURL, thisContent, urlInfo):
        
        if urlInfo.isValid == "0":
            return
        
        self.totalPages += 1
                
        self.parser.clear()
        self.parser.parseData(thisContent, urlInfo.contentEndByte - urlInfo.contentStartByte + 1)
        
        cntPhone = self.parser.keywordFrePhone.size()
        cntPhoneTag = self.parser.keywordFreTag.size()
        
        #if cntPhone != 0 or cntPhoneTag != 0:
        #    self.totalDataFoundPages += 1           
            
        totalPhones = cntPhone + cntPhoneTag
        
        if totalPhones == 0 :
            return
        
        totalPhoneAfterMerge = 0
        
        totalPhoneAfterMerge = self.keywordFreTag.merge(self.parser.keywordFreTag)
        totalPhoneAfterMerge += self.keywordFrePhone.merge(self.parser.keywordFrePhone)
        
        if totalPhoneAfterMerge == 0 and totalPhones == 1:
            return
        
        strKeyPhone, strFrePhone = self.parser.keywordFrePhone.get()
        strKeyTag, strFreTag = self.parser.keywordFreTag.get()
                
        strByteInfo = str(urlInfo.contentNo) + " " + str(urlInfo.urlStartByte) + " " + str(urlInfo.urlEndByte) + " " + str(urlInfo.contentStartByte) + " " + str(urlInfo.contentEndByte) + " " + str(urlInfo.isValid) 


        self.totalDataFoundPages += 1
        
        strData = "\n\t\t<URL_INFO>"
        strData += "\n\t\t\t<URL>" + thisURL + "</URL>"
        if len(urlInfo.crawlTime) > 0:
            strData += "\n\t\t\t<CRAWL_TIME>" + urlInfo.crawlTime + "</CRAWL_TIME>"
        strData += "\n\t\t\t<KEYWORD_INFO>"
        strData += "\n\t\t\t\t<KEYWORDS>" + strKeyPhone + "</KEYWORDS>"
        strData += "\n\t\t\t\t<FREQUENCIES>" + strFrePhone + "</FREQUENCIES>"
        strData += "\n\t\t\t</KEYWORD_INFO>"
        strData += "\n\t\t\t<KEYWORD_IN_TAG>"
        strData += "\n\t\t\t\t<KEYWORDS>" + strKeyTag + "</KEYWORDS>"
        strData += "\n\t\t\t\t<FREQUENCIES>" + strFreTag + "</FREQUENCIES>"
        strData += "\n\t\t\t</KEYWORD_IN_TAG>"
        strData += "\n\t\t\t<BYTE_INFO>" + strByteInfo + "</BYTE_INFO>"
        strData += "\n\t\t\t<PHONE>" + str(totalPhones) + "</PHONE>"
        strData += "\n\t\t</URL_INFO>\n"

        self.file.write(strData)
        self.file.flush()
        
class FileChooser(Dialog):

    command = "tk_chooseDirectory"

    def _fixresult(self, widget, result):
        if result:
            self.options["initialdir"] = result
        self.directory = result
        return result

    def askForDirectory(self, **options):
        return apply(FileChooser, (), options).show()

if __name__ == '__main__':

    #print tkFileDialog.askdirectory()
    #tkFileDialog.
    #fileChooser = FileChooser()
    #strInputLocation = fileChooser.askForDirectory()
    #print strInputLocation
    directoryDetector = DirectoryDetector("D:/HostData","D:/Data")
    directoryDetector.detect()
        
        
        
        
        
        
        
    
