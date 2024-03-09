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
Null sink component.  To ignore a component's outbox connect it to this
component and the box will be emptied but not used in any way.  This will be
necessary with syncronized linkages.
"""
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished, shutdownMicroprocess
class nullSinkComponent(component):
   Inboxes=["inbox","control"]
   Outboxes=["outbox", "signal"] # Pipeline expects these to exist

   def mainBody(self):
      while self.dataReady("inbox"):
         data = self.recv("inbox")
      if self.dataReady("control"):
         data = self.recv("control")
         if isinstance(data,producerFinished) or isinstance(data, shutdownMicroprocess):
            return 0
      return 1

__kamaelia_components__  = ( nullSinkComponent, )


if __name__ =="__main__":
   print ("This module has no system test")
