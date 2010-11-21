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
================================
Sending an output to many places
================================

This component copies data sent to its inbox to multiple, specified outboxes.
This allows you to 'fan out' a data source to several predetermined
destinations.



Example Usage
-------------
Output data source both to a file and to the console::

    Graphline( source  = MyDataSource(...),
               split   = Fanout(["toConsole","toFile"]),
               file    = SimpleFileWriter(filename="outfile"),
               console = ConsoleEchoer(),
               linkages = {
                 ("source","outbox")   : ("split","inbox"),
                 ("split","toConsole") : ("console","inbox"),
                 ("split","toFile")    : ("file","inbox"),
               }
             ).run()



How does it work?
-----------------

At initialization, specify a list of names for outboxes. Once the component is
activated, any data sent to its "inbox" inbox will be replicated out to the
list of outboxes you specified.

In effect, data sent to the "inbox" inbox is 'fanned out' to the specified set
of destinations.

Nothing is sent to the "outbox" outbox.

If a shutdownMicroprocess or producerFinished message is received on the
"control" inbox, then it is sent on to the "signal" outbox and the component
terminates.

There is no corresponding 'Fanout' of data flowing into the "control" inbox.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Fanout(component):
   """\
   Fanout(boxnames) -> new Fanout component.

   A component that copies anything received on its "inbox" inbox to the named
   list of outboxes.
   
   Keyword arguments:
   
   - boxnames  -- list of names for the outboxes any input will be fanned out to.
   """

   Inboxes  = { "inbox"   : "Data to be fanned out",
                "control" : "Shutdown signalling",
              }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "Shutdown signalling"
              }
              
   def __init__(self, boxnames):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      self.Outboxes = dict(self.__class__.Outboxes) # Copy the class outboxes into the instance outboxes
      for boxname in boxnames:
          self.Outboxes[boxname] = "Copy of data received at 'inbox' inbox"
      super(Fanout, self).__init__()
      
   def main(self):
      """Main loop."""
      while 1:
         while self.dataReady("inbox"):
            data = self.recv("inbox")
            for boxname in self.Outboxes:
               self.send(data, boxname)
         while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, shutdownMicroprocess) or isinstance(data,producerFinished):
               self.send(data, "signal")
               return
         if not self.anyReady(): # This should be the case here.
             self.pause()
         yield 1

__kamaelia_components__  = ( Fanout, )

import Kamaelia.Support.Deprecate as Deprecate

fanout = Deprecate.makeClassStub(
    Fanout,
    "Use Kamaelia.Util.Fanout:Fanout instead of Kamaelia.Util.Fanout:fanout",
    "WARN"
    )





























   