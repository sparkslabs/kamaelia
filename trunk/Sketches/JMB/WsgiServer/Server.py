#!/usr/bin/python

# Import socket to get at constants for socketOptions
import socket
import pprint
import string
import sys
from datetime import datetime
import serverinfo
from wsgiref.validate import validator

# We need to import Axon - Kamaelia's core component system - to write Kamaelia components!
import Axon

# Import the server framework, the HTTP protocol handling, the minimal request handler, and error handlers

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer

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
            return errorpages.getErrorPage(400, request.get("errormsg",""))
        else:
            for (prefix, handler) in URLHandlers:
                if request["raw-uri"][:len(prefix)] == prefix:
                    request["uri-prefix-trigger"] = prefix
                    request["uri-suffix"] = request["raw-uri"][len(prefix):]
                    return handler(request)

        return errorpages.getErrorPage(404, "No resource handlers could be found for the requested URL")

    return createRequestHandler
        
def sanitizePath():
    """Joins sys.path into a : separated string with no empty elements"""
    path = sys.path
    filter(lambda elem: elem, path)    #remove all empty elements
    return string.join(path, ':')

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
    Wraps the Application object's results in HTML
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
        
def getServerInfo(uri_server):
    split_server = uri_server.split(":")
    return (split_server[0], split_server[1])

def stringifyEnviron(environ):
    """
    Converts environ variables to strings for wsgi compliance
    """
    header_list = []
    header_dict = environ['headers']
    
    for key in header_dict:
        line = "%s: %s\n" % (key, header_dict[key])
        header_list.append(line)
    
    environ['headers'] = ''.join(header_list)
    environ['peerport'] = str(environ['peerport'])
    

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
        """
        Method to be passed to WSGI application object
        
        TODO:  implement exc_info
        """
        
        self.status = status
        self.response_headers = response_headers

    def munge_headers(self):
        for header in self.environ["headers"]:
            cgi_varname = "HTTP_"+header.replace("-","_").upper()
            self.environ[cgi_varname] = self.environ["headers"][header]
            
        pprint.pprint(self.environ)
        pprint.pprint(self.environ["headers"])
        
    def initRequiredVars(self):
        """
        This method initializes all variables that are required to be present 
        (including ones that could possibly be empty.
        """
        self.environ["REQUEST_METHOD"] = self.request["method"]
        
        # Portion of URL that relates to the application object.
        self.environ["SCRIPT_NAME"] = self.app_name
        
        # Remainder of request path after "SCRIPT_NAME"
        self.environ["PATH_INFO"] = self.environ["uri-suffix"]
        
        # Server name published to the outside world
        self.environ["SERVER_NAME"] = self.server_name
        
        # Server port published to the outside world
        self.environ["SERVER_PORT"] =  self.server_port
        
        #Protocol to respond to
        self.environ["SERVER_PROTOCOL"] = self.request["protocol"]
        
        #==================================
        #WSGI variables
        #==================================
        self.environ["wsgi.version"] = serverinfo.WSGI_VER
        self.environ["wsgi.url_scheme"] = self.request["protocol"].lower()
        self.environ["wsgi.errors"] = sys.stderr  #TODO:  Convert to a log stream
        self.environ["wsgi.multithread"] = 0
        self.environ["wsgi.multiprocess"] = 0
        self.environ["wsgi.run_once"] = 0
        self.environ["wsgi.input"] = sys.stdin   #TODO:  FIX THIS
        
    def initOptVars(self):
        """This method initializes all variables that are optional"""
        # Portion of request URL that follows the ? - may be empty or absent
        if self.environ["uri-suffix"].find("?") != -1:
            self.environ["QUERY_STRING"] = \
                self.environ["uri-suffix"][self.environ["uri-suffix"].find("?")+1:]
        else:
            self.environ["QUERY_STRING"] = ""
            
        # Contents of an HTTP_CONTENT_TYPE field
        self.environ["CONTENT_TYPE"] = self.headers.get("content-type","")
        
        # Contents of an HTTP_CONTENT_LENGTH field
        self.environ["CONTENT_LENGTH"] = self.headers.get("content-length","") 
        #self.environ["DOCUMENT_ROOT"] = self.homedirectory
        self.environ["PATH"] = sanitizePath()
        self.environ["DATE"] = datetime.now().isoformat()
        self.environ["SERVER_ADMIN"] = serverinfo.SERVER_ADMIN
        self.environ["SERVER_SOFTWARE"] = serverinfo.SERVER_SOFTWARE
        self.environ["SERVER_SIGNATURE"] = "%s Server at %s port %s" % \
                    (serverinfo.SERVER_SOFTWARE, self.server_name, self.server_port) 
        
        #needs fixing - doesn't work on all systems
        self.environ["SERVER_ADDR"] = socket.gethostbyname(socket.gethostname())
        
    def unsupportedVars(self):
        consider = " **CONSIDER ADDING THIS -- eg: "
        self.environ["HTTP_REFERER"] = consider + "-"
        self.environ["SERVER_SIGNATURE"] = consider + "...."
        self.environ["SCRIPT_FILENAME"] = consider + \
            "/usr/local/httpd/sites/com.thwackety/cgi/test.pl"
        self.environ["REQUEST_URI"] = consider + "/cgi-bin/test.pl"
        self.environ["SCRIPT_URL"] = consider + "/cgi-bin/test.pl"
        self.environ["SCRIPT_URI"] = consider + "http://thwackety.com/cgi-bin/test.pl"
        self.environ["REMOTE_ADDR"] = consider + "192.168.2.5"
        self.environ["REMOTE_PORT"] = consider + "56669"
        self.environ["GATEWAY_INTERFACE"] = consider + "CGI/1.1"
        
    def main(self):
        self.headers = self.environ["headers"]
        self.server_name, self.server_port = getServerInfo(self.request["uri-server"])

        self.initRequiredVars()
        self.initOptVars()

        self.munge_headers()
        
        #stringify all variables for wsgi compliance
        stringifyEnviron(self.environ)
        
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

class WebServer(MoreComplexServer):
    routing = [
               ["/wsgi", WSGIHandler("/wsgi", HTML_WRAP(simple_app)) ],
              ]
    protocol=HTTPProtocol()
    port=8082
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

WebServer().run()

"""
Changed Webserver to use the newer MoreComplexServer:
   * Requried change to HTTPServer
   * HTTPParser

IPs now in request object passed out for a handler with keys
   * peer, peerip
   * localip, localport





"""


















