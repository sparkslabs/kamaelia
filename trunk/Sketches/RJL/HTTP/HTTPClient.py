#!/usr/bin/env python
#
# FIXME: Uses the selector service, but has no way of indicating to the
#        selector service that its services are no longer required.
#        This needs resolving.
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
"""\
=================
SingleShotHTTPClient
=================

This component is for downloading a file from an HTTP server.
Send to its "inbox"
inbox to send data to the server. Pick up data received from the server on its
"outbox" outbox.



Example Usage
-------------
TO DO


How does it work?
-----------------
Barely
"""


from Axon.Component import component
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Internet.TCPClient import TCPClient
import string, time

from HTTPParser import *

def intval(mystring):
    try:
        retval = int(mystring)
    except ValueError:
        retval = None
    return retval

def removeTrailingCr(line):
    if len(line) == 0:
        return ""
    elif line[-1] == "\r":
        return line[0:-1]
    else:
        return line

class HTTPRequest(object):
    def __init__(self, requestobject, redirectcount):
        super(HTTPRequest, self).__init__()
        self.requestobject = requestobject
        self.redirectcount = redirectcount

class SingleShotHTTPClient(component): 
    """\
    SingleShotHTTPClient() -> component that can download a file using HTTP by URL

    Arguments:
    - url     -- the URL of the file to download
    """
   
    Inboxes =  {             
        "inbox"          : "UNUSED",
        "control"        : "UNUSED",
                    
        "_parserinbox"   : "Data from HTTP parser",
        "_parsercontrol" : "Signals from HTTP parser",
        "_tcpcontrol"    : "Signals from TCP client",
    }
        

    Outboxes = {
        "outbox"         : "Requested file",
        "debug"          : "Output to aid debugging",
        
        "_parsersignal"  : "Signals for HTTP parser",
                
        "_tcpoutbox"     : "Send over TCP connection",
        "_tcpsignal"     : "Signals shutdown of TCP connection",
        
        "signal"         : "UNUSED"
    }
        
    def __init__(self, starturl):
        print "SingleShotHTTPClient.__init__()"
        super(SingleShotHTTPClient, self).__init__()
        self.tcpclient = None
        self.httpparser = None
        self.requestqueue = []
        self.starturl = starturl
        print "Start url: " + starturl
        
    def formRequest(self, url):
        """Craft a HTTP request string for the supplied url"""
        splituri = splitUri(url)
        
        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]
        
        splituri["request"] = "GET " + splituri["raw-uri"] + " HTTP/1.1\r\nHost: " + host + "\r\nUser-agent: Kamaelia HTTP Client 0.3 (RJL)\r\nConnection: Keep-Alive\r\n\r\n" #keep-alive is a work around for lack of shutdown notification in TCPClient
        return splituri

    def makeRequest(self, request):
        """Connect to the remote HTTP server and send request"""
        self.tcpclient = None
        self.httpparser = None
        port = intval(request.requestobject.get("uri-port", ""))
        if port == None:
            port = 80
        
        self.tcpclient = TCPClient(request.requestobject["uri-server"], port)
        self.httpparser = HTTPParser(mode="response")
                
        self.link( (self, "_tcpoutbox"),       (self.tcpclient, "inbox") )
        self.link( (self, "_tcpsignal"),       (self.tcpclient, "control") )
        self.link( (self.tcpclient, "signal"), (self, "_tcpcontrol") )

        self.link( (self.tcpclient, "outbox"), (self.httpparser, "inbox") ) #incoming TCP data -> HTTPParser directly
        
        self.link( (self, "_parsersignal"), (self.httpparser, "control") )
        self.link( (self.httpparser, "outbox"), (self, "_parserinbox") )
        self.link( (self.httpparser, "signal"), (self, "_parsercontrol") )

        self.addChildren( self.tcpclient, self.httpparser )
        self.tcpclient.activate()
        self.httpparser.activate()
        self.response = ""
        self.send(request.requestobject["request"], "_tcpoutbox")

    def shutdownKids(self):
        """Close TCP connection and HTTP parser"""    
        if self.tcpclient != None and self.httpparser != None:
            self.removeChild(self.tcpclient)
            self.removeChild(self.httpparser)    
            self.send(shutdown(), "_tcpsignal")
            self.send(shutdown(), "_parsersignal")
            self.tcpclient = None
            self.httpparser = None

    def handleRedirect(self, header):
        if header["responsecode"] == "302" or header["responsecode"] == "303" or header["responsecode"] == "307":
            # location header gives the redirect URL
            newurl = header["headers"].get("location", "")
            if newurl != "":
                redirectedrequest = HTTPRequest(self.formRequest(newurl), self.currentrequest.redirectcount + 1)
                self.requestqueue.append(redirectedrequest)
                return True
            else:
                return False
                # do something equivalent to what we'd do for 404
        else:
            return False
                            
    def main(self):
        self.requestqueue.append(HTTPRequest(self.formRequest(self.starturl), 0))
        while self.mainBody():
            yield 1
        self.send(producerFinished(), "signal")
        yield 1
        return
        
    def mainBody(self):
        self.send("SingleShotHTTPClient.mainBody()", "debug")
        while self.dataReady("_parserinbox"):
            msg = self.recv("_parserinbox")
            if isinstance(msg, ParsedHTTPHeader):
                self.send("SingleShotHTTPClient received a ParsedHTTPHeader on _parserinbox", "debug")                        
                # if the page is a redirect page
                if not self.handleRedirect(msg.header):
                    if msg.header["responsecode"] == "200":
                        self.send(msg, "outbox") # if not redirecting then send the response on
                    else:  #treat as not found
                        pass
                        
            elif isinstance(msg, ParsedHTTPBodyChunk):
                self.send("SingleShotHTTPClient received a ParsedHTTPBodyChunk on _parserinbox", "debug")
                if len(self.requestqueue) == 0: # if not redirecting then send the response on
                    self.send(msg, "outbox")
                
            elif isinstance(msg, ParsedHTTPEnd):
                self.send("SingleShotHTTPClient received a ParsedHTTPEnd on _parserinbox", "debug")
                if len(self.requestqueue) == 0: # if not redirecting then send the response on
                    self.send(msg, "outbox")
                self.shutdownKids()
            
        while self.dataReady("_parsercontrol"):
            temp = self.recv("_parsercontrol")
            self.send("SingleShotHTTPClient received something on _parsercontrol", "debug")
            
        while self.dataReady("_tcpcontrol"):
            msg = self.recv("_tcpcontrol")
            self.send(msg, "_parsersignal")

        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, shutdown):
                self.shutdownKids()
                return 0

        # if we're not currently downloading a page
        if self.tcpclient == None:
            # then either we've finished or we should download the next URL (if we've been redirected)
            if len(self.requestqueue) > 0:
                self.currentrequest = self.requestqueue.pop(0)
                if self.currentrequest.redirectcount == 3: # 3 redirects is excessive, give up, we're probably in a loop anyway
                    return 0
                else:
                    self.makeRequest(self.currentrequest)
            else:
                return 0
                    
        self.pause()
        return 1

