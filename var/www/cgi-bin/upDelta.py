#This will basically take the variable delta, assign it to a file within my server,
#and then it will do nothing. When the editor is loaded again, it will load with setContents(delta)
import path from os

log = open("log", "w")
log.write("fuck")
log.write(os.dirname)
