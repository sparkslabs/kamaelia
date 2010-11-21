#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module demonstrates the Minimal HTTP Handler along
with some custom-written components.

System Requirements
-------------------
This example requires a UNIX operating system to run.
"""

import socket
import Axon

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Protocol.HTTP.Handlers.Minimal import MinimalFactory
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol

from Kamaelia.Chassis.Pipeline import Pipeline

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

class HelloHandler(Axon.Component.component):
    """\
    This is the hello handler.  It will respond to every request with a
    Hello world message (with some HTML formatting)
    """
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
    """\
    Like the unix command "cat", this takes whatever has been passed as an
    argument and forwards it out it's standard output - in this case out the
    outbox "outbox".
    """
    def __init__(self, *args):
        super(Cat, self).__init__()
        self.args = args
    def main(self):
        self.send(self.args, "outbox")
        self.send(Axon.Ipc.producerFinished(self), "signal")        
        yield 1

class ExampleWrapper(Axon.Component.component):
    """\
    This component will simply wrap any input it receives into a dictionary
    that the HTTP Server can use to form a response.  Note that this code
    works this way for example purposes.  In most instances, it's better to
    buffer your output and send everything at once.
    """
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
    """\
    This handler will join the 'Cat' handler and ExampleWrapper together
    such that the 'Cat' will forward the request dictionary on to the
    ExampleWrapper, which will wrap the data in a response dictionary and
    forward the data on to the HTTP Server.
    """
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
