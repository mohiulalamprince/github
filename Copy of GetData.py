import os
import sys

class GetData:
    
    def __init__(self, fileName = "DataFoundURL.xml"):
        
        self.outputLocation = fileName
        self.readSize  = 1024 * 1024 * 100
        
    def getContent(self, thisLocation, startByte = -1, endByte = -1):
        
        if not os.path.exists(thisLocation):
            print "File Not Found: ", thisLocation
            return
        
        if startByte > endByte:
            print "Invalid Byte Info "
            return
        
        if startByte == -1 or endByte == -1:
            
            startByte = 1
            endByte = os.path.getsize(thisLocation)
            
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
    
    getData = GetData()
    getData.getContent("""D:\OfficeWork\Development\WebCrawler\BusinessSearch\Data\Output\NewLargestHost\Business Data\DataFoundURL.xml""", 141169602, 202550001)
    #getData.getContent("D:/africaexport_single/www.africaexports.co.zaOut.xml")    
            
    
        
        
