#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Axon.Ipc import producerFinished, notify

class socketShutdown(producerFinished):
   """Message to indicate that the network connection has been closed."""
   pass

class newCSA(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(newCSA, self).__init__(caller, CSA)
   def handlesWriting(self):
      return True

class shutdownCSA(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(shutdownCSA, self).__init__(caller, CSA)
   def shutdown(self):
      return True

class newServer(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      #notify.__init__(self, caller, CSA)
      super(newServer, self).__init__(caller, CSA)
   def handlesWriting(self):
      print "we're being checked"
      return False
