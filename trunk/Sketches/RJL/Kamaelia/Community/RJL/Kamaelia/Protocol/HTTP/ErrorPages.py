#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
