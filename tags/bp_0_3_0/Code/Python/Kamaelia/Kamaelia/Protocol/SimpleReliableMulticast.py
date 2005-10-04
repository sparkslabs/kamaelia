#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
import Axon
from Kamaelia.Util.PipelineComponent import pipeline

from Kamaelia.Protocol.Framing import Framer as _Framer
from Kamaelia.Protocol.Framing import DeFramer as _DeFramer

from Kamaelia.Protocol.Framing import DataChunker as _DataChunker
from Kamaelia.Protocol.Framing import DataDeChunker as _DataDeChunker

class Annotator(Axon.Component.component):
   def main(self):
      n=1
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            self.send((n, item), "outbox")
            n = n + 1



class RecoverOrder(Axon.Component.component):
   def main(self):
      bufsize = 30
      datasource = []
      while 1:
         yield 1
         if self.dataReady("inbox"):
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
    return pipeline(
        Annotator(),
        _Framer(),
        _DataChunker()
    )

def SRM_Receiver():
    return pipeline(
        _DataDeChunker(),
        _DeFramer(),
        RecoverOrder()
    )

if __name__ == "__main__":
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
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

    pipeline(Source(),
             SRM_Sender(),
             Duplicate(),
             Throwaway(),
             Reorder(),
             SRM_Receiver(),
             consoleEchoer()
    ).run()
