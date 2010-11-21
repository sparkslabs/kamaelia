#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
"""This module includes various useful functions for setting a webserver up."""

import sys, logging, os
def processPyPath(ServerConfig):
    """Use ServerConfig to add to the python path."""
    if ServerConfig.get('pypath_append'):
        path_append = ServerConfig['pypath_append'].split(':')
        #expand all ~'s in the list
        path_append = [os.path.expanduser(path) for path in path_append]
        sys.path.extend(path_append)
    
    if ServerConfig.get('pypath_prepend'):
        path_prepend = ServerConfig['pypath_prepend'].split(':')
        path_prepend.reverse()
        for path in path_prepend:
            path = os.path.expanduser(path)
            sys.path.insert(0, path)
            
def normalizeUrlList(url_list):
    """Add necessary default entries that the user did not enter."""
    for dict in url_list:
        if not dict.get('kp.app_object'):
            dict['kp.app_object'] = 'application'
            
def normalizeWsgiVars(WsgiConfig):
    """Put WSGI config data in a state that the server expects."""
    WsgiConfig['wsgi_ver'] = tuple(WsgiConfig['wsgi_ver'].split('.'))
    
def initializeLogger(consolename='kamaelia'):
    """This sets up the logging system."""
    formatter = logging.Formatter('%(levelname)s/%(name)s: %(message)s')
    
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    consolelogger = logging.getLogger(consolename)
    consolelogger.setLevel(logging.DEBUG)
    consolelogger.addHandler(console)
    from Kamaelia.Apps.JMB.Common.Console import setConsoleName
    setConsoleName(consolename)
    
    from atexit import register
    register(killLoggers)

def killLoggers():
    """Shuts down the logging system and flushes input."""
    logging.shutdown()
