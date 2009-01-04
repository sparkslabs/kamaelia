#!/usr/bin/python
"""
This example demonstrates using the Minimal file handler for
serving static web content.

System Requirements
-------------------
This example requires a UNIX operating system.
"""


# Import socket to get at constants for socketOptions
import socket

# Import the server framework, the HTTP protocol handling and the minimal request handler

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

# Our configuration

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

#Here we define our routing.  This tells us that the root of the server will run
#the minimal request handler, a static file server.
routing = [
    ['/', MinimalFactory(indexfilename, homedirectory)]
    ]

# Finally we create the actual server and run it.

ServerCore(protocol=HTTPProtocol(routing),
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()
