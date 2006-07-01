#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

#possible dirty hack to sort things out...
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

import array
from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.SimpleServerComponent import SimpleServer
from Axon.Ipc import producerFinished, errorInformation
import string, time, website

from HTTPParser import HTTPParser
import HTTPResourceGlue # this works out what the correct response to a request is

def currentTimeHTTP():
    curtime = time.gmtime()
    return time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT", curtime)

class HTTPServer(component):
    """\
    HTTPServer() -> new HTTPServer
    """
    
    Inboxes =  { "inbox"         : "TCP data stream - receive",
                 "mime-outbox"   : "Data from MIME handler",
                 "mime-signal"   : "Error signals from MIME handler",
                 "http-outbox"   : "Data from HTTP resource retriever",
                 "http-signal"   : "Error signals from the HTTP resource retriever",
                 "control"       : "Receive shutdown etc. signals" }


    Outboxes = { "outbox"        : "TCP data stream - send",
                 "mime-inbox"    : "To MIME handler",
                 "mime-control"  : "To MIME handler",
                 "http-inbox"    : "To HTTP resource retriever",
                 "http-control"  : "To HTTP resource retriever's signalling inbox",
                 "signal"        : "UNUSED" }

    def __init__(self):
        super(HTTPServer, self).__init__()

    def initialiseComponent(self):
        self.mimehandler = HTTPParser()
        self.httphandler = HTTPRequestHandler()
        #self.httphandler.filereader = TriggeredFileReader()
        
        self.link( (self,"mime-inbox"), (self.mimehandler,"inbox") )
        self.link( (self,"mime-control"), (self.mimehandler,"control") )
        self.link( (self.mimehandler,"outbox"), (self, "mime-outbox") )
        self.link( (self.mimehandler,"signal"), (self, "mime-signal") )

        self.link( (self, "http-inbox"), (self.httphandler, "inbox") )
        self.link( (self, "http-control"), (self.httphandler, "control") )
        self.link( (self.httphandler, "outbox"), (self, "http-outbox") )
        self.link( (self.httphandler, "signal"), (self, "http-signal") )

        #elf.link( (self.httphandler, "filereader-inbox"), (self.httphandler.filereader, "inbox") )
        #self.link( (self.httphandler.filereader,"outbox"), (self.httphandler, "filereader-outbox") )
        
        self.addChildren(self.mimehandler, self.httphandler) #self.httphandler.filereader)
        self.httphandler.activate()
        self.mimehandler.activate()
        #self.httphandler.filereader.activate()

    def main(self):
        self.initialiseComponent()
        loop = True
        while loop:
            yield 1
            while self.dataReady("inbox"):
                temp = self.recv("inbox")
                self.send(temp, "mime-inbox")

            while self.dataReady("control"):
                temp = self.recv("control")
                if isinstance(temp, producerFinished):
                    self.send(temp, "mime-control")
                elif isinstance(temp, shutdownMicroprocess) or isinstance(temp, shutdown):
                    self.send(shutdown(), "mime-control")
                    self.send(shutdown(), "http-control")
                    #print "HTTPServer received shutdown"
                    loop = False
                    break
            
            while self.dataReady("http-outbox"):
                temp = self.recv("http-outbox")
                self.send(temp, "outbox")

            while self.dataReady("mime-outbox"):
                temp = self.recv("mime-outbox")
                self.send(temp, "http-inbox")

            while self.dataReady("mime-signal"):
                temp = self.recv("mime-signal")
                if isinstance(temp, producerFinished):
                    pass
                    #we don't need to care yet - wait 'til the request handler finishes
            
            while self.dataReady("http-signal"):
                temp = self.recv("http-signal")
                if isinstance(temp, producerFinished):
                    sig = producerFinished(self)
                    self.send(sig, "mime-control")                
                    self.send(sig, "signal")
                    loop = False
                    #close the connection
            
            self.pause()
                
        self.closeDownComponent()
        
    def closeDownComponent(self):
        for child in self.childComponents():
            self.removeChild(child)
        self.mimehandler = None
        self.httphandler = None

