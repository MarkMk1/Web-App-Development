#!/usr/bin/env python

import os
import json

def saveJSON(username, password, data):
	#targetDir = '\\userData'
	#os.chdir(targetDir)
	with open(username+password+'.JSON', 'w') as outfile:
		json.dump(data, outfile)
		outfile.close

#sampleJSON = {"glossary": {"title": "example glossary","GlossDiv": {"title": "S","GlossList": {"GlossEntry": {"ID": "SGML","SortAs": "SGML","GlossTerm": "Standard Generalized Markup Language","Acronym": "SGML","Abbrev": "ISO 8879:1986","GlossDef": {"para": "A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso": ["GML", "XML"]},"GlossSee": "markup"}}}}}
#saveJSON('mark', 'cats', sampleJSON)

def loadJSON(username, password):
    #targetDir = '\\userData'
    #os.chdir(targetDir)
    JSON = {}
    with open(username+password+'.JSON') as outfile:
        data = json.load(outfile)
        return data
