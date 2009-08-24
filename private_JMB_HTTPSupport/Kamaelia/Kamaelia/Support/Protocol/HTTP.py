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
"""\
HTTP Server Utility Functions
=============================

This is a module of utility functions to be used with an HTTP server component
such as Kamaelia.Protocol.HTTP.HTTPServer.HTTPServer



Request Translators
--------------------

Sometimes it is helpful to have the parsed HTTP request come in a different format.
With a request translator, you may have the format of a parsed HTTP request changed
before it gets to your handler.  You may use the function ReqTranslatorFactory to
create a factory function that will create your handler using the request translator
you specify automatically.



ReqTranslatorFactory
~~~~~~~~~~~~~~~~~~~~~~

This function will make a factory that can create handlers for the HTTP Server
If this is used, the requests coming in to that handler will be formatted using
the given translator:
  
- hand  -- a factory function that returns a handler to be used by the HTTP Server
- trans -- a function that takes a request and returns a translated dictionary to be used by the handler.
  
  
  
WSGILikeTranslator
~~~~~~~~~~~~~~~~~~~~~~~

This function will translate the HTTPParser's syntax into a more WSGI-like syntax.
Pass it to the HTTPProtocol factory function and requests will be sent to your
resource handler with a subset of a WSGI environ dictionary.  You just need to
supply more of the wsgi variables (like wsgi.input).

  request - the request to be translated
  
This function will return the translated dictionary.



ConvertHeaders
~~~~~~~~~~~~~~

Converts environ variables to strings for wsgi compliance.  Also puts the 
request headers into CGI variables:

- request  -- The request as formatted by the HTTP Server
- environ  -- the WSGI environ dict to contain the converted headers


  
Popping request dictionaries
----------------------------

A fairly common practice in dealing with HTTP dictionaries is to "pop" a URI.
That is to say, to move one level down in the webserver's "Filesystem."  The main
function for doing this is PopURI, which requires you to manually specify the keys
to use from the dictionary.  Also provided are PopKamaeliaURI and PopWsgiURI.



PopKamaeliaURI
~~~~~~~~~~~~~~

This is a function to pop a level from the PATH_INFO key into the SCRIPT_NAME
key of a WSGI-like dictionary:

- request -- a WSGI-like dictionary


  
PopWsgiURI
~~~~~~~~~~

This is a function to pop a level from the uri-suffix into the uri-prefix-trigger
key of a request dictionary.

- request  -- a request dictionary



HTTP Protocol
-------------

These functions are included to simplify using the HTTPServer.  Instead of instantiating
an HTTPServer directly, you may wish to use the included HTTPProtocol factory function
if you are using the HTTPServer with ServerCore.  You may also use the requestHandlers
function to generate a createRequestHandler function to pass to the HTTPServer.

To use HTTPProtocol with ServerCore, use the following::

    from Kamaelia.Support.Protocol.HTTP import HTTPProtocol
    from Kamaelia.Chassis.ConnectedServer import ServerCore
    from Kamaelia.Protocol.Handlers.Minimal import MinimalFactory

    routing = [['/', MinimalFactory('index.html', 'htdocs')]]
    ServerCore(
        protocol=HTTPProtocol(routing),
        port = 8080,
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)).run()


    
HTTPProtocol
~~~~~~~~~~~~

This function will generate an HTTP Server that may be used with ServerCore.

- routing  -- An iterable of iterables.  Each item in the main iterabe may be thought
  of as an entry in the HTTPServer's "routing table."  An entry's syntax is roughly
  as follows::

      [
          ...
          [<URI prefix>, <Handler factory>]
          ...
      ]
      
  See above for example syntax.
    
- errorPages - A component to create in the event of an error.  That component's
  __init__ function must accept two arguments:  the error code (as an integer)
  and a message to be displayed (although it can ignore these if it so chooses)
 
 
    
requestHandlers
~~~~~~~~~~~~~~~

This function will generate a createRequestHandlers function for use with HTTPServer

- routing  -- An iterable of iterables formatted the same as HTTPProtocol.
- errorPages  -- A component to create in the event of an error.  That component's
  __init__ function must accept two arguments:  the error code (as an integer)
  and a message to be displayed (although it can ignore these if it so chooses)



Misc
----

These are various other functions:

CheckSlashes
~~~~~~~~~~~~

This function will make sure that a URI begins with a slash and does not end
with a slash:

- item  -- the uri to be checked
- sl_char  -- the character to be considered a 'slash' for the purposes of this function
"""

