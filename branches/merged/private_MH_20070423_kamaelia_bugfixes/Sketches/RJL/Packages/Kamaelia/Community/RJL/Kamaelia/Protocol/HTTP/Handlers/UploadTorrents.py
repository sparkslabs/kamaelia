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
"""\
========================
Upload Torrents
========================
A session-based HTTP request handler for HTTPServer.
UploadTorrents saves .torrent files that are uploaded to it as POST
data and stores the number of .torrent files save to a file "meta.txt".
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

import Kamaelia.Community.RJL.Kamaelia.Protocol.HTTP.ErrorPages

Sessions = {}

def UploadTorrentsWrapper(request):
    """Returns an UploadTorrents component, manages that components lifetime and access."""
    
    sessionid = request["uri-suffix"]
    if Sessions.has_key(sessionid):
        session = Sessions[sessionid]
        if session["busy"]:
            return ErrorPages.websiteErrorPage(500, "Session handler busy")
        else:
            return session["handler"]
    else:
        session = { "busy": True, "handler": UploadTorrents(sessionid) }
        Sessions[sessionid] = session
        return session["handler"]

        
class UploadTorrents(component):
    def __init__(self, sessionid):
        super(UploadTorrents, self).__init__()
        self.sessionid = sessionid
        
    def main(self):
        counter = 0
        while 1:
            counter += 1
            torrentfile = fopen(str(counter) + ".torrent")
            metafile = fopen("meta.txt")
            metafile.write(str(counter))
            metafile.close()
            
            resource = {
                "statuscode" : "200",
                "data" : u"<html><body>%d</body></html>" % counter,
                "incomplete" : False,
                "type"       : "text/html"
            }
            receivingpost = False
            while receivingpost:
                while self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    torrentfile.write(msg)
                while self.dataReady("control"):
                    msg = self.recv("control")
                    if isinstance(msg, producerFinished):
                        receivingpost = False
                
                if receivingpost:
                    yield 1
                    self.pause()
            
            torrentfile.close()
            self.send(resource, "outbox")
            self.send(producerFinished(self), "signal")
            Sessions[self.sessionid]["busy"] = False
            self.pause()
            yield 1
            
__kamaelia_components__  = ( UploadTorrents, )
