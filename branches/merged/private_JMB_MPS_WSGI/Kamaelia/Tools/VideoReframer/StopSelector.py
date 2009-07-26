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
