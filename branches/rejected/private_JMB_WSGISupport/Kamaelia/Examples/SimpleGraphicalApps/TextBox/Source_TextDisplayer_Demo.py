#!/usr/bin/env python
#
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

import time
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.UI.Pygame.Text import TextDisplayer

#the long lines are there on purpose, to see if the component wraps text correctly.

class TimedLineSender(Axon.ThreadedComponent.threadedcomponent):
    text =  """\
            To be, or not to be: that is the question:
            Whether 'tis nobler in the mind to suffer
            The slings and arrows of outrageous fortune,
            Or to take arms against a sea of troubles,
            And by opposing end them? To die: to sleep;
            No more; and by a sleep to say we end
            The heart-ache and the thousand natural shocks That flesh is heir to, 'tis a consummation Devoutly to be wish'd. To die, to sleep;
            To sleep: perchance to dream: ay, there's the rub;
            For in that sleep of death what dreams may come
            When we have shuffled off this mortal coil,
            Must give us pause: there's the respect
            That makes calamity of so long life;
            """
    strip_leading = True
    debug = True
    delay = 0.5
    def main(self):
        lines = self.text.split('\n')
        for line in lines:
            if self.strip_leading:
                line = line.lstrip()
            time.sleep(self.delay)
            self.send(line) # remove preding spaces 
        self.send(producerFinished(), 'signal')

Pipeline(TimedLineSender(),
         TextDisplayer()).run()
