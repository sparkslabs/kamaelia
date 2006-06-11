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
from Axon.Ipc import producerFinished, shutdownMicroprocess
import string

def splitUri(requestobject):
    splituri = string.split(requestobject["raw-uri"], "://")
    if len(splituri) > 1:
        requestobject["uri-protocol"] = splituri[0]
        requestobject["raw-uri"] = requestobject["raw-uri"][len(splituri[0] + "://"):]
    
    splituri = string.split(requestobject["raw-uri"], "/")
    if splituri[0] != "":
        requestobject["uri-server"] = splituri[0]
        requestobject["raw-uri"] = requestobject["raw-uri"][len(splituri[0]):]
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
        
        self.requeststate = 1 # awaiting request line
        self.lines = []
        self.readbuffer = ""

    def dataFetch(self):
        if self.dataReady("inbox"):
            self.readbuffer += self.recv("inbox")
            return 1
        else:
            return 0
            
    def shouldShutdown(self):
        while self.dataReady("control"):
            temp = self.recv("control")
            if isinstance(temp, shutdownMicroprocess) or isinstance(temp, producerFinished):
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
            if self.mode == "request":
                requestobject = { "bad": False, "headers": {}, "raw-uri": "", "version": "0.9", "method": "", "protocol":"" }
            else:
                requestobject = { "bad": False, "headers": {}, "responsecode": "", "version": "0.9", "method": "", "protocol":"" }
            
            #state 1 - awaiting initial line
            currentline = None
            while currentline == None:
                if self.shouldShutdown(): return
                while self.dataFetch():
                    pass
                currentline = self.nextLine()
                if currentline == None:
                    self.pause()
                    yield 1
                
            #print "Initial line found"
            splitline = string.split(currentline, " ")
            
            if len(splitline) < 2:
                requestobject["bad"] = True
                # bad request
            else:
                if len(splitline) < 3:
                    # must be HTTP/0.9
                    requestobject["method"] = splitline[0]
                    requestobject["raw-uri"] = splitline[1]
                    requestobject["protocol"] = "HTTP"
                    requestobject["version"] = "0.9"
                else: #deal with normal HTTP including badly formed URIs
                    requestobject["method"] = splitline[0]

                    #next line supports all working clients but also 
                    #some broken clients that don't encode spaces properly!
                    requestobject["raw-uri"] = string.join(splitline[1:-1], "%20") 
                    protvers = string.split(splitline[-1], "/")
                    if len(protvers) != 2:
                        requestobject["bad"] = True
                        requestobject["version"] = "0.9"
                    else:
                        requestobject["protocol"] = protvers[0]
                        requestobject["version"] = protvers[1]
                    
                    splitUri(requestobject)
                    
                #foo://toor:letmein@server.bigcompany.com:80/bla?this&that=other could be handled better

                if requestobject["method"] == "PUT" or requestobject["method"] == "POST":
                    bodiedrequest = True
                else:
                    bodiedrequest = False

                if requestobject["version"] != "HTTP/0.9":
                    #state 2 - as this is a valid request, we now accept headers	
                    previousheader = ""
                    endofheaders = False
                    while not endofheaders:
                        if self.shouldShutdown(): return						
                        while self.dataFetch():
                            pass
                            
                        currentline = self.nextLine()
                        while currentline != None:
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
                if requestobject["headers"].has_key("host"):
                    requestobject["uri-server"] = requestobject["headers"]["host"]
                
                if bodiedrequest:
                    #state 3 - the headers are complete - awaiting the message
                    if not requestobject["headers"].has_key("content-length"):
                        #this is not strictly required - it breaks compatible with chunked encoding
                        #but will do for now
                        requestobject["bad"] = 411 #length required
                    else:
                        if string.lower(requestobject["headers"].get("expect", "")) == "100-continue":
                            #we're supposed to say continue, but this is a pain
                            #and everything still works if we don't
                            pass
                            
                        bodylength = int(requestobject["headers"]["content-length"])
                         
                        while len(self.readbuffer) < bodylength:
                            if self.shouldShutdown(): return						
                            while self.dataFetch():
                                pass
                            if len(self.readbuffer) < bodylength:
                                self.pause()
                                yield 1
                        requestobject["body"] = self.readbuffer[:bodylength]
                        self.readbuffer = self.readbuffer[bodylength:]

                #state 4 - request complete, send it on
            #print "Request sent on."
            #print requestobject
            
            if requestobject["version"] == "1.1":
                requestobject["headers"]["connection"] = requestobject["headers"].get("connection", "keep-alive")
            else:
                requestobject["headers"]["connection"] = requestobject["headers"].get("connection", "close")
                    
            self.send(requestobject, "outbox")
            if string.lower(requestobject["headers"].get("connection", "")) == "close":
                self.send(producerFinished(), "signal") #this functionality is semi-complete
                return