from Kamaelia.Protocol.HTTP.HTTPServer import HTTPServer

####################################
#Translator stuff
####################################
def ReqTranslatorFactory(hand, trans):
    """\
    This function will make a factory that can create handlers for the HTTP Server
    If this is used, the requests coming in to that handler will be formatted using
    the given translator.
      
    - hand  -- a factory function that returns a handler to be used by the HTTP Server
    - trans  -- a function that takes a request and returns a translated dictionary to be used by the handler.
    """
    def _getHandler(request):
        request = trans(request)
        return hand(request)
    
    return _getHandler


def WSGILikeTranslator(request):
    """\
    This function will translate the HTTPParser's syntax into a more WSGI-like syntax.
    Pass it to the HTTPProtocol factory function and requests will be sent to your
    resource handler with a subset of a WSGI environ dictionary.  You just need to
    supply more of the wsgi variables (like wsgi.input).
    
    - request  -- the request to be translated
      
    This function will return the translated dictionary.
    """
    environ = {}
    #print request
    
    environ['REQUEST_METHOD'] = request['method']
    environ['REQUEST_URI'] = request['raw-uri']
    environ['SCRIPT_NAME'] = request['uri-prefix-trigger']
    if not environ['SCRIPT_NAME'].startswith('/'):
        environ['SCRIPT_NAME'] = '/%s' % (environ['SCRIPT_NAME'])
    elif environ['SCRIPT_NAME'] == '/':
        environ['SCRIPT_NAME'] = ''
    environ['PATH_INFO'] = request['uri-suffix']
    if not environ['PATH_INFO'].startswith('/') and environ['PATH_INFO']:
        environ['PATH_INFO'] = '/%s' % (environ['PATH_INFO'])
    
    question_mark_index = request['raw-uri'].find('?')
    if question_mark_index != -1:
        split_uri = request['raw-uri'].split('?')
        environ['QUERY_STRING'] = split_uri[1]
        pq_index = environ['PATH_INFO'].find('?')
        if pq_index != -1:
            environ['PATH_INFO'] = environ['PATH_INFO'][:pq_index]
        environ['NON_QUERY_URI'] = request['raw-uri'][:question_mark_index]
    else:
        environ['QUERY_STRING'] = ''
        environ['NON_QUERY_URI'] = environ['REQUEST_URI']
    
    environ['CONTENT_TYPE'] = request['headers'].get('content-type', '')
    environ['CONTENT_LENGTH'] = request['headers'].get('content-length', '')
    
    split_server = request['uri-server'].split(':')
    if len(split_server)  > 1:
        environ['SERVER_NAME'] = split_server[0]
        environ['SERVER_PORT'] = split_server[1]
    else:
        environ['SERVER_NAME'] = split_server[0]
        environ['SERVER_PORT'] = ''
    
    environ['SERVER_PROTOCOL'] = '%s/%s' % (request['protocol'], request['version'])
    environ['SERVER_SOFTWARE'] = 'Kamaelia HTTPServer/0.6.0'
    
    environ['REMOTE_ADDR'] = request['peer']
    environ['REMOTE_PORT'] = request['peerport']
    
    environ['wsgi.url_scheme'] = request['uri-protocol'].lower()
    
    ConvertHeaders(request, environ)
    
    return environ
    
    
def ConvertHeaders(request, environ):
    """\
    Converts environ variables to strings for wsgi compliance.  Also puts the 
    request headers into CGI variables.
    
    - request  -- The request as formatted by the HTTP Server
    - environ  -- the WSGI environ dict to contain the converted headers
    """
    for header in request["headers"]:
        cgi_varname = "HTTP_"+header.replace("-","_").upper()
        environ[cgi_varname] = request["headers"][header]

    if environ.get('HTTP_CONTENT_TYPE'):
        del environ['HTTP_CONTENT_TYPE']
    if environ.get('HTTP_CONTENT_LENGTH'):
        del environ['HTTP_CONTENT_LENGTH']

