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
NOTE:  This is experimental software.  It has not been fully tested and will
probably break or behave in unexpected ways.

This is the WSGI handler for ServerCore.  It works by importing a module and
pulling out the relevant application object from it.  It will wait on the
HTTPParser to transmit the body in full before proceeding.  Thus, it is probably
not a good idea to use any WSGI apps requiring a lot of large file uploads.
"""

from pprint import pprint, pformat
import sys, os, re, cStringIO, cgitb, copy, traceback, gc, weakref
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
    def read(self, number=0):
        return ''
    def readlines(self, number=0):
        return[]
    def close(self):
        pass
    
_null_fl = NullFileLike()


class _WsgiHandler(threadedcomponent):
    """Choosing to run the WSGI app in a thread rather than the same
       context, this means we don't have to worry what they get up
       to really"""
    Inboxes = {
        'inbox' : 'Used to receive the body of requests from the HTTPParser',
        'control' : 'NOT USED',
    }
    Outboxes = {
        'outbox' : 'used to send page fragments',
        'signal' : 'send producerFinished messages',
        '_signal-lw' : 'shut down the log writable',
    }
    Debug = False
    def __init__(self, app, request, log_writable, WsgiConfig, **argd):
        super(_WsgiHandler, self).__init__(**argd)
        self.request = request
        self.environ = {}
        self.environ.update(request['custom'] )

        print 'request received for [%s]' % (self.request['raw-uri'])

        self.app = app
        self.log_writable = log_writable
        self.response_dict = {}
        self.wsgi_config = WsgiConfig
        self.write_called = False

    def main(self):
        #print 'Referrers to WsgiHandler:'
        #print '\n ', gc.get_referrers(self)
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


def WsgiHandler(log_writable, WsgiConfig, url_list):
    """
    This method checks the URI against a series of regexes from urls.py to determine which
    application object to route the request to, imports the file that contains the app object,
    and then extracts it to be passed to the newly created WSGI Handler.
    """
    class _getWsgiHandler(object):
        def __init__(self, log_writable, WsgiConfig, url_list):
            self.log_writable = log_writable
            self.WsgiConfig = WsgiConfig
            self.url_list = url_list
            self.app_objs = {}
            self.compiled_regexes = {}
            for dict in url_list:
                self.compiled_regexes[dict['kp.regex']] = re.compile(dict['kp.regex'])
        def __call__(self, request):
            matched_dict = False
            regexes = self.compiled_regexes
            urls = self.url_list
            split_uri = request['raw-uri'].split('/', 2)
            split_uri = [x for x in split_uri if x]  #remove any empty strings
            for url_item in urls:
                if regexes[url_item['kp.regex']].search(split_uri[0]):
                    request['SCRIPT_NAME'] = '/' + split_uri.pop(0)
                    request['PATH_INFO'] = '/' + '/'.join(split_uri) #This is cleaned up in _WsgiHandler.InitRequiredVars
                    matched_dict = url_item
                    break
    
            if not matched_dict:
                raise WsgiError('Page not found and no 404 pages enabled! Check your urls file.')
    
            if self.app_objs.get(matched_dict['kp.regex']):  #Have we found this app object before?
                app = self.app_objs[matched_dict['kp.regex']]    #If so, pull it out of app_objs
            else:                                       #otherwise, find the app object
                try:
                    module = _importWsgiModule(matched_dict['kp.import_path'])
                    app = getattr(module, matched_dict['kp.app_object'])
                    self.app_objs[matched_dict['kp.regex']] = app
                except ImportError: #FIXME:  We should probably display some kind of error page rather than dying
                    raise WsgiImportError("WSGI application file not found.  Please check your urls file.")
                except AttributeError:
                    raise WsgiImportError("Your WSGI application file was found, but the application object was not. Please check your urls file.")
            request['custom'] = matched_dict
            #dump_garbage()
            return _WsgiHandler(app, request, log_writable, WsgiConfig, Debug=True)
    return _getWsgiHandler(log_writable, WsgiConfig, url_list)

def dump_garbage():
    print '\nGARBAGE'
    gc.collect()
    print '\nGARBAGE OBJECTS:'
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80:s = s[:77]+'...'
        print type(x), '\n  ', s

class WsgiImportError(Exception):
    """
    This exception is to indicate that there was an error in importing a WSGI app.
    """
    pass

class WsgiError(Exception):
    """
    This is just a generic exception class.  As of right now, it is only thrown
    when write is called before start_response, so it's primarily an exception
    that is thrown when an application messes up, but that may change!
    """
    pass

class WsgiAppError(Exception):
    """
    This is an exception that is used if a Wsgi application does something it shouldnt.
    """
    pass

def _importWsgiModule(name):
    """
    Just a copy/paste of the example my_import function from here:
    http://docs.python.org/lib/built-in-funcs.html
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
