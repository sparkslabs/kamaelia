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

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
import string

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
        
class HTTPParser(component):
    Inboxes =  { "inbox"         : "Raw HTTP requests/responses",
                 "control"       : "UNUSED" }
    Outboxes = { "outbox"        : "HTTP request object",
                 "signal"        : "UNUSED" }
    
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
            requestobject["bad"] = True
            requestobject["version"] = "0.9"
        else:
            requestobject["protocol"] = protvers[0]
            requestobject["version"]  = protvers[1]
    
    def dataFetch(self):
        if self.dataReady("inbox"):
            self.readbuffer += self.recv("inbox")
            return 1
        else:
            return 0
    
    def shouldShutdown(self):
        while self.dataReady("control"):
            temp = self.recv("control")
            if isinstance(temp, shutdownMicroprocess) or isinstance(temp, producerFinished) or isinstance(temp, shutdown):
                #print "HTTPParser should shutdown"
                return True
        
        return False
        
    def nextLine(self):
        lineendpos = string.find(self.readbuffer, "\n")
        if lineendpos == -1:
            return None
        else:
            line = removeTrailingCr(self.readbuffer[:lineendpos])
            self.readbuffer = self.readbuffer[lineendpos + 1:] #the remainder after the \n
            #print "Received line: " + line
            return line
    
    def main(self):

        while 1:
            #print "HTTPParser::main - stage 0"
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
           
            #print "Awaiting initial line"
            #state 1 - awaiting initial line
            currentline = None
            while currentline == None:
                #print "HTTPParser::main - stage 1"
                if self.shouldShutdown(): return
                while self.dataFetch():
                    pass
                currentline = self.nextLine()
                if currentline == None:
                    self.pause()
                    yield 1
                
            #print "Initial line found"
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
                    requestobject = splitUri(string.join(splitline[1:-1], "%20") )
                    self.splitProtocolVersion(splitline[-1], requestobject)
                    
                    if requestobject["protocol"] != "HTTP":
                        requestobject["bad"] = True
            else:
                #e.g. HTTP/1.1 200 OK that's fine
                if len(splitline) < 2:
                    requestobject["version"] = "0.9"
                else:
                    requestobject["responsecode"] = splitline[1]
                    self.splitProtocolVersion(splitline[0], requestobject)
            
            if not requestobject["bad"]:
                if self.mode == "response" or requestobject["method"] == "PUT" or requestobject["method"] == "POST":
                    bodiedrequest = True
                else:
                    bodiedrequest = False

                if requestobject["version"] != "0.9":
                    #state 2 - as this is a valid request, we now accept headers	
                    previousheader = ""
                    endofheaders = False
                    while not endofheaders:
                        #print "HTTPParser::main - stage 2"
                        if self.shouldShutdown(): return						
                        while self.dataFetch():
                            pass
                            
                        currentline = self.nextLine()
                        while currentline != None:
                            #print "HTTPParser::main - stage 2.1"
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

                #print "HTTPParser::main - stage 2 complete"
                if requestobject["headers"].has_key("host"):
                    requestobject["uri-server"] = requestobject["headers"]["host"]
                
            if requestobject["version"] == "1.1":
                requestobject["headers"]["connection"] = requestobject["headers"].get("connection", "keep-alive")
            else:
                requestobject["headers"]["connection"] = requestobject["headers"].get("connection", "close")

                if bodiedrequest:
                    #print "HTTPParser::main - stage 3 start"
                    #state 3 - the headers are complete - awaiting the message
                    if requestobject["headers"].get("transfer-encoding","").lower() == "chunked":
                        while 1:
                            #print "HTTPParser::main - stage 3"
                            while currentline == None:
                                #print "HTTPParser::main - stage 3.chunked.1"
                                if self.shouldShutdown(): return
                                while self.dataFetch():
                                    pass
                                currentline = self.nextLine()
                                if currentline == None:
                                    self.pause()
                                    yield 1
                            splitline = currentline.split(";")
                            bodylength = splitline[0].atoi(16)
                            if bodylength == 0:
                                break
                            
                            while len(self.readbuffer) < bodylength:
                                #print "HTTPParser::main - stage 3.chunked.2"
                                if self.shouldShutdown(): return						
                                while self.dataFetch():
                                    pass
                                if len(self.readbuffer) < bodylength:
                                    self.pause()
                                    yield 1
                            requestobject["body"] += self.readbuffer[:bodylength]
                    elif requestobject["headers"].has_key("content-length"):
                        if string.lower(requestobject["headers"].get("expect", "")) == "100-continue":
                            #we're supposed to say continue, but this is a pain
                            #and everything still works if we don't just with a few secs delay
                            pass
                        
                        
                        bodylength = int(requestobject["headers"]["content-length"])
                         
                        while len(self.readbuffer) < bodylength:
                            #print "HTTPParser::main - stage 3.length known.1"
                            if self.shouldShutdown(): return						
                            while self.dataFetch():
                                pass
                            if len(self.readbuffer) < bodylength:
                                self.pause()
                                yield 1
                        requestobject["body"] = self.readbuffer[:bodylength]
                        self.readbuffer = self.readbuffer[bodylength:]
                    elif requestobject["headers"]["connection"] == "close":
                        connectionopen = True
                        while connectionopen:
                            #print "HTTPParser::main - stage 3.connection close.1"
                            if self.shouldShutdown(): return						
                            while self.dataFetch():
                                pass
                            while self.dataReady("control"):
                                temp = self.recv("control")
                                if isinstance(temp, producerFinished):
                                    connectionopen = False
                                    break
                                elif isinstance(temp, shutdownMicroprocess) or isinstance(temp, shutdown):
                                    return
                                    
                            if connectionopen:
                                self.pause()
                                yield 1
                        requestobject["body"] = self.readbuffer
                        self.readbuffer = ""
                    else:
                        #no way of knowing how long the body is
                        requestobject["bad"] = 411 #length required
                       

                #state 4 - request complete, send it on
            #print "Request sent on."
            #print requestobject
            
                    
            self.send(requestobject, "outbox")
            if string.lower(requestobject["headers"].get("connection", "")) == "close":
                #print "HTTPParser connection close"
                self.send(producerFinished(), "signal") #this functionality is semi-complete
                return
