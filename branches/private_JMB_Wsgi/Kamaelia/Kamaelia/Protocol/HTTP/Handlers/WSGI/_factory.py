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
This module is what you use to create a WSGI Handler.  
"""

import re

from _WSGIHandler import _WsgiHandler
from Kamaelia.Support.Protocol.HTTP import ReqTranslatorFactory, WSGILikeTranslator, \
    PopWsgiURI
import logging

_loggerInitialized = False

def WSGIFactory(WSGIConfig, url_list, errorlog='error.log', 
                    logger_name='kamaelia.wsgi.application', errorhandler=None):
    """
    Creates a WSGI Handler using url routing.

      WSGIConfig - A WSGIConfig object
      url_list - A URL list to look up App objects.  It must contain three keys:
          kp.regex - the regex to match the uri against (will only match the first
            section)
          kp.import_path - The path to import the WSGI application object from
          kp.app_object - the attribute of the module named in kp.import_path that
            names the WSGI application object
      error_log - The file to store errors in
      logger_name - The name of the python logger to log errors to
    """
    class _getWsgiHandler(object):
        def __init__(self,WSGIConfig, url_list, translator=WSGILikeTranslator):
            self.WsgiConfig = WSGIConfig
            self.url_list = url_list
            self.app_objs = {}
            self.compiled_regexes = {}
            self.translator = translator
            self.errorhandler = errorhandler
            if not self.errorhandler:
                from Kamaelia.Protocol.HTTP.ErrorPages import ErrorPageHandler
                self.errorhandler = ErrorPageHandler
            for dictionary in url_list:
                self.compiled_regexes[dictionary['kp.regex']] = re.compile(dictionary['kp.regex'])
            _initializeLoggers(errorlog, logger_name)            
        def __call__(self, request):
            matched_dict = False
            regexes = self.compiled_regexes
            urls = self.url_list
            
            request = self.translator(request)
            
            split_uri = request['PATH_INFO'].split('/', 2)
            split_uri = [x for x in split_uri if x]  #remove any empty strings
            
            #Potential FIXME:  If split_uri is empty, we set the fist item to something
            #that wouldn't be in the url.  It feels like a hack, but seems to work.
            #Could this be a potential security risk or source of a bug?
            if not split_uri:
                split_uri = ['||||']
            
            for url_item in urls:
                if regexes[url_item['kp.regex']].search(split_uri[0]):
                    PopWsgiURI(request)
                    matched_dict = url_item
                    break
    
            if not matched_dict:
                return self.errorhandler(500, 'Page not found and no 404 handler configured')
    
            if self.app_objs.get(matched_dict['kp.regex']):  #Have we found this app object before?
                app = self.app_objs[matched_dict['kp.regex']]    #If so, pull it out of app_objs
            else:                                       #otherwise, find the app object
                try:
                    module = _importWsgiModule(matched_dict['kp.import_path'])
                    app = getattr(module, matched_dict['kp.app_object'])
                    self.app_objs[matched_dict['kp.regex']] = app
                except ImportError: #FIXME:  We should probably display some kind of error page rather than dying
                    return self.errorhandler(404, 'Module not found.')
                except AttributeError:
                    return self.errorhandler(404, 'Page found, but app object missing.')
            request.update(matched_dict)
            if matched_dict.get('kp.nounicode'):
                #Convert all elements in the request to strings
                request = dict([(str(k), str(v)) for k, v in request.iteritems()])
            return _WsgiHandler(app, request, WSGIConfig, Debug=True)
    return _getWsgiHandler(WSGIConfig, url_list)

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

def SimpleWSGIFactory(WSGIConfig, app_object, errorlog='error.log',
                        logger_name='kamaelia.wsgi.apps', errorhandler=None):
    """
    Creates a WSGI Handler that can handle only one WSGI Application.

      WSGIConfig - A WSGIConfig object
      app_object - The WSGI application object to run
      error_log - The file to store errors in
      logger_name - The name of the python logger to log errors to
    """
    _initializeLoggers(errorlog, logger_name)
    def _getWsgiHandler(request):
        request = WSGILikeTranslator(request)
        return _WsgiHandler(app_object, request, WSGIConfig)
    
    return _getWsgiHandler
    
def _initializeLoggers(errorlog, logger_name):
    global _loggerInitialized
    if not _loggerInitialized:
        _loggerInitialized = True
        logger = logging.getLogger(logger_name)
        handler = logging.FileHandler(errorlog)
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)

class WSGIImportError(Exception):
    """
    This exception is to indicate that there was an error in importing a WSGI app.
    """
    pass
