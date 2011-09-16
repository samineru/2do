#! /usr/bin/env python
import sys
import os.path
from optparse import OptionParser
#2do.py
#assumes .2do if there is no specified todolist name


def vPrint(string, threshhold = 1):
    if int(options.verbosity) >= threshhold:
        print string

def processFile(filePath):
    vPrint("opening '" + filePath + "'", 3)
    
    if filePath[-1] == '/': #If the user has given a directory
		fileHandler = easyOpen(filePath + ".2do") #assume presence of .2do
    else:
        fileHandler = easyOpen(filePath)#otherwise open given file
    
    directory = filePath[:filePath.rfind("/")+1]
    filename = shortFileName(filePath)	
    
    vPrint("\n  " + filePath + ":", 2)
        
    for line in fileHandler:
        processLine(line[:-1], directory)

    vPrint("} END " + filePath +"\n", 2)

def processLine(line, directory):
    vPrint("Processing " + line + " at " + directory, 3)
    cleanLine = line.lstrip(" \t") #remove all leading spaces and tabs
    if not cleanLine:
        pass
    #If the cleaned line begins with ./ it is a reference to another todo
    elif (cleanLine[0:2] == "./") & options.recurse: 
		#So go process that
        processFile(directory+line.lstrip(" ")[2:])
    elif cleanLine[0] =="#": #If it's commented
        pass
    elif cleanLine == "":
		pass 
    else:
        print line #Otherwise print it

def shortFileName(filePath):
    return filePath[filePath.rfind("/")+1:]

def easyOpen(filePath):
	if os.path.isfile(filePath):
		return open(filePath);
	else:
		vPrint ("'" + filePath+ "' not found", 1)
                exit()

parser = OptionParser()
parser.add_option("-v", "--verbosity",
				  action="store", dest="verbosity", default=1,
				  help="1 = minimal, 2 = verbose, 3 = debug, 4 = OH GOD WHAT DID YOU DO")
				  
parser.add_option("-n", "--inhibit-recursion",
				  action="store_false", dest="recurse", default=True,
				  help="Prevent inline replacement of references to other todolists")

options, args = parser.parse_args()
if args:
 filePath = args[0]
else:
	if os.path.isfile(".2do"):
		filePath = ".2do"
	else:
		print "No file found!"; exit()

vPrint ("Setting verbosity level to " + str(options.verbosity), 3)
vPrint ("Setting recursion to " + str(options.recurse), 3)



if filePath:
	processFile(filePath)
else:
	vPrint ("No .2do file found, or other file given", 1)


