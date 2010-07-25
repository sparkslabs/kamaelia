# -*- coding: utf-8 -*-

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

# http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1200236224
# 
import time
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 1
    def main(self):
        while 1:
            time.sleep(self.interval)
            self.send("tick", "outbox")

class WakeableIntrospector(Axon.Component.component):
    def main(self):
        while 1:
            Q = [ q.name for q in self.scheduler.listAllThreads() ]
            Q.sort()
            self.send("\n*debug* THREADS"+ str(Q)+"\n", "outbox")
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            while self.dataReady("inbox"):
                self.recv("inbox")

def activate():
    Pipeline(
        PeriodicWakeup(),
        WakeableIntrospector(),
        ConsoleEchoer(),
    ).activate()
