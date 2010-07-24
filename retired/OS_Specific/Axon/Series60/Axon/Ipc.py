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
