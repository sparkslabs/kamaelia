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
