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

import re

from WsgiHandler import _WsgiHandler
from Kamaelia.Protocol.HTTP import PopURI

def WsgiFactory(log_writable, WsgiConfig, url_list):
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

def SimpleWsgiFactory(log_writable, WsgiConfig, app_object, script_name='/'):
    """
    This is a simple factory function that is useful if you know at compile time
    that you will only support one application.
    """
    
    def _getWsgiHandler(request):
        print request
        split_uri = request['PATH_INFO'].split('/')
        split_uri = [x for x in split_uri if x] #remove any empty strings
        
        script_name_trim = script_name.strip('/')
        if script_name:
            if script_name_trim == split_uri[0] and script_name != '/':
                PopURI(request)
            elif script_name == '/':
                request['SCRIPT_NAME'] = ''
                request['PATH_INFO'] = '/'.join(split_uri)
            else:
                raise WsgiImportError('Script name error!')

        else:
            raise WsgiImportError("You must specify script_name to use SimpleWsgiFactory!")
        return _WsgiHandler(app_object, request, log_writable, WsgiConfig)
    
    return _getWsgiHandler

class WsgiImportError(Exception):
    """
    This exception is to indicate that there was an error in importing a WSGI app.
    """
    pass
