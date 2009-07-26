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
