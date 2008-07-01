#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: JMB
"""
WSGI Handler
=============

NOTE:  This is experimental software.  It has not been fully tested and will
probably break or behave in unexpected ways.

This is the WSGI handler for ServerCore.  It will wait on the
HTTPParser to transmit the body in full before proceeding.  Thus, it is probably
not a good idea to use any WSGI apps requiring a lot of large file uploads (although
it could theoretically function fairly well for that purpose as long as the concurrency
level is relatively low).

For more information on WSGI, what it is, and to get a general overview of what
this component is intended to adapt the ServerCore to do, see one of the following
links:

* http://www.python.org/dev/peps/pep-0333/ (PEP 333)
* http://www.wsgi.org/wsgi/ (WsgiStart wiki)
* http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface (Wikipedia article on WSGI)

-------------
Dependencies
-------------

This component depends on the wsgiref module, which is included with python 2.5.
Thus if you're using an older version, you will need to install it before using
this component.  

The easiest way to install wsgiref is to use easy_install, which may be downloaded
from http://peak.telecommunity.com/DevCenter/EasyInstall .  You may then install
wsgiref using the command "sudo easy_install wsgiref" (without the quotes of course).

Please note that Kamaelia Publish includes wsgiref.

-----------------------------
How do I use this component?
-----------------------------

The easiest way to use this component is to use the WsgiHandler factory function
that is included in Factory.py in this package.  That method has URL handling that
will route a URL to the proper place.  There is also a SimpleWsgiHandler that may
be used if you only want to support one application object.  For more information
on how to use these functions, please see Factory.py.  Also please note that both
of these factory functions are made to work with ServerCore/SimpleServer.  Here is
an example of how to create a simple WSGI server:

from Kamaelia.Protocol.HTTP import HTTPProtocol
from Kamaelia.Experimental.Wsgi.Factory import WsgiFactory
import Kamaelia.Experimental.Wsgi.Log as Log
import Kamaelia.Experimental.Wsgi.LogWritable as LogWritable

WsgiConfig = {
    'wsgi_ver' : (1, 0),
    'server_admin' : 'Jason Baker',
    'server_software' : 'Kamaelia Publish'
}

url_list = [ #Note that this is a list of dictionaries.  Order is important.
    {
        'kp.regex' : 'simple',
        'kp.import_path' : 'Kamaelia.Support.SimpleApp',    #Note that the module need not be imported
        'kp.app_obj' : 'simple_app',
    }
    {
        'kp.regex' : '.*',  #The .* means that this is a 404 handler
        'kp.import_path' : 'Kamaelia.Support.WsgiApps.ErrorHandler',
        'kp.app_obj' : 'application',
    }
]

routing = [['/', WsgiFactory(log_writable, WsgiConfig, url_list)]]

ServerCore(
    protocol=HTTPProtocol(routing),
    port=8080,
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)).run()

------------------
Internal overview
------------------

request object
~~~~~~~~~~~~~~~

This component expects to be passed a request object in the same format as is created
by the HTTPParser.  The request object may contain a 'custom' dictionary entry whose values
will be passed to the application in the environ object.  For example, the request
object may look as follows:

{
    ...
    'custom' : {'kp.regex' : 'simple'},
    ...
}

This will translate into a WSGI environ dictionary as follows:

{
    ...
    'kp.regex' : 'simple',
    ...
}

wsgi.input
~~~~~~~~~~~

PEP 333 requires that the WSGI environ dictionary also contain a file-like object
that holds the body of the request.  Currently, the WsgiHandler will wait for the
full request before starting the application (which is not optimal behavior).  If
the method is not PUT or POST, the handler will use a pre-made null-file object that
will always return empty data.  This is an optimization to lower peak memory usage
and to speed things up.

WsgiConfig
~~~~~~~~~~~

The WsgiHandler requires a WsgiConfig dictonary for general configuration info. The
following items are required to be defined:

* wsgi_ver: the WSGI version as a Tuple.  You want to use (1, 0)
* server_admin: the name and/or email address of the server's administrator
* server_software: The software and/or software version that runs the server
"""

from pprint import pprint, pformat
import sys, os, cStringIO, cgitb, copy, traceback
from datetime import datetime
from wsgiref.util import is_hop_by_hop
import Axon
from Axon.ThreadedComponent import threadedcomponent
from Axon.Component import component
from Axon.Ipc import producerFinished
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
from Kamaelia.Protocol.HTTP import HTTPProtocol
from wsgiref.validate import validator


