import SocketServer

class Test:
    def __init__(self):
        self.x = 5
    def getX():
        return self.x

class EchoRequestHandler(SocketServer.BaseRequestHandler, Test):

    def setup(self):
        print self.client_address, 'connected!'
        #self.request.send('hi ' + str(self.client_address) + '\n')

    def handle(self):
        data = 'dummy'
        test = Test()
        print 'testing'
        while data:
            data = self.request.recv(1024)
            print 'x=' + str(test.x)
            print data 

    def finish(self):
        print self.client_address, 'disconnected!'
        #self.request.send('bye ' + str(self.client_address) + '\n')

    #server host is a tuple ('host', port)

#server = SocketServer.ThreadingTCPServer(('', 50008), EchoRequestHandler)
#server.serve_forever()

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("", 50008))

server_socket.listen(5)


while 1:

    client_socket, address = server_socket.accept()

    print "I got a connection from ", address

    data = client_socket.recv(512)
	
    print data