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

   def __init__(self, **argd):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(EchoProtocol, self).__init__( **argd) # Accept default in/outboxes

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