Axon.Box.ShowAllTransits = False

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

def normalizeEnviron(request, environ):
    """
    Converts environ variables to strings for wsgi compliance and deletes extraneous
    fields.  Also puts the request headers into CGI variables.
    """
    for header in request["headers"]:
        cgi_varname = "HTTP_"+header.replace("-","_").upper()
        environ[cgi_varname] = request["headers"][header]

    if environ.get('HTTP_CONTENT_TYPE'):
        del environ['HTTP_CONTENT_TYPE']
    if environ.get('HTTP_CONTENT_LENGTH'):
        del environ['HTTP_CONTENT_LENGTH']
        
class NullFileLike (object):
    """
    This is a file-like object that is meant to represent an empty file.
    """
    def read(self, number=0):
        return ''
    def readlines(self, number=0):
        return[]
    def readline(self):
        return ''
    def close(self):
        pass
    def next():
        raise StopIteration()
    
_null_fl = NullFileLike()


class _WsgiHandler(threadedcomponent):
    """
    This is a WSGI handler that is used to serve WSGI applications.  Typically,
    URL routing is to be done in the factory method that creates this.  Thus,
    the handler must be passed the application object.
    """
    Inboxes = {
        'inbox' : 'Used to receive the body of requests from the HTTPParser',
        'control' : 'NOT USED',
    }
    Outboxes = {
        'outbox' : 'used to send page fragments',
        'signal' : 'send producerFinished messages',
    }
    Debug = False
    def __init__(self, app, request, log_writable, WsgiConfig, **argd):
        """
        app - The WSGI application to run
        request - the request object that is generated by HTTPParser
        log_writable - a LogWritable object to be passed as a wsgi.errors object.
        WsgiConfig - General configuration about the WSGI server.
        """
        super(_WsgiHandler, self).__init__(**argd)
        self.request = request
        self.environ = {}
        if request.get('custom'):
            self.environ.update(request['custom'] )

        print 'request received for [%s]' % (self.request['raw-uri'])

        self.app = app
        self.log_writable = log_writable
        self.response_dict = {}
        self.wsgi_config = WsgiConfig
        self.write_called = False

    def main(self):
        try:
            self.server_name, self.server_port = self.request['uri-server'].split(':')
        except ValueError:
            self.server_name = self.request['uri-server']
            self.server_port = '80'
        #Get the server name and the port number from the server portion of the
        #uri.  E.G. 127.0.0.1:8082/moin returns 127.0.0.1 and 8082

        self.headers = self.request["headers"]

        if self.request['method'] == 'POST' or self.request['method'] == 'PUT':
            body = self.waitForBody()
            self.memfile = cStringIO.StringIO(body)
        else:
            self.memfile = _null_fl

        #The WSGI validator complains if we close the memfile from wsgi.input directly
        self.environ['wsgi.input'] = self.memfile

        self.initRequiredVars(self.wsgi_config)
        self.initOptVars(self.wsgi_config)

        normalizeEnviron(self.request, self.environ)
