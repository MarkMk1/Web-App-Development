#!/usr/bin/python3
import csv
import cgi
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


'''
Server settings
'''
HOST_NAME = '' # Change to webserver host
PORT_NUMBER = 8080 # Change to 80 on production server

'''
Configure cgi
'''
cgi_dir = "s1811185\WebAppDev\\"

'''
Handler class subclassing CGIHTTPRequestHandler to define how the POST request is handled
CGIHTTPRequestHandler can be enabled in the command line by passing the --cgi option:
e.g. python -m http.server --cgi 8000
'''
class user_handler_class(BaseHTTPRequestHandler):
	def do_POST(self):		
		print( "incoming POST request from: ", self.client_address )
		#cgi handles GET requests by default, so need to explicitly set to POST and pass in the do_POST's rfile and headers
		postData = cgi.FieldStorage(
									fp=self.rfile,
									headers=self.headers,
									environ={'REQUEST_METHOD':'POST'})
		print(postData)

		#A name and password should be attached to every POST request so server knows where the request is coming from. 
		if "name" in postData and "password" in postData:
			clientName =  postData.getvalue('name')
			clientPass =  postData.getvalue('password')

			with open(cgi_dir + 'User_Info.csv', newline='') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					name = row["name"]
					password = row["pwd"]
					jsonFileLocation = row['a']
					if clientName == name:
						if clientPass == password:
							userJsonFileLocation = jsonFileLocation
					else:
						break
						#TODO username and pass not found, add them to the csv instead of breaking out

			if "data" in postData:
				#TODO If data is included then this is a save and upload action and not a login, so save the data to the userJsonFile add the data to the editor page and return the editor page.
				pass
			else:
				#TODO No data means this is a login return the editor page and load up jsonFile using the jsonFileLocation.
				pass

		else:
			pass
			#TODO this needs to return a 404 page instea of pass.

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