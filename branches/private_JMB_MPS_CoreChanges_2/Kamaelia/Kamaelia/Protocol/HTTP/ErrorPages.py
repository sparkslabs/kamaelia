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
        
class ErrorPageHandler(component):
    """
    This is the default error page handler.  It is essentially the above function
    getErrorPage mapped to a resource handler for the HTTPServer.
    """
    def __init__(self, statuscode, message):
        self.statuscode = statuscode
        self.message = message
        super(ErrorPageHandler, self).__init__()
    def main(self):
        self.send(getErrorPage(self.statuscode, self.message))
        yield 1
        self.send(producerFinished(self), 'signal')

