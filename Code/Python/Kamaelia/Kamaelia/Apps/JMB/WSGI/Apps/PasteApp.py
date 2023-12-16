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

raise NotImplementedError("Slated for removal since depends on Paste")

from paste.deploy import loadapp
import os

__app_objs__ = {}

def application(environ, start_response):
    if __app_objs__.get(environ['kp.paste_source']):
        app = __app_objs__[environ['kp.paste_source']]
    else:
        app = loadapp(environ['kp.paste_source'])
        
    return app(environ, start_response)
