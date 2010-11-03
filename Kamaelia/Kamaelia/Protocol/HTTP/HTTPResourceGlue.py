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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
HTTP Resource Glue 

What does it do?
====================
It picks the appropriate resource handler for a request using any of the
request's attributes (e.g. uri, accepted encoding, language, source etc.)

Its basic setup is to match prefixes of the request URI each of which have
their own predetermined request handler class (a component class).

HTTPResourceGlue also creates an instance of the handler component,
allowing complete control over its __init__ parameters.
Feel free to write your own for your webserver configuration.
"""

# import the modules that you want for your website
import types

from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal
from Kamaelia.Protocol.HTTP.Handlers.SessionExample import SessionExampleWrapper
from Kamaelia.Protocol.HTTP.Handlers.UploadTorrents import UploadTorrentsWrapper

import Kamaelia.Protocol.HTTP.ErrorPages

# then define what paths should trigger those modules, in order of priority
# i.e. put more specific URL handlers first
URLHandlers = [
    ["/session/"               , SessionExampleWrapper],
    ["/torrentupload"          , UploadTorrentsWrapper],
    ["/"                       , lambda r : Minimal(request=r, homedirectory="htdocs/", indexfilename="index.html")],

    # "/" should always be last as it catches all
]
# the second item should be a component class that takes one parameter (the request)
# OR some other function that takes one parameter returns a component instance


# this function decides what function should deal with a request
def createRequestHandler(request):
    if request.get("bad"):
        return ErrorPages.websiteErrorPage(400, request.get("errormsg",""))
    else:
        for (prefix, handler) in URLHandlers:
            if request["raw-uri"][:len(prefix)] == prefix:
                request["uri-prefix-trigger"] = prefix
                request["uri-suffix"] = request["raw-uri"][len(prefix):]
                return handler(request)

    return ErrorPages.websiteErrorPage(404, "No resource handlers could be found for the requested URL.")
