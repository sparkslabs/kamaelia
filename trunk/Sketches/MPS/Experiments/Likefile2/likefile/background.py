#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
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
