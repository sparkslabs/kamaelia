#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

"""Helper classes and components for HTTP"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class HTTPMakePostRequest(component):
    """\
    HTTPMakePostRequest is used to turn messages into HTTP POST requests
    for SimpleHTTPClient.
    """
    def __init__(self, uploadurl):
        super(HTTPMakePostRequest, self).__init__()
        self.uploadurl = uploadurl
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                msg = { "url" : self.uploadurl, "postbody" : msg }
                self.send(msg, "outbox")
            
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return

            self.pause()

if __name__ == "__main__":
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    
    postscript = raw_input("Post Script URL: ") # e.g. "http://www.example.com/upload.php"
    
    pipeline(
        ConsoleReader(eol=""),
        HTTPMakePostRequest(postscript),
        SimpleHTTPClient()
    ).run()
