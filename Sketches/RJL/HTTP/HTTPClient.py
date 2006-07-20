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
"""\
=================
Single-Shot HTTP Client
=================

This component is for downloading a single file from an HTTP server.
Pick up data received from the server on its "outbox" outbox.

Example Usage
-------------
Generally you should use SimpleHTTPClient in preference to this.
If you want to use it directly, note that it doesn't output strings
but ParsedHTTPHeader, ParsedHTTPBodyChunk and ParsedHTTPEnd like
HTTPParser.

pipeline(
    SingleShotHTTPClient("http://www.google.co.uk/"),
    SomeComponentThatUnderstandsThoseMessageTypes()
).run()
    

How does it work?
-----------------
SingleShotHTTPClient creates an HTTPParser instance and then connects
to the HTTP server using a TCPClient component. It sends an HTTP request
and then any response from the server is received by the HTTPParser.
HTTPParser processes the response and outputs it in parts as:

ParsedHTTPHeader,
ParsedHTTPBodyChunk,
ParsedHTTPBodyChunk,
       ...
ParsedHTTPBodyChunk,
ParsedHTTPEnd

If SingleShotHTTPClient detects that the requested URL is a redirect page
(using the Location header) then it begins this cycle anew with the URL
of the new page, otherwise the parts of the page output by HTTPParser are
sent on through "outbox". 

=================
Simple HTTP Client
=================

This component downloads the pages corresponding to HTTP URLs received
on "inbox" and outputs their contents (file data) as a message, one per
URL, in the order they were received.

Example Usage
-------------

pipeline(
    ConsoleReader(">>> ", ""),
    SimpleHTTPClient(),
    SimpleFileWriter("downloadedfile.txt"),
).run()

How does it work?
-----------------
SimpleHTTPClient uses the Carousel component to create a new
SingleShotHTTPClient component for every URL requested. As URLs are
handled sequentially, there is only one SSHC at anyone time.

"""

from Axon.Component import component
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Carousel import Carousel
from Axon.Ipc import producerFinished, shutdownMicroprocess, shutdown
from Kamaelia.Internet.TCPClient import TCPClient as TCPClient
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

def AttachConsoleToDebug(comp):
    comp.debuggingconsole = ConsoleEchoer()
    comp.link((comp, "debug"), (comp.debuggingconsole, "inbox"))
    comp.debuggingconsole.activate()
    
