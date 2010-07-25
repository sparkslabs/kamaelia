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

import ServerConfig
from Wsgi.WsgiHandler import HTML_WRAP,  Handler
import Wsgi.LogWritable as LogWritable
import Static.Minimal as Minimal
from wsgiref.validate import validator
from DescartesCore import ServerCore
import socket
import Kamaelia.Util.Log as Log

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

def HTTPProtocol():
    def foo(self,**argd):
        print self.routing
        return HTTPServer(requestHandlers(self.routing),**argd)
    return foo

def requestHandlers(URLHandlers, errorpages=None):
    if errorpages is None:
        import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
        errorpages = ErrorPages
    def createRequestHandler(request):
        if request.get("bad"):
            return errorpages.getErrorPage(400, request.get("errormsg",""))
        else:
            for (prefix, handler) in URLHandlers:
                if request["raw-uri"][:len(prefix)] == prefix:
                    request["uri-prefix-trigger"] = prefix
                    request["uri-suffix"] = request["raw-uri"][len(prefix):]
                    return handler(request)

        return errorpages.getErrorPage(404, "No resource handlers could be found for the requested URL")

    return createRequestHandler


log = Log.Logger('wsgi.log', wrapper=Log.nullWrapper)

log_writable = LogWritable.WsgiLogWritable('wsgi.log')
log_writable.activate()

log.activate()


class DescartesServer(ServerCore):
    routing = [
               ['/static', Minimal.Handler('index.html', './Static/www/', '/static')],
               ["/", Handler(log_writable, ServerConfig.WsgiConfig, '/') ],
              ]
    protocol=HTTPProtocol()
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

des = DescartesServer()
des.run()
