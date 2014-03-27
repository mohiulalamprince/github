import socket
import sys
import threading


class HandleClient(threading.Thread):
    
    def __init__(self, serverSocket, clientSocket, packetSize = 1024):
        
        threading.Thread.__init__(self)
        self.serverSocket = serverSocket
        self.clientSocket = clientSocket
        self.packetSize = packetSize
        
    def run(self):
        
        self.clientSocket.send("Hi Client ")
        clientMsg = self.clientSocket.recv(self.packetSize)
        print "Data From Client: ",  clientMsg
            
    
            
class Server(threading.Thread):
    
    def __init__(self, serverIP="127.0.0.1", serverPort=5000, maximumConnection = 10):
        
        threading.Thread.__init__(self)
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.serverSocket = None
        self.maximumConnection = maximumConnection
        self.isStopServer = False
        
    def startServer(self):
        
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.serverIP, self.serverPort))
            self.serverSocket.listen(self.maximumConnection)
            return True           
        except:
            print "Unable to Start Server"
            print "[ERROR] ", str(sys.exc_info())
            return False
        
    def stopServer(self):
        self.isStopServer = True
        
    def closeServer(self):
        
        self.isStopServer = True
        
        try:
            if self.serverSocket != None:
                self.serverSocket.close()

            if self.clientSocket != None:
                self.clientSocket.close()
        except:
            print "Unable to Close Server"
            print "[ERROR] ", str(sys.exc_info())
            
    def __serveClient(self):
        
        try:
            while not self.isStopServer:
                
                print "Server Waiting for New Connection ..."                
                self.clientSocket, clientAddress = self.serverSocket.accept()                
                print "New Connection From : ", clientAddress[0]                
                self.handleClient(self.clientSocket)
        except:
            print "[ERROR] ", str(sys.exc_info())

    def handleClient(self, clientSocket):        
        clientMsg = clientSocket.recv(1024)
        print "Data From Client: ",  clientMsg
        clientSocket.send("Hi Client ")
            
    def handleClient_(self, clientSocket):
        
        handleClient = HandleClient(self, clientSocket)
        handleClient.start()
            
    def run(self):
        
        self.__serveClient()
        print "Server Stopeed"
            
            
if __name__ == "__main__":
    
    server = Server()
    server.startServer()
    server.start()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        
        
