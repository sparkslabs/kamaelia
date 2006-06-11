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
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.SimpleServerComponent import SimpleServer
from Axon.Ipc import producerFinished, errorInformation
import string, time, website
from Lagger import Lagger
from HTTPParser import HTTPParser

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
        while 1:
            yield 1
            while self.dataReady("inbox"):
                temp = self.recv("inbox")
                self.send(temp, "mime-inbox")

            while self.dataReady("control"):
                temp = self.recv("control")
                if isinstance(temp, shutdownMicroprocess) or isinstance(temp, producerFinished):
                    self.send(temp, "mime-control")
                    self.send(temp, "http-control")
                    return
            
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
                    return
                    #close the connection
                    
            self.pause()
            
    def closeDownComponent(self):
        for child in self.childComponents():
            self.removeChild(child)
        self.mimehandler = None
        self.httphandler = None

class HTTPRequestHandler(component):
    Inboxes =  { "inbox"               : "Raw HTTP requests",
                 #"filereader-outbox"   : "File reader's outbox",
                 "control"             : "Signal component termination" }
    Outboxes = { "outbox"              : "HTTP request object",
                 #"filereader-inbox"    : "File reader's inbox",
                 "signal"              : "Signal connection to close" }

    def convertUnicodeToByteStream(self, data):
        return data.encode("utf-8")
        
    def __init__(self):
        super(HTTPRequestHandler, self).__init__()
        

    def fetchResource(self, request):
        for (prefix, handler) in website.URLHandlers:
            if request["raw-uri"][:len(prefix)] == prefix:
                resource = handler(request)
                return resource
        
    def formHeaderResponse(self, resource, protocolversion):
        if resource["statuscode"] == "200": statustext = "200 OK"
        if resource["statuscode"] == "400": statustext = "400 Bad Request"
        if resource["statuscode"] == "404": statustext = "404 Not Found"
        if resource["statuscode"] == "500": statustext = "500 Internal Server Error"
        if resource["statuscode"] == "501": statustext = "501 Not Implemented"
        if resource["statuscode"] == "411": statustext = "411 Length Required"

        if (protocolversion == "0.9"):
            header = ""        
        else:
            header = "HTTP/1.1 " + statustext + "\nServer: Kamaelia HTTP Server (RJL) 0.2\nDate: " + currentTimeHTTP() + "\n"
            if resource.has_key("charset"):
                header += "Content-type: " + resource["type"] + "; " + resource["charset"] + "\n"
            else:
                header += "Content-type: " + resource["type"] + "\n"
            header += "Content-length: " + str(len(resource["data"])) + "\n\n"
        return header

    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                request = self.recv("inbox")
                print "Request for " + request["raw-uri"]
                if request["bad"] == "411":
                    pagedata = website.getErrorPage(411, "Um - content-length plz!")
                    self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
                elif request["bad"]:
                    pagedata = website.getErrorPage(400, "Your request sucked!")
                    self.send(self.formHeaderResponse(pagedata, "1.0") + pagedata["data"], "outbox")

                elif request["protocol"] != "HTTP":
                    pagedata = website.getErrorPage(400, "Non-HTTP")
                    self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
                else:
                    if request["version"] > "1.0" and not request["headers"].has_key("host"):
                        pagedata = website.getErrorPage(400, "could not find host header")
                        self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
                    elif request["method"] == "GET" or request["method"] == "POST":
                        pagedata = self.fetchResource(request)
                        if isinstance(pagedata["data"], unicode):
                             pagedata["data"] = self.convertUnicodeToByteStream(pagedata["data"])
                             pagedata["charset"] = "utf-8"
                             
                        self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
                    else:
                        pagedata = website.getErrorPage(501,"The request method is not implemented")
                        self.send(self.formHeaderResponse(pagedata, request["version"]) + pagedata["data"], "outbox")
                        print "Sent 501 not implemented response"                    
                    
                    if request["version"] == "1.1":
                        connection = request["headers"].get("connection", "keep-alive")
                    else:
                        connection = request["headers"].get("connection", "close")
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
    pipeline(
        Introspector(),
        TCPClient("127.0.0.1", 1500),
    ).activate()
    #Lagger().activate()
    scheduler.run.runThreads(slowmo=0)
