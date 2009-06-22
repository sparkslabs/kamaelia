#!/usr/bin/python
"""
This is the beginnings of a Kamaelia based webserver that is generally useful.
It is being used as the core basis of Kamaelia Publish
"""


# Import socket to get at constants for socketOptions
import socket
import pprint

# We need to import Axon - Kamaelia's core component system - to write Kamaelia components!
import Axon

# Import the server framework, the HTTP protocol handling, the minimal request handler, and error handlers

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Chassis.ConnectedServer import ServerCore

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
    for i in sorted(environ.keys()):
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
    def __init__(self, app_name, request, app):
        super(_WSGIHandler, self).__init__()
        self.app_name = app_name
        self.request = request
        self.environ = request
        self.app = app

    def start_response(self, status, response_headers):
        self.status = status
        self.response_headers = response_headers

    def munge_headers(self):
        for header in self.environ["headers"]:
            cgi_varname = "HTTP_"+header.replace("-","_").upper()
            self.environ[cgi_varname] = self.environ["headers"][header]
        pprint.pprint(self.environ)
        pprint.pprint(self.environ["headers"])

    def main(self):
        required = "*** REQUIRED FIX THIS ***"
        headers = self.environ["headers"]
        self.environ["REQUEST_METHOD"] = required  # Required
        self.environ["SCRIPT_NAME"] = self.app_name  # Portion of URL that relates to the application object. May be empty. (eg /cgi-bin/test.pl)
        self.environ["PATH_INFO"] = self.environ["uri-suffix"]  # Remainder of request path after "SCRIPT_NAME", designating a content path may be empty.
        
        if self.environ["uri-suffix"].find("?") != -1:
            self.environ["QUERY_STRING"] = self.environ["uri-suffix"][self.environ["uri-suffix"].find("?")+1:]
        else:
            self.environ["QUERY_STRING"] = ""
#        self.environ["QUERY_STRING"] = required    # Portion of request URL that follows the ? - may be empty or absent
        self.environ["CONTENT_TYPE"] = headers.get("content-type","") # Contents of an HTTP_CONTENT_TYPE field - may be absent or empty
        self.environ["CONTENT_LENGTH"] = headers.get("content-length","") # Contents of an HTTP_CONTENT_LENGTH field - may be absent or empty
        self.environ["SERVER_NAME"] = required     # Server name published to the outside world
        self.environ["SERVER_PORT"] = required     # Server port published to the outside world
        self.environ["SERVER_PROTOCOL"] = required # Version of protocol client _sent us_ (what they would like back)

        consider = " **CONSIDER ADDING THIS -- eg: "
        self.environ["SERVER_ADDR"] = consider + "192.168.2.9"
        self.environ["HTTP_REFERER"] = consider + "-"
        self.environ["SERVER_ADMIN"] = consider + "[no address given]"
        self.environ["SERVER_SIGNATURE"] = consider + "...."
        self.environ["SERVER_SOFTWARE"] = consider + "Apache/1.3.33 (Darwin)"
        self.environ["SCRIPT_FILENAME"] = consider + "/usr/local/httpd/sites/com.thwackety/cgi/test.pl"
        self.environ["DOCUMENT_ROOT"] = consider + "/usr/local/httpd/sites/com.thwackety/docs"
        self.environ["REQUEST_URI"] = consider + "/cgi-bin/test.pl"
        self.environ["SCRIPT_URL"] = consider + "/cgi-bin/test.pl"
        self.environ["SCRIPT_URI"] = consider + "http://thwackety.com/cgi-bin/test.pl"
        self.environ["REMOTE_ADDR"] = consider + "192.168.2.5"
        self.environ["REMOTE_PORT"] = consider + "56669"
        self.environ["DATE"] = consider + "Sat Sep 15 15:42:25 2007" #####
        self.environ["PATH"] = consider + "/bin:/sbin:/usr/bin:/usr/sbin:/usr/libexec:/System/Library/CoreServices"
        self.environ["GATEWAY_INTERFACE"] = consider + "CGI/1.1"

        self.munge_headers()
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

def WSGIHandler(app_name, app):
    def R(request):
        return _WSGIHandler(app_name, request,app)
    return R

def HTTPProtocol():
    def foo(self,**argd):
        print self.routing
        return HTTPServer(requestHandlers(self.routing),**argd)
    return foo

# Finally we create the actual server and run it.

class WebServer(ServerCore):
    routing = [
               ["/wsgi", WSGIHandler("/wsgi", HTML_WRAP(simple_app)) ],
              ]
    protocol=HTTPProtocol()
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

WebServer().run()

"""
Changed Webserver to use the newer ServerCore
   * Requried change to HTTPServer
   * HTTPParser

IPs now in request object passed out for a handler with keys
   * peer, peerip
   * localip, localport





"""


















