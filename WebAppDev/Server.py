#!/usr/bin/python3
import os
import csv
import cgi
import time
import simplejson as json 
from bs4 import BeautifulSoup # HTML Parsing
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPMessage


'''
Server settings
'''
HOST_NAME = '' # Change to webserver host
PORT_NUMBER = 8080 # Change to 80 on production server

'''
Handler class subclassing BaseHTTPRequestHandler to define how the POST and GET requests are handled
'''
class user_handler_class(BaseHTTPRequestHandler):

	'''
	GET requests will only serve the index.html page, images and css via GET request, everything else will be posted
	'''
	def do_GET(self):
		print('GET %s' % (self.path))
		if self.path == "/":
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			with open(os.path.join(os.path.realpath(__file__)[0:-10], 'www','index.html'), 'r') as myfile:
				self.wfile.write(myfile.read().encode("utf-8"))	
		else:
			# Get the file path.
			path = os.path.join(os.path.realpath(__file__)[0:-10], "www", *self.path.split("/")) # Split up self.path and convert it to a folder path
			dirpath = None
			print('FILE %s' % (path))

			# Send the index.html page if browser tries to access folder
			if os.path.exists(path) and os.path.isdir(path):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				with open(os.path.join(os.path.realpath(__file__)[0:-10], 'www','index.html'), 'r') as myfile:
					self.wfile.write(myfile.read().encode("utf-8"))	

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
			else:
				self.send_error(404)

	'''
	POST request will handle user login and user data updating.
	'''
	def do_POST(self):		
		print( "incoming POST request from: ", self.client_address )
		# cgi handles GET requests by default, so need to explicitly set to POST and pass in the do_POST's rfile and header

		print(self.headers["Content-Type"])		
		'''
		cgi doesn't seem to support json so keeping it for parsing the form data but manually parsing the json POST
		So, here we look at the POST header Content-Type and if it's a form we let cgi handle it, if it's json then
		we use simplejson to parse, dump and load the POST data
		'''
		if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
			postData =  cgi.FieldStorage(
										fp=self.rfile,
										headers=self.headers,
									environ={'REQUEST_METHOD':'POST'})
		elif self.headers["Content-Type"] == "application/json":
			# To read the rfile we need to get the length which is recorded in the header, then using simplejson to parse the json object.
			postRawData =  self.rfile.read(int(self.headers["Content-Length"]))
			postData = json.loads(postRawData)
		print(postData)

		'''
		This section of logic handles the POST request as such:
		1. Checks the POST contains username and password, otherwise doesn't do anything
		2. Checks the username and password have been used before, if not then creates an entry for it.
		3. Checks the POST for data or not. If it contains data then it is a sync/upload POST if not it is a login
		4. Login POST retrieves the page and uses BeautifulSoup to embed the user's data into the editor page
		5. sync/upload POST will store the data to the json file associated with the username and password
		'''
		# A name and password should be attached to every POST request so server knows where the request is coming from. 
		if "name" in postData and "password" in postData:
			# The cgi stores the form variabls in miniFieldStorage and the json is stored as a Dict so we need to get the name 
			# and password differently for both types of POSTs
			if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
				clientName =  postData.getvalue('name')
				clientPass =  postData.getvalue('password')
			elif self.headers["Content-Type"] == "application/json":
				clientName =  str(postData['name'])
				clientPass =  str(postData['password'])

			print("Name received: " + clientName + " Password received: " + clientPass)

			# Checks if username and password exist in User_Info and if not it will create an entry for it.
			with open(os.path.join(os.path.realpath(__file__)[0:-10],'User_Info.csv'), "r+", newline='') as csvfile:
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
					# username and pass not found, add them to the csv 
					fieldnames = ['name','pwd','a']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({'name': clientName, 'pwd': clientPass,'a': clientName + clientPass + ".json"})
					with open(clientName + clientPass + ".json", 'w') as jsonFile:
						jsonFile.write("")
			if "data" in postData:				
				# If data is included in POST request then this is a save and upload action and not a login, 
				# so save the data to the userJsonFile add the data to the editor page and return the editor page.
				clientData =  postData['data']
				print("clientData: "+ str(clientData))
				with open(clientName + clientPass + ".json", 'w') as jsonFile:
					json.dump(clientData, jsonFile)
				
			else:
				# No data means this is a login return the editor page and load up jsonFile using the jsonFileLocation.
				# Read the user's data and insert it into the Editor.html using beautifulsoup and return it.
				with open(clientName + clientPass + ".json") as jsonFile:  
					try:  
						data = json.load(jsonFile)
					except:
						with open(os.path.join(os.path.realpath(__file__)[0:-10],'default.json')) as jsonDefaultFile:  
							data = json.load(jsonDefaultFile)
				with open(os.path.join(os.path.realpath(__file__)[0:-10],'www','Editor.html'), 'r') as myfile:
					editorPage = myfile.read()
					soup = BeautifulSoup(editorPage, 'html.parser')					
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					# Send the html message
					userDataScript = soup.find('script', {"id" : "userData"})
					userDataScript.insert(1,"\nvar _name = \"" + clientName + "\";\n")
					userDataScript.insert(2,"var _password = \"" + clientPass + "\";\n")
					userDataScript.insert(3,"var userData = " + str(data) + ";\n")
					self.wfile.write(soup.encode("utf-8"))
		else:
			self.send_error(404)

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