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
      super(newServer, self).__init__(caller, CSA)
   def handlesWriting(self):
      return False

#
# Two new classes to simplify the selector.
# 
# Note that hasOOB is only to be set for SOCKETS, and relates to out of band
# information regarding the socket. This is used to put the specific thing
# to monitor into the exceptions set (places we get out of band info)
#
# For more help as to what's going on with exceptionals, look at
#   $ man 2 select_tut
#
# This may get simplified further at some point to simply add in a newExceptionalReader
# message (indeed I'm in two minds right now about that!)
#


class newWriter(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
    will return the CSA."""
    def __init__(self, caller, CSA):
        super(newWriter, self).__init__(caller, CSA)
        self.hasOOB = False 

class newReader(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(newReader, self).__init__(caller, CSA)
      self.hasOOB = False

class newExceptional(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(newExceptional, self).__init__(caller, CSA)
      self.hasOOB = False

class removeReader(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(removeReader, self).__init__(caller, CSA)
      self.hasOOB = False

class removeWriter(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(removeWriter, self).__init__(caller, CSA)
      self.hasOOB = False

class removeExceptional(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA):
      super(removeExceptional, self).__init__(caller, CSA)
      self.hasOOB = False

