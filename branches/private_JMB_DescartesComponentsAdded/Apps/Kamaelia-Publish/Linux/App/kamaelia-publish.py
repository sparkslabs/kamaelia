#!/usr/bin/env

import ServerConfig
import sys
from Kamaelia.Experimental.Wsgi.WsgiHandler import HTML_WRAP,  Handler
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable
import Kamaelia.Protocol.HTTP.Handlers.Minimal as Minimal
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer
import socket
import Kamaelia.Util.Log as Log

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

sys.path.append(ServerConfig.WSGI_DIR)

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


log = Log.Logger(ServerConfig.WSGI_APP_LOG, wrapper=Log.nullWrapper)

log_writable = LogWritable.WsgiLogWritable(ServerConfig.WSGI_APP_LOG)
log_writable.activate()

log.activate()


class DescartesServer(MoreComplexServer):
    routing = [
               #['/static', Minimal.Handler('index.html', './Static/www/', '/static')],
               ["/", Handler(log_writable, ServerConfig.WsgiConfig, '/') ],
              ]
    protocol=HTTPProtocol()
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

des = DescartesServer()
des.run()
