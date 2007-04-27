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
====================================
Lossy connections between components
====================================

A component that passes on any data it receives, but will throw it away if the
next component's inbox is unable to accept new items.



Example Usage
-------------
Using a lossy connector to drop excess data::
    src = fastProducer().activate()
    lsy = LossyConnector().activate()
    dst = slowConsumer().activate()

    src.link( (src,"outbox"), (lsy,"inbox") )
    src.link( (lsy,"outbox"), (dst,"inbox"), pipewidth=1 )

The outbox of the lossy connector is joined to a linkage that can buffer a
maximum of one item. Once full, the lossy connector causes items to be dropped.

    

How does it work?
-----------------

This component receives data on its "inbox" inbox and immediately sends it on
out of its "oubox" outbox.

If the act of sending the data causes a noSpaceInBox exception, then it is
caught, and the data that it was trying to send is simply discarded.

I a producerFinished or shutdownMicroprocess message is received on the
component's "control" inbox, then the message is forwarded on out of its
"signal" outbox and the component then immediately terminates.
"""

from Axon.Component import component
from Axon.AxonExceptions import noSpaceInBox
from Axon.Ipc import producerFinished, shutdownMicroprocess

class LossyConnector(component):
    """\
    LossyConnector() -> new LossyConnector component

    Component that forwards data from inbox to outbox, but discards data if
    destination is full.
    """
    Inboxes  = { "inbox"   : "Data to be passed on",
                 "control" : "Shutdown signalling",
               }
    Outboxes = { "outbox" : "Data received on 'inbox' inbox",
                 "signal" : "Shutdown signalling",
               }
               
    def mainBody(self):
        """Main loop body."""
        while self.dataReady("inbox"):
            try:
                self.send(self.recv())
            except noSpaceInBox:
                pass # This is the lossy bit although most data will get through normally.
        if self.dataReady("control"):
            mes = self.recv("control")
            if isinstance(mes, producerFinished) or isinstance(mes, shutdownMicroprocess):
                self.send(mes,"signal")
                return 0
        return 1

__kamaelia_components__  = ( LossyConnector, )

class lossyConnector(LossyConnector):
    """DEPRECATED"""
    pass

