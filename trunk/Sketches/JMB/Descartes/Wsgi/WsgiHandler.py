import socket
import pprint
import string
import sys
import os
import cStringIO
from datetime import datetime
from wsgiref.validate import validator
import LogWritable
import Axon
from Axon.ThreadedComponent import threadedcomponent
#from Axon.Component import component
import Kamaelia.Util.Log as Log


from Kamaelia.Chassis.ConnectedServer import MoreComplexServer

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

Axon.Box.ShowAllTransits = False
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
        iterator = app(environ, start_response)
        first_yield = iterator.next()
        yield "<html>\n"
        yield "<body>\n"
        yield first_yield
        for i in iterator:
            yield i
        yield "</body>\n"
        yield "</html>\n"
    return gen

def getServerInfo(uri_server):
    split_server = uri_server.split(":")
    return (split_server[0], split_server[1])

def normalizeEnviron(environ):
    """
    Converts environ variables to strings for wsgi compliance and deletes extraneous
    fields.
    """
    header_list = []
    header_dict = environ['headers']

    for key in header_dict:
        line = "%s: %s\n" % (key, header_dict[key])
        header_list.append(line)

    environ['headers'] = ''.join(header_list)
    environ['peerport'] = str(environ['peerport'])
    environ['localport'] = str(environ['localport'])
    del environ['bad']


class _WsgiHandler(threadedcomponent):
    """Choosing to run the WSGI app in a thread rather than the same
       context, this means we don't have to worry what they get up
       to really"""
    Inboxes = {
        'inbox' : 'NOT USED',
        'control' : 'NOT USED',
    }
    Outboxes = {
        'outbox' : 'used to send page fragments',
        'signal' : 'send producerFinished messages',
        '_signal-lw' : 'shut down the log writable',
    }

    def __init__(self, app_name, request, app, log_writable, WsgiConfig):
        super(_WsgiHandler, self).__init__()
        self.app_name = app_name
        self.request = request
        self.environ = request
        self.app = app
        self.log_writable = log_writable
        self.status = self.response_headers = False
        self.wsgi_config = WsgiConfig

    def main(self):


        self.headers = self.environ["headers"]
        self.server_name, self.server_port = getServerInfo(self.request["uri-server"])

        self.initRequiredVars(self.wsgi_config)
        self.initOptVars(self.wsgi_config)

        self.munge_headers()

        #stringify all variables for wsgi compliance
        normalizeEnviron(self.environ)

        #PEP 333 specifies that we're not supposed to buffer output here,
        #so pulling the iterator out of the app object
        app_iter = self.app(self.environ, self.start_response)

        first_response = app_iter.next()
        if self.response_headers:
            self.write(first_response)
        else:
            raise WsgiError()

        for fragment in app_iter:
            page = {
                'data' : fragment,
            }
            self.send(page, 'outbox')

        app_iter.close()

        self.send(Axon.Ipc.producerFinished(self), "signal")

    def start_response(self, status, response_headers, exc_info=None):
        """
        Method to be passed to WSGI application object
        """
        #TODO:  Add more exc_info support
        if exc_info:
            raise exc_info[0], exc_info[1], exc_info[2]

        self.status = status
        self.response_headers = response_headers

        return self.write

    def write(self, body_data):
        page = {
            'data' : body_data,
        }
        self.send(page, 'outbox')

    def munge_headers(self):
        for header in self.environ["headers"]:
            cgi_varname = "HTTP_"+header.replace("-","_").upper()
            self.environ[cgi_varname] = self.environ["headers"][header]

        pprint.pprint(self.environ)
        pprint.pprint(self.environ["headers"])

    def generateRequestMemFile(self):
        """
        Creates a memfile to be stored in wsgi.input
        """
        CRLF = '\r\n'

        full_request = "%s %s %s/%s%s" % \
            (self.environ['method'], self.environ['raw-uri'], self.environ['protocol'], self.environ['version'], CRLF)

        header_list = []
        for key in self.environ['headers']:
            header_list.append("%s: %s%s" % (key, self.environ['headers'][key], CRLF))

        full_request = full_request + string.join(header_list) + '\n' + self.environ['body']
        print "full_request: \n" + full_request

        return cStringIO.StringIO(full_request)

    def initRequiredVars(self, wsgi_config):
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
        self.environ["wsgi.version"] = wsgi_config['WSGI_VER']
        self.environ["wsgi.url_scheme"] = self.request["protocol"].lower()
        self.environ["wsgi.errors"] = self.log_writable

        self.environ["wsgi.multithread"] = False
        self.environ["wsgi.multiprocess"] = False
        self.environ["wsgi.run_once"] = True
        self.environ["wsgi.input"] = self.generateRequestMemFile()

    def initOptVars(self, wsgi_config):
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
        self.environ["PATH"] = os.environ['PATH']
        self.environ["DATE"] = datetime.now().isoformat()
        self.environ["SERVER_ADMIN"] = wsgi_config['SERVER_ADMIN']
        self.environ["SERVER_SOFTWARE"] = wsgi_config['SERVER_SOFTWARE']
        self.environ["SERVER_SIGNATURE"] = "%s Server at %s port %s" % \
                    (wsgi_config['SERVER_SOFTWARE'], self.server_name, self.server_port)

    def unsupportedVars(self):
        """
        Probably won't be used.  This is just a list of environment variables that
        aren't implemented as of yet.
        """
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

def Handler(app_name,  app, log_writable, WsgiConfig):
    def R(request):
        return _WsgiHandler(app_name, request,app, log_writable, WsgiConfig)
    return R

def HTTPProtocol():
    def foo(self,**argd):
        print self.routing
        return HTTPServer(requestHandlers(self.routing),**argd)
    return foo

class WsgiError(Exception):
    def __init__(self):
        super(WsgiError, self).__init__()

def FindWsgiModule(request):
    pass
