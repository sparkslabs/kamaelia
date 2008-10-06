#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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

Q. Why is it "cheap and cheerful"?
A. Because it uses a thread just for itself. All clocks could share a
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
    from Kamaelia.Community.RJL.Kamaelia.Util.DataSource import TriggeredSource
    from Kamaelia.Util.Console import ConsoleEchoer
    
    # Example - print "fish" every 3 seconds.
    pipeline(
        CheapAndCheerfulClock(3.0),
        TriggeredSource("Fish\n"),
        ConsoleEchoer()
    ).run()
