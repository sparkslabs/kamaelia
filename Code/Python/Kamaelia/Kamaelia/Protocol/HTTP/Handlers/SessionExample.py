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
# ------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: RJL
"""\
========================
Session Example
========================
A simple persistent request handler component.
Each time a URL that is handled by this component is requested, the page's
'hit counter' is incremented and shown to the user as text.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

import Kamaelia.Protocol.HTTP.ErrorPages

Sessions = {}

def SessionExampleWrapper(request):
    sessionid = request["uri-suffix"]
    if (sessionid in Sessions):
        session = Sessions[sessionid]
        if session["busy"]:
            return ErrorPages.websiteErrorPage(500, "Session handler busy")
        else:
            return session["handler"]
    else:
        session = { "busy" : True, "handler" : SessionExample(sessionid) }
        Sessions[sessionid] = session
        return session["handler"]


class SessionExample(component):
    def __init__(self, sessionid):
        super(SessionExample, self).__init__()
        self.sessionid = sessionid

    def main(self):
        counter = 0
        while 1:
            counter += 1
            resource = {
                "statuscode" : "200",
                "data" : u"<html><body>%d</body></html>" % counter,
                "incomplete" : False,
                "content-type"       : "text/html"
            }
            self.send(resource, "outbox")
            self.send(producerFinished(self), "signal")
            Sessions[self.sessionid]["busy"] = False
            self.pause()
            yield 1

__kamaelia_components__  = ( SessionExample, )
