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
This is a simple WSGI way of serving static content.  If you use it with Kamaelia's
WSGI handler, it runs in its own thread so there's no need to worry about non-blocking
IO!

This is really just a wrapper around Static Cling by Luke Arno that will expand
the user directory (ex:  ~/foo will be expanded into /home/jason/foo)

This application requires the following custom environ entries:

* kp.static_path:  The path to pull static data from.  For example if http://foo.com/static/index.html
would pull the file ~/www/index.html if kp.static_path is ~/www
* kp.index_file:  The file to open if no file is specified.  For example, http://foo.com/static
would translate into http://foo.com/static/index.html if kp.index_file is 'index.html'.
"""

from support.la_static import Cling
import os

def static_app(environ, start_response):
    environ['kp.static_path'] = os.path.expanduser(environ['kp.static_path'])
    #from pprint import pprint
    #pprint(environ)
    return Cling(environ['kp.static_path'], index_file=environ['kp.index_file']) (environ, start_response)
