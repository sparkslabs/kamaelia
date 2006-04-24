#!/usr/bin/env python2.3
#
#      TODO: Thread shutdown
#      TODO: How to allow the thread to start new components?
#            (ie we only yield 1, not a newComponent or any value from the
#            thread.)
#      TODO: Number of minor issues fixed - thread shutdown is an issue though!
#            Added simple trace statements into the code.
#
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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

from Component import component
from Microprocess import microprocess
from Scheduler import scheduler
import threading

class threadedcomponent(component):
    """\
    Revised threading component
    """
    
    def __init__(self):
        super(threadedcomponent,self).__init__()

        self._thethread = threading.Thread(target=self._launchthread)
        self._localmprocess = microprocess(thread=self._localmain())
        self._threadscheduler = scheduler()
        
    def activate(self, Scheduler=None, Tracker=None):
        # activate mprocess placeholder, representing the thread
        # might also be the one that moves data through inbox/outbox queues
        self._localmprocess.activate(Scheduler, Tracker)
        
        # activate the actual component mprocess inside the thread's scheduler
        return super(threadedcomponent,self).activate(self._threadscheduler, Tracker)
    
    def _localmain(self):
        """Placeholder microprocess, representing the thread, in the 'main' scheduler"""
        self._thethread.start()
        while self._thethread.isAlive():
            yield 1
            
    def _launchthread(self):
        self._threadscheduler.runThreads()
            
    # write your own main function body



if __name__ == "__main__":
    import time,sys
    
    class TheThread(threadedcomponent):
        def main(self):
            t = time.time()
            for i in range(1,10):
                while time.time() < t:
                    pass
                t=t+1.0
                sys.stdout.write("Threaded: "+str(i)+"\n")
                sys.stdout.flush()
                yield 1
                
    class NotThread(component):
        def main(self):
            t = time.time()
            for i in range(1,20):
                while time.time() < t:
                    yield 1
                t=t+0.5
                sys.stdout.write("Normal: "+str(i)+"\n")
                sys.stdout.flush()
                    
    TheThread().activate()
    NotThread().run()
