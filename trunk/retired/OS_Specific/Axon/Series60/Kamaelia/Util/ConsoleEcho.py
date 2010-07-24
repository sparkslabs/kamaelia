#!/usr/bin/env python2.3
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
Console Echoer Component. Optionally passes the data it recieves through to
it's outbox - making it useful for inline (or end of line) debugging.

"""
from Axon.Component import component, scheduler

class consoleEchoer(component):
   Inboxes=["inbox","control"]
   Outboxes=["outbox"]

   def __init__(self, forwarder=False):
      super(consoleEchoer,self).__init__()# !!!! Must happen, if this method exists
      self.forwarder=forwarder

   def mainBody(self):
      if self.dataReady("inbox"):
         data = self.recv("inbox")
         print data
         if self.forwarder:
            self.send(data, "outbox")
            return 1
         return 2
      if self.dataReady("control"):
         data = self.recv("control")
         if data == "shutdown":
            return 0
      return 3

if __name__ =="__main__":
   print "This module has no system test"
#   myComponent("A",3,1)
#   myComponent("B",2).activate()
#   scheduler.run.runThreads()
