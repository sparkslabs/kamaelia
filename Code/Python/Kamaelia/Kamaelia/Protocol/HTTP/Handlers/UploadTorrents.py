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
========================
Upload Torrents
========================
A session-based HTTP request handler for HTTPServer.
UploadTorrents saves .torrent files that are uploaded to it as POST
data and stores the number of .torrent files save to a file "meta.txt".
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

import Kamaelia.Protocol.HTTP.ErrorPages

Sessions = {}

def UploadTorrentsWrapper(request):
    """Returns an UploadTorrents component, manages that components lifetime and access."""

    sessionid = request["uri-suffix"]
    if (sessionid in Sessions):
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
                "content-type"       : "text/html"
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
