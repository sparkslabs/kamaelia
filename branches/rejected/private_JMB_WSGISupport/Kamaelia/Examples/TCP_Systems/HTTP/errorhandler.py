#! /usr/bin/env python
"""
This module demonstrates the use of the error handler
HTTP component.  When run, it will pull up nothing
but 404s.
"""
#We need this for the socket options.
import socket

#The main server chassis
from Kamaelia.Chassis.ConnectedServer import ServerCore

#This imports a convenience function that runs the HTTP
#protocol.
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

#The error page handler.  I'll assume you know why we're
#including this.  :-)
from Kamaelia.Protocol.HTTP.ErrorPages import ErrorPageHandler

routing = []

#Create the server and run it.
ServerCore(
    #Note that we really don't have to pass ErrorPageHandler
    #to HTTPProtocol.  We're just doing it to show you where
    #it comes into play.
    protocol=HTTPProtocol(routing, ErrorPageHandler),
    port = 8082,
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ).run()
