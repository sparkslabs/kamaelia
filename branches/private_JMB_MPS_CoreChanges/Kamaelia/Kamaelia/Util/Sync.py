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
================================================
Wait for 'n' items before sending one of them on
================================================

For every 'n' items received, one is sent out (the first one received in the
latest batch).



Example Usage
-------------

Wait for two tasks to finish, before propagating the shutdown message::

    Graphline( A    = TaskA(),
               B    = TaskB(),
               SYNC = Sync(2),
               linkages = {
                   ("A", "signal") : ("SYNC", "inbox"),
                   ("B", "signal") : ("SYNC", "inbox"),

                   ("SYNC", "outbox") : ("SYNC", "control"),
                   ("SYNC", "signal") : ("", "signal"),
               }

The slightly strange wiring is to make sure the Sync component is also shut
down. The shutdown message is used to shutdown Sync itself. The shutdown message
it emits is then the one that propogates out of the graphline.



Behaviour
---------

At initialisation, specify the number of items Sync should wait for.

Once that number of items have arrived at Sync's "inbox" inbox; the first that
arrived is sent on out of its "outbox" outbox. This process is repeated until
Sync is shut down.

If more han the specified number of items arrive in one go; the excess items
roll over to the next cycle. They are not ignored or lost.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class Sync(component):
    """\
    Sync([n]) -> new Sync component.
    
    After ever 'n' items received, the first in each batch received is sent on.
    
    Keyword arguments::
        
    - n  -- The number of items to expect (default=2)
    """
    
    Inboxes = { "inbox"   : "Data items",
                "control" : "Shutdown signalling",
              }

    Outboxes = { "outbox" : "First data item from last batch",
                 "signal" : "Shutdown signalling",
               }
    
    def __init__(self, n=2):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Sync,self).__init__()
        self.n=n
        
    def main(self):
        """Main loop"""
        while 1:
            for i in range(self.n):
                while not self.dataReady("inbox"):
                    while self.dataReady("control"):
                        msg = self.recv("control")
                        self.send(msg,"signal")
                        if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                            return
                    self.pause()
                    yield 1
                data = self.recv("inbox")
            self.send(data,"outbox")


__kamaelia_components__ = ( Sync, )
