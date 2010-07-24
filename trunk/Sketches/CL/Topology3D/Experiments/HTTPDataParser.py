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

from Axon.Component import component
from Axon.Ipc import WaitComplete
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

class HTTPDataParser(component):
    """\
    SimpleXMLParser() -> new SimpleXMLParser component.

    Send XML data to the "inbox" inbox, and events describing documents, elements
    and blocks of characters (as parsed by SAX) will be sent out of the "outbox"
    outbox.
    """
    Inboxes = { "inbox"   : "Incoming XML",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox"  : "XML events",
                 "signal"  : "Shutdown signalling",
               }

    def __init__(self):
        super(HTTPDataParser, self).__init__()
        self.waitingEvents = []
        self.shutdownMsg = None
        self.nd = 0
    
    def checkShutdown(self):
        """\
        Collects any new shutdown messages arriving at the "control" inbox, and
        returns "NOW" if immediate shutdown is required, or "WHENEVER" if the
        component can shutdown when it has finished processing pending data.
        """
        while self.dataReady("control"):
            newMsg = self.recv("control")
            if isinstance(newMsg, shutdownMicroprocess):
                self.shutdownMsg = newMsg
            elif self.shutdownMsg is None and isinstance(newMsg, producerFinished):
                self.shutdownMsg = newMsg
        if isinstance(self.shutdownMsg, shutdownMicroprocess):
            return "NOW"
        elif self.shutdownMsg is not None:
            return "WHENEVER"
        else:
            return None
        

    def main(self):
        
        while 1:

            # terminate if forced to
            if self.checkShutdown() == "NOW":
                break

            while self.dataReady("inbox"):
                # feed data into parser
                data = self.recv("inbox")
                print type(data)
                #print self.nd
                #print data
                #self.nd += 1
                #print self.nd

                # parser outpputted something? send it on
                while self.waitingEvents:
                    for _ in self.safesend( self.waitingEvents.pop(0), "outbox"):
                        yield _

                    if self.checkShutdown() == "NOW":
                        break

            if not self.dataReady("inbox"):
                if self.checkShutdown() in ["WHENEVER","NOW"]:
                    break

            self.pause()
            yield 1