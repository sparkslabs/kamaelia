#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, time, dircache, os
from cgi import escape

import MimeTypes
import ErrorPages

def sanitizeFilename(filename):
    output = ""
    for char in filename:
        if char >= "0" and char <= "9": output += char
        elif char >= "a" and char <= "z": output += char
        elif char >= "A" and char <= "Z": output += char
        elif char == "-" or char == "_" or char == ".": output += char
    return output

def sanitizePath(uri): #needs work
    outputpath = []
    while uri[0] == "/": #remove leading slashes
        uri = uri[1:]
        if len(uri) == 0: break
    
    splitpath = string.split(uri, "/")
    for directory in splitpath:
        if directory == ".":
            pass
        elif directory == "..":
            if len(outputpath) > 0: outputpath.pop()
        else:
            outputpath.append(directory)
    outputpath = string.join(outputpath, "/")
    return outputpath

def websiteListFilesPage(directory):
    files = dircache.listdir(homedirectory + directory)
    data = u"<html>\n<title>" + directory + u"</title>\n<body style='background-color: black; color: white;'>\n<h2>" + directory + u"</h2>\n<p>Files</p><ul>"
    
    
    for entry in files:
        data += u"<li><a href=\"" + directory + entry + u"\">" + entry + u"</a></li>\n"
    data += u"</ul></body>\n</html>\n\n"
    
    return {
        "statuscode" : "200",
        "data"       : data,
        "type"       : "text/html"
    }

def handler(request):
    print "websiteMinimal.handler"
    try:
        filename = sanitizePath(request["raw-uri"])
        if os.path.isdir(homedirectory + filename):
            if filename[-1:] != "/": filename += "/"
            if os.path.isfile(homedirectory + filename + indexfilename):
                filename += indexfilename
            else:
                yield websiteListFilesPage(filename)
                return
         
        filetype = MimeTypes.workoutMimeType(filename)
                
        sourcefile = open(homedirectory + filename, "rb", 0)
        
        data = sourcefile.read(1024)
        data = (data, sourcefile.read(1024))
        
        resource = {
            "type" : filetype,
            "statuscode" : "200",
            "data" : data[0],
            "incomplete" : len(data[1]) != 0,
        }
        yield resource

        while len(data[1]) > 0:
            data = (data[1], sourcefile.read(1024))
            resource["data"] = data[0]
            resource["incomplete"] = (len(data[1]) != 0)
            yield resource
        
        sourcefile.close()
           
        
    except IOError:
        resource = ErrorPages.getErrorPage(404)
        yield resource
        
    return


indexfilename = "index.html"
homedirectory = "./"
