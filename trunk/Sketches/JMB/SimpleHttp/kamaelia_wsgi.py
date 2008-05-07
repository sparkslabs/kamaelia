#!/usr/bin/python

import socket
from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer
from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

homedirectory = "./www"
indexfilename = "index.html"

def requestHandlers(URLHandlers):
    def createRequestHandler(request):
        if request.get("bad"):
            return ErrorPages.websiteErrorPage(400, request.get("errormsg", ""))
        else:
            for (prefix, handler) in URLHandlers:
                if request["raw-uri"][:len(prefix)] == prefix:
                    request["uri-prefix-trigger"] = prefix
                    request["uri-suffix"] = request["raw-uri"][len(prefix):]
                    return handler(request)
        return ErrorPages.websiteErrorPage(404, "No resource handlers found for the requested URL.")
        
    return createRequestHandler

def servePage(request):
    return Minimal(request=request,
                   homedirectory=homedirectory,
                   indexfilename=indexfilename)
                   
def HTTPProtocol():
     return HTTPServer(requestHandlers([
                          ["/", servePage ],
                      ]))

SimpleServer(protocol=HTTPProtocol,
             port=8000,
             socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ).run()