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
print('Your name is ' + theName(name))
print('Your age is ' + theName(age))
print('Your favourite sport is ' + theName(sport))
print('</BODY></HTML>')