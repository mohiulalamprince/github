import os
import sys
import socket

class ProfileValidatorServer:
    
    def __init__(self, contentLoc = os.getcwd()):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.portNo = 8888
        self.contentLoc = contentLoc
                
    def listen(self):
        
        try:
            self.socket.bind(("", self.portNo))
            self.socket.listen(10)
        except:
            print 'Unable to bind/listen'
            print sys.exc_info()
            
        try:
        
            print 'Server Running...'
        
            while True:
                
                clientSocket, newAddress = self.socket.accept()
                strRequest = clientSocket.recv(1024)
                
                print 'New Request: ', strRequest
                print 'From: ', address[0]
                wTokens = strRequest.strip().split(" ")
                
                if len(wTokens) < 3:
                    strResult = "<html>Request Format Error: "+ strRequest + "</html>"
                else:
                    fileLocation = os.path.join(self.contentLoc, wTokens[0].strip())
                    strResult = self.getContent(fileLocation, long(wTokens[1].strip()), long(wTokens[2].strip()))
                
                clientSocket.send(strResult)
                clientSocket.close()
            
        except:
        
            print sys.exc_info()
        
    def getContent(self, thisLocation, startByte = -1, endByte = -1):
        
        if not os.path.exists(thisLocation):
            print "File Not Found: ", thisLocation
            return "<html>" + "File Not Found: " + str(thisLocation) + "</html>"
        
        if startByte > endByte:
            print "Invalid Byte Info "
            return "<html>" + "Invalid Byte Info" + "</html>"

        if startByte == 0:
            startByte = 1
        
        if startByte == -1 or endByte == -1:
            
            startByte = 1
            endByte = os.path.getsize(thisLocation)

        try:
            
            inputFile = open(thisLocation, 'rb')
            
            inputFile.seek(startByte-1)
            dataLength = endByte - startByte + 1

            totalReadSize = 0
            dataBuffer = ""
              
            while totalReadSize < dataLength:
                
                if totalReadSize + self.readSize >= dataLength:
                    self.readSize = dataLength - totalReadSize
                                    
                totalReadSize += self.readSize
                dataBuffer += inputFile.read(self.readSize)                              
        except:
            
            print "Exception During Process"
            print "[Exception] ", sys.exc_info()
            return "<html>" + "[Exception] " + str(sys.exc_info()) + "</html>"
            
        finally:
            
            if inputFile != None:
                inputFile.close()

            return dataBuffer

        
if __name__ == '__main__':
    
    profileValidatorServer = ProfileValidatorServer()
    profileValidatorServer.listen()
        
        
        
        
        
        
        
            
