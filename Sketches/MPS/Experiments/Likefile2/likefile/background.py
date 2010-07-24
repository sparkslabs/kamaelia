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
"""

Out of the original code for background, this seems the most likely to
remain intact.

"""


from Axon.Scheduler import scheduler
from Axon.Component import component
import threading

import Axon.CoordinatingAssistantTracker as cat

class background(threading.Thread):
    """A python thread which runs a scheduler. Takes the same arguments at creation that scheduler.run.runThreads accepts."""
    lock = threading.Lock()
    def __init__(self,slowmo=0,zap=False):
        if not background.lock.acquire(False):
            raise "only one scheduler for now can be run!"
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True) # Die when the caller dies
        self.zap = zap
    def run(self):
        if self.zap:
            X = scheduler()
            scheduler.run = X
            cat.coordinatingassistanttracker.basecat.zap()
        scheduler.run.waitForOne()
        scheduler.run.runThreads(slowmo = self.slowmo)
        background.lock.release()

if __name__ == "__main__":
    from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle
    import time

    background = background().start()
    
    MagnaDoodle().activate()
    while 1:
        time.sleep(1)
        print "."
