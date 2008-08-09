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


####################################
#Translator stuff
####################################
def TranslatorFactory(hand, trans):    
    def _getHandler(request):
        request = trans(request)
        return hand(request)
    
    return _getHandler


def WSGILikeTranslator(request):
    """
    This function will translate the HTTPParser's syntax into a more WSGI-like syntax.
    Pass it to the HTTPProtocol factory function and requests will be sent to your
    resource handler with a subset of a WSGI environ dictionary.  You just need to
    supply more of the wsgi variables (like wsgi.input).
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

def PopURI(request, sn_key, pi_key, ru_key):
    if not request.get(sn_key):
        #print '%s not found' % (sn_key)
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

def checkSlashes(item='', sl_char='/'):
    if not item.startswith(sl_char):
        item = sl_char + item
    return item.rstrip('/')

def PopWsgiURI(request):
    return PopURI(request, 'SCRIPT_NAME', 'PATH_INFO', 'NON_QUERY_URI')

def PopKamaeliaURI(request):
    return PopURI(request, 'uri-prefix-trigger', 'uri-suffix', 'raw-uri')