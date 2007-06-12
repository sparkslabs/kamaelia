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
===================================
Find the maximum of a set of values
===================================

Send a list of values to Max and it will send out the maximum value in the list.



Example Usage
-------------

Supplying three lists of items, and the greatest is selected from each.

    >>> Pipeline( DataSource( [ (1,4,2,3), ('d','a','b','c'), ('xx','xxx') ] ),
                  Max(),
                  ConsoleEchoer(),
                ).run()

When run this will output::

   4dxxx



Behaviour
---------

Send a list of comparable items to the "inbox" inbox and the greatest of those
items (the maximum of the list) will be sent out of the "outbox" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class Max(component):
    """\
    Max() -> new Max component.
    
    Send a list of values to its "inbox" inbox, and the maximum value from that
    list is sent out the "outbox" outbox.
    """
    
    Inboxes = { "inbox"   : "Lists of values",
                "control" : "Shutdown signalling",
              }

    Outboxes = { "outbox" : "Maximum value from the lists",
                 "signal" : "Shutdown signalling",
               }
               
    def main(self):
        """Main loop"""
        while 1:
            while self.dataReady("inbox"):
                items = self.recv("inbox")
                self.send( max(items), "outbox")
                
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                    return
            
            self.pause()
            yield 1

__kamaelia_components__ = ( Max, )

            
if __name__ == "__main__":
    from Kamaelia.Util.DataSource import DataSource
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import Pipeline
    
    Pipeline( DataSource( [ (1,4,2,3), ('d','a','b','c'), ('xx','xxx') ] ),
              Max(),
              ConsoleEchoer(),
            ).run()

    
    