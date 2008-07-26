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

def WSGILikeTranslator(request):
    environ = {}
    print request
    
    environ['REQUEST_METHOD'] = request['method']
    environ['REQUEST_URI'] = request['raw-uri']
    environ['SCRIPT_NAME'] = request['uri-prefix-trigger']
    if not environ['SCRIPT_NAME'].startswith('/'):
        environ['SCRIPT_NAME'] = '/%s' % (environ['SCRIPT_NAME'])
    elif environ['SCRIPT_NAME'] == '/':
        environ['SCRIPT_NAME'] = ''
    environ['PATH_INFO'] = request['uri-suffix']
    if not environ['PATH_INFO'].startswith('/'):
        environ['PATH_INFO'] = '/%s' % (environ['PATH_INFO'])
    
    if request['raw-uri'].find('?') != -1:
        split_uri = request['raw-uri'].split('?')
        environ['QUERY_STRING'] = split_uri[1]
        q_index = environ['PATH_INFO'].find('?')
        if q_index != -1:
            environ['PATH_INFO'] = environ['PATH_INFO'][:q_index]
    else:
        environ['QUERY_STRING'] = ''
    
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
    
    environ['wsgi.url_scheme'] = request['uri-protocol']
    
    ConvertHeaders(request, environ)
    
    return environ
    
    
def ConvertHeaders(request, environ):
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
