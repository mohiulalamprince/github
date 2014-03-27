import os
import sys

class GetHostFromFinishedHost:

    def __init__(self):

        self.outputFileName = "AllFinishedHosts.txt"
        self.outputFileName01 = "AllFinishedHosts01.txt"
        self.inputFolder = ""
        self.allFinishedHosts = {}
        self.allFinishedHosts01 = {}
        self.totalURLs = 0
        self.totalDownload = 0

    def parseLine(self, thisLine):
        
        wTokens =  thisLine.split(" ")
        return filter(lambda x: len(x) > 0, wTokens)

    def saveHost(self, hostName, totalDownload, totalURL):

        try:
            self.totalDownload += int(totalDownload)
            self.totalURLs += int(totalURL)
        except:
            print hostName," ", totalDownload," ", totalURL
            return

        if int(totalURL) <=1 or int(totalDownload) <= 1:
            if not self.allFinishedHosts01.has_key(hostName):
                self.outputFile01.write(hostName+"\n")
                self.allFinishedHosts01[hostName] = True
                return

        if not self.allFinishedHosts.has_key(hostName):
            self.outputFile.write(hostName+"\n")
            self.allFinishedHosts[hostName] = True
            
    def parseAllHosts(self, thisFile):

        try:
            inputFile = open(thisFile, "r")

            for line in inputFile.readlines():
                wTokens = self.parseLine(line)

                if len(wTokens) > 5:                    
                    self.saveHost(wTokens[1], wTokens[3], wTokens[5])                 
        except:
            print "[Exception] ", sys.exc_info()
        finally:
            self.closeFile(inputFile)

    def closeFile(self, thisFile):
        if thisFile != None:
            thisFile.close()        
        
    def getHosts(self, inputFolder = os.getcwd()):

        try:
            self.inputFolder = inputFolder
            self.outputFile = open(self.outputFileName, "w")
            self.outputFile01 = open(self.outputFileName01, "w")
            
            for fileName in os.listdir(inputFolder):
                if fileName.endswith("txt"):
                    print "NowExtracting HostFrom :", fileName
                    self.parseAllHosts(os.path.join(inputFolder, fileName))
        except:
            print "[Exception] ", sys.exc_info()
        finally:
            print "Total Finished Hosts: ", len(self.allFinishedHosts)
            print "Total Finished Hosts(01): ", len(self.allFinishedHosts01)
            print "Total Download: ", self.totalDownload
            print "Total URLs: ", self.totalURLs
            self.closeFile(self.outputFile)
            self.closeFile(self.outputFile01)

                
if __name__ == "__main__":

    getHostFromFinishedHost = GetHostFromFinishedHost()
    getHostFromFinishedHost.getHosts()
        
    
