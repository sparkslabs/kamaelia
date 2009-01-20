#!/usr/bin/python

# Import socket to get at constants for socketOptions
import socket

# Import the server framework, the HTTP protocol handling and the minimal request handler

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

# Our configuration

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

print \
"""
About
-----
This example demonstrates using the Minimal file handler for
serving static web content.

System Requirements
-------------------
This example requires a UNIX operating system.

What it does
------------
It runs a basic webserver on http://127.0.0.1:8082/ which looks for any files to
serve from the docroot. This is hardcoded in this file as being %s . The correct
mimetype is also served.

Specifically, it starts up a ServerCore instance which starts an HTTPProtocol handler
when a client connects on port 8082. The HTTPProtocol handler is configured using
a simplistic request routing table that matches "/" against the Minimal handler -
which just reads an appropriate file from a preconfigured location and serves that
back to the user.

""" % (homedirectory, )


#Here we define our routing.  This tells us that the root of the server will run
#the minimal request handler, a static file server.
routing = [
    ['/', MinimalFactory(indexfilename, homedirectory)]
    ]

# Finally we create the actual server and run it.

ServerCore(protocol=HTTPProtocol(routing),
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()
