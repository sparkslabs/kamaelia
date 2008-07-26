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

from Kamaelia.Chassis.Graphline import Graphline
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

class HTTPShutdownLogicHandling(component):
    Inboxes = {
        "inbox": "unused - this is a pure signalling component",
        "Pcontrol": "To signal to the http parser",
        "Hcontrol": "To signal to the http connection handler",
        "control": "Standard inbox where we get shutdown messages from the socket",
    }
    Outboxes = {
        "outbox": "unused - this is a pure signalling component",
        "Psignal": "To signal to the http parser",
        "Hsignal": "To signal to the http connection handler",
        "signal": "Standard outbox - re-shutdown",
    }
    def main(self):
        keepconnectionopen= True
        while keepconnectionopen:
            yield 1
            while not self.anyReady():
                self.pause()
                yield 1
            while self.dataReady("control"):           # Control messages from the socket
                temp = self.recv("control")
                if isinstance(temp, producerFinished): # Socket has stopped sending us data (can still send data to it)
                    self.send(temp, "Psignal")         # pass on to the HTTP Parser. (eg could be a POST request)
#                    print "PRODUCER SHUTDOWN"

                elif isinstance(temp, shutdown):       # Socket is telling us connection is dead
                    self.send(shutdown(), "Psignal")
                    self.send(shutdown(), "Hsignal")
                    keepconnectionopen = False
#                    print "SOCKET DEAD"

            while self.dataReady("Pcontrol"):          # Control messages from the HTTP Parser
                temp = self.recv("Pcontrol")
                if isinstance(temp, producerFinished): # HTTP Parser is telling us they're done parsing
                    pass                               # XXXX Handling of shutdown messages from parser ???
#                    print "PARSER FINISHED"
                    self.send(temp, "Hsignal") # Pass on to the HTTP Handler

            while self.dataReady("Hcontrol"):          # Control messages from the HTTP Handler
                temp = self.recv("Hcontrol")
                if isinstance(temp, producerFinished): # Have finished sending data to the client
                    sig = producerFinished(self)       #
                    self.send(sig, "Psignal")          # Make sure HTTP Parser is shutting down - (should send a "shutdown" message)
                    self.send(sig, "signal")
                    keepconnectionopen = False
#                    print "HTTP HANDLER DEAD"

        self.send(producerFinished(), "signal")        # We're done, close the connection.
        yield 1                                        # And quit

def HTTPServer(createRequestHandler, requestTranslator=None, **argd):
    """\
    HTTPServer() -> new HTTPServer component capable of handling a single connection

    Arguments:
       -- createRequestHandler - a function required by HTTPRequestHandler that
                                 creates the appropriate request-handler component
                                 for each request, see HTTPResourceGlue
    """
    return Graphline(
        PARSER = HTTPParser(**argd), # Since this is where the data goes first!
        HANDLER = HTTPRequestHandler(createRequestHandler),
        CORELOGIC = HTTPShutdownLogicHandling(),
        linkages = {
            # Data Handling
            ("self",   "inbox"):  ("PARSER","inbox"),
            ("PARSER", "outbox"): ("HANDLER","inbox"),
            ("HANDLER","outbox"): ("self","outbox"),

            # Signalling Handling
            ("self","control"):      ("CORELOGIC","control"),
            ("CORELOGIC","Psignal"): ("PARSER","control"),
            ("CORELOGIC","Hsignal"): ("HANDLER","control"),
            ("CORELOGIC","signal"):  ("self","signal"),

            ("PARSER","signal"):     ("CORELOGIC","Pcontrol"),
            ("HANDLER","signal"):    ("CORELOGIC","Hcontrol"),
        }
    )

__kamaelia_components__  = ( HTTPShutdownLogicHandling )
__kamaelia_prefabs__  = ( HTTPServer, )

if __name__ == '__main__':
    import socket
    from Kamaelia.Chassis.ConnectedServer import ServerCore
    from Kamaelia.Protocol.HTTP import HTTPProtocol
    from Kamaelia.Protocol.HTTP.Translators.WSGILike import WSGILikeTranslator
    
    class handler(component):
        def __init__(self, request):
            self.request = request
            super(handler, self).__init__()
        def main(self):
            from pprint import pformat
            resource = {
                'statuscode' : 200,
                'headers' : [('content-type', 'text/plain')],
                'data' : pformat(self.request),
            }
            self.send(resource, 'outbox')
            self.send(producerFinished(self), 'signal')
            yield 1

    routing = [['/', handler]]

    ServerCore(
        protocol=HTTPProtocol(routing, WSGILikeTranslator),
        port=8082,
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ).run()
