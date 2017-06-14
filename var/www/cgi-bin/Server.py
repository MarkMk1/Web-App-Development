#!/usr/bin/python3
import cgi
import csv
import os
from http.server import CGIHTTPRequestHandler, HTTPServer
import time

HOST_NAME = '' # Change to webserver host
PORT_NUMBER = 8080 # Change to 80 on production server

form = cgi.FieldStorage()
enteredName =  form.getvalue('name')
enteredPass =  form.getvalue('password')
cgi_dir = "s1811185\WebAppDev\\"

'''
Handler class subclassing CGIHTTPRequestHandler to define how the POST request is handled
CGIHTTPRequestHandler can be enabled in the command line by passing the --cgi option:
e.g. python -m http.server --cgi 8000
'''
class user_handler_class(CGIHTTPRequestHandler):
	def do_POST(self):
		print( "incoming POST request from: ", self.client_address )

		

'''
run function to create and start http server instance httpd
'''
def run(server_class=HTTPServer, handler_class=user_handler_class):
    server_address = (HOST_NAME, PORT_NUMBER) #Change this to 80 in production server 
    httpd = server_class(server_address, handler_class)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
    	httpd.serve_forever()
    except KeyboardInterrupt:
    	print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

    httpd.server_close()
    
'''
Server to receive, store and send user data in JSON format using python3 HTTPServer.
'''
if __name__ == '__main__':
	run()