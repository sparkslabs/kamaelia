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
"""\
=============================
Shutdown the Selector service
=============================

StopSelector asks the Selector service to shutdown; either immediately, or when
triggered by anything being sent to any of its inboxes.

**NOTE** This probably isn't the most ideal way to do things - but it does
actually *work* for the moment :-)



Example Usage
-------------

Receive data from myserver.com port 1500, save it to a file, then finish::
    
    Pipeline( TCPClient("myserver.com",1500),
              SimpleFileWriter("received_data"),
              StopSelector(),
            ).run()



Behaviour
---------

At initialisation specify whether StopSelector should wait to be triggered or
act immediately. The default behaviour is to act immediately
(waitForTriger=False).

If asked, StopSelector will wait for anything to be sent to its "inbox" or
"control" inboxes. It will then immediately ask the Selector service to
shutdown, and immediately terminate.

Otherwise, StopSelector will do this as soon as it is activated, and will then
immediately terminate.

If it was triggered by a message being sent to the "control" inbox then this
will be sent on our of the "signal" outbox just before termination. Otherwise a
producerFinished message will be sent on just before termination.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

from Kamaelia.Internet.Selector import Selector
from Axon.Ipc import shutdown


class StopSelector(component):
    """\
    StopSelector([waitForTigger]) -> new StopSelector component.

    Asks the Selector service to shutdown; either immediately, or when triggered
    by anything being sent to any of its inboxes.

    Keyword arguments::

    - waitForTrigger  -- True to wait to be triggered, else False (default=False)
    """
    
    Inboxes = { "inbox"   : "Anything, as trigger",
                "control" : "Shutdown signalling",
              }

    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling",
                 "selector_shutdown" : "Ask the selector to shut down"
               }
    
    def __init__(self, waitForTrigger=False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(StopSelector,self).__init__()
        self.waitForTrigger=waitForTrigger

    def main(self):
        """Main loop"""
        
        if self.waitForTrigger:
            while not self.anyReady():
                self.pause()
                yield 1
            
        # stop the selector
        selectorService, selectorShutdownService, newSelectorService = Selector.getSelectorServices(self.tracker) # get a reference to a     
        link = self.link((self,"selector_shutdown"),selectorShutdownService)
        
        self.send(shutdown(),"selector_shutdown")
        self.unlink(thelinkage=link)
        
        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
            self.send(producerFinished(self), "signal")


__kamaelia_components__ = ( StopSelector, )
