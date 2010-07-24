#!/usr/bin/env python
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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
========================
Cheap And Cheerful Clock
========================

Outputs the message True repeatedly. The interval between messages is the
parameter "interval" specified at the creation of the component.

This component is useful because it allows another component to sleep,
not using any CPU time, but waking periodically (components are unpaused
when they are sent a message).

Why is it "cheap and cheerful"?

...Because it uses a thread just for itself. All clocks could share a
single thread if some services kung-fu was pulled.
Opening lots of threads is a bad thing - they have much greater
overhead than normal generator-based components. However, the 
one-thread-per-clock approach used here is many times shorter
and simpler than one using services.
"""

import time

from Axon.ThreadedComponent import threadedcomponent

# threadedcomponent so we can sleep without pausing other components
class CheapAndCheerfulClock(threadedcomponent):
    """Outputs the message True every interval seconds"""
    def __init__(self, interval):
        super(CheapAndCheerfulClock, self).__init__()
        self.interval = interval

    def main(self):
        while 1:
            self.send(True, "outbox")
            time.sleep(self.interval) # wait self.interval seconds
            
__kamaelia_components__  = ( CheapAndCheerfulClock, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.DataSource import TriggeredSource
    from Kamaelia.Util.Console import ConsoleEchoer
    
    # Example - print "fish" every 3 seconds.
    pipeline(
        CheapAndCheerfulClock(3.0),
        TriggeredSource("Fish\n"),
        ConsoleEchoer()
    ).run()
