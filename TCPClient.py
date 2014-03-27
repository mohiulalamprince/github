#!/usr/bin/env python

import socket
import sys

def clientTest(query):
	HOST = '127.0.0.1'

	PORT = 6060

	data = None	

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(1)
	try:
		sock.connect((HOST, PORT))
	except socket.error, msg:
		sys.stderr.write("[ERROR] %s\n" % msg[1])
		sys.exit(2)
	print 'sending'
	sock.send(query)
	data = sock.recv(512)

	print(data)	
