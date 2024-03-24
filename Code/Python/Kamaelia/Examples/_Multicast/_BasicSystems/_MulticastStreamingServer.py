#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Basic acceptance test harness for the Multicast_sender and receiver
# components.
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
#

import Axon

file_to_stream = "../../SupportingMediaFiles/KDE_Startup_2.ogg"

def tests():
   from Axon.Scheduler import scheduler
   import Kamaelia.File.ReadFileAdaptor
   from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver

   class testComponent(Axon.Component.component):
      def main(self):
        source = Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor(file_to_stream, 
                                                          readmode="bitrate",
                                                          bitrate=400000,
                                                          chunkrate=50)
        sender   = Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600)
        self.link((source,"outbox"), (sender,"inbox"))

        self.addChildren(source, sender)
        yield Axon.Ipc.newComponent(*(self.children))
        while 1:
           yield 1

   harness = testComponent()
   harness.activate()
   scheduler.run.runThreads(slowmo=0)

if __name__=="__main__":

    tests()
     