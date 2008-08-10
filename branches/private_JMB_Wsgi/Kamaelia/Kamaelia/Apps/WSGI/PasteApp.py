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
This is a wrapper around Paste Deploy's loadapp function.  It is useful if you would
rather use Paste Deploy's configuration file URL routing instead of the URL handling
built into Kamaelia.Experimental.Wsgi.Factory or if you would like to serve Pylons
apps.

Custom environ entries
-----------------------

This app requires the following custom environ variables:

* kp.paste_source:  A string to be passed to loadapp.  Is a URI for either a config
file or egg.  See http://pythonpaste.org/deploy/#basic-usage for more info.

Dependencies
-------------

This application requires Paste Deploy (obviously).
"""

from paste.deploy import loadapp
import os

__app_objs__ = {}

def application(environ, start_response):
    if __app_objs__.get(environ['kp.paste_source']):
        app = __app_objs__[environ['kp.paste_source']]
    else:
        app = loadapp(environ['kp.paste_source'])
        
    return app(environ, start_response)
