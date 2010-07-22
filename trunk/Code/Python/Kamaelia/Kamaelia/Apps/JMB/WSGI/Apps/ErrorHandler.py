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
This is an error serving application.  It currently only supports serving 404
pages, but may be adapted to serve other kinds of error pages.

This app requires no custom environment variables or dependencies.
"""


from Kamaelia.Protocol.HTTP import ErrorPages
from Kamaelia.Protocol.HTTP.HTTPServer import MapStatusCodeToText

def application(environ, start_response):
    """
    This is just a plain old error page serving application.
    """
    error = 404

    status = MapStatusCodeToText[str(error)]
    response_headers = [('Content-type', 'text/html')]

    start_response(status, response_headers)

    requested_path = environ['SCRIPT_NAME'] + environ['PATH_INFO']

    ErrorPage = ErrorPages.getErrorPage(error, '%s not found.' % (requested_path))['data']
    yield ErrorPage
