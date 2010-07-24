#!/usr/bin/python
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
=========================
Broken Network Simulation
=========================

Components to simulate properties of an unreliable network connection.
Specifically: out of order delivery, duplication, and loss of packets.

Original author: Tom Gibson (whilst at BBC)



Example Usage
-------------

Testing a forward-error correction scheme to cope with an unreliable network::
    
    Pipeline( RateControlledFileReader("sourcefile",rate=1000000),
              MyForwardErrorCorrector(),
              Duplicate(),
              Throwaway(),
              Reorder(),
              MyErrorRecoverer(),
              SimpleFileWriter("receiveddata")
            ).activate()



Duplicate, Throwaway, Reorder
-----------------------------

These three components all receive data and, respectively, randomly duplicate
packets, re-order packets or throw some packets away.

They can be used to simulate the effects of multicast delivery over wireless or
a WAN.



More details
------------

These component all receive data on their "inbox" inbox and send it on to their
"outbox" outbox. However, they will sometimes tamper with the data in the
manners described!

None of these components terminate when sent shutdown messages.



History
-------
This was used for the development of a simple recovery
protocol. The actual version in use replaces the string2tuple and
tuple2string code (in sketches in tomg.py, omitted here), with something
more robust.

"""

import random

from Axon.Component import component

class Duplicate(component):
   """\
   Duplicate() -> new component.

   This component passes on data it receives. Sometimes it randomly duplicates
   items.
   """
   def main(self):
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            if random.randrange(0,10) == 0:
               self.send(item, "outbox")
               self.send(item, "outbox")
            else:
               self.send(item, "outbox")

class Throwaway(component):
   """\
   Throwaway() -> new component.

   This component passes on data it receives, but sometimes it doesn't!
   """
   def main(self):
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            if random.randrange(0,10) != 0:
               self.send(item, "outbox")

class Reorder(component):
    """\
    Reorder() -> new component

    This component passes on data it receives, but will sometimes jumble it up
    (reordering it).
    """
    def main(self):
        newlist = []
        while 1:
            yield 1
            if self.dataReady("inbox"):
                item = self.recv("inbox")
                newlist.append(item)
                if len(newlist) == 8:
                    temp = random.randrange(0,7)
                    self.send(newlist[temp], "outbox")
                    newlist.remove(newlist[temp])

__kamaelia_components__  = ( Duplicate, Throwaway, Reorder)

if __name__ == "__main__":
    import time
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer

    class Source(component):
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

    class Annotator(component):
       def main(self):
          n=1
          while 1:
             yield 1
             if self.dataReady("inbox"):
                item = self.recv("inbox")
                self.send((n, item), "outbox")
                n = n + 1

    class RecoverOrder(component):
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


    Pipeline(Source(),
             Annotator(),
             Duplicate(),
             Throwaway(),
             Reorder(),
             RecoverOrder(),
             ConsoleEchoer()
    ).run()