def makeSSHTTPClient(url):
    return SingleShotHTTPClient(url)

class SimpleHTTPClient(component):
    Inboxes = {
        "inbox"           : "URLs to download",
        "control"         : "Shut me down",
        "_carouselready"  : "Receive NEXT when carousel has completed a request",
        "_carouselinbox"  : "Data from SingleShotHTTPClient via Carousel"
    }
    Outboxes = {
        "outbox"          : "Requested file's data string",
        "signal"          : "Signal I have shutdown",
        "_carouselnext"   : "Create a new SingleShotHTTPClient",
        "_carouselsignal" : "Shutdown the carousel",
        "debug"           : "Information to aid debugging"
    }

    def __init__(self):
        """Create and link to a carousel object"""

        self.send("SimpleHTTPClient.__init__()", "debug")    
        super(SimpleHTTPClient, self).__init__()

        self.carousel = Carousel(componentFactory=makeSSHTTPClient)
        self.addChildren(self.carousel)
        self.link((self, "_carouselnext"),        (self.carousel, "next"))
        self.link((self, "_carouselsignal"),      (self.carousel, "control"))
        self.link((self.carousel, "outbox"),      (self, "_carouselinbox"))
        self.link((self.carousel, "requestNext"), (self, "_carouselready"))        
        self.carousel.activate()
        
    def cleanup(self):
        self.send("SimpleHTTPClient.cleanup()", "debug")
        self.send(shutdown(), "_carouselsignal")
        self.removeChild(self.carousel)
        self.send(producerFinished(), "signal")
        
    def main(self):
        self.send("SimpleHTTPClient.main()", "debug")
        finished = False
        while not finished:
            yield 1
            while self.dataReady("inbox"):
                url = self.recv("inbox")
                self.send("SimpleHTTPClient received url " + url, "debug")
                self.send(url, "_carouselnext")
                
                filebody = ""
                carouselbusy = True
                
                while carouselbusy:
                    yield 1
                    while self.dataReady("_carouselinbox"):
                        msg = self.recv("_carouselinbox")
                        if isinstance(msg, ParsedHTTPBodyChunk):
                            filebody += msg.bodychunk
                            
                    while self.dataReady("control"):
                        msg = self.recv("control")
                        if isinstance(msg, producerFinished):
                            producerfinished = True
                        elif isinstance(msg, shutdown):
                            self.cleanup()
                            
                    while self.dataReady("_carouselready"):
                        msg = self.recv("_carouselready")
                        carouselbusy = False

                    self.pause()
                self.send(filebody, "outbox")
                filebody = ""
                        
            self.pause()
            
        self.cleanup()

if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter
    
    # type in a URL e.g. http://www.google.co.uk and have it saved to disk
    pipeline(
        ConsoleReader(">>> ", ""),
        SimpleHTTPClient(),
        SimpleFileWriter("downloadedfile.txt"),
    ).run()
