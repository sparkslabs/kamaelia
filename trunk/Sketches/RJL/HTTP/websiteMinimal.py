#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, time, dircache, os
from cgi import escape

def getErrorPage(errorcode, msg = ""):
    if errorcode == 400:
        return { "statuscode" : "400",
                 "data"       : u"<html>\n<title>400 Bad Request</title>\n<body style='background-color: black; color: white;'>\n<h2>400 Bad Request</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
                 "type"       : "text/html" }
    elif errorcode == 404:
        return { "statuscode" : "404",
                 "data"       : u"<html>\n<title>404 Not Found</title>\n<body style='background-color: black; color: white;'>\n<h2>404 Not Found</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
                 "type"       : "text/html" }
    elif errorcode == 500:
        return { "statuscode" : "500",
                 "data"       : u"<html>\n<title>500 Internal Server Error</title>\n<body style='background-color: black; color: white;'>\n<h2>500 Internal Server Error</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
                 "type"       : "text/html" }
    elif errorcode == 501:
        return { "statuscode" : "501",
                 "data"       : u"<html>\n<title>501 Not Implemented</title>\n<body style='background-color: black; color: white;'>\n<h2>501 Not Implemented</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
                 "type"       : "text/html" }

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
                 "type"       : "text/html" }

def websiteHandlerDefault(request):
    try:
        filename = sanitizePath(request["raw-uri"])
        if os.path.isdir(filename):
            if filename[-1:] != "/": filename += "/"
            if os.path.isfile(filename + indexfilename):
                filename += indexfilename
            else:
                return websiteListFilesPage(filename)
         
        filetype = workoutMimeType(filename)
        sourcefile = open(homedirectory + filename, "rb", 0)
        data = sourcefile.read()
        sourcefile.close()
           
        resource = {
            "type" : filetype,
            "statuscode" : "200",
            "data" : data
        }
    except IOError:
        resource = getErrorPage(404)
    
    return resource


def workoutMimeType(filename):
    fileextension = string.rsplit(filename,".",1)[-1]
    if extensionToMimeType.has_key(fileextension):
        return extensionToMimeType[fileextension]
    else:
        return "application/octet-stream"

extensionToMimeType = {
    "png"  : "image/png",
    "gif"  : "image/gif",
    "jpg"  : "image/jpeg",
    "jpeg" : "image/jpeg",
    "txt"  : "text/plain",
    "htm"  : "text/html",
    "html" : "text/html",
    "css"  : "text/css",
    "cool" : "text/cool"
}	

indexfilename = "index.html"
homedirectory = "./"
URLHandlers = [
    ["/"                       , websiteHandlerDefault]
]
