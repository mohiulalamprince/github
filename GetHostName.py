import os
import sys

class GetHostName:

    def parseLine(self, thisLine, strTokens = " "):
        
        wTokens =  thisLine.split(strTokens)
        return filter(lambda x: len(x) > 0, wTokens)

    def closeFile(self, thisFile):

        if thisFile != None:
            thisFile.close()

    def getHostName(self, inputFileLocation):

        inputFile = None
        outputFile = None


        if not os.path.exists(inputFileLocation):
            print "File Not Found"
            return

        try:

            inputFile = open(inputFileLocation, "r")
            outputFile = open(inputFileLocation+".parsed", "w")

            line = ""

            while True:

                line = inputFile.readline().strip()

                if len(line) == 0:
                    break

                wTokens = self.parseLine(line)

                if wTokens > 0:
                    wTokens = self.parseLine(wTokens[0], "=")
                    outputFile.write("http://"+wTokens[1]+"/\n")                    
        except:
            print "Exception: ", str(sys.exc_info())
        finally:
            self.closeFile(inputFile)
            self.closeFile(outputFile)


if __name__ == "__main__":

    getHostName = GetHostName()
    getHostName.getHostName("E:\\HostForSingleProfileParser\\hostList.txt") 
                

                
                
