#!/usr/bin/env

import ServerConfig
import sys, socket
from pprint import pprint
from Kamaelia.Experimental.Wsgi.WsgiHandler import HTML_WRAP,  Handler
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable
import Kamaelia.Protocol.HTTP.Handlers.Minimal as Minimal
from Kamaelia.Chassis.ConnectedServer import SimpleServer
import Kamaelia.Util.Log as Log
from Kamaelia.File.ConfigFile import DictFormatter, UrlListFormatter, ParseConfigFile

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

sys.path.append(ServerConfig.WsgiAppLog)

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

def main():
    url_list = ParseConfigFile(ServerConfig.URL_LIST_LOCATION, [DictFormatter(), UrlListFormatter()])
#    pprint(url_list)


    log = Log.LogWriter(ServerConfig.WsgiAppLog, wrapper=Log.nullWrapper)

    log_writable = LogWritable.WsgiLogWritable(ServerConfig.WsgiAppLog)
    log_writable.activate()

    class KPServer(SimpleServer):
        routing = [
                   #['/static', Minimal.Handler('index.html', './Static/www/', '/static')],
                   ["/", Handler(log_writable, ServerConfig.WsgiConfig, url_list)],
                  ]
        protocol=HTTPProtocol()
        port=8082
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.activate()

    des = KPServer()
    print "Serving on port %s" % (ServerConfig.PORT)
    des.run()

main()
