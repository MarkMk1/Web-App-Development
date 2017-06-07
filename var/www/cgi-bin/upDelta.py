#!/usr/bin/env python

import os
import sys
import cgi

# This will basically take the variable delta, assign it to a file within my server,
# and then it will do nothing. When the editor is loaded again, it will load with setContents(delta)

data = cgi.FieldStorage()

log = open("log", "w")
log.write("test")
log.write(os.dirname)
log.write(data.delta)
log.write(data.dir)

log.close()