# Needed to allow import
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
This module contains a factory function for 
"""
import types
from itertools import izip
from HTTPServer import HTTPServer, MapStatusCodeToText

def HTTPProtocol(routing):
    """
    This is a convenience method that you should probably use when creating a
    server rather than creating an HTTPServer directly.
    """
    def _getHttpServer(**argd):
        return HTTPServer(requestHandlers(routing), **argd)
    return _getHttpServer

if __name__ == '__main__':
   request = {
       'raw-uri' : '/foo/bar/foobar',
       'SCRIPT_NAME' : 'foo',
       'PATH_INFO' : 'bar/foobar'
   }
   PopUri(request)
   print request