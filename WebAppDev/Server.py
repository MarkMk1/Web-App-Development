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
Handler class subclassing BaseHTTPRequestHandler to define how the POST request is handled
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
			print("Name received: " + clientName + " Password received: " + clientPass)

			with open('User_Info.csv', "r+", newline='') as csvfile:
				userExists = False
				reader = csv.DictReader(csvfile)
				for row in reader:
					name = row["name"]
					password = row["pwd"]
					jsonFileLocation = row['a']
					if clientName == name:
						if clientPass == password:
							userJsonFileLocation = jsonFileLocation
							userExists = True	
				if not userExists:
					#username and pass not found, add them to the csv 
					fieldnames = ['name','pwd','a']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({'name': clientName, 'pwd': clientPass,'a': clientName + clientPass + ".json"})

			if "data" in postData:				
				# If data is included in POST request then this is a save and upload action and not a login, 
				# so save the data to the userJsonFile add the data to the editor page and return the editor page.
				clientData =  postData.getvalue('data')
				print("clientData: "+ clientData)
				with open(clientName + clientPass + ".json", 'w') as jsonFile:
					data=jsonFile.write(clientData)
				
			else:
				#TODO No data means this is a login return the editor page and load up jsonFile using the jsonFileLocation.
				pass

			#load

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