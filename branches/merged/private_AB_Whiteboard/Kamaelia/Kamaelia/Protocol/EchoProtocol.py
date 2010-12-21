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
"""
====================
Simple Echo Protocol
====================

A simple protocol component that echoes back anything sent to it.

It simply copies its input to its output.



Example Usage
-------------

A simple server that accepts connections on port 1501, echoing back anything sent
to it::

    >>> SimpleServer(protocol=EchoProtocol, port=1501).run()

On a unix/linux client::

    > telnet <server ip> 1501
    Trying <server ip>...
    Connected to <server ip>...
    hello world, this will be echoed back when I press return (newline)
    hello world, this will be echoed back when I press return (newline)
    oooh, thats nice!
    oooh, thats nice!



How does it work?
-----------------

The component receives data on its "inbox" inbox and immediately copies it to
its "outbox" outbox.

If a producerFinished or shutdownMicroprocess message is received on its
"control" inbox, the component sends a producerFinished message to its "signal"
outbox and terminates.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess


class EchoProtocol(component):
   """\
   EchoProtocol() -> new EchoProtocol component

   Simple component that copies anything sent to its "inbox" inbox to its "outbox"
   outbox.
   """

   def __init__(self):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(EchoProtocol, self).__init__() # Accept default in/outboxes

   def mainBody(self):
      """Main body."""
      self.pause()
      
      while self.dataReady("inbox"):
         data = self.recv("inbox")
         #print "NetServ : We were sent data - "
         #print "We should probably do something with it now? :-)"
         #print "I know, let's sling it straight back at them :-)"
         self.send(data,"outbox")
         
      return self.shutdown()

   def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       while self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

__kamaelia_components__  = ( EchoProtocol, )


if __name__ == '__main__':
   from Kamaelia.Chassis.ConnectedServer import SimpleServer

   SimpleServer(protocol=EchoProtocol, port=1501).run()
