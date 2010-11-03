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
