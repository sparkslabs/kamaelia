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
