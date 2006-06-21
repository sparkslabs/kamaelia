#!/usr/bin/python
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
"""Kamaelia Concurrency Component Framework.

IPC Classes

"""
class ipc(object):
   """Message base class"""
   pass

class newComponent(ipc):
   """Message used to inform the scheduler of a new component that needs a thread
   of control and activating"""
   def __init__(self, *components):
      self._components = components
   def components(self):
      return self._components

class shutdownMicroprocess(ipc):
   def __init__(self, *microprocesses):
      self._microprocesses = microprocesses
   def microprocesses(self):
      return self._microprocesses


class notify(ipc):
   """Message used to notify the system of an event"""
   def __init__(self, caller, payload):
      self.object = payload
      self.caller = caller

class status(ipc):
   """General Status message"""
   def __init__(self, status):
      self._status =status
   def status(self):
      return self._status

class wouldblock(ipc):
   """Message used to indicate to the scheduler that the system is likely to block now, why, and
   reasons to awaken the system"""
   def __init__(self,caller):
      self.caller = caller

class producerFinished(ipc):
   """Message to indicate that the producer has completed its work and will produce no more output."""
   def __init__(self,caller=None,message=None):
      self.caller = caller
      self.message = message

class errorInformation(ipc):
   """A message to indicate that a non fatal error has occured in the component.  It may skip processing errored data but should respond correctly to future messages."""
   def __init__(self, caller, exception=None, message=None):
      self.caller = caller # the component that the error occured in.
      self.exception = exception # if an exception was caught the exception object
      self.message = message # the message with bad data that caused the exception or error

if __name__ == '__main__':
   print "This class currently contains no test code."
