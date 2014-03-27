#!/usr/bin/env python


import threading
import sys
import socket



class Client():
    
    def __init__(self, serverIP="127.0.0.1", serverPort=5000):

        print "Bad Client"
        self.serverIP = serverIP
        self.serverPort = serverPort
        
    
    def sendRequest(self):
        
        clientSocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        print "Connection to Server ..."
        clientSocket.connect((self.serverIP, self.serverPort))
        print "Connected With Server."
        serverMsg = clientSocket.recv(1024)
        print "Server Msg: ", serverMsg
        #clientSocket.send("I'm Client")


if __name__ == "__main__":
    
    client = Client()
    client.sendRequest()
