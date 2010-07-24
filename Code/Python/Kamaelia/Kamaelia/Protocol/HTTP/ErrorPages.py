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
"""
This page contains the default HTTP Error handling.  There are two ways to call
this code:  either use getErrorPage to get the dictionary containing the error
directly or by using an ErrorPageHandler to send the page out.
"""
from Axon.Ipc import producerFinished
from Axon.Component import component

def getErrorPage(errorcode, msg = ""):
    """\
    Get the HTML associated with an (integer) error code.
    """

    if errorcode == 400:
        return {
            "statuscode" : "400",
            "data"       : u"<html>\n<title>400 Bad Request</title>\n<body style='background-color: black; color: white;'>\n<h2>400 Bad Request</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
            "content-type"       : "text/html",
        }

    elif errorcode == 404:
        return {
            "statuscode" : "404",
            "data"       : u"<html>\n<title>404 Not Found</title>\n<body style='background-color: black; color: white;'>\n<h2>404 Not Found</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
            "content-type"       : "text/html"
        }

    elif errorcode == 500:
        return {
            "statuscode" : "500",
            "data"       : u"<html>\n<title>500 Internal Server Error</title>\n<body style='background-color: black; color: white;'>\n<h2>500 Internal Server Error</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
            "content-type"       : "text/html"
        }

    elif errorcode == 501:
        return {
            "statuscode" : "501",
            "data"       : u"<html>\n<title>501 Not Implemented</title>\n<body style='background-color: black; color: white;'>\n<h2>501 Not Implemented</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
            "content-type"       : "text/html"
        }
    
    elif errorcode == 502:
        return {
            "statuscode" : 502,
            "data" : u"<html>\n<title>502 Bad Gateway</title>\n<body style='background-color: black; color: white;'>\n<h2>502 Bad Gateway</h2>\n<p>%s</p></body>\n</html>\n\n" \
                                                                                     % (msg),
            "content-type" : "text/html"
        }

    else:
        return {
            "statuscode" : str(errorcode),
            "data"       : u"",
            "content-type"       : "text/html"
        }

from Kamaelia.Util.OneShot import OneShot

def ErrorPageHandler(statuscode, message):
    """
    This is the default error page handler.  It is essentially the above function
    getErrorPage mapped to a resource handler for the HTTPServer.
    """
    return OneShot( getErrorPage(statuscode, message)  )
    
__kamaelia_prefabs__  = ( ErrorPageHandler, )
