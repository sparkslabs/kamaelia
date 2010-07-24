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
=================================================
Collate everything received into a single message
=================================================

Buffers all data sent to it. When shut down, sends all data it has received as
collated as a list in a single message.



Example Usage
-------------

Read a file, in small chunks, then collate them into a single chunk::
    
    Pipeline( RateControlledFileReader("big_file", ... ),
              Collate(),
              ...
            )
            


Behaviour
---------

Send data items to its "inbox" inbox to be collated.

Send a producerFinished or shutdownMicroprocess message to the "control" inbox
to terminate this component. 

All collated data items will be sent out of the "outbox" outbox as a list in a
single message. The items are collated in the same order they first arrived.

The component will then send on the shutdown message to its "signal" outbox and
immediately terminate.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class Collate(component):
    """\
    Collate() -> new Collate component.
    
    Buffers all data sent to it. When shut down, sends all data it has received
    as a single message.
    """
    
    Inboxes = { "inbox"   : "Data items",
                "control" : "Shutdown signalling",
              }

    Outboxes = { "outbox" : "All data items collated into one message",
                 "signal" : "Shutdown signalling",
               }
    
    def main(self):
        """Main loop"""
        collated = []
        while 1:
            while self.dataReady("inbox"):
                collated.append(self.recv("inbox"))
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                    self.send(collated,"outbox")
                    self.send(msg,"signal")
                    return
                else:
                    self.send(msg,"signal")
            
            self.pause()
            yield 1
            
__kamaelia_components__ = ( Collate, )
