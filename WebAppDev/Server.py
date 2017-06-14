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
	# Server will need to serve the index.html page via GET request
	def do_GET(self):
		print('GET %s' % (self.path))
		if self.path == "/":
			with open(os.path.join('www','index.html'), 'r') as myfile:
				indexPage=myfile.read() #.replace('\n', '')
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				# Send the html message
				self.wfile.write(indexPage.encode("utf-8"))	
		else:
			# Get the file path.
			path = os.path.join("www", *self.path.split("/")) #Split up self.path and convert it to a folder path
			dirpath = None
			print('FILE %s' % (path))

			#Send the index.html page if browser tries to access folder
			if os.path.exists(path) and os.path.isdir(path):
				with open(os.path.join('www','index.html'), 'r') as myfile:
					indexPage=myfile.read() #.replace('\n', '')
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					# Send the html message
					self.wfile.write(indexPage.encode("utf-8"))	

			# Allow the user to type "///" at the end to see the
			# directory listing.
			if os.path.exists(path) and os.path.isfile(path):
				# This is valid file, send it as the response
				# after determining whether it is a type that
				# the server recognizes.
				_, ext = os.path.splitext(path)
				ext = ext.lower()
				content_type = {
					'.css': 'text/css',
					'.gif': 'image/gif',
					'.htm': 'text/html',
					'.html': 'text/html',
					'.jpeg': 'image/jpeg',
					'.jpg': 'image/jpg',
					'.js': 'text/javascript',
					'.png': 'image/png',
					'.text': 'text/plain',
					'.txt': 'text/plain',
				}

				# If it is a known extension, set the correct
				# content type in the response.
				if ext in content_type:
					self.send_response(200)  # OK
					self.send_header('Content-type', content_type[ext])
					self.end_headers()

					with open(path) as ifp:
						self.wfile.write(ifp.read().encode("utf-8"))
				else:
					# Unknown file type or a directory.
					# Treat it as plain text.
					self.send_response(200)  # OK
					self.send_header('Content-type', 'text/plain')
					self.end_headers()

					with open(path) as ifp:
						self.wfile.write(ifp.read().encode("utf-8"))



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
				with open(os.path.join('www','Editor.html'), 'r') as myfile:
					editorPage=myfile.read() #.replace('\n', '')
					print(editorPage)
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					# Send the html message
					self.wfile.write(editorPage.encode("utf-8"))

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