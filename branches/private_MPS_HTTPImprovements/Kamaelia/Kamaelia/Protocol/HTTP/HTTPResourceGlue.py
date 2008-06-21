#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