class SingleShotHTTPClient(component): 
    """\
    SingleShotHTTPClient() -> component that can download a file using HTTP by URL

    Arguments:
    - starturl     -- the URL of the file to download
    - [postbody]   -- data to POST to that URL
    - [connectionclass] -- specify a class other than TCPClient to connect with
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
        
    def __init__(self, starturl, postbody = "", connectionclass = TCPClient):
        #print "SingleShotHTTPClient.__init__()"
        super(SingleShotHTTPClient, self).__init__()
        self.tcpclient = None
        self.httpparser = None
        self.requestqueue = []
        self.starturl = starturl
        self.connectionclass = connectionclass
        
        self.postbody = postbody
        #print "Start url: " + starturl
        
    def formRequest(self, url):
        """Craft a HTTP request string for the supplied url"""
        splituri = splitUri(url)
        
        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]

        splituri["request"] = []        
        if self.postbody == "":    
            splituri["request"].append("GET " + splituri["raw-uri"] + " HTTP/1.1\r\n")
        else:
            splituri["request"].append("POST " + splituri["raw-uri"] + " HTTP/1.1\r\n")
            splituri["request"].append("Content-Length: " + str(len(self.postbody)) + "\r\n")

        splituri["request"].append("Host: " + host + "\r\n")
        splituri["request"].append("User-agent: Kamaelia HTTP Client 0.3 (RJL)\r\n")
        splituri["request"].append("Connection: Keep-Alive\r\n") # keep-alive is a work around for lack of shutdown notification in TCPClient
        splituri["request"].append("\r\n") 

        splituri["request"] = [string.join(splituri["request"], "")] # might improve performance by sending more together
        
        if self.postbody != "":
            splituri["request"].append(self.postbody)
        
        return splituri

    def makeRequest(self, request):
        """Connect to the remote HTTP server and send request"""
        self.tcpclient = None
        self.httpparser = None
        port = intval(request.requestobject.get("uri-port", ""))
        if port == None:
            port = 80
        
        self.tcpclient = self.connectionclass(request.requestobject["uri-server"], port)
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
        if isinstance(request.requestobject["request"], str):
            self.send(request.requestobject["request"], "_tcpoutbox")
        else:
            for part in request.requestobject["request"]:
                self.send(part, "_tcpoutbox")

    def shutdownKids(self):
        """Close TCP connection and HTTP parser"""
        if self.tcpclient != None and self.httpparser != None:
            self.send(producerFinished(), "_tcpsignal")
            self.send(shutdown(), "_parsersignal")
            self.removeChild(self.tcpclient)
            self.removeChild(self.httpparser)            
            self.tcpclient = None
            self.httpparser = None

    def handleRedirect(self, header):
        """Check for a redirect response and queue the fetching the page it points to if it is such a response.
        Returns true if it was a redirect page and false otherwise."""
        
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
        """Main loop."""
        self.requestqueue.append(HTTPRequest(self.formRequest(self.starturl), 0))
        while self.mainBody():
            #print "SingleShotHTTPClient.main"
            yield 1
        self.send(producerFinished(self), "signal")
        yield 1
        return
        
    def mainBody(self):
        """Called repeatedly by main loop. Checks inboxes and processes messages received.
        Start the fetching of the new page if the current one is a redirect and has been
        completely fetched."""
        
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
                return 1
            
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

def makeSSHTTPClient(paramdict):
    """Creates a SingleShotHTTPClient for the given URL. Needed for Carousel."""
    
    return SingleShotHTTPClient(paramdict.get("url",""), paramdict.get("postbody",""))

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
        super(SimpleHTTPClient, self).__init__()
        #AttachConsoleToDebug(self)
        self.debug("SimpleHTTPClient.__init__()")    
        
        self.carousel = Carousel(componentFactory=makeSSHTTPClient)
        self.addChildren(self.carousel)
        self.link((self, "_carouselnext"),        (self.carousel, "next"))
        self.link((self, "_carouselsignal"),      (self.carousel, "control"))
        self.link((self.carousel, "outbox"),      (self, "_carouselinbox"))
        self.link((self.carousel, "requestNext"), (self, "_carouselready"))        
        self.carousel.activate()
        
    def cleanup(self):
        """Destroy child components and send producerFinished when we quit."""    
        self.debug("SimpleHTTPClient.cleanup()")
        self.send(producerFinished(self), "_carouselsignal") #shutdown() not currently supported by Carousel
        self.send(producerFinished(self), "signal")
        self.removeChild(self.carousel)        
        self.unpause()
        
    def debug(self, msg):
        self.send(msg, "debug")
        
    def main(self):
        """Main loop."""
        self.debug("SimpleHTTPClient.main()\n")
        finished = False
        while not finished:
            yield 1
            self.debug("SimpleHTTPClient.main1")
            while self.dataReady("inbox"):
                paramdict = self.recv("inbox")
                if isinstance(paramdict, str):
                    paramdict = { "url": paramdict }
                    
                self.debug("SimpleHTTPClient received url " + paramdict.get("url","") + "\n")
                self.send(paramdict, "_carouselnext")
                
                filebody = ""
                carouselbusy = True
                
                while carouselbusy:
                    yield 1
                    #print "SimpleHTTPClient.main2"
                    while self.dataReady("_carouselinbox"):
                        msg = self.recv("_carouselinbox")
                        if isinstance(msg, ParsedHTTPBodyChunk):
                            filebody += msg.bodychunk
                            
                    while self.dataReady("control"):
                        msg = self.recv("control")
                        if isinstance(msg, producerFinished):
                            finished = True
                        elif isinstance(msg, shutdown):
                            self.cleanup()
                            return
                            
                    while self.dataReady("_carouselready"):
                        msg = self.recv("_carouselready")
                        carouselbusy = False

                    self.pause()
                self.send(filebody, "outbox")
                filebody = ""
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    finished = True
                elif isinstance(msg, shutdown):
                    self.cleanup()
                    return
                    
            self.pause()
        
        self.debug("eoml in SimpleHTTPClient")
        self.cleanup()
        yield 1
        return
        
if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter
    
    # type in a URL e.g. http://www.google.co.uk and have that page saved to disk
    pipeline(
        ConsoleReader(">>> ", ""),
        SimpleHTTPClient(),
        SimpleFileWriter("downloadedfile.txt"),
    ).run()
