#!/usr/bin/python

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

def logRequest(request):
	file = open("request.log", "a")
	for key in request:
		output_string = '"%s" : "%s"\n' % (key, request[key])
		file.write(output_string)
	file.close()
	

def requestHandlers(URLHandlers):
    def createRequestHandler(request):
        logRequest(request)
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
