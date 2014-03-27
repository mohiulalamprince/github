import os
import sys
import time
from Reader import Reader
from sgmllib import SGMLParser
from URLLister import URLLister
from urlparse import urlparse
from datetime import datetime

class HostExtractor(Reader):

    def __init__(self, inputDirectory, outputDirectory="", readSize=1024*1024*200):

        Reader.__init__(self, inputDirectory, readSize)
        self.outputDirectory = outputDirectory
        self.totalURLProcessed = 0
        self.totalDifferentHostFound = 0
        self.totalHostProcessed = 0
        self.foundHosts = {}
        self.urlLister = URLLister()
        self.lastTime = 0
        self.startedTime = datetime.now()
        
        if os.path.exists(os.path.join(outputDirectory, "AllHosts.txt")):  
            self.outputFile = open(os.path.join(outputDirectory, "AllHosts.txt"), "a")
        else:
            self.outputFile = open(os.path.join(outputDirectory, "AllHosts.txt"), "w")

    def saveExtractedHosts(self):

        strData = ""        

        for hostName in self.foundHosts.keys():
            strData += hostName + "\n"       
        try:
            self.outputFile.write(strData)
            self.outputFile.flush()
            self.totalDifferentHostFound += len(self.foundHosts)
        except:
            print "Unable to Save Extracted Hosts"
            print "[Exception] ", sys.exc_info()

    def getHostName(self, thisURL):

        hostName = ""
        parsedURL = urlparse(thisURL)

        if parsedURL.netloc == "":
            return ""

        if parsedURL.scheme == "":     
            return "http://" + parsedURL.netloc + "/"
        else:
            return parsedURL.scheme + "://" + parsedURL.netloc + "/"            
                    
        
    def processData(self, thisURL, thisContent):

        #print "Now Parsing URL: ", thisURL
        #print "Content Length: ", len(thisContent)
        try:
            self.urlLister.reset()
            self.urlLister.feed(thisContent)
        except:
            pass

        #print "TotalURLFound: ", len(self.urlLister.urls)
        for url in self.urlLister.urls:
            hostName = self.getHostName(url)
            if len(hostName)> 0 and not self.foundHosts.has_key(hostName):
                self.foundHosts[hostName] = True

        self.totalURLProcessed += 1

        if self.totalURLProcessed % 100 == 0:
            print "\nTotal URL Processed:           ", self.totalURLProcessed
            print "Total Host Processed:            ", self.totalHostProcessed
            print "Total Different Host Found:      ", self.totalDifferentHostFound + len(self.foundHosts)
            print "Time for Last 100 :              ", time.clock() - self.lastTime
            print "Start Time:                      ", self.startedTime
            print "Total Time:                      ", (datetime.now() - self.startedTime)
            print ""
            self.lastTime = time.clock()
            
    def getLastProcessHostInfo(self):

        configFileName = os.path.join(self.outputDirectory, "lastHost.config")
        lastHostName = ""
        configFile = None

        if os.path.exists(configFileName):
            try:
                configFile = open(configFileName, "r")
                configValues = configFile.read().strip().split("#")
                if len(configValues) == 4:
                    lastHostName = configValues[0]
                    self.totalHostProcessed = int(configValues[1])
                    self.totalDifferentHostFound = int(configValues[2])
                    self.totalURLProcessed = int(configValues[3])
                else:
                    lastHostName = ""
                    self.totalHostProcessed = 0
                    self.totalDifferentHostFound = 0
                    self.totalURLProcessed = 0
            except:
                print "[Exception] ", sys.exc_info()
            finally:
                self.closeFile(configFile)
                return lastHostName
        else:
            print "No Config File Found."
            return lastHostName

    def saveFinishedHost(self, thisHost):
        
        configFileName = os.path.join(self.outputDirectory, "lastHost.config")
        configFile = None
        
        try:
            configFile = open(configFileName, "w")
            configFile.write(thisHost +"#"+ str(self.totalHostProcessed) +"#"+ str(self.totalDifferentHostFound) +"#"+ str(self.totalURLProcessed))
        except:
            print "[Exception] ", sys.exc_info()
        finally:
            self.closeFile(configFile)
                            
    def closeFile(self, thisFile):
        if thisFile != None:
            thisFile.close() 
                
    def extract(self):

        lastHostName = self.getLastProcessHostInfo()

        try:
            lb = self.allHostsName.index(lastHostName)
        except ValueError:
            lb = 0
        
        for cIDX in range(lb, len(self.allHostsName)):
            self.processHost("http://"+ self.allHostsName[cIDX] +"/")
            self.saveExtractedHosts()
            self.foundHosts = {}
            self.totalHostProcessed += 1
            self.saveFinishedHost(self.allHostsName[cIDX])

        self.closeFile(self.outputFile)            

if __name__ == "__main__":

    hostExtractor = HostExtractor("E:/ReCrawlHostDataLargest/HostData")
    hostExtractor.extract()



            
            
