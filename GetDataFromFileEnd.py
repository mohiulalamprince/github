import os
import sys

class GetDataFromFileEnd:
    
    def __init__(self, fileName = "FetchedData.txt"):
        
        self.outputLocation = fileName
        self.readSize  = 1024 * 1024 * 100

    def get(self, thisLocation, size):

        if not os.path.exists(thisLocation):
            print "File Not Found: ", thisLocation
            return

        size = size * 1024 * 1024
        startByte = 0
        
        fileSZ = os.path.getsize(thisLocation)

        if size > fileSZ:
            startByte = 0
        else:
            startByte = fileSZ - size

        self.getContent(thisLocation, startByte)
        
    def getContent(self, thisLocation, startByte = -1, endByte = -1):
        
        if not os.path.exists(thisLocation):
            print "File Not Found: ", thisLocation
            return

        if startByte == 0:
            startByte = 1
        
        if endByte == -1:
            endByte = os.path.getsize(thisLocation)
        
        if startByte > endByte:
            print "Invalid Byte Info "
            return
            
        try:
            
            inputFile = open(thisLocation, 'r')
            outputFile = open(self.outputLocation, 'w')
            
            inputFile.seek(startByte-1)
            dataLength = endByte - startByte + 1
                
            totalReadSize = 0                
              
            while totalReadSize < dataLength:
                
                if totalReadSize + self.readSize >= dataLength:
                    self.readSize = dataLength - totalReadSize
                                    
                totalReadSize += self.readSize
                dataBuffer = inputFile.read(self.readSize)                              
                outputFile.write(dataBuffer)
                outputFile.flush()
  
        except:
            
            print "Exception During Process"
            print "[Exception] ", sys.exc_info()
            
        finally:
            
            if inputFile != None:
                inputFile.close()
                
            if outputFile != None:
                outputFile.close()

if __name__ == "__main__":

    fileName = "F:\\OfficeWork\\Development\\BusinessSearch\\Working\\Python Scripts\\Profiles.xml"
    size = 1
    getDataFromFileEnd = GetDataFromFileEnd()
    getDataFromFileEnd.get(fileName, size)


    
