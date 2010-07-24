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

# Import socket to get at constants for socketOptions

import socket

# Import the server framework, the HTTP protocol handling, the minimal request handler, and error handlers

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer
from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

# Our configuration

homedirectory = "/srv/www/htdocs/"
indexfilename = "index.html"

# This allows for configuring the request handlers in a nicer way. This is candidate
# for merging into the mainline code. Effectively this is a factory that creates functions
# capable of choosing which request handler to use.

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

# This factory allows us to configure the minimal request handler.

def servePage(request):
    return Minimal(request=request,
                   homedirectory=homedirectory,
                   indexfilename=indexfilename)


# A factory to create configured HTTPServer components - ie HTTP Protocol handling components

def HTTPProtocol():
    return HTTPServer(requestHandlers([
                          ["/", servePage ],
                      ]))

# Finally we create the actual server and run it.

SimpleServer(protocol=HTTPProtocol,
             port=8082,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ).run()
