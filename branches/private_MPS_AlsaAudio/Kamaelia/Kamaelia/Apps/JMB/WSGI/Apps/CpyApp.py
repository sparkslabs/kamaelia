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
This is a simple application for serving CherryPy applications.  It requires an import
path for the CherryPy module and the root attribute of it.

Custom environ entries
-----------------------

This module requires the following custom environ entries:
* kp.cpy_import_path:  The python import path for the CherryPy module you wish to run
ex:  'Package.Subpackage.CpyModule'
* kp.cpy_root_attribute: The name of the root attribute of the CherryPy app.

Dependencies
-------------

This app requires CherryPy version 3.1.
"""

import cherrypy

def application(environ, start_response):
    mod = importModule(environ['kp.cpy_import_path'])
    root = getattr(mod, environ['kp.cpy_root_attribute'])
    
    from pprint import pprint
    pprint(environ)
    
    return cherrypy.tree.mount(root(), environ['kp.cpy_http_path'])(environ, start_response)

def importModule(name):
    """
    Just a copy/paste of the example my_import function from here:
    http://docs.python.org/lib/built-in-funcs.html
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
