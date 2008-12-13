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
"""
Simple Server class.

Provides a framework for creating generic protocol handlers to
deal with information coming in on a single port (and a single
port only). This however covers a large array of server types.

This code is based on the code used for testing the Internet Connection
abstraction layer.

EXTERNAL CONNECTORS
      * inboxes : ["_oobinfo"]
      * outboxes=None

Strictly speaking _oobinfo isn't an external connector - it's used for plumbing
internal components into the Simple Server. (The PLS sends messages to
the Simple Server - such as "new connection" on this connector)

In practice, this component provides no external connectors for your use.
"""

import Axon as _Axon
from Kamaelia.Chassis.ConnectedServer import SimpleServer

class simpleServerProtocol(_Axon.Component.component):
   pass

if __name__ == '__main__':

   from Axon.Scheduler import scheduler
   class SimpleServerTestProtocol(simpleServerProtocol):
      def __init__(self):
         super(SimpleServerTestProtocol, self).__init__()
         assert self.debugger.note("SimpleServerTestProtocol.__init__",1, "Starting test protocol")

      def mainBody(self):
         if self.dataReady("inbox"):
            data = self.recv("inbox")
            print "Got data", data
            assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "NetServ : We were sent data - ")
            assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "We should probably do something with it now? :-)")
            assert self.debugger.note("SimpleServerTestProtocol.mainBody",1, "I know, let's sling it straight back at them :-)")
            self.send(data,"outbox")
         if self.dataReady("control"):
            data = self.recv("control")
            return 0
         return 1

      def closeDownComponent(self):
         assert self.debugger.note("SimpleServerTestProtocol.closeDownComponent",1, "Closing down test protcol")

   SimpleServer(protocol=SimpleServerTestProtocol).activate()
   scheduler.run.runThreads(slowmo=0)
