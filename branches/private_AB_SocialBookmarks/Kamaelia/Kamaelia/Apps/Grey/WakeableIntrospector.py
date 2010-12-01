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

"""\
===============================
On Demand/Wakeable Introspector
===============================

This component grabs a list of all running/runnable components whenever it
receives a message on its inbox "inbox". This list is then sorted, and
noted to a logfile.



Example Usage
-------------

This component is intended to be used with PeriodicWakeup, as follows::

    Pipeline(
         PeriodicWakeup(interval=20),
         WakeableIntrospector(logfile="/tmp/trace"),
    )



How does it work?
-----------------

This component uses the fact that we can ask the scheduler for a list of
running componenents, takes this, sorts it and dumps the result to a
logfile.

It then sits quietly waking for a message (any message) on the inbox "inbox".



Termination
-----------

This component will shutdown if any message is sent to its control inbox.


TODO
----

In retrospect, it may've been nicer to split the introspection from the
logging. Better termination/shutdown would be a good idea.

"""

import Axon

class WakeableIntrospector(Axon.Component.component):
#    logfile = "greylist-debug.log"
#    def noteToLog(self, line):
#        try:
#            x = open(self.logfile,"a")
#        except IOError:
#            x = open(self.logfile,"w")
#        x.write(line+"\n")
#        x.flush()
#        x.close()
    def main(self):
        while not self.dataReady("control"):
            Q = [ q.name for q in self.scheduler.listAllThreads() ]
            Q.sort()
            self.send(Q, "outbox")
#            self.noteToLog("*debug* THREADS"+ str(Q))
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            for _ in self.Inbox("inbox"):
                pass

        self.send(self.recv("control"),"signal")

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Append import Append
from Kamaelia.Util.PureTransformer import PureTransformer

def LoggingWakeableIntrospector(logfile="greylist-debug.log"):
    return Pipeline(
              WakeableIntrospector(),
              PureTransformer(lambda x : "*debug* THREADS"+ str(x)+"\n" ),
              Append(filename=logfile, hold_open=False),
           )


__kamaelia_components__  = ( WakeableIntrospector, )
__kamaelia_prefabs__  = ( LoggingWakeableIntrospector, )
