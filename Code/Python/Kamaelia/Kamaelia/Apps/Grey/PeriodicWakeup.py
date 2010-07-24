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

"""\
================================
Simple Periodic Sender Component
================================

Simply sends a message every X seconds.


Example Usage
-------------
Used as follows::

    PeriodicWakeup()

It will send the message "tick" to the outbox "outbox" every 300 seconds.

To configure the delay or message, modify this::
    
    PeriodicWakeup(message="tock", delay=1)

Termination
-----------
This component does not at present terminate. It should

How does it work?
-----------------

This is just a threaded component can calls time.sleep

Todo
----

Add in termination/shutdown code.
Shift into the main code tree.

"""
class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 300
    message = "tick"
    def main(self):
        while not self.dataReady("control"):
            time.sleep(self.interval)
            self.send(self.message, "outbox") # sleeper must awaken
        self.send(self.recv("control"), "signal")
__kamaelia_components__  = ( PeriodicWakeup, )
