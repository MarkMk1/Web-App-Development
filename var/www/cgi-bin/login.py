#!C:\python35
import cgi
import csv
import os


form = cgi.FieldStorage()
enteredName =  form.getvalue('name')
enteredPass =  form.getvalue('password')
cgi_dir = "s1811185\WebAppDev\\"

#print("Location: http://win371.ad.utwente.nl/student/s1811185/webappdev/editor.html")
#How do I get the Location: whatever thing while also using this page to store a variable? Can I? 
print("Content-type:text/html\r\n\r\n")
print('<HTML><HEAD><TITLE>Login</TITLE></HEAD>')
print('<BODY>')
with open(cgi_dir + 'User_Info.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		name = row['name']
		password = row['pwd']
		dir = row['a']
		if enteredName == name:
			if enteredPass == password:
				user_dir = dir
				print("<script>localStorage.setItem(\"dir\"," + "\"" + user_dir + "\"" + " )</script>")
				print("<a href=\"http://win371.ad.utwente.nl/student/s1811185/webappdev/editor.html\">Project 1</a>")
				break
		else:
			print("bg")
			name = "fuck you"
			password = "dickshit"
			dir = "www.suckabagofdicks.com"

			
#print(name)
#print(password)
#print(dir)
	#print('<p>' + row['name'] + ' : ' + row['pwd'] + '</p>')
	#print(row['name'], row['pwd'])
#print(name + ', ' + pwd)
print('</BODY></HTML>')

