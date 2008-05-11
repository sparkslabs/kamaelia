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
# -------------------------------------------------------------------------
"""\
=================
HTTP Parser
=================

This component is for transforming HTTP requests or responses
into multiple easy-to-use dictionary objects.

Example Usage
-------------
Unless you are implementing a new HTTP component you should not
use this component directly. Either SimpleHTTPClient, HTTPServer (in
conjuncton with SimpleServer) or SingleShotHTTPClient will
likely serve your needs.

If you want to use it directly, note that it doesn't output strings
but ParsedHTTPHeader, ParsedHTTPBodyChunk and ParsedHTTPEnd objects.

If you want to play around with parsing HTTP responses: (like a client)

pipeline(
    ConsoleReader(),
    HTTPParser(mode="response"),
    ConsoleEchoer()
).run()

If you want to play around with parsing HTTP requests: (like a server)

pipeline(
    ConsoleReader(),
    HTTPParser(mode="response"),
    ConsoleEchoer()
).run()
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
import string

#modify to handle %20 style encoding
def splitUri(url):
    requestobject = { "raw-uri": url, "uri-protocol": "", "uri-server": "" }
    splituri = string.split(requestobject["raw-uri"], "://")
    if len(splituri) > 1:
        requestobject["uri-protocol"] = splituri[0]
        requestobject["raw-uri"] = requestobject["raw-uri"][len(splituri[0] + "://"):]
    
    splituri = string.split(requestobject["raw-uri"], "/")
    if splituri[0] != "":
        requestobject["uri-server"] = splituri[0]
        requestobject["raw-uri"] = requestobject["raw-uri"][len(splituri[0]):]
    else:
        if requestobject["uri-protocol"] != "": #then it's the server
            requestobject["uri-server"] = requestobject["raw-uri"]
            requestobject["raw-uri"] = "/"
        else:
            requestobject["uri-server"] = ""
        
    splituri = string.split(requestobject["uri-server"], ":")
    if len(splituri) == 2:
        requestobject["uri-port"] = splituri[1]
        requestobject["uri-server"] = splituri[0]
    
    splituri = string.split(requestobject["uri-server"], "@")
    if len(splituri) == 2:
        requestobject["uri-username"] = splituri[0]
        requestobject["uri-server"] = requestobject["uri-server"][len(splituri[0] + "@"):]
        splituri = string.split(requestobject["uri-username"], ":")
        if len(splituri) == 2:
            requestobject["uri-username"] = splituri[0]
            requestobject["uri-password"] = splituri[1]
            
    return requestobject
    
def removeTrailingCr(line):
    if len(line) == 0:
        return line
    elif line[-1] == "\r":
        return line[0:-1]
    else:
        return line

class ParsedHTTPHeader(object):
    def __init__(self, header):
        self.header = header
    
class ParsedHTTPBodyChunk(object):
    def __init__(self, bodychunk):
        self.bodychunk = bodychunk
        
class ParsedHTTPEnd(object):
    pass
    
class HTTPParser(component):
    """Component that transforms HTTP requests or responses from a
    single TCP connection into multiple easy-to-use dictionary objects."""
    
    Inboxes =  {
        "inbox"         : "Raw HTTP requests/responses",
        "control"       : "UNUSED"
    }
    Outboxes = {
        "outbox"        : "HTTP request object",
        "debug"         : "Debugging information",
        "signal"        : "UNUSED"
    }
    
    def __init__(self, mode="request"):
        super(HTTPParser, self).__init__()
        self.mode = mode
        #print "Parser init"
        self.requeststate = 1 # awaiting request line
        self.lines = []
        self.readbuffer = ""
        
    def splitProtocolVersion(self, protvers, requestobject):
        protvers = protvers.split("/")
        if len(protvers) != 2:
            requestobject["protocol"] = protvers[0]
            requestobject["version"] = "0"
        else:
            requestobject["protocol"] = protvers[0]
            requestobject["version"]  = protvers[1]
    
    def dataFetch(self):
        """Read once from inbox (generally a TCP connection) and add
        what is received to the readbuffer. This is somewhat inefficient for long lines maybe O(n^2)"""
        if self.dataReady("inbox"):
            self.readbuffer += self.recv("inbox")
            return 1
        else:
            return 0
            
    def debug(self, msg):
        self.send(msg, "debug")
    
    def shouldShutdown(self):
        while self.dataReady("control"):
            temp = self.recv("control")
            if isinstance(temp, shutdown):
                self.debug("HTTPParser should shutdown")
                return True
        
        return False
        
    def nextLine(self):
        "Fetch the next complete line in the readbuffer, if there is one"
        lineendpos = string.find(self.readbuffer, "\n")
        if lineendpos == -1:
            return None
        else:
            line = removeTrailingCr(self.readbuffer[:lineendpos])
            self.readbuffer = self.readbuffer[lineendpos + 1:] #the remainder after the \n
            self.debug("Fetched line: " + line)
            return line
    
    def main(self):

        while 1:
            self.debug("HTTPParser::main - stage 0")
            if self.mode == "request":
                requestobject = { "bad": False,
                                  "headers": {},
                                  "raw-uri": "",
                                  "version": "0.9",
                                  "method": "",
                                  "protocol": "",
                                  "body": "" }
            else:
                requestobject = { "bad": False,
                                  "headers": {},
                                  "responsecode": "",
                                  "version": "0.9",
                                  "method": "",
                                  "protocol": "",
                                  "body": "" }
           
            self.debug("HTTPParser::main - awaiting initial line")
            #state 1 - awaiting initial line
            currentline = None
            while currentline == None:
                self.debug("HTTPParser::main - stage 1")
                if self.shouldShutdown(): return
                while self.dataFetch():
                    pass
                currentline = self.nextLine()
                if currentline == None:
                    self.pause()
                    yield 1
                
            self.debug("HTTPParser::main - initial line found")
            splitline = string.split(currentline, " ")
            
            if self.mode == "request":
                #e.g. GET / HTTP/1.0
                if len(splitline) < 2:
                    requestobject["bad"] = True
                elif len(splitline) == 2:
                    # must be HTTP/0.9
                    requestobject["method"] = splitline[0]
                    requestobject["raw-uri"] = splitline[1]
                    requestobject["protocol"] = "HTTP"
                    requestobject["version"] = "0.9"
                else: #deal with normal HTTP including badly formed URIs
                    requestobject["method"] = splitline[0]

                    #next line supports all working clients but also 
                    #some broken clients that don't encode spaces properly!
                    #update is used to merge the uri-dictionary with the request object
                    requestobject.update(splitUri(string.join(splitline[1:-1], "%20")))
                    self.splitProtocolVersion(splitline[-1], requestobject)
                    
                    #if requestobject["protocol"] != "HTTP":
                    #    requestobject["bad"] = True
            else:
                #e.g. HTTP/1.1 200 OK that's fine
                if len(splitline) < 2:
                    requestobject["bad"] = True
                else:
                    requestobject["responsecode"] = splitline[1]
                    self.splitProtocolVersion(splitline[0], requestobject)
            
            if not requestobject["bad"]:
                if self.mode == "response" or requestobject["method"] == "PUT" or requestobject["method"] == "POST":
                    bodiedrequest = True
                else:
                    bodiedrequest = False

                #state 2 - as this is a valid request, we now accept headers	
                previousheader = ""
                endofheaders = False
                while not endofheaders:
                    self.debug("HTTPParser::main - stage 2")
                    if self.shouldShutdown(): return						
                    while self.dataFetch():
                        pass
                        
                    currentline = self.nextLine()
                    while currentline != None:
                        self.debug("HTTPParser::main - stage 2.1")
                        if currentline == "":
                            #print "End of headers found"
                            endofheaders = True
                            break
                        else:
                            if currentline[0] == " " or currentline[0] == "\t": #continued header
                                requestobject["headers"][previousheader] += " " + string.lstrip(currentline)
                            else:
                                splitheader = string.split(currentline, ":")
                                #print "Found header: " + splitheader[0]
                                requestobject["headers"][string.lower(splitheader[0])] = string.lstrip(currentline[len(splitheader[0]) + 1:])
                        currentline = self.nextLine()
                        #should parse headers header
                    if not endofheaders:
                        self.pause()
                        yield 1

                self.debug("HTTPParser::main - stage 2 complete")
                if requestobject["headers"].has_key("host"):
                    requestobject["uri-server"] = requestobject["headers"]["host"]
                
                if requestobject["version"] == "1.1":
                    requestobject["headers"]["connection"] = requestobject["headers"].get("connection", "keep-alive")
                else:
                    requestobject["headers"]["connection"] = requestobject["headers"].get("connection", "close")

                # The header section is complete, so send it on.
                self.send(ParsedHTTPHeader(requestobject), "outbox")
                if bodiedrequest:
                    self.debug("HTTPParser::main - stage 3 start")
                    #state 3 - the headers are complete - awaiting the message
                    if requestobject["headers"].get("transfer-encoding","").lower() == "chunked":
                        bodylength = -1
                        while bodylength != 0:
                            self.debug("HTTPParser::main - stage 3.chunked")                        
                            currentline = None
                            while currentline == None:
                                self.debug("HTTPParser::main - stage 3.chunked.1")
                                if self.shouldShutdown(): return
                                while self.dataFetch():
                                    pass
                                currentline = self.nextLine()
                                if currentline == None:
                                    self.pause()
                                    yield 1
                            #print requestobject
                            splitline = currentline.split(";")

                            try:
                                bodylength = string.atoi(splitline[0], 16)
                            except ValueError:
                                print "Warning: bad chunk length in request/response being parsed by HTTPParser"
                                bodylength = 0
                                requestobject["bad"] = True

                            self.debug("HTTPParser::main - chunking: '%s' '%s' %d" % (currentline, splitline, bodylength))
                             
                            if bodylength != 0:                                
                                while len(self.readbuffer) < bodylength:
                                    self.debug("HTTPParser::main - stage 3.chunked.2")
                                    if self.shouldShutdown(): return						
                                    while self.dataFetch():
                                        pass
                                        
                                    if len(self.readbuffer) < bodylength:
                                        self.pause()
                                        yield 1
                                # we could do better than this - this will eat memory when overly large chunks are used
                                self.send(ParsedHTTPBodyChunk(self.readbuffer[:bodylength]), "outbox")
                            
                            if self.readbuffer[bodylength:bodylength + 2] == "\r\n":
                                self.readbuffer = self.readbuffer[bodylength + 2:]
                            elif self.readbuffer[bodylength:bodylength + 1] == "\n":
                                self.readbuffer = self.readbuffer[bodylength + 1:]
                            else:
                                print "Warning: no trailing new line on chunk in HTTPParser"
                                requestobject["bad"] = True
                                break
                            
                            if bodylength == 0:
                                break
                    elif requestobject["headers"].has_key("content-length"):
                        if string.lower(requestobject["headers"].get("expect", "")) == "100-continue":
                            #we're supposed to say continue, but this is a pain
                            #and everything still works if we don't just with a few secs delay
                            pass
                        self.debug("HTTPParser::main - stage 3.length-known start")
                        
                        bodylengthremaining = int(requestobject["headers"]["content-length"])
                         
                        while bodylengthremaining > 0:
                            #print "HTTPParser::main - stage 3.length known.1"
                            if self.shouldShutdown(): return						
                            while self.dataFetch():
                                pass
                             
                            if bodylengthremaining < len(self.readbuffer): #i.e. we have some extra data from the next request
                                self.send(ParsedHTTPBodyChunk(self.readbuffer[:bodylengthremaining]), "outbox")
                                self.readbuffer = self.readbuffer[bodylengthremaining:]
                                bodylengthremaining = 0
                            elif len(self.readbuffer) > 0:
                                bodylengthremaining -= len(self.readbuffer)
                                self.send(ParsedHTTPBodyChunk(self.readbuffer), "outbox")
                                self.readbuffer = ""
                                
                            if bodylengthremaining > 0:
                                self.pause()
                                yield 1
                        
                        self.readbuffer = self.readbuffer[bodylengthremaining:] #for the next request
                    else: #we'll assume it's a connection: close jobby
                        #THIS CODE IS BROKEN AND WILL NOT TERMINATE UNTIL CSA SIGNALS HALF-CLOSURE OF CONNECTIONS!
                        self.debug("HTTPParser::main - stage 3.connection-close start")
                        connectionopen = True
                        while connectionopen:
                            #print "HTTPParser::main - stage 3.connection close.1"
                            if self.shouldShutdown(): return						
                            while self.dataFetch():
                                #print "!"
                                pass
                                
                            if len(self.readbuffer) > 0:
                                self.send(ParsedHTTPBodyChunk(self.readbuffer), "outbox")
                                self.readbuffer = ""
                                
                            while self.dataReady("control"):
                                #print "!"                            
                                temp = self.recv("control")
                                if isinstance(temp, producerFinished):
                                    connectionopen = False
                                    break
                                elif isinstance(temp, shutdown):
                                    return
                            
                            
                            if connectionopen:
                                self.pause()
                                yield 1
                    #else:
                    #    #no way of knowing how long the body is
                    #    requestobject["bad"] = 411 #length required
                    #    #print "HTTPParser::main - stage 3.bad"

                #state 4 - request complete, send it on
            self.debug("HTTPParser::main - request sent on")
            #print requestobject
            
                    
            self.send(ParsedHTTPEnd(), "outbox")
            if string.lower(requestobject["headers"].get("connection", "")) == "close":
                #print "HTTPParser connection close"
                self.send(producerFinished(), "signal") #this functionality is semi-complete
                return

__kamaelia_components__  = ( HTTPParser, )
