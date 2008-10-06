#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
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
