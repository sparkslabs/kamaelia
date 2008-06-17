#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# ------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: RJL
"""\
========================
Minimal
========================
A simple HTTP request handler for HTTPServer.
Minimal serves files within a given directory, guessing their
MIME-type from their file extension.

Example Usage
-------------
See HTTPResourceGlue.py for how to use request handlers.
"""

import string, time, dircache, os
#from cgi import escape

from Axon.Ipc import producerFinished, shutdown
from Axon.Component import component

from Kamaelia.File.BetterReading import IntelligentFileReader
import Kamaelia.Protocol.HTTP.MimeTypes as MimeTypes
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

def sanitizeFilename(filename):
    """Remove all non-numeric characters other than periods, underscores, and dashes"""
    def check_char(char):
        if char >= "0" and char <= "9": return true
        elif char >= "a" and char <= "z": return true
        elif char >= "A" and char <= "Z": return true
        elif char == "-" or char == "_" or char == ".": return true
        else: return false
    
    return filter(check_char, filename)

def sanitizePath(uri):
    """Strip all leading slashes and remove all dots"""
    outputpath = []
    uri = uri.strip('/')
    
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

# old setup used functions - this needs to be converted to work with
# the new component-based handler system
#def websiteListFilesPage(directory):
#    files = dircache.listdir(homedirectory + directory)
#    data = u"<html>\n<title>" + directory + u"</title>\n<body style='background-color: black; color: white;'>\n<h2>" + #directory + u"</h2>\n<p>Files</p><ul>"
#    
#    
#    for entry in files:
#        data += u"<li><a href=\"" + directory + entry + u"\">" + entry + u"</a></li>\n"
#    data += u"</ul></body>\n</html>\n\n"
#    
#    return {
#        "statuscode" : "200",
#        "data"       : data,
#        "type"       : "text/html"
#    }

# a one shot request handler
class Minimal(component):
    """\
    A simple HTTP request handler for HTTPServer which serves files within a
    given directory, guessing their MIME-type from their file extension.
    
    Arguments:
    -- request - the request dictionary object that spawned this component
    -- homedirectory - the path to prepend to paths requested
    -- indexfilename - if a directory is requested, this file is checked for inside it, and sent if found
    """
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
    
    
    def __init__(self, request, indexfilename = "index.html", homedirectory = "htdocs/"):
            self.request = request
            self.indexfilename = indexfilename
            self.homedirectory = homedirectory
            super(Minimal, self).__init__()
        
    def main(self):
        """Produce the appropriate response then terminate."""
        filepath = self.homedirectory + sanitizePath(self.request["raw-uri"])
        
        error = None
        try:
            if os.path.exists(filepath):
                if os.path.isdir(filepath):
                    filepath = filepath + self.indexfilename
            
                filetype = MimeTypes.workoutMimeType(filepath) 
                resource = {
                        "type"           : filetype,
                        "statuscode"     : "200",
                        #"length" : os.path.getsize(homedirectory + filename) 
                }
                self.send(resource, "outbox")
            else:
                print "Error 404!"
                print "filepath: %s" % (filepath)
                print "os.path.exists(filepath)", os.path.exists(filepath)
                print "os.path.isdir(filepath)", (os.path.isdir(filepath))
                error = 404
                
        except OSError, e:
            error = 404
            
        print "filepath: " + filepath
            
        if error == 404:
            resource = ErrorPages.getErrorPage(404)
            resource["incomplete"] = False
            self.send(resource, "outbox")
            self.send(producerFinished(self), "signal")
            return
            
        self.filereader = IntelligentFileReader(filepath, 50000, 10)
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
                self.send("GARBAGE", "_fileprompt") # we use this to wakeup the filereader
                        
            while self.dataReady("_filecontrol") and not self.dataReady("_fileread"):
                msg = self.recv("_filecontrol")
                if isinstance(msg, producerFinished):
                    done = True
                    
            self.pause()
        
        self.send(producerFinished(self), "signal")

__kamaelia_components__  = ( Minimal, )
