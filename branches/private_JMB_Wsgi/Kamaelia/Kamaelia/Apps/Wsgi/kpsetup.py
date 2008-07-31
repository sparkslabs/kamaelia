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
import sys
def processPyPath(ServerConfig):
    """Use the Server configuration data to actually configure the server."""
    print ServerConfig
    if ServerConfig.get('pypath_append'):
        path_append = ServerConfig['pypath_append'].split(':')
        sys.path.extend(path_append)
    
    if ServerConfig.get('pypath_prepend'):
        path_prepend = ServerConfig['pypath_prepend'].split(':')
        path_prepend.reverse()
        for path in path_prepend:
            sys.path.insert(0, path)
            
def normalizeUrlList(url_list):
    """Add necessary default entries that the user did not enter."""
    for dict in url_list:
        if not dict.get('kp.app_object'):
            dict['kp.app_object'] = 'application'
            
def normalizeWsgiVars(WsgiConfig):
    """Put WSGI config data in a state that the server expects."""
    WsgiConfig['wsgi_ver'] = tuple(WsgiConfig['wsgi_ver'].split('.'))
