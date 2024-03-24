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
#
"""
The purpose of this example is to show that the PAR shutsdown cleanly
even if the message sent is a producerFinished() message. Essentially
it's an acceptance test.
"""

# Checked: 2024/03/24

import os
import time
import Axon


from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.PAR import PAR

class timedShutdown(Axon.ThreadedComponent.threadedcomponent):
    TTL = 1
    def main(self):
        time.sleep(self.TTL)
        self.send(Axon.Ipc.producerFinished(), "signal")

class ChattySlowShutdown(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while not self.dataReady("control"):
            print( self.name, "Still waiting")
            time.sleep(1)

        for i in range(3):
            print( self.name, "Shutting down slowly")
            time.sleep(1)
        self.send(self.recv("control"), "signal")

Pipeline(
        timedShutdown(TTL=3),
        PAR(
            ChattySlowShutdown(),
            PAR(
                ChattySlowShutdown(),
                ChattySlowShutdown(),
                Pipeline( 
                   PAR ( 
                      Pipeline( 
                         PAR( 
                           ChattySlowShutdown(), 
                           ChattySlowShutdown(),
                           ChattySlowShutdown()
                         ),
                      ),
                      Pipeline(
                         PAR(
                           ChattySlowShutdown(), 
                           ChattySlowShutdown(), 
                           ChattySlowShutdown()
                         ),
                      ),
                   ),
                ),
            ),
        ),
).run()

print( "PAR shutdown")
