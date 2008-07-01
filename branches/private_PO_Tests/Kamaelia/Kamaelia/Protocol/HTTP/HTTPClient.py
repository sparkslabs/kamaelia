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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
=======================
Single-Shot HTTP Client
=======================

This component is for downloading a single file from an HTTP server.
Pick up data received from the server on its "outbox" outbox.

Generally you should use SimpleHTTPClient in preference to this.



Example Usage
-------------

How to use it::

    Pipeline(
        SingleShotHTTPClient("http://www.google.co.uk/"),
        SomeComponentThatUnderstandsThoseMessageTypes()
    ).run()

If you want to use it directly, note that it doesn't output strings
but ParsedHTTPHeader, ParsedHTTPBodyChunk and ParsedHTTPEnd like
HTTPParser. This makes has the advantage of not buffering huge
files in memory but outputting them as a stream of chunks.
(with plain strings you would not know the contents of the
headers or at what point that response had ended!)



How does it work?
-----------------

SingleShotHTTPClient accepts a URL parameter at its creation (to __init__).
When activated it creates an HTTPParser instance and then connects
to the webserver specified in the URL using a TCPClient component.
It sends an HTTP request and then any response from the server is received
by the HTTPParser.

HTTPParser processes the response and outputs it in parts as::

    ParsedHTTPHeader,
    ParsedHTTPBodyChunk,
    ParsedHTTPBodyChunk,
    ...
    ParsedHTTPBodyChunk,
    ParsedHTTPEnd

If SingleShotHTTPClient detects that the requested URL is a redirect page
(using the Location header) then it begins this cycle anew with the URL
of the new page, otherwise the parts of the page output by HTTPParser are
sent on to "outbox". 



==================
Simple HTTP Client
==================

This component downloads the pages corresponding to HTTP URLs received
on "inbox" and outputs their contents (file data) as a message, one per
URL, to "outbox" in the order they were received.

Example Usage
-------------

Type URLs, and they will be downloaded and placed, back to back in "downloadedfile.txt"::

    Pipeline(
        ConsoleReader(">>> ", ""),
        SimpleHTTPClient(),
        SimpleFileWriter("downloadedfile.txt"),
    ).run()



How does it work?
-----------------

