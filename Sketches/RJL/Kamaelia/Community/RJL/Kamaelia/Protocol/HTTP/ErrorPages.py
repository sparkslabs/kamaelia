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
"""\
========================
websiteErrorPage
========================
A simple HTTP request handler for HTTPServer.
websiteErrorPage generates basic HTML error pages for an HTTP server.
"""

from Axon.Component import component

def getErrorPage(errorcode, msg = ""):
    if errorcode == 400:
        return {
            "statuscode" : "400",
            "data"       : u"<html>\n<title>400 Bad Request</title>\n<body style='background-color: black; color: white;'>\n<h2>400 Bad Request</h2>\n<p>" + msg + "</p></body>\n</html>\n\n",
            "type"       : "text/html",
        }

    elif errorcode == 404:
        return {
            "statuscode" : "404",
            "data"       : u"<html>\n<title>404 Not Found</title>\n<body style='background-color: black; color: white;'>\n<h2>404 Not Found</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
            "type"       : "text/html"
        }

    elif errorcode == 500:
        return {
            "statuscode" : "500",
            "data"       : u"<html>\n<title>500 Internal Server Error</title>\n<body style='background-color: black; color: white;'>\n<h2>500 Internal Server Error</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
            "type"       : "text/html"
        }
        
    elif errorcode == 501:
        return {
            "statuscode" : "501",
            "data"       : u"<html>\n<title>501 Not Implemented</title>\n<body style='background-color: black; color: white;'>\n<h2>501 Not Implemented</h2>\n<p>" + msg + u"</p></body>\n</html>\n\n",
            "type"       : "text/html"
        }
        
    else:
        return {
            "statuscode" : str(errorcode),
            "data"       : u"",
            "type"       : "text/html"
        }
                 
class websiteErrorPage(component):
    def __init__(self, errorcode, msg = ""):
        super(websiteErrorPage, self).__init__()
        self.errorcode = errorcode
        self.msg = msg

    def main(self):
        resource = getErrorPage(self.errorcode, self.msg) # get the error page
        resource["incomplete"] = False # mark its data as being complete (i.e. no more chunks to come)
        self.send(resource, "outbox") # send it on to HTTPRequestHandler
        self.send(producerFinished(self), "signal") # and signal that this component has terminated

__kamaelia_components__  = ( websiteErrorPage, )