####################################
#URI manipulations
####################################
def PopURI(request, sn_key, pi_key, ru_key):
    """\
    This function is used to pop a directory from the PATH_INFO key to the SCRIPT_NAME
    key (named by pi_key and sn_key respectively).  This is logically equivalent
    to moving down a level in the webserver's 'file system.'
    
    You may also use the convenience functions PopWsgiURI (if the dictionary is
    formatted as a WSGI environ dict) and PopKamaeliaURI (if the dictionary is
    formatted as created by the HTTP Server)
    
    - request -- the dictionary containing the keys to be manipulated
    - sn_key  -- the key that the SCRIPT_NAME is referenced by in request
    - pi_key  -- the key that the PATH_INFO is referenced by in request
    - ru_key  -- the key that represents the full URI (without a query string)
    """
    if not request.get(sn_key):
        split_uri = request[ru_key].split('/')
        split_uri = [x for x in split_uri if x]
        if split_uri:
            request[sn_key] = '/' + split_uri.pop(0)
            request[pi_key] = '/'.join(split_uri)
            if request[pi_key]:
                request[pi_key] = '/' + request[pi_key]
        else:   #The request must have been for root
            request[sn_key] = '/'
            request[pi_key] = ''
    else:
        sn_split = request[sn_key].split('/')
        pi_split = request[pi_key].split('/')
        pi_split = [x for x in pi_split if x]
        sn_split.append(pi_split.pop(0))
        request[sn_key] = '/'.join(sn_split)
        request[sn_key] = checkSlashes(request[sn_key])
        if request[pi_key]:
            request[pi_key] = '/'+('/'.join(pi_split))
        else:
            request[pi_key] = ''
        request[pi_key] = checkSlashes(request[pi_key])

def PopWsgiURI(request):
    """\
    This is a function to pop a level from the PATH_INFO key into the SCRIPT_NAME
    key of a WSGI-like dictionary.
    
    - request  -- a WSGI-like dictionary
    """
    return PopURI(request, 'SCRIPT_NAME', 'PATH_INFO', 'NON_QUERY_URI')

def PopKamaeliaURI(request):
    """\
    This is a function to pop a level from the uri-suffix into the uri-prefix-trigger
    key of a request dictionary.
    
    - request  -- a request dictionary
    """
    return PopURI(request, 'uri-prefix-trigger', 'uri-suffix', 'non-query-uri')

def checkSlashes(item='', sl_char='/'):
    """\
    This function will make sure that a URI begins with a slash and does not end
    with a slash.

    - item  -- the uri to be checked
    - sl_char  -- the character to be considered a 'slash' for the purposes of this function
    """
    if not item.startswith(sl_char):
        item = sl_char + item
    return item.rstrip('/')

####################################
#Factory functions
####################################
def HTTPProtocol(routing, errorhandler=None):
    """\
    This function will generate an HTTP Server that may be used with ServerCore.

    - routing  -- An iterable of iterables
    - errorPages  -- A component to create in the event of an error
    
    Each sub iterable in the routing argument may be thought of as an entry in
    the HTTPServer's "routing table."  An entry's syntax is roughly as follows::
    
      [
          ...
          [<URI prefix>, <Handler factory>]
          ...
      ]

    That component's __init__ function must accept two arguments: the error code
    (as an integer) and a message to be displayed (although it can ignore these
    if it so chooses)
    """
    def _getHttpServer(**argd):
        return HTTPServer(requestHandlers(routing, errorhandler), **argd)
    return _getHttpServer
    
def requestHandlers(routing, errorhandler=None):
    """\
    This function will generate a createRequestHandlers function for use with HTTPServer

    - routing  -- An iterable of iterables
    - errorPages  -- A component to create in the event of an error
    
    Each sub iterable in the routing argument may be thought of as an entry in
    the HTTPServer's "routing table."  An entry's syntax is roughly as follows::
    
      [
          ...
          [<URI prefix>, <Handler factory>]
          ...
      ]

    That component's __init__ function must accept two arguments: the error code
    (as an integer) and a message to be displayed (although it can ignore these
    if it so chooses)
    """
    if errorhandler is None:
        from Kamaelia.Protocol.HTTP.ErrorPages import ErrorPageHandler
        errorhandler = ErrorPageHandler
    def createRequestHandler(request):
        if request.get("bad"):
            return errorhandler(400, request.get("errormsg",""))
        else:
            for (prefix, handler) in routing:
                if request["non-query-uri"][:len(prefix)] == prefix:
                    request['uri-prefix-trigger'] = prefix
                    request['uri-suffix'] = request["non-query-uri"][len(prefix):]
                    return handler(request)

        return errorhandler(404, 'No resource handler found for URI %s' 
                            % (request['raw-uri']))

    return createRequestHandler


