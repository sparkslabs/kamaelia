#!/usr/bin/env python2.3

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
