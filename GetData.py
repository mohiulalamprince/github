import os

class GetData:
    
    def __init__(self, fileName = "FetchedData.txt"):
        
        self.outputLocation = fileName
        self.readSize  = 1024 * 1024 * 32
        
    def getContent(self, thisLocation, startByte = -1, endByte = -1):
        
        if not os.path.exists(thisLocation):
            print "File Not Found: ", thisLocation
            return
        
        if startByte > endByte:
            print "Invalid Byte Info "
            return

        if startByte == 0:
            startByte = 1
        
        if startByte == -1 or endByte == -1:
            
            startByte = 1
            endByte = os.path.getsize(thisLocation)

        try:
            
            inputFile = open(thisLocation, 'rb')
            #outputFile = open(self.outputLocation, 'wb')
            
            inputFile.seek(startByte-1)
            dataLength = endByte - startByte + 1


            totalReadSize = 0
            dataBuffer = ""
              
            while totalReadSize < dataLength:
                
                if totalReadSize + self.readSize >= dataLength:
                    self.readSize = dataLength - totalReadSize
                                    
                totalReadSize += self.readSize
                dataBuffer += inputFile.read(self.readSize)                              
                #outputFile.write(dataBuffer)
                #outputFile.flush()
  
        except:
            
            print "Exception During Process"
            print "[Exception] ", sys.exc_info()
            
        finally:
            
            if inputFile != None:
                inputFile.close()

            return dataBuffer


if __name__ == "__main__":


    ob = GetData()
    print ob.getContent("F:\\OfficeWork\\Development\\BusinessSearch\\Working\\Python Scripts\\FetchedData.txt")