class HTTPRequestHandler(component):
    Inboxes =  {
        "inbox"   : "Raw HTTP requests",
        "control" : "Signal component termination"
    }
    
    Outboxes = {
        "outbox"  : "HTTP responses",
        "signal"  : "Signal connection to close"
    }

    def convertUnicodeToByteStream(self, data):
        return data.encode("utf-8")
        
    def __init__(self):
        super(HTTPRequestHandler, self).__init__()
        
    def provideResource(self, request):
        resourceGen = HTTPResourceGlue.fetchResource(request)
        
        try:
            resource = resourceGen.next()
            # if the response is marked as complete, we need not used chunked transfer encoding
                
            complete = not resource.get("incomplete", True) 
            
            if request["method"] == "HEAD": #just send the header
                complete = True
                resource["data"] = ""
                
            if complete == True:
                # support unicode strings as resource data (as opposed to octet-strings)
                if isinstance(resource["data"], unicode):
                    resource["data"] = self.convertUnicodeToByteStream(resource["data"])
                    resource["charset"] = "utf-8"
                
                # form and send the header, including a content-length header
                self.send(self.formResponseHeader(resource, request["version"], "explicit"), "outbox")
                # send the message body (page data)
                self.send(resource["data"], "outbox")
                return "explicit"
                
            else:
                lengthMethod = "chunked" # preferred encoding is chunked

                if request["version"] < "1.1":
                    lengthMethod = "close"
                
                self.send(self.formResponseHeader(resource, request["version"], lengthMethod), "outbox")

                while 1:
                    if lengthMethod == "chunked":
                        self.send(hex(len(resource["data"]))[2:] + "\r\n", "outbox")
                        self.send(resource["data"], "outbox")
                        self.send("\r\n", "outbox")
                    elif lengthMethod == "close":
                        self.send(resource["data"], "outbox")
                    
                    resource["data"] = ""
                    resource.update(resourceGen.next())
                
                
        except StopIteration, e:
            print "StopIteration in provideResource"
            if lengthMethod == "chunked":
                self.send("0\r\n\r\n");
            return lengthMethod;

    def formResponseHeader(self, resource, protocolversion, lengthMethod = "explicit"):
        if isinstance(resource.get("statuscode"), int):
            resource["statuscode"] = str(resource["statuscode"])
        elif not isinstance(resource.get("statuscode"), str):
            resource["statuscode"] = "500"
                    
        if resource["statuscode"] == "200": statustext = "200 OK"
        elif resource["statuscode"] == "400": statustext = "400 Bad Request"
        elif resource["statuscode"] == "404": statustext = "404 Not Found"
        elif resource["statuscode"] == "500": statustext = "500 Internal Server Error"
        elif resource["statuscode"] == "501": statustext = "501 Not Implemented"
        elif resource["statuscode"] == "411": statustext = "411 Length Required"
        elif resource["statuscode"] == "501": statustext = "411 Not Implemented"
        else: statustext = resource["statuscode"]

        if (protocolversion == "0.9"):
            header = ""        
        else:
            header = "HTTP/1.1 " + statustext + "\r\nServer: Kamaelia HTTP Server (RJL) 0.2\r\nDate: " + currentTimeHTTP() + "\r\n"
            if resource.has_key("charset"):
                header += "Content-Type: " + resource["type"] + "; " + resource["charset"] + "\r\n"
            else:
                header += "Content-Type: " + resource["type"] + "\r\n"
            
            if lengthMethod == "explicit":
                header += "Content-length: " + str(len(resource["data"])) + "\r\n"
            elif lengthMethod == "chunked":
                header += "Transfer-Encoding: chunked\r\n"
                header += "Connection: keep-alive\r\n"                
            else: #connection close
                header += "Connection: close\r\n"

            header += "\r\n";            
        return header

    def checkRequestValidity(self, request):
        if request["protocol"] != "HTTP":
            request["bad"] = "400"
            
        elif request["version"] > "1.0" and not request["headers"].has_key("host"):
            request["bad"] = "400"
            request["error-msg"] = "Host header required."
            
        if request["method"] not in ("GET", "HEAD", "POST"):
            request["bad"] = "501"
       
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                request = self.recv("inbox")
                print "Request for " + request["raw-uri"]
                
                # add ["bad"] and ["error-msg"] keys to the request if it is invalid
                self.checkRequestValidity(request)
                    
                if request["version"] == "1.1":
                    connection = request["headers"].get("connection", "keep-alive")
                else:
                    connection = request["headers"].get("connection", "close")


                if self.provideResource(request) == "close":
                    connection = "close"
                    
                if connection.lower() == "close":
                    self.send(producerFinished(), "signal") #this functionality is semi-complete
                    return

            while self.dataReady("control"):
                temp = self.recv("control")
                if isinstance(temp, shutdownMicroprocess) or isinstance(temp, producerFinished):
                    return

            self.pause()

if __name__ == '__main__':
    from Axon.Component import scheduler
    import socket
    SimpleServer(protocol=HTTPServer, port=8082, socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).activate()
    #pipeline(
    #    Introspector(),
    #    TCPClient("127.0.0.1", 1500),
    #).activate()
    #Lagger().activate()
    scheduler.run.runThreads(slowmo=0)
