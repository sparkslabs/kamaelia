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
===============================================
Tags items with an incrementing sequence number
===============================================

TagWithSequenceNumber tags items with a sequence numbers, for example:  0, 1, 
2, 3, ... etc. The default initial value of the sequence is a 0.

It takes in items on its "inbox" inbox and outputs (seqnum, item) tuples on its
"outbox" outbox. 



Example Usage
-------------

Tagging frames from a Dirac video file with a frame number, starting with 1::
    
    Pipeline( RateControlledFileReader("videofile.dirac", readmode="bytes", rate=... ),
              DiracDecoder(),
              TagWithSequenceNumber(initial=1),
              ...
            )



Behaviour
---------

At initialisation, specify the initial sequence number to use.

Send an item to TagWithSequenceNumber's "inbox" inbox, and it will send 
(seqnum, item) to its "outbox" outbox.

The sequence numbers begin 0, 1, 2, 3, ... etc ad infinitum.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class TagWithSequenceNumber(component):
    """\
    TagWithSequenceNumber() -> new TagWithSequenceNumber component.
    
    Send 'item' to the "inbox" inbox and it will be tagged with a sequence
    number, and sent out as (seqnum, 'item') to the "outbox" outbox.
    
    Sequence numbering goes 0, 1, 2, 3, ... etc.
    
    """
    
    Inboxes = { "inbox"   : "Items",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Items tagged with a sequence number, in the form (seqnum, item)",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, initial=0):
        super(TagWithSequenceNumber,self).__init__()
        self.initial=initial
    
    def main(self):
        """Main loop"""
        index = self.initial
        while 1:
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                self.send( (index,msg), "outbox")
                index+=1
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    self.send(msg, "signal")
                    return
                
            self.pause()
            yield 1


__kamaelia_components__ = ( TagWithSequenceNumber, )
