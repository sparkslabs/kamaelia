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

import OSC
import Axon
import random
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Internet.UDP import SimplePeer

class NumberGen(Axon.Component.component):
    def __init__(self):
        super(NumberGen, self).__init__()
        random.seed()
        
    def main(self):
        while 1:
            self.send(random.random(), "outbox")
            yield 1

class OSCTest(Axon.Component.component):
    def __init__(self):
        super(OSCTest, self).__init__()
    
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                message = OSC.OSCMessage("/OSCTest")
                message.append(self.recv("inbox"))
                self.send(message.getBinary(), "outbox")
            yield 1

if __name__ == "__main__":
    Pipeline(NumberGen(), OSCTest(), SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000)).run()
