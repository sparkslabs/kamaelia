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
This is a WSGI app for serving Django apps simply.  Unfortunately, it doesn't do
that just yet and and won't work as you expect it.  Thus, it's not going to go in
the main Kamaelia tree just yet, but I'll leave it in the Kamaelia Publish distribution
for all the masochists out there.  :)
"""

import os, sys
from static import static_app

import django.core.handlers.wsgi

_paths_set = set([])

def application(environ = {}, start_response = None):
    if not environ['kp.project_path'] in _paths_set:
        _paths_set.add(environ['kp.project_path'])
        sys.path.append(environ['kp.project_path'])
        
    #django doesn't handle PATH_INFO or SCRIPT_NAME variables properly in the current version
    if environ.get('kp.django_path_handling', False):
        environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        
    #from pprint import pprint
    #pprint(environ)
    
    os.environ['DJANGO_SETTINGS_MODULE'] = environ['kp.django_settings_module']
    _application = django.core.handlers.wsgi.WSGIHandler()
    return _application(environ, start_response)
