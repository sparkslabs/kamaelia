#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=========================
Simple Reliable Multicast
=========================

A pair of Pipelines for encoding (and decoding again) a stream of data such that
is can be transported over an unreliable connection that may lose, duplicate or
reorder data.

These components will ensure that data arrives in the right order and that
duplicates are removed. However it cannot recover lost data.


Example Usage
-------------
Reliably transporting a file over multicast (assuming no packets are lost)::

    Pipeline(RateControlledFileReader("myfile"),
             SRM_Sender(),
             Multicast_transceiver("0.0.0.0", 0, "1.2.3.4", 1000),
            ).activate()

On the client::

    class discardSeqnum(component):
        def main(self):
            while 1:
                if self.dataReady("inbox"):
                    (_, data) = self.recv("inbox")
                    self.send(data,"outbox")
    
    Pipeline( Multicast_transceiver("0.0.0.0", 1000, "1.2.3.4", 0)
              SRM_Receiver(),
              discardSeqnum(),
              ConsoleEchoer()
            ).activate()



How does it work?
-----------------

SRM_Sender is a Pipeline of three components:

- Annotator    -- annotates a data stream with sequence numbers
- Framer       -- frames the data
- DataChunker  -- inserts markers between frames

SRM_Receiver is a Pipeline of three components:

- DataDeChunker  -- recovers chunks based on markers
- DeFramer       -- removes framing
- RecoverOrder   -- sorts data by sequence numbers

These components will ensure that data arrives in the right order and that
duplicates are removed. However it cannot recover lost data. But the final
output is (seqnum,data) pairs - so there is enough information for the
receiver to know that data has been lost.

The Annotator component receives data on its "inbox" inbox, and emits
(seqnum, data) tuples on its "outbox" outbox. The sequence numbers start at 1
and increments by 1 for each item.

The Annotator component does not terminate and ignores messages arriving on its
"control" inbox.

See documentation for the other components for details of their design and
behaviour.
"""

import Axon
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Protocol.Framing import Framer as _Framer
from Kamaelia.Protocol.Framing import DeFramer as _DeFramer

from Kamaelia.Protocol.Framing import DataChunker as _DataChunker
from Kamaelia.Protocol.Framing import DataDeChunker as _DataDeChunker


class Annotator(Axon.Component.component):
   """\
   Annotator() -> new Annotator component.

   Takes incoming data and outputs (n, data) where n is an incrementing sequence
   number, starting at 1.
   """
   def main(self):
      """Main loop"""
      n=1
      while 1:
         yield 1
         while self.dataReady("inbox"):
            item = self.recv("inbox")
            self.send((n, item), "outbox")
            n = n + 1



class RecoverOrder(Axon.Component.component):
   """\
   RecoverOrder() -> new RecoverOrder component.

   Receives and buffers (seqnum, data) pairs, and reorders them by ascending
   sequence number and emits them (when its internal buffer is full).
   """
   def main(self):
      """Main loop."""
      bufsize = 30
      datasource = []
      while 1:
         if not self.anyReady():
             self.pause()
         yield 1
         while self.dataReady("inbox"):
            item = self.recv("inbox")
            datasource.append(item)
      
            if len(datasource) == bufsize:
               datasource.sort()
               try:
                  if datasource[0] != datasource[1]:
                     self.send(datasource[0], "outbox")
               except IndexError:
                   self.send(datasource[0], "outbox")
               del datasource[0]

      need_clean_shutdown_make_this_true_and_fix = False
      if need_clean_shutdown_make_this_true_and_fix:
         while datasource != []:
            try:
               if datasource[0] != datasource[1]:
                     self.send(datasource[0], "outbox")
            except IndexError:
                     self.send(datasource[0], "outbox")
            del datasource[0]


            
def SRM_Sender():
    """\
    Simple Reliable Multicast sender.

    Sequence numbers, frames and chunks a data stream, making it suitable for
    sending over an unreliable connection that may lose, reorder or duplicate
    data. Can be decoded by SRM_Receiver.

    This is a Pipeline of components.
    """
    return Pipeline(
        Annotator(),
        _Framer(),
        _DataChunker()
    )

def SRM_Receiver():
    """\
    Simple Reliable Multicast receiver.

    Dechunks, deframes and recovers the order of a data stream that has been
    encoded by SRM_Sender.

    Final emitted data is (seqnum, data) pairs.

    This is a Pipeline of components.
    """
    return Pipeline(
        _DataDeChunker(),
        _DeFramer(),
        RecoverOrder()
    )

__kamaelia_components__  = ( Annotator, RecoverOrder, )
__kamaelia_prefabs__ = ( SRM_Sender, SRM_Receiver)
    
if __name__ == "__main__":
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Internet.Simulate.BrokenNetwork import Duplicate, Throwaway, Reorder
    
    import time
    import random

    class Source(Axon.Component.component):
       def __init__(self,  size=100):
          super(Source, self).__init__()
          self.size = size
       def main(self):
          i = 0
          t = time.time()
          while 1:
             yield 1
             if time.time() - t > 0.01:
                i = i + 1
                self.send(str(i), "outbox")
                t = time.time()

    Pipeline(Source(),
             SRM_Sender(),
             Duplicate(),
             Throwaway(),
             Reorder(),
             SRM_Receiver(),
             ConsoleEchoer()
    ).run()
