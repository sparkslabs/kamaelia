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

import socket

from Axon.LikeFile import likefile, background
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
background().start()

import Axon

from Kamaelia.Chassis.ConnectedServer import MoreComplexServer
from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer
from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

from Kamaelia.Chassis.Pipeline import Pipeline

# Our configuration

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

def requestHandlers(URLHandlers):
    def createRequestHandler(request):
        if request.get("bad"):
            return ErrorPages.websiteErrorPage(400, request.get("errormsg",""))
        else:
            for (prefix, handler) in URLHandlers:
                if request["raw-uri"][:len(prefix)] == prefix:
                    request["uri-prefix-trigger"] = prefix
                    request["uri-suffix"] = request["raw-uri"][len(prefix):]
                    return handler(request)

        return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL")

    return createRequestHandler


def servePage(request):
    return Minimal(request=request, homedirectory=homedirectory, indexfilename=indexfilename)

class PeerProxy(Axon.ThreadedComponent.threadedcomponent):
    def __init__(self, request):
        super(PeerProxy, self).__init__()
        self.request = request

    def main(self):
        uri = self.request.get('uri-suffix',"/")
        p = likefile( SimpleHTTPClient() )
        p.put("http://kamaelia.sourceforge.net/%s" % uri)
        pagedata= p.get()
        p.shutdown()
        print pagedata

        resource = {
           "type"           : "text/html",
           "statuscode"     : "200",
        }
        self.send(resource, "outbox")
        page = { "data" : pagedata }
        self.send(page, "outbox")
        self.send(Axon.Ipc.producerFinished(self), "signal")

def HTTPProtocol(*args,**argd):
    return HTTPServer(requestHandlers([
                          ["/peer", PeerProxy ],
                          ["/", servePage ],
                      ]))

MoreComplexServer(protocol=HTTPProtocol,
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).activate()

import time
while 1:
    time.sleep(1)
