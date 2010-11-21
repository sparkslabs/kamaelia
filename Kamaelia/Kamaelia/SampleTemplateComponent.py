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
Sample Template Component.
Use this as the basis for your components!

"""
from Axon.Component import component, scheduler
class CallbackStyleComponent(component):
   #Inboxes=["inbox","control"] List of inbox names if different
   #Outboxes=["outbox","signal"] List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self,label,looptimes,selfstart=0):
      super(CallbackStyleComponent, self).__init__() # !!!! Must happen, if this method exists
      self.looptimes = looptimes
      self.label = label
      if selfstart:
         self.activate()

   def initialiseComponent(self):
      print "DEBUG:", self.label, "initialiseComponent"
      return 1

   def mainBody(self):
      print "DEBUG: ",self.label, "Now in the main loop"
      self.looptimes = self.looptimes -1
      return self.looptimes

   def closeDownComponent(self):
      print "DEBUG: ",self.label,"closeDownComponent"


class StandardStyleComponent(component):
   #Inboxes=["inbox","control"] List of inbox names if different
   #Outboxes=["outbox","signal"] List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self,label,looptimes):
      super(CallbackStyleComponent, self).__init__() # !!!! Must happen, if this method exists
      self.looptimes = looptimes
      self.label = label

   def main(self):
      print "DEBUG:", self.label, "initialiseComponent"
      yield 1
      while 1:
          print "DEBUG: ",self.label, "Now in the main loop"
          self.looptimes = self.looptimes -1
          yield self.looptimes

      print "DEBUG: ",self.label,"closeDownComponent"

__kamaelia_components__  = ( CallbackStyleComponent, StandardStyleComponent )


if __name__ =="__main__":
   myComponent("A",3,1)
   myComponent("B",2).activate()
   scheduler.run.runThreads()
