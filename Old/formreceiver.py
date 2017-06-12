<<<<<<< HEAD
#C:\python35
import cgi
# cgitb to provide debugging info
import cgitb
cgitb.enable()
print('Content-type: text/html')
print('')
# note the empty print line above is required!
print('<HTML><HEAD><TITLE>Python Test</TITLE></HEAD>')
print('<BODY>')

theRequest = cgi.FieldStorage()
theName = theRequest.getfirst("name", "undefined")
theAge = theRequest.getfirst("age", "undefined")
theSport = theRequest.getfirst("sport", "undefined")
print("<p>Your name is " + theName + "</p>")
print('<p> You are ' + theAge + '</p>')
print('<p> Your favourite sport is ' + theSport + '</p>')
=======
#C:\python35
import cgi
# cgitb to provide debugging info
import cgitb
cgitb.enable()
print('Content-type: text/html')
print('')
# note the empty print line above is required!
print('<HTML><HEAD><TITLE>Python Test</TITLE></HEAD>')
print('<BODY>')

theRequest = cgi.FieldStorage()
theName = theRequest.getfirst("name", "undefined")
theAge = theRequest.getfirst("age", "undefined")
theSport = theRequest.getfirst("sport", "undefined")
print("<p>Your name is " + theName + "</p>")
print('<p> You are ' + theAge + '</p>')
print('<p> Your favourite sport is ' + theSport + '</p>')
>>>>>>> origin/master
print('</BODY></HTML>')