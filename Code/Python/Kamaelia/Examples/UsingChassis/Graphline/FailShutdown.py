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

# Checked: 2024/03/24

import time
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

class Pinger(Axon.ThreadedComponent.threadedcomponent):
    tosend = [ ]
    box = "signal"
    delay = 0.3
    def main(self):
        i = 0
        for i in self.tosend:
            time.sleep(1.0)
            self.send(Axon.Ipc.producerFinished(), self.box)
            print( "PINGER: sent", i)
    
class Waiter(Axon.Component.component):
    def main(self):
        print( "WAITER", self.id, "waiting")
        while not self.dataReady("control"):
            if not self.anyReady(): self.pause()
            yield 1
        msg = self.recv("control")
        print( "WAITER", self.id, "shutting down having recieved:", msg)
        self.send(msg, "signal")
        yield 1

class Whinger(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while not self.dataReady("control"):
            print( "WHINGER: waiting for shutdown")
            time.sleep(1)
        print( "WHINGER: shutdown")


print( """
This example will fail to shutdown.

    Pipeline(
        Pinger(tosend=[Axon.Ipc.producerFinished()],box="signal"),
        Graphline(
            TO_SHUTDOWN1 = Waiter(),
            TO_SHUTDOWN2 = Waiter(),
            linkages = {
                ("self", "control") : ("TO_SHUTDOWN1", "control"),
            }
        ),
        Whinger(),
    ).run()

The reason for this is twofold:

   * The user has chosen to link the graphlines control passed through to a
     child
   * That child does not tell the other components to shutdown, so they
     don't. 
   * No one passes on the shutdown as a result to the outside world, meaning
     the Whinger() keeps on whinging.

""")

Pipeline(
    Pinger(tosend=[Axon.Ipc.producerFinished()],box="signal"),
    Graphline(
        TO_SHUTDOWN1 = Waiter(),
        TO_SHUTDOWN2 = Waiter(),
        linkages = {
            ("self", "control") : ("TO_SHUTDOWN1", "control"),
        }
    ),
    Whinger(),
).run()
