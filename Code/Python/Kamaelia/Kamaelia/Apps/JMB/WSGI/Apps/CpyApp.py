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

raise NotImplementedError("Slated for removal since depends on CherryPy")

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
