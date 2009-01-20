#!/usr/bin/python
__doc__ = \
"""
Synopsis
--------
This module demonstrates the Minimal HTTP Handler along
with some custom-written components.

System Requirements
-------------------
This example requires a UNIX operating system to run.

What it does
------------

It runs a basic webserver on http://127.0.0.1:8082/ . It dispatches HTTP
requests to different handlers based on the request path. There are 3
different handlers in this example:

Requests prefixed
    * /echo are handled by the EchoHandler
    * /hello are handled by the HelloHandler

All other requests prefixed by / are handled by a default "Minimal" handler.

The two custom handlers ...
    * EchoHandler returns a dictionary to the user with the details of the
      request.
    * HelloHandler simply responds with Hello World.

... are provided as simple example custom handlers.

Example URLs:
    http://127.0.0.1:8082/echo
    http://127.0.0.1:8082/hello
    http://127.0.0.1/
"""

import socket
import Axon

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

from Kamaelia.Chassis.Pipeline import Pipeline

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

#This is the hello handler.  It will respond to every request with a Hello world
#message (with some HTML formatting)
class HelloHandler(Axon.Component.component):
    def __init__(self, request):
        super(HelloHandler, self).__init__()
        self.request = request

    def main(self):
        resource = {
           "type"           : "text/html",
           "statuscode"     : "200",
           "length": len("<html><body><h1>Hello World</h1><P> Game Over!! </body></html>"),
        }
        self.send(resource, "outbox"); yield 1
        page = {
          "data" : "<html><body><h1>Hello World</h1><P> Game Over!! </body></html>"
        }
        self.send(page, "outbox"); yield 1
        self.send(Axon.Ipc.producerFinished(self), "signal")        
        yield 1

#This is the request echoer.  It will simply forward a request on to the next component.
class RequestEchoer(Axon.Component.component):
    def __init__(self, *args):
        super(RequestEchoer, self).__init__()
        self.args = args
    def main(self):
        self.send(self.args, "outbox")
        self.send(Axon.Ipc.producerFinished(self), "signal")        
        yield 1

#This component will simply wrap any input it receives into a dictionary that the
#HTTP Server can use to form a response.  Note that this code works this way for
#example purposes.  In most instances, it's better to buffer your output and send
#everything at once.
class ExampleWrapper(Axon.Component.component):
 
    def main(self):
        # Tell the browser the type of data we're sending!
        resource = {
           "type"           : "text/html",
           "statuscode"     : "200",
        }
        self.send(resource, "outbox"); yield 1

        # Send the header 
        header = {
          "data" : "<html><body>"
        }
        self.send(header, "outbox"); yield 1

        # Wait for it....
        while not self.dataReady("inbox"):
            self.pause()
            yield 1

        # Send the data we recieve as the page body
        while self.dataReady("inbox"):
            pageData = {
               "data" : str(self.recv("inbox"))
            }
            self.send(pageData, "outbox"); yield 1

        # send a footer
        footer = {
          "data" : "</body></html>"
        }
        self.send(footer, "outbox"); yield 1

        # and shutdown nicely
        self.send(Axon.Ipc.producerFinished(self), "signal")        
        yield 1

#This handler will join the RequestEchoer and ExampleWrapper together such that
#the RequestEchoer will forward the request dictionary on to the ExampleWrapper,
#which will wrap the data in a response dictionary and forward the data on to the
#HTTP Server.
def EchoHandler(request):
    return Pipeline ( RequestEchoer(request), ExampleWrapper() )

def servePage(request):
    return Minimal(request=request, 
                   homedirectory=homedirectory, 
                   indexfilename=indexfilename)

routing = [
            ["/echo", EchoHandler ],
            ["/hello", HelloHandler ],
            ["/", MinimalFactory(indexfilename, homedirectory) ],
          ]

print __doc__

ServerCore(protocol=HTTPProtocol(routing),
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()
