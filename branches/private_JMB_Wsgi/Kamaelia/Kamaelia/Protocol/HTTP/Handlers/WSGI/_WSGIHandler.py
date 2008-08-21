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
"""
WSGI Handler
=============

NOTE:  This is experimental software.

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

WsgiConfig = {
    'wsgi_ver' : (1, 0),
    'server_admin' : 'Jason Baker',
    'server_software' : 'Kamaelia Publish'
}

url_list = [ #Note that this is a list of dictionaries.  Order is important.
    {
        'kp.regex' : 'simple',
        'kp.import_path' : 'Kamaelia.Apps.Wsgi.Apps.Simple',
        'kp.app_obj' : 'simple_app',
    }
    {
        'kp.regex' : '.*',  #The .* means that this is a 404 handler
        'kp.import_path' : 'Kamaelia.Apps.Wsgi.Apps.ErrorHandler',
        'kp.app_obj' : 'application',
    }
]

routing = [['/', WsgiFactory(WsgiConfig, url_list)]]

ServerCore(
    protocol=HTTPProtocol(routing),
    port=8080,
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)).run()

------------------
Internal overview
------------------

request object
~~~~~~~~~~~~~~~

Note that certain WSGI applications will require configuration
data from the urls file.  If you use the WsgiFactory to run this
handler, all options specified in the urls file will be put into
the environment variable with a kp. in front of them.  

For example, the 'regex' entry in a urls file would go into the
environ dictionary like this if it was set to 'simple':

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

FIXME:  It would be nice if the WsgiConfig were made into an object rather than a
dictionary.
"""

from pprint import pprint, pformat
import sys, os, cStringIO, cgitb, traceback, logging, copy
from datetime import datetime
from wsgiref.util import is_hop_by_hop
import Axon
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished
import Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages
from xml.sax.saxutils import unescape
        
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
    
class ErrorLogger(object):
    """This is the file-like object intended to be used for wsgi.errors."""
    def __init__(self, logger):
        self.logger = logger
    def write(self, data):
        self.logger.error(data)
    def writelines(self, seq):
        data = '\n'.join(seq)
        self.logger.error(data)
    def flush(self):
        pass
    
_null_fl = NullFileLike()

class _WsgiHandler(threadedcomponent):
    """
    This is a WSGI handler that is used to serve WSGI applications.  Typically,
    URL routing is to be done in the factory method that creates this.  Thus,
    the handler must be passed the application object.  You probably don't need
    to instantiate this class directly.
    
    It will respond to the following signals:
    
     producerFinished - This is used by the HTTPServer to indicate that the full
     body has been transmitted.  This will not shut down this component, and in
     fact will make it BEGIN processing the request.  If the request is not a
     POST or PUT request, the Handler will ignore this signal.
     
    Any other signals that this component may receive may result in undefined
    behavior, but this component will most likely ignore them.
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
    def __init__(self, app, request, WsgiConfig, **argd):
        """
        app - The WSGI application to run
        request - the request object that is generated by HTTPParser
        log_writable - a LogWritable object to be passed as a wsgi.errors object.
        WsgiConfig - General configuration about the WSGI server.
        """
        super(_WsgiHandler, self).__init__(**argd)
        self.environ = request

        batch_str = self.environ.get('batch', '')
        if batch_str:
            batch_str = 'batch ' + batch_str
            print 'request received for [%s] %s' % \
               (self.environ['REQUEST_URI'], batch_str)

        self.app = app
        self.response_dict = {}
        self.wsgi_config = WsgiConfig
        self.write_called = False
        self.pf_received = False #Have we received a producerFinished signal?
        self.logger = logging.getLogger('kp')
        self.log = ErrorLogger(self.logger)

    def main(self):
        if self.environ['REQUEST_METHOD'] == 'POST' or self.environ['REQUEST_METHOD'] == 'PUT':
            try:
                body = self.waitForBody()
            except:
                self._error(503, sys.exc_info())
                self.send(producerFinished(self), 'signal')
                return
            self.memfile = cStringIO.StringIO(body)
        else:
            self.memfile = _null_fl

        self.initWSGIVars(self.wsgi_config)

        #pprint(self.environ)

        not_done = True
        try:
            #PEP 333 specifies that we're not supposed to buffer output here,
            #so pulling the iterator out of the app object
            app_return = self.app(self.environ, self.start_response)
            if isinstance(app_return, (list)):
                response = app_return.pop(0)
                self.write(response)
                [self.sendFragment(x) for x in app_return]

            else:
                app_iter = iter(app_return)
                response = app_iter.next()#  License:  LGPL
                while not response:
                    response = app_iter.next()
                self.write(response)
                [self.sendFragment(x) for x in app_iter if x]
                app_iter.close()
                if hasattr(app_iter, 'close'):
                    app_iter.close()
        except:
            self._error(503, sys.exc_info()) #Catch any errors and log them and print
                                             #either an error message or a stack
                                             #trace (depending if debug is set)

        self.memfile.close()
        
        #The Kamaelia Publish Peer depends on the producerFinished signal being sent
        #AFTER this handler has received a producerFinished signal.  Thus, we wait
        #until we get a signal before finishing up.
        if not self.pf_received:
            while not self.dataReady('control'):
                self.pause()
        self.send(Axon.Ipc.producerFinished(self), "signal")

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
        #Will be caught by _error    
            raise WsgiAppError('start_response called a second time without exc_info!  See PEP 333.')

        #PEP 333 requires that an application NOT send any hop-by-hop headers.
        #Therefore, we check for any of them in the headers the application
        #returns.  If so, an exception is raised to be caught by _error.
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
            self.send(self.response_dict, 'outbox')
            self.write_called = True
        elif self.write_called:
            self.sendFragment(body_data)
        #the following errors will be caught and sent to _error
        elif not self.response_dict and not self.write_called:
            raise WsgiError("write() called before start_response()!")
        else:
            raise WsgiError('Unkown error in write.')

    def _error(self, status=500, body_data=('', '', '')):
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

        self.log.write(''.join(traceback.format_exception(body_data[0], body_data[1], body_data[2], '\n')))


    def waitForBody(self):
        """
        This internal method is used to make the WSGI Handler wait for the body
        of an HTTP request before proceeding.

        FIXME:  We should really begin executing the Application and pull the
        body as needed rather than pulling it all up front.
        """
        buffer = []
        not_done = True
        while not_done:
            for msg in self.Inbox('control'):
                #print msg
                if isinstance(msg, producerFinished):
                    not_done = False
                    self.pf_received = True

            for msg in self.Inbox('inbox'):
                if isinstance(msg, str):
                    text = msg
                elif isinstance(msg, dict):
                    text = msg.get('body', '')
                    text = unescape(text)
                else:
                    text = ''
                if not isinstance(text, str):
                    text = str(text)
                    
                buffer.append(text)
                
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

    def initWSGIVars(self, wsgi_config):
        """
        This method initializes all variables that are required to be present
        (including ones that could possibly be empty).
        """
        #==================================
        #WSGI variables
        #==================================
        self.environ["wsgi.version"] = wsgi_config['wsgi_ver']
        self.environ["wsgi.errors"] = self.log
        self.environ['wsgi.input'] = self.memfile

        self.environ["wsgi.multithread"] = True
        self.environ["wsgi.multiprocess"] = False
        self.environ["wsgi.run_once"] = False



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