#        pprint(self.request)

        try:
            #PEP 333 specifies that we're not supposed to buffer output here,
            #so pulling the iterator out of the app object
            app_iter = iter(self.app(self.environ, self.start_response))

            first_response = app_iter.next()#  License:  LGPL
            self.write(first_response)

            [self.sendFragment(x) for x in app_iter]
        except:
            self._error(503, sys.exc_info())
        try:
            app_iter.close()  #WSGI validator complains if the app object returns an iterator and we don't close it.
        except:
            pass  #it was a list, so we're good

        self.memfile.close()
        #print "Waiting..."
        #self.pause(5)
        #print 'unpausing'
        self.log_writable.flush()
        del self.environ
        del self.request
        self.send(Axon.Ipc.producerFinished(self), "signal")
        #print 'WsgiHandler dead'

    def start_response(self, status, response_headers, exc_info=None):
        """
        Method to be passed to WSGI application object to start the response.
        """
        if exc_info:
            try:
                raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None
        elif self.response_dict:
            raise WsgiAppError('start_response called a second time without exc_info!  See PEP 333.')

        #pprint(response_headers)

        for key,value in response_headers:
            if is_hop_by_hop(key):
                raise WsgiAppError('Hop by hop header specified')

        self.response_dict['headers'] = copy.copy(response_headers)
        self.response_dict['statuscode'] = status

        return self.write

    def write(self, body_data):
        """
        Write method to be passed to WSGI application object.  Used to write
        unbuffered output to the page.  You probably don't want to use this
        unless you have good reason to.
        """
        if self.response_dict and not self.write_called:
            self.response_dict['data'] = body_data
            #print '==RESPONSE DICTIONARY=='
            #pprint(self.response_dict)
            self.send(self.response_dict, 'outbox')
            self.write_called = True
        elif self.write_called:
            self.sendFragment(body_data)
        elif not self.response_dict and not self.write_called:
            raise WsgiError("write() called before start_response()!")
        else:
            raise WsgiError('Unkown error in write.')

    def _error(self, status=503, body_data=('', '', '')):
        """
        This is an internal method used to print an error to the browser and log
        it in the wsgi log.
        """
        if self.Debug:
            resource = {
                'statuscode' : status,
                'type' : 'text/html',
                'data' : cgitb.html(body_data),
            }
            self.send(resource, 'outbox')
        else:
            self.send(ErrorPages.getErrorPage(status, 'An internal error has occurred.'), 'outbox')

        self.log_writable.write(''.join(traceback.format_exception(body_data[0], body_data[1], body_data[2], '\n')))
        self.log_writable.flush()


    def waitForBody(self):
        """
        This internal method is used to make the WSGI Handler wait for the body
        of an HTTP request before proceeding.

        FIXME:  We should really begin executing the Application and pull the
        body as needed rather than pulling it all up front.
        """
        buffer = []     #Wait on the body to be sent to us
        not_done = True
        while not_done:
            while self.dataReady('control'):
                if isinstance(self.recv('control'), producerFinished):
                    not_done = False

            while self.dataReady('inbox'):
                buffer.append(self.recv('inbox').bodychunk)

            if not_done and not self.anyReady():
                self.pause()
        return ''.join(buffer)


    def sendFragment(self, fragment):
        """
        This is a pretty simple method.  It's used to send a fragment if an app
        yields a value beyond the first.
        """
        page = {
            'data' : fragment,
            }
        #print 'FRAGMENT'
        #pprint(page)
        self.send(page, 'outbox')

    def initRequiredVars(self, wsgi_config):
        """
        This method initializes all variables that are required to be present
        (including ones that could possibly be empty).
        """
        self.environ["REQUEST_METHOD"] = self.request["method"]

        # Server name published to the outside world
        self.environ["SERVER_NAME"] = self.server_name

        # Server port published to the outside world
        self.environ["SERVER_PORT"] =  self.server_port

        #Protocol to respond to
        self.environ["SERVER_PROTOCOL"] = "%s/%s" %(self.request['protocol'], self.request['version'])

        self.environ['SCRIPT_NAME'] = self.request['SCRIPT_NAME']
        path_info = self.request['PATH_INFO']
        qindex = path_info.find('?')
        if qindex != -1:
            self.environ['PATH_INFO'] = path_info[:qindex]
            self.environ['QUERY_STRING'] = path_info[(qindex+1):]
        else:
            self.environ['PATH_INFO'] = path_info
            self.environ['QUERY_STRING'] = ''

        #==================================
        #WSGI variables
        #==================================
        self.environ["wsgi.version"] = wsgi_config['wsgi_ver']
        self.environ["wsgi.url_scheme"] = self.request["protocol"].lower()
        self.environ["wsgi.errors"] = self.log_writable

        self.environ["wsgi.multithread"] = True
        self.environ["wsgi.multiprocess"] = False
        self.environ["wsgi.run_once"] = False

    def initOptVars(self, wsgi_config):
        """This method initializes all variables that are optional"""

        # Contents of an HTTP_CONTENT_TYPE field
        self.environ["CONTENT_TYPE"] = self.headers.get("content-type","")

        # Contents of an HTTP_CONTENT_LENGTH field
        self.environ["CONTENT_LENGTH"] = self.headers.get("content-length","")
        #self.environ["DOCUMENT_ROOT"] = self.homedirectory
        self.environ["SERVER_ADMIN"] = wsgi_config['server_admin']
        self.environ["SERVER_SOFTWARE"] = wsgi_config['server_software']
        self.environ["SERVER_SIGNATURE"] = "%s Server at %s port %s" % \
                    (wsgi_config['server_software'], self.server_name, self.server_port)
        self.environ['REMOTE_ADDR'] = self.request['peer']



class WsgiError(Exception):
    """
    This is used to indicate an internal error of some kind.  It is thrown if the
    write() callable is called without start_response being called.
    """
    pass

class WsgiAppError(Exception):
    """
    This is an exception that is used if a Wsgi application does something it shouldnt.
    """
    pass
