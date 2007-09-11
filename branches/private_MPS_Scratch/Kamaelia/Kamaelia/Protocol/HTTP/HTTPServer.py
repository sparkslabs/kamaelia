#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
========================
HTTP Server
========================
The fundamental parts of a webserver - an HTTP request parser and a request
handler/response generator. One instance of this component can handle one
TCP connection. Use a SimpleServer or similar component to allow several
concurrent HTTP connections to the server.

Example Usage
-------------

    def createhttpserver():
        return HTTPServer(HTTPResourceGlue.createRequestHandler)

    SimpleServer(protocol=createhttpserver, port=80).run()

This defines a function which creates a HTTPServer instance with 
HTTPResourceGlue.createRequestHandler as the request handler component
creator function. This function is then called by SimpleServer for every
new TCP connection.

How does it work?
-----------------
HTTPServer creates and links to a HTTPParser and HTTPRequestHandler component.
Data received over TCP is forwarded to the HTTPParser and the output of 
HTTPRequestHandler forwarded to the TCP component's inbox for sending.

See HTTPParser (in HTTPParser.py) and HTTPRequestHandler (below) for details
of how these components work.

HTTPServer accepts a single parameter - a request handler function which is
passed onto and used by HTTPRequestHandler to generate request handler 
components. This allows different HTTP server setups to run on different
ports serving completely different content.

========================
HTTP Request Handler
========================
HTTPRequestHandler accepts parsed HTTP requests (from HTTPParser) and outputs
appropriate responses to those requests.

How does it work?
-----------------
HTTPServer creates 2 subcomponents - HTTPParser and HTTPRequestHandler which
handle the processing of requests and the creation of responses respectively.

Both requests and responses are handled in a stepwise manner (as opposed to processing a
whole request or response in one go) to reduce latency and cope well with bottlenecks.

One request handler (self.handler) component is used per request - the particular 
component instance (including parameters, component state) is picked by a function
called createRequestHandler - a function specified by the user. A suitable definition
of this function is available in HTTPResourceGlue.py.

Generally you will have a handler spawned for each new request, terminating after completing
the sending of the response. However, it is also possible to use a 'persistent' component
if you do the required jiggery-pokery to make sure that at any one time this component is
not servicing more than one request simultaenously ('cause it wouldn't work).

What does it support?
---------------------
Components as request handlers (hurrah!).

3 different ways in which the response data (body) can be terminated:

Chunked transfer encoding
*************************
This is the most complex of the 3 ways and was introduced in HTTP/1.1. Its performance is
slightly worse that the other 2 as multiple length-lines have to be added to the data stream.
It is recommended for responses whose size is not known in advance as it allows keep-alive
connections (more than one HTTP request per TCP connection).

Explicit length
*************************
This is the easiest of the 3 ways but requires the length of the response to be known before
it is sent. It uses a header 'Content-Length' to indicate this value.
This method is prefered for any response whose length is known in advance.

Connection: close
*************************
This method closes (or half-closes) the TCP connection when the response is
complete. This is highly inefficient when the client wishes to download several
resources as a new TCP connection must be created and destroyed for each
resource. This method is retained for HTTP/1.0 compatibility.
It is however preferred for responses that do not have a true end,
e.g. a continuous stream over HTTP as the alternative, chunked transfer
encoding, has poorer performance.

The choice of these three methods is determined at runtime by the
characteristics of the first response part produced by the request handler
and the version of HTTP that the client supports
(chunked requires 1.1 or higher).

What may need work?
========================
- HTTP standards-compliance (e.g. handling of version numbers for a start)
- Requests for byte ranges, cache control (though these may be better implemented
    in each request handler)
- Performance tuning (also in HTTPParser)
- Prevent many MBs of data being queued up because TCPClient finds it has a slow
    upload to the remote host
"""

import string, time, array

from Axon.Ipc import producerFinished, shutdown
from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent

from Kamaelia.Protocol.HTTP.HTTPParser import *
from Kamaelia.Protocol.HTTP.HTTPRequestHandler import HTTPRequestHandler

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

class HTTPServer(component):
    """\
    HTTPServer() -> new HTTPServer component capable of handling a single connection

    Arguments:
       -- createRequestHandler - a function required by HTTPRequestHandler that
                                 creates the appropriate request-handler component
                                 for each request, see HTTPResourceGlue
    """

    Inboxes =  { "inbox"         : "TCP data stream - receive",
                 "mime-signal"   : "Error signals from MIME handler",
                 "http-signal"   : "Error signals from the HTTP resource retriever",
                 "control"       : "Receive shutdown etc. signals" }


    Outboxes = { "outbox"        : "TCP data stream - send",
                 "mime-control"  : "To MIME handler",
                 "http-control"  : "To HTTP resource retriever's signalling inbox",
                 "signal"        : "UNUSED" }

    def __init__(self, createRequestHandler):
        super(HTTPServer, self).__init__()
        self.createRequestHandler = createRequestHandler

    def initialiseComponent(self):
        """Create an HTTPParser component to convert the requests we receive
        into a more convenient form and a HTTPRequestHandler component to
        sort out the correct response to requests received. Then link them
        together and to the TCP component"""
        #
        # XXXX - This code structure implies it should be using a Graphline
        #        structure with a central control component
        #

        self.mimehandler = HTTPParser()
        self.httphandler = HTTPRequestHandler(self.createRequestHandler)

        self.link( (self,"mime-control"), (self.mimehandler,"control") )
        self.link( (self.mimehandler, "signal"), (self, "mime-signal") )

        self.link( (self.mimehandler, "outbox"), (self.httphandler, "inbox") )

        self.link( (self, "http-control"), (self.httphandler, "control") )
        self.link( (self.httphandler, "signal"), (self, "http-signal") )

        self.addChildren(self.mimehandler, self.httphandler)
        self.httphandler.activate()
        self.mimehandler.activate()

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
                elif isinstance(temp, shutdown):
                    self.send(shutdown(), "mime-control")
                    self.send(shutdown(), "http-control")
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
        "Remove my subcomponents (HTTPParser, HTTPRequestHandler)"
        for child in self.childComponents():
            self.removeChild(child)
        self.mimehandler = None
        self.httphandler = None

__kamaelia_components__  = ( HTTPServer,)

if __name__ == '__main__':
    import socket

    from Kamaelia.Chassis.ConnectedServer import SimpleServer

    # this works out what the correct response to a request is
    from Kamaelia.Protocol.HTTP.HTTPResourceGlue import createRequestHandler 

    def createhttpserver():
        return HTTPServer(createRequestHandler)

    SimpleServer(
        protocol=createhttpserver,
        port=8082,
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ).run()
