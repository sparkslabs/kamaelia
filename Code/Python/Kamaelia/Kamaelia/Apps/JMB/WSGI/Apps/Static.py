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

Dependencies
---------------
This source file requires Static by Luke Arno.
"""

raise NotImplementedError("Slated for removal since depends on 'Static' ")

from support.la_static import Cling
import os

def static_app(environ, start_response):
    environ['kp.static_path'] = os.path.expanduser(environ['kp.static_path'])
    #from pprint import pprint
    #pprint(environ)
    return Cling(environ['kp.static_path'], index_file=environ['kp.index_file']) (environ, start_response)
