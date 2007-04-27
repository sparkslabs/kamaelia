#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
===============================================
Tags items with an incrementing sequence number
===============================================

TagWithSequenceNumber tags items with a sequence numbers, starting with  0, 1, 
2, 3, ... etc.

It takes in items on its "inbox" inbox and outputs (seqnum, item) tuples on its
"outbox" outbox. 



Example Usage
-------------

Tagging frames from a Dirac video file with a frame number::
    
    Pipeline( RateControlledFileReader("videofile.dirac", readmode="bytes", rate=... ),
              DiracDecoder(),
              TagWithSequenceNumber(),
              ...
            )



Behaviour
---------

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
    
    def main(self):
        """Main loop"""
        index = 0
        while 1:
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                self.send( (index,msg), "outbox")
#                print index
                index+=1
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    self.send(msg, "signal")
                    return
                
            self.pause()
            yield 1


__kamaelia_components__ = ( TagWithSequenceNumber, )
