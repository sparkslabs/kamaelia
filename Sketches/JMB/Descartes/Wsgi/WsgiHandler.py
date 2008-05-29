import socket
import pprint
import string
import sys
import os
import re
import cStringIO
from datetime import datetime
from wsgiref.validate import validator
import copy
import LogWritable
import urls
import Axon
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component
import Kamaelia.Util.Log as Log

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

def normalizeEnviron(environ):
    """
    Converts environ variables to strings for wsgi compliance and deletes extraneous
    fields.  Also puts the request headers into CGI variables.
    """
    header_list = []
    header_dict = environ['headers']
    
    for header in environ["headers"]:
        cgi_varname = "HTTP_"+header.replace("-","_").upper()
        environ[cgi_varname] = environ["headers"][header]

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

    def __init__(self, app_name, app, request, log_writable, WsgiConfig):
        super(_WsgiHandler, self).__init__()
        self.app_name = app_name
        self.request = request
        self.environ = copy.deepcopy(request)
        #Some part of the server holds a reference to the request.
        #Since we have to format the data in some different ways than the
        #HTTPParser expects, we need to give the environ object its own
        #copy of the object.
        
        self.app = app
        self.log_writable = log_writable
        self.status = self.response_headers = False
        self.wsgi_config = WsgiConfig

    def main(self):

        self.server_name, self.server_port = self.request['uri-server'].split(':')
        #Get the server name and the port number from the server portion of the
        #uri.  E.G. 127.0.0.1:8082/moin returns 127.0.0.1 and 8082

        self.headers = self.environ["headers"]

        self.initRequiredVars(self.wsgi_config)
        self.initOptVars(self.wsgi_config)

        #stringify all variables for wsgi compliance
        normalizeEnviron(self.environ)
        
        pprint.pprint(self.environ)

        #PEP 333 specifies that we're not supposed to buffer output here,
        #so pulling the iterator out of the app object
        app_iter = iter(self.app(self.environ, self.start_response))

        first_response = app_iter.next()
        if self.response_headers and self.status:
            self.write(first_response)

        for fragment in app_iter:
            page = {
                'data' : fragment,
            }
            self.send(page, 'outbox')
        
        try:
            app_iter.close()  #WSGI validator complains if the app object returns an iterator and we don't close it.
        except:
            pass  #it was a list, so we're good
        
        self.environ['wsgi.input'].close()
        self.send(Axon.Ipc.producerFinished(self), "signal")

    def start_response(self, status, response_headers, exc_info=None):
        """
        Method to be passed to WSGI application object to start the response.
        """
        #TODO:  Add more exc_info support
        if exc_info:
            try:    
                raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None

        self.status = status
        self.response_headers = response_headers

        return self.write

    def write(self, body_data):
        """
        Write method to be passed to WSGI application object.  Used to write
        unbuffered output to the page.  You probably don't want to use this
        unless you have good reason to.
        """
        if self.response_headers and self.status:
            page = {
                'data' : body_data,
            }
            self.send(page, 'outbox')

        else:
            raise WsgiError("write() called before start_response()!")

    def generateRequestMemFile(self):
        """
        Creates a memfile to be stored in wsgi.input.  Uses cStringIO which may be vulnerable to DOS attacks.
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
        (including ones that could possibly be empty).
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

def Handler(log_writable, WsgiConfig, substituted_path):
    """
    This method checks the URI against a series of regexes from urls.py to determine which
    application object to route the request to, imports the file that contains the app object,
    and then extracts it to be passed to the newly created WSGI Handler.
    """
    def _getWsgiHandler(request):
        requested_uri = sanitizePath(request['raw-uri'], substituted_path, request)
        print requested_uri
        for url_item in urls.UrlList:
            print 'trying ' + url_item[0]
            if re.search(url_item[0], requested_uri):
                print url_item[0] + 'succesful!'
                u, mod, app_attr, app_name = url_item
                break
        module = _importWsgiModule(mod)
        app = getattr(module, app_attr)
        return _WsgiHandler(app_name, app, request, log_writable, WsgiConfig)
    return _getWsgiHandler

def HTTPProtocol():
    """
    Pretty standard method.  Returns a function object to implement the HTTP protocol.
    """
    def foo(self,**argd):
        print self.routing
        return HTTPServer(requestHandlers(self.routing),**argd)
    return foo

class WsgiError(Exception):
    """
    This is just a generic exception class.  As of right now, it is only thrown
    when write is called before start_response, so it's primarily an exception
    that is thrown when an application messes up, but that may change!
    """
    def __init__(self):
        super(WsgiError, self).__init__()

def _importWsgiModule(name):
    """
    Just a copy/paste of the example my_import function from here:
    http://docs.python.org/lib/built-in-funcs.html
    """
    print 'importing ' + name
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def sanitizePath(uri, substituted_path, request):
    """
    Almost a straight copy and paste from the minimal request handler.
    """
    uri = uri.replace(substituted_path, '', 1)

    outputpath = []    
    
    for directory in uri.split("/"):
        print directory
        if directory == ".":
            pass
        elif directory == "..":
            if len(outputpath) > 0: outputpath.pop()
        elif directory.find('?') != -1:
            query_split = directory.split('?')
            query_part = query_split[-1]
            directory_part = query_split[0]
            request['QUERY_STRING'] = query_part
            outputpath.append(directory_part)
            #also just so happens to be a WSGI variable.
        else:
            outputpath.append(directory)
    print outputpath
    outputpath = '/'.join(outputpath)
    return outputpath
