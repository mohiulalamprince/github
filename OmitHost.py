import os
import sys

## This class uses for remove host from a file(s) , lets list "A" contains hosts ["a", "b", "c"] and list "B" contains hosts ["k", "c"] then result will ["a", "b"]
## List "A" and "B" gets hosts from file(s)

class OmitHost:

    def __init__(self,inputFolder=os.getcwd()):

        self.hostListA = {}
        self.hostListB = {}
        self.workingFolder = inputFolder
        self.outputFileName = os.path.join(self.workingFolder, "HostListDifferent.txt")
        self.outputFileNameOmited = os.path.join(self.workingFolder, "HostListOmited.txt")
        self.totalDifferentHosts = 0
        self.totalHostsOmited = 0

    def load(self, hostList, fileList):

        for fileName in fileList:
            fileName = os.path.join(self.workingFolder, fileName)
            self.loadHosts(hostList, fileName)

    def loadHosts(self, hostList, hostFileLocation):

        try:

            print "Host Loading From: ", hostFileLocation
            inputFile = open(hostFileLocation, "r")

            for line in inputFile.readlines():
                line = line.strip()
                if not hostList.has_key(line):
                    hostList[line] = True   
        except:
            print "[Exception 3] ", sys.exc_info()
        finally:
            self.closeFile(inputFile)       

    def closeFile(self, thisFile):
        if thisFile != None:
            thisFile.close()

    def omitHosts(self, thisFileLocation):

        try:

            print "Host Omiting From: ", thisFileLocation
            inputFile = open(thisFileLocation, "r")

            for hostName in inputFile.readlines():
                hostName = hostName.strip()
                if not self.hostListA.has_key(hostName):
                    self.hostListA[hostName] = True
                    if not self.hostListB.has_key(hostName):
                        self.outputFile.write(hostName+"\n")
                        self.totalDifferentHosts += 1
                    else:
                        self.outputFileOmited.write(hostName+"\n")
                        self.totalHostsOmited += 1
        except:
            print "[Exception 2] ", sys.exc_info()
        finally:
            self.closeFile(inputFile)

    def omit(self, fileListA, fileListB):

        try:
            self.load(self.hostListB, fileListB)
            self.outputFile = open(self.outputFileName, "w")
            self.outputFileOmited = open(self.outputFileNameOmited, "w")

            for fileName in fileListA:
                fileName = os.path.join(self.workingFolder, fileName)
                self.omitHosts(fileName)           

        except:
            print "[Exception 1] ", sys.exc_info()
        finally:
            self.closeFile(self.outputFile)
            self.closeFile(self.outputFileOmited)
            print "Different Hosts Found: ", self.totalDifferentHosts
            print "Omited Hosts: ", self.totalHostsOmited


if __name__ == "__main__":

    fileListA = ["AllUniqeHostNameGoogleYahooSubtracted.txt"]
    fileListB = ["AllFinishedHosts.txt"]

    omitHost = OmitHost()
    omitHost.omit(fileListA, fileListB)

