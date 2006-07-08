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

import array
from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.SimpleServerComponent import SimpleServer
import string, time, website

from HTTPParser import *
import HTTPResourceGlue # this works out what the correct response to a request is

def currentTimeHTTP():
    curtime = time.gmtime()
    return time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT", curtime)

class HTTPServer(component):
    """\
    HTTPServer() -> new HTTPServer
    """
    
    Inboxes =  { "inbox"         : "TCP data stream - receive",
                 "mime-signal"   : "Error signals from MIME handler",
                 "http-signal"   : "Error signals from the HTTP resource retriever",
                 "control"       : "Receive shutdown etc. signals" }


    Outboxes = { "outbox"        : "TCP data stream - send",
                 "mime-control"  : "To MIME handler",
                 "http-control"  : "To HTTP resource retriever's signalling inbox",
                 "signal"        : "UNUSED" }

    def __init__(self):
        super(HTTPServer, self).__init__()

    def initialiseComponent(self):
        self.mimehandler = HTTPParser()
        self.httphandler = HTTPRequestHandler()
        #self.httphandler.filereader = TriggeredFileReader()
        
        self.link( (self,"mime-control"), (self.mimehandler,"control") )
        self.link( (self.mimehandler, "signal"), (self, "mime-signal") )

        self.link( (self.mimehandler, "outbox"), (self.httphandler, "inbox") )
        
        self.link( (self, "http-control"), (self.httphandler, "control") )
        self.link( (self.httphandler, "signal"), (self, "http-signal") )
        
        self.addChildren(self.mimehandler, self.httphandler) #self.httphandler.filereader)
        self.httphandler.activate()
        self.mimehandler.activate()
        #self.httphandler.filereader.activate()

        self.link((self.httphandler, "outbox"), (self, "outbox"), passthrough=2)
        self.link((self, "inbox"), (self.mimehandler, "inbox"), passthrough=1)
      
    def main(self):
        self.initialiseComponent()
        loop = True
        while loop:
            yield 1
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
        "inbox"         : "Raw HTTP requests",
        "control"       : "Signal component termination",
        "_handlerinbox"   : "Output from the request handler",
        "_handlercontrol" : "Signals from the request handler"        
    }
    
    Outboxes = {
        "outbox"  : "HTTP responses",
        "signal"  : "Signal connection to close",
        "_handleroutbox" : "POST data etc. for the request handler"
    }

    MapStatusCodeToText = {
        "100" : "100 Continue",
        "200" : "200 OK",
        "302" : "302 Found",
        "304" : "304 Non Modified",        
        "400" : "400 Bad Request",
        "401" : "401 Unauthorised",
        "401" : "403 Forbidden",
        "404" : "404 Not Found",
                        
        #UNCOMMON RESPONSES
        "201" : "201 Created",
        "202" : "202 Accepted", # AKA non-commital response
        "203" : "203 Non-Authoritative Information",
        "204" : "204 No Content",
        "205" : "205 Reset Content",
        "206" : "206 Partial Content",
        "300" : "300 Multiple Choices",
        "301" : "301 Moved Permanently",
        "303" : "303 See Other",
        "305" : "305 Use Proxy",
        "307" : "307 Temporary Redirect",
        "402" : "402 Payment Required",
        "405" : "405 Method Not Allowed",
        "406" : "406 Not Acceptable",
        "407" : "407 Proxy Authentication Required",
        "408" : "408 Request Timeout",
        "409" : "409 Conflict",
        "410" : "410 Gone",
        "411" : "411 Length Required",
        "412" : "412 Precondition Failed",
        "413" : "413 Request Entity Too Large",
        "414" : "414 Request-URI Too Long",
        "415" : "415 Unsupported Media Type",
        "416" : "416 Requested Range Not Satisfiable",
        "417" : "417 Expectation Failed",
        "500" : "500 Internal Server Error",
        "501" : "501 Not Implemented",
        "502" : "502 Bad Gateway",
        "503" : "503 Service Unavailable",
        "505" : "HTTP Version Not Supported"
    }
    
    def resourceUTF8Encode(self, resource):
        if isinstance(resource["data"], unicode):
            resource["data"] = resource["data"].encode("utf-8")
            resource["charset"] = "utf-8"
        
    def __init__(self):
        super(HTTPRequestHandler, self).__init__()

    def formResponseHeader(self, resource, protocolversion, lengthMethod = "explicit"):
        if isinstance(resource.get("statuscode"), int):
            resource["statuscode"] = str(resource["statuscode"])
        elif not isinstance(resource.get("statuscode"), str):
            resource["statuscode"] = "500"
                    
        statustext = self.MapStatusCodeToText.get(resource["statuscode"], "500 Internal Server Error")

        if (protocolversion == "0.9"):
            header = ""        
        else:
            header = "HTTP/1.1 " + statustext + "\r\nServer: Kamaelia HTTP Server (RJL) 0.4\r\nDate: " + currentTimeHTTP() + "\r\n"
            if resource.has_key("charset"):
                header += "Content-Type: " + resource["type"] + "; " + resource["charset"] + "\r\n"
            else:
                header += "Content-Type: " + resource["type"] + "\r\n"
            
            if lengthMethod == "explicit":
                header += "Content-Length: " + str(resource["length"]) + "\r\n"
                
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
       
    def waitingOnNetworkToSend(self):
        return len(self.outboxes["outbox"]) > 1

    def connectResourceHandler(self):
        self.link((self.handler, "outbox"), (self, "_handlerinbox"))
        self.link((self.handler, "signal"), (self, "_handlercontrol"))        
        self.link((self, "_handleroutbox"), (self.handler, "inbox"))
        self.addChildren(self.handler) 
        self.handler.activate()

    def disconnectResourceHandler(self):
        self.unlink((self.handler, "outbox"), (self, "_handlerinbox"))
        self.unlink((self, "_handleroutbox"), (self.handler, "inbox"))        
        self.removeChild(self.handler) 

    def sendChunkExplicit(self, resource):
        if len(resource.get("data","")) > 0:
            self.resourceUTF8Encode(resource)
            self.send(resource["data"], "outbox")
                
    def sendChunkChunked(self, resource):
        if len(resource.get("data","")) > 0:
            self.resourceUTF8Encode(resource)
            self.send(hex(len(resource["data"]))[2:] + "\r\n", "outbox")
            self.send(resource["data"], "outbox")
            self.send("\r\n", "outbox")

    def sendEndChunked(self):
         self.send("0\r\n\r\n", "outbox")

    def sendEndClose(self):
        self.send(producerFinished(self), "outbox")
        
    def sendEndExplicit(self):
        pass
        
    def main(self):
        while 1:
            yield 1        

            while self.dataReady("inbox"):
                request = self.recv("inbox")
                if not isinstance(request, ParsedHTTPHeader):
                    continue
                request = request.header
                
                #ParsedHTTPHeader
                print "Request for " + request["raw-uri"]
                
                # add ["bad"] and ["error-msg"] keys to the request if it is invalid
                self.checkRequestValidity(request)
                
                if request["version"] == "1.1":
                    connection = request["headers"].get("connection", "keep-alive")
                else:
                    connection = request["headers"].get("connection", "close")
                    
                self.handler = HTTPResourceGlue.createRequestHandler(request)
                
                assert(self.handler != None) # if no URL handlers match our request then HTTPResourceGlue should produce a 404 handler
                # Generally even that will not happen because you'll set a "/" handler which catches all
                     
                self.connectResourceHandler()
                
                lengthMethod = ""
                senkChunk = None
                
                while not self.dataReady("_handlerinbox") or self.waitingOnNetworkToSend():
                    self.pause()
                    yield 1
                    
                msg = self.recv("_handlerinbox")
                
                if msg.get("complete"):
                    lengthMethod = "explicit"
                    msg["length"] = len(msg["data"])

                elif msg.has_key("length"):
                    lengthMethod = "explicit"
                        
                if lengthMethod == "explicit":
                    # form and send the header, including a content-length header
                    self.send(self.formResponseHeader(msg, request["version"], "explicit"), "outbox")
                    sendChunk = self.sendChunkExplicit
                    sendEnd = self.sendEndExplicit
                    
                elif request["version"] < "1.1":
                    lengthMethod = "close"
                    self.send(self.formResponseHeader(msg, request["version"], "close"), "outbox")
                    sendChunk = self.sendChunkExplicit
                    sendEnd = self.sendEndClose                
                else:
                    lengthMethod = "chunked"
                    self.send(self.formResponseHeader(msg, request["version"], "chunked"), "outbox")
                    sendChunk = self.sendChunkChunked
                    sendEnd = self.sendEndChunked
                    
                requestEndReached = False
                while 1:
                    if msg:
                        sendChunk(msg)
                        msg = None
                        
                    yield 1
                    if self.dataReady("inbox") and not requestEndReached:
                        request = self.recv("inbox")
                        if isinstance(request, ParsedHTTPEnd):
                            requestEndReached = True
                        else:
                            assert(isinstance(request, ParsedHTTPBodyChunk))
                            self.send(request.bodychunk, "_handleroutbox")
                    elif self.dataReady("_handlerinbox") and not self.waitingOnNetworkToSend():
                        msg = self.recv("_handlerinbox")
                        
                    elif self.dataReady("_handlercontrol") and not self.dataReady("_handlerinbox"):
                        ctrl = self.recv("_handlercontrol")
                        print ctrl
                        if isinstance(ctrl, producerFinished):
                            break
                    else:
                        self.pause()
                
                sendEnd()
                self.disconnectResourceHandler()
                print "sendEnd"
                if lengthMethod == "close" or connection.lower() == "close":
                    self.send(producerFinished(), "signal") #this functionality is semi-complete
                    return

            while self.dataReady("control"):
                temp = self.recv("control")
                if isinstance(temp, shutdown) or isinstance(temp, producerFinished):
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
