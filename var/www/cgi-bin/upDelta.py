#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = ""
hostPort = 80

def do_POST(self):
	print( "incomming http: ", self.path )

	content_length = len(delta.encode("utf-8")) # <--- Gets the size of data
	post_data = self.rfile.read(content_length) # <--- Gets the data itself
	self.send_response(200)
	print(post_data)
	input("prompt: ")
	client.close()

	#import pdb; pdb.set_trace()


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))



#import os
#import sys
#import cgi

# This will basically take the variable delta, assign it to a file within my server,
# and then it will do nothing. When the editor is loaded again, it will load with setContents(delta)

#data = cgi.FieldStorage()

#log = open("log", "w")
#log.write("test")
#log.write(os.dirname)
#log.write(data.delta)
#log.write(data.dir)

#log.close()
=======
#This will basically take the variable delta, assign it to a file within my server,
#and then it will do nothing. When the editor is loaded again, it will load with setContents(delta)
#import path from os

#log = open("log", "w")
#log.write("fuck")
#log.write(os.dirname)

