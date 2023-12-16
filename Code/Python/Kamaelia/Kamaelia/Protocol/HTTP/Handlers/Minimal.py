#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

System Requirements
-------------------
This component requires a UNIX system to be run currently.
"""

import string, time, os
#import dircache  # Used to be used, currently comment out and is a python-2-ism so removed
#from cgi import escape

from Axon.Ipc import producerFinished, shutdown
from Axon.Component import component

from Kamaelia.File.BetterReading import IntelligentFileReader
import Kamaelia.Protocol.HTTP.MimeTypes as MimeTypes
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

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
    uri = uri.lstrip('/')

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

# FIXME: I tend to dislike <X>Factory functions. It tends to miss what's
# FIXME: actually being done. What this is really doing is creating
# FIXME: PreconfiguredMinimalHandlers for a specific server configuration.
# FIXME: As a result this name should change. Not a block to merge, but will
# FIXME: need revisiting really.
# FIXME: Also, this change strikes me as change for change's sake :-/
def MinimalFactory(indexfilename='index.html', homedirectory='htdocs'): 
    def _getMinimal(request):
        return Minimal(request, indexfilename, homedirectory)
    
    return _getMinimal

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
#        "content-type"       : "text/html"
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
    
    # FIXME: If this used inheritable defaults instead, this would actually
    # FIXME: probably eliminate the need for the factory function above.

    def __init__(self, request, indexfilename='index.html', homedirectory='htdocs/', **argd):
        super(Minimal, self).__init__(**argd)
        self.request = request
        self.indexfilename = indexfilename
        self.homedirectory = homedirectory

    def main(self):
        """Produce the appropriate response then terminate."""
        filename = sanitizePath(self.request["uri-suffix"])
        if not (self.homedirectory.endswith('/') or filename.startswith('/')):
            filepath = self.homedirectory + '/' + filename   # FIXME: Should use os.path.join 
        else:
            filepath = self.homedirectory + filename         # FIXME: Should use os.path.join

        # print (filepath)

        # FIXME: Logic here looks a little bust actually, and can probably
        # FIXME: be reworked further and simplified.
        filetype = MimeTypes.workoutMimeType(filename)

        error = None
        try:
            if os.path.exists(filepath):
                if os.path.isdir(filepath):
                    filepath += self.indexfilename  # FIXME: Assumes X/index.html always exists
                    
                resource = {
                    "content-type"   : filetype,
                    "statuscode"     : 200,
                }
                self.send(resource, "outbox")                    
            else:
                print ("Error 404, " + filename + " is not a file")
                print ("self.homedirectory(%s) , filename(%s)" % (self.homedirectory , filename))
                print ("os.path.exists(self.homedirectory + filename)", os.path.exists(self.homedirectory + filename))
                print ("not os.path.isdir(self.homedirectory + filename)", (not os.path.isdir(self.homedirectory + filename)))
                error = 404

        except OSError:
            e = sys.exc_info()[1]
            error = 404

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
