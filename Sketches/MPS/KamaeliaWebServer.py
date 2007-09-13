#!/usr/bin/python

# Import socket to get at constants for socketOptions
import socket
import pprint

# We need to import Axon - Kamaelia's core component system - to write Kamaelia components!
import Axon

# Import the server framework, the HTTP protocol handling, the minimal request handler, and error handlers

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

Axon.Box.ShowAllTransits = False

# This allows for configuring the request handlers in a nicer way. This is candidate
# for merging into the mainline code. Effectively this is a factory that creates functions
# capable of choosing which request handler to use.

def requestHandlers(URLHandlers, errorpages=None):
    if errorpages is None:
        import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
        errorpages = ErrorPages
    def createRequestHandler(request):
        if request.get("bad"):
            return errorpages.websiteErrorPage(400, request.get("errormsg",""))
        else:
            for (prefix, handler) in URLHandlers:
                if request["raw-uri"][:len(prefix)] == prefix:
                    request["uri-prefix-trigger"] = prefix
                    request["uri-suffix"] = request["raw-uri"][len(prefix):]
                    return handler(request)

        return errorpages.websiteErrorPage(404, "No resource handlers could be found for the requested URL")

    return createRequestHandler

class HelloHandler(Axon.Component.component):
    def __init__(self, request):
        super(HelloHandler, self).__init__()
        self.request = request

    def main(self):
        resource = {
           "statuscode"     : "200",
           "headers"    : [
                ("content-type", "text/html"),
           ]
        }
        self.send(resource, "outbox"); yield 1
        page = {
          "data" : "<html><body><h1>Hello World</h1><P>Woo!!</body></html>",
        }
        self.send(page, "outbox"); yield 1
        self.send(Axon.Ipc.producerFinished(self), "signal")
        yield 1

# ----------------------------------------------------------------------------------------------------
#
# Simple WSGI Handler
#
import time
def simple_app(environ, start_response):
    """Simplest possible application object""" 
    status = '200 OK'
    response_headers = [('Content-type','text/html'),('Pragma','no-cache')]
    start_response(status, response_headers)
    yield '<P> My Own Hello World!\n'
    for i in environ:
        yield "<li>%s: %s\n" % (i, environ[i])
    yield "<li> Date:" + time.ctime()

# ----------------------------------------------------------------------------------------------------
#
# Simple WSGI Handler
#
def HTML_WRAP(app):
    """
    Wraps the output of app in HTML
    """
    def gen(environ, start_response):
        """The standard WSGI interface"""
        yield "<html>\n"
        yield "<body>\n"
        for i in app(environ, start_response):
            yield i
        yield "</body>\n"
        yield "</html>\n"
    return gen

class _WSGIHandler(Axon.ThreadedComponent.threadedcomponent):
    """Choosing to run the WSGI app in a thread rather than the same
       context, this means we don't have to worry what they get up
       to really"""
    def __init__(self, request, app):
        super(_WSGIHandler, self).__init__()
        self.request = request
        self.environ = request
        self.app = app

    def start_response(self, status, response_headers):
        self.status = status
        self.response_headers = response_headers

    def main(self):
        R = [ x for x in self.app(self.environ, self.start_response) ]
        resource = {
           "statuscode" : self.status,
           "headers"    : self.response_headers,
        }
        self.send(resource, "outbox")
        for fragment in R:
            page = {
              "data" : fragment,
            }
            self.send(page, "outbox")
        self.send(Axon.Ipc.producerFinished(self), "signal")

def WSGIHandler(app):
    def R(request):
        return _WSGIHandler(request,app)
    return R

def HTTPProtocol(self):
    return HTTPServer(requestHandlers([
                          ["/", WSGIHandler(
                                  HTML_WRAP(
                                    simple_app))
                          ],
                      ]))

# Finally we create the actual server and run it.

class WebServer(SimpleServer):
    protocol=HTTPProtocol
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

WebServer().run()