SimpleHTTPClient uses the Carousel component to create a new
SingleShotHTTPClient component for every URL requested. As URLs are
handled sequentially, it has only one SSHC child at anyone time.
"""

import string, time

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Internet.TCPClient import TCPClient

from Kamaelia.Protocol.HTTP.HTTPParser import *

class ParsedHTTPRedirect(object):
    def __init__(self, redirectto):
        self.redirectto = redirectto

def intval(mystring):
    """Convert a string to an integer, representing errors by None"""
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
    - [postbody]   -- data to POST to that URL - if set to None becomes an empty body in to a POST (of PUT) request
    - [connectionclass] -- specify a class other than TCPClient to connect with
    - [method]     -- the HTTP method for the request (default to GET normally or POST if postbody != ""
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

    def __init__(self, starturl, postbody = "", connectionclass = TCPClient, extraheaders = None, method = None):
#        print "SingleShotHTTPClient.__init__()"
        super(SingleShotHTTPClient, self).__init__()
        self.tcpclient = None
        self.httpparser = None
        self.requestqueue = []
        self.starturl = starturl
        self.connectionclass = connectionclass
        self.method = method

        self.postbody = postbody
        if extraheaders is not None:
            self.extraheaders = extraheaders
        else:
            self.extraheaders = {}

    def formRequest(self, url):
        """Craft a HTTP request string for the supplied url"""
        splituri = splitUri(url)

        host = splituri["uri-server"]
        if splituri.has_key("uri-port"):
            host += ":" + splituri["uri-port"]

        splituri["request"] = []
        method = self.method
        if self.postbody == "":
            if not method:
                method = 'GET'
            splituri["request"].append(method + " " + splituri["raw-uri"] + " HTTP/1.1\r\n")
        else:
            if not method:
                method = 'POST'
            splituri["request"].append(method + " " + splituri["raw-uri"] + " HTTP/1.1\r\n")
            if self.postbody != None:
                splituri["request"].append("Content-Length: " + str(len(self.postbody)) + "\r\n")
            else:
                splituri["request"].append("Content-Length: 0\r\n")

        splituri["request"].append("Host: " + host + "\r\n")
        splituri["request"].append("User-agent: Kamaelia HTTP Client 0.3 (RJL)\r\n")
        splituri["request"].append("Connection: Keep-Alive\r\n") # keep-alive is a work around for lack of shutdown notification in TCPClient
        for header in self.extraheaders:
            splituri["request"].append("%s: %s\r\n" % (header, self.extraheaders[header]))

        splituri["request"].append("\r\n") 

        splituri["request"] = [string.join(splituri["request"], "")] # might improve performance by sending more together

#        print splituri["request"]

        if self.postbody not in [None, ""]:
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

        if header["responsecode"] in ["301", "302", "303", "307"]:
            # location header gives the redirect URL
            newurl = header["headers"].get("location", "")
            if newurl != "":
                self.send(ParsedHTTPRedirect(redirectto=newurl), "outbox")
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
#            print "SingleShotHTTPClient.main"
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
            if isinstance(msg, shutdown):
                self.shutdownKids()
                return 0
            else:
                for i in range(100):
                   print "control message in HTTPClient!!",i,msg

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
    # get the "url" and "postbody" keys from paramdict to use as the arguments of SingleShotHTTPClient
    return SingleShotHTTPClient(paramdict.get("url", ""), 
                                paramdict.get("postbody", ""),
                                extraheaders = paramdict.get("extraheaders", None),
                                method = paramdict.get('method', None)
                               )

class SimpleHTTPClient(component):
    Inboxes = {
        "inbox"           : "URLs to download - a dict {'url':'x', 'postbody':'y'} or a just the URL as a string ",
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

        # now create our Carousel subcomponent
        self.carousel = Carousel(componentFactory=makeSSHTTPClient)
        self.addChildren(self.carousel)
        self.link((self, "_carouselnext"),        (self.carousel, "next"))
        self.link((self, "_carouselsignal"),      (self.carousel, "control"))
        self.link((self.carousel, "outbox"),      (self, "_carouselinbox"))
        self.link((self.carousel, "requestNext"), (self, "_carouselready"))

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
        self.carousel.activate()
        finished = False

        while not finished:
            yield 1
            self.debug("SimpleHTTPClient.main1\n")

            while self.dataReady("inbox"):
                paramdict = self.recv("inbox")

                # we accept either string or dict messages - if it's a string then
                # we assume you mean that's the URL you want fecthed

                if isinstance(paramdict, str):
                    paramdict = { "url": paramdict }

                self.debug("SimpleHTTPClient received url " + paramdict.get("url","") + "\n")

                # request creation of a new SingleShotHTTPClient by Carousel
                self.send(paramdict, "_carouselnext")

                # store as a list of strnigs then join at the 
                # end to avoid O(n^2) time string cat'ing behaviour
                filebody = []

                carouselbusy = True

                while carouselbusy:
                    yield 1

                    while self.dataReady("_carouselinbox"):
                        msg = self.recv("_carouselinbox")
                        if isinstance(msg, ParsedHTTPBodyChunk):
                            filebody.append(msg.bodychunk)

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
                self.send(string.join(filebody, ""), "outbox")

                filebody = [] # free up some memory used by the now unneeded list

            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    finished = True
                elif isinstance(msg, shutdown):
                    self.cleanup()
                    return

            self.pause()

        self.debug("eoml in SimpleHTTPClient\n")
        self.cleanup()
        yield 1
        return

__kamaelia_components__  = ( SimpleHTTPClient, SingleShotHTTPClient, )

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.File.Writing import SimpleFileWriter

    # Example - type in a URL e.g. http://www.google.co.uk and have that page saved to disk
    Pipeline(
        ConsoleReader(">>> ", ""),
        SimpleHTTPClient(),
        SimpleFileWriter("downloadedfile.txt"),
    ).run()
