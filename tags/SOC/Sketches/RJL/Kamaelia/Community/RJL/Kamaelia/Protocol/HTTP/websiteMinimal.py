#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
========================
websiteMinimal
========================
A simple HTTP request handler for HTTPServer.
websiteMinimal serves files within a given directory, guessing their
MIME-type from their file extension.
"""

import string, time, dircache, os
#from cgi import escape

from Axon.Ipc import producerFinished, shutdown
from Axon.Component import component

from Kamaelia.Community.RJL.Kamaelia.File.BetterReading import IntelligentFileReader
import Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.MimeTypes as MimeTypes
import Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

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
            if os.path.exists(homedirectory + filename) and not os.path.isdir(homedirectory + filename):
                resource = {
                    "type"           : filetype,
                    "statuscode"     : "200",
                    #"length" : os.path.getsize(homedirectory + filename) 
                }
                self.send(resource, "outbox")
            else:
                print "Error 404, " + homedirectory + filename + " is not a file"
                error = 404
                
        except OSError, e:
            error = 404
            
        if error == 404:
            resource = ErrorPages.getErrorPage(404)
            resource["incomplete"] = False
            self.send(resource, "outbox")
            self.send(producerFinished(self), "signal")
            return
            
        self.filereader = IntelligentFileReader(homedirectory + filename, 50000, 10)
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

__kamaelia_components__  = ( websiteMinimal, )

indexfilename = "index.html"
homedirectory = "htdocs/"
