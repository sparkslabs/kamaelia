#!/usr/bin/python

import socket
import Axon

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

from Kamaelia.Chassis.Pipeline import Pipeline

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

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

class Cat(Axon.Component.component):
    def __init__(self, *args):
        super(Cat, self).__init__()
        self.args = args
    def main(self):
        self.send(self.args, "outbox")
        self.send(Axon.Ipc.producerFinished(self), "signal")        
        yield 1

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

def EchoHandler(request):
    return Pipeline ( Cat(request), ExampleWrapper() )

def servePage(request):
    return Minimal(request=request, 
                   homedirectory=homedirectory, 
                   indexfilename=indexfilename)

routing = [
            ["/echo", EchoHandler ],
            ["/hello", HelloHandler ],
            ["/", MinimalFactory(indexfilename, homedirectory) ],
          ]

ServerCore(protocol=HTTPProtocol(routing),
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()
