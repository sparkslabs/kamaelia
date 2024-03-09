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
"""
RtpPacker Component
===================

Takes data from a preframer:

   * Creates an RTP Header Object
   * Uses the timestamp & sample count to generate an RTP timestamp

"""
from Axon.Component import component, scheduler

class RtpPacker(component):
   Inboxes=["inbox"]   # List of inbox names if different
   Outboxes=["outbox"] # List of outbox names if different
   #Usescomponents=[] # List of classes used.
   def __init__(self,label,looptimes,selfstart=0):
      super(RtpPacker, self).__init__() # !!!! Must happen, if this method exists

   def initialiseComponent(self):
      return 1

   def mainBody(self):
      return 1

   def closeDownComponent(self):
      "closeDownComponent"
      pass

__kamaelia_components__  = ( RtpPacker, )


if __name__ =="__main__":
   # myComponent("A",3,1)
   # myComponent("B",2).activate()
   # scheduler.run.runThreads()
   pass
