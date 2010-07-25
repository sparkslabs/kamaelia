#!/usr/bin/python
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

import time
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

class Pinger(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        time.sleep(1.0)
        self.send(Axon.Ipc.producerFinished(), "signal")
        print "sent 1!"
        time.sleep(0.5)
        self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
        print "sent 2!"
        time.sleep(0.5)
    
class Waiter(Axon.Component.component):
    def main(self):
        while not self.dataReady("control"):
            print self.name, "waiting"
            if not self.anyReady():
                 self.pause()
            yield 1
        msg = self.recv("control")
        print self.name, "shutting down having recieved:", msg
        self.send("passedon", "signal")
        yield 1

Pipeline(
    Pinger(),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        TO_SHUTDOWN3 = Waiter(),
        linkages = {
            ("TO_SHUTDOWN1", "signal") : ("TO_SHUTDOWN2", "control"),
        }
    ),
    ConsoleEchoer(),
).run()
