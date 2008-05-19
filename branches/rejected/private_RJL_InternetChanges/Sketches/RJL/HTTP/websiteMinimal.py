#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import string, time, dircache, os
from cgi import escape

import MimeTypes
import ErrorPages

from Axon.Ipc import producerFinished, shutdown

import sys
sys.path.append("../Util/")
sys.path.append("../File/")
from Axon.Component import component
from BetterReading import IntelligentFileReader

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

# a one shot request handler
class websiteMinimal(component):
    Inboxes = {
        "inbox"        : "UNUSED",
        "control"      : "UNUSED",
        "_fileread"    : "File data",
        "_filecontrol" : "Signals from file reader"
    }
    Outboxes = {
        "outbox"      : "Response dictionaries",
        "signal"      : "UNUSED",
		"_fileprompt" : "Get the file reader to do some reading",
        "_filesignal" : "Shutdown the file reader"
	}
    
    
    def __init__(self, request):
	    self.request = request
	    super(websiteMinimal, self).__init__()
        
    def main(self):
        print "websiteMinimal.handler"
        filename = sanitizePath(self.request["raw-uri"])
        #if os.path.isdir(homedirectory + filename):
        #    if filename[-1:] != "/": filename += "/"
        #    if os.path.isfile(homedirectory + filename + indexfilename):
        #        filename += indexfilename
        #    else:
        #        yield websiteListFilesPage(filename)
        #        return
         
        filetype = MimeTypes.workoutMimeType(filename)
        
        error = None
        try:
            if os.path.isfile(homedirectory + filename):
                resource = {
                    "type"           : filetype,
                    "statuscode"     : "200",
                    "length" : os.path.getsize(homedirectory + filename) 
                }
                self.send(resource, "outbox")
            else:
                error = 404
                
        except OSError, e:
            error = 404
            
        if error == 404:
            resource = ErrorPages.getErrorPage(404)
            resource["incomplete"] = False
            self.send(resource, "outbox")
            self.send(producerFinished(self), "signal")
            return
            
        self.filereader = IntelligentFileReader(homedirectory + filename, 30000, 5)
        self.link((self, "_fileprompt"), (self.filereader, "inbox"))
        self.link((self, "_filesignal"), (self.filereader, "control"))
        self.link((self.filereader, "outbox"), (self, "_fileread"))
        self.link((self.filereader, "signal"), (self, "_filecontrol"))
        self.addChildren(self.filereader)
        self.filereader.activate()
        yield 1        
        
        done = False
        while not done:
            yield 1
            while self.dataReady("_fileread") and len(self.outboxes["outbox"]) < 3:
                msg = self.recv("_fileread")
                resource = { "data" : msg }
                self.send(resource, "outbox")
                
            if len(self.outboxes["outbox"]) < 3:
                self.send("GARBAGE", "_fileprompt")
                        
            while self.dataReady("_filecontrol") and not self.dataReady("_fileread"):
                msg = self.recv("_filecontrol")
                if isinstance(msg, producerFinished):
                    done = True
                    
            self.pause()
        
        self.send(producerFinished(self), "signal")
        #print "websiteMinimal terminated"

indexfilename = "index.html"
homedirectory = "~/kamhttpsite/"
