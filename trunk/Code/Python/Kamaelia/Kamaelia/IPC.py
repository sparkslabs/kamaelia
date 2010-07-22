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

from Axon.Ipc import producerFinished, notify, shutdownMicroprocess

class socketShutdown(producerFinished):
   """Message to indicate that the network connection has been closed."""
   pass

class serverShutdown(shutdownMicroprocess):
   """Message to indicate that the server should shutdown"""
   pass

class newCSA(notify):
   """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""
   def __init__(self, caller, CSA, sock=None):
      super(newCSA, self).__init__(caller, CSA)
      self.sock = sock
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

