#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import Axon
from Kamaelia.Apps.Europython09.BB.Exceptions import GotShutdownMessage

class LineOrientedInputBuffer(Axon.Component.component):
    def main(self):
        linebuffer = []
        gotline = False
        line = ""
        try:
            while 1:
                # Get a line
                while (not gotline):
                    if self.dataReady("control"):
                        raise GotShutdownMessage()

                    if self.dataReady("inbox"):
                        msg = self.recv("inbox")
                        if "\r\n" in msg:
                           linebuffer.append( msg[:msg.find("\r\n")+2] )
                           line = "".join(linebuffer)
                           gotline = True
                           linebuffer = [ msg[msg.find("\r\n")+2:] ]
                        else:
                           linebuffer.append( msg )
                    yield 1
                if self.dataReady("control"):
                    raise GotShutdownMessage()

                # Wait for receiver to be ready to accept the line
                while len(self.outboxes["outbox"]) > 0:
                    self.pause()
                    yield 1
                    if self.dataReady("control"):
                        raise GotShutdownMessage()

                # Send them the line, then rinse and repeat.
                self.send(line, "outbox")
                yield 1
                gotline = False
                line = ""

        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")
            return

        self.send(producerFinished(), "signal")

