import ServerConfig
from Wsgi.WsgiHandler import HTML_WRAP,  Handler
from wsgiref.validate import validator
from DescartesCore import ServerCore
import socket
import Kamaelia.Util.Log as Log
import Handlers.Wsgi.LogWritable as LogWritable

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
               ["/wsgi", Handler("/wsgi", validator(HTML_WRAP(simple_app)), log_writable, ServerConfig.WsgiConfig) ],
              ]
    protocol=HTTPProtocol()
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

des = DescartesServer()
des.run()
