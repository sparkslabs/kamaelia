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
===========================
Pass on the first item only
===========================

The first item sent to FirstOnly will be passed on. All other items are ignored.



Example Usage
-------------

Displaying the frame rate, just once, from video when it is decoded::

    Pipeline( ...
              DiracDecoder(),
              FirstOnly(),
              SimpleDetupler("frame_rate"),
              ConsoleEchoer(),
            )



Behaviour
---------

The first data item sent to FirstOnly's "inbox" inbox is immediately sent on
out of its "outbox" outbox.

Any subsequent data sent to its "inbox" inbox is discarded.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class FirstOnly(component):
    """\
    FirstOnly() -> new FirstOnly component.

    Passes on the first item sent to it, and discards everything else.
    """

    Inboxes = { "inbox" : "Data items",
                "control" : "Shutdown signalling"
              }
              
    Outboxes = { "outbox" : "First data item received",
                 "signal" : "Shutdown signalling",
               }
                    
    def main(self):
        """Main loop"""
        while not self.dataReady("inbox"):
            if self.dataReady("control"):
                self.send(self.recv("control"),"signal")
                return
            self.pause()
            yield 1
            
        self.send(self.recv("inbox"),"outbox")
        
        while not self.dataReady("control"):
            while self.dataReady("inbox"):
                self.recv("inbox")          # absorb anything sent to me
            self.pause()
            yield 1
            
        self.send(self.recv("control"),"signal")
        
__kamaelia_components__ = ( FirstOnly, )
