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
=====================
One-shot sending data
=====================

OneShot and TriggeredOneShot send a single specified item to their "outbox"
outbox and immediately terminate.

TriggeredOneShot waits first for anything to arrive at its "inbox" inbox,
whereas OneShot acts as soon as it is activated.


Example Usage
-------------

A way to create a component that writes data to a given filename, based on
(filename,data) messages sent to its "next" inbox::

    Carousel( lambda filename, data :
                Pipeline( OneShot(data),
                          SimpleFileWriter(filename),
                        ),
            )

A graphline that opens a TCP connection to myserver.com port 1500, and sends an
a one off message::

    Pipeline( OneShot("data to send to server"),
              TCPClient("myserver.com", 1500),
            ).run()

Shutting down a connection to myserver.com port 1500 as soon as a reply is
received from the server::
    
    Graphline( NET   = TCPClient("myserver.com", 1500),
               SPLIT = TwoWaySplitter(),
               STOP  = TriggeredOneShot(producerFinished()),
               linkages = {
                   ("", "inbox" )      : ("NET", "inbox"),
                   ("NET", "outbox")   : ("SPLIT", "inbox"),
                   ("SPLIT", "outbox") : ("", "outbox"),
                   
                   ("SPLIT", "outbox2") : ("STOP", "inbox"),
                   ("STOP", "outbox")   : ("NET", "control"),
                   ("", "control")      : ("NET", "control"),
                   ("NET", "signal")    : ("SPLIT", "control"),
                   ("SPLIT", "signal")  : ("", "signal"),
                   ("SPLIT", "signal2"),: ("STOP", "control"),
               },
             )



OneShot Behaviour
-----------------

At initialisation, specify the message to be sent by OneShot.

As soon as OneShot is activated, the specified message is sent out of the
"outbox" outbox. A producerFinished message is also sent out of the "signal"
outbox. The component then immediately terminates.



TriggeredOneShot Behaviour
--------------------------

At initialisation, specify the message to be sent by TriggeredOneShot.

Send anything to the "inbox" inbox and TriggeredOneShot will immediately send
the specified message out of the "outbox" outbox. A producerFinished message is
also sent out of the "signal" outbox. The component then immediately terminates.

If a producerFinished or shutdownMicroprocess message is received on the
"control" inbox. It is immediately sent on out of the "signal" outbox and the
component then immediately terminates.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class OneShot(component):
    """\
    OneShot(msg) -> new OneShot component.
    
    Immediately sends the specified message and terminates.
    
    Keyword arguments::
        
    - msg  -- the message to send out
    """
    
    Inboxes = { "inbox"   : "NOT USED",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Item is sent out here",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, msg=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(OneShot, self).__init__()
        self.msg = msg
    
    def main(self):
        """Main loop"""
        self.send(self.msg,"outbox")
        yield 1
        self.send(producerFinished(self),"signal")


class TriggeredOneShot(component):
    """\
    OneShot(msg) -> new OneShot component.
    
    Waits for anything to arrive at its "inbox" inbox, then immediately sends
    the specified message and terminates.
    
    Keyword arguments::
        
    - msg  -- the message to send out
    """
    
    Inboxes = { "inbox"   : "Anything, as trigger",
                "control" : "Shutdown signalling",
              }
    Outboxes = { "outbox" : "Item is sent out here",
                 "signal" : "Shutdown signalling",
               }
               
    def __init__(self, msg=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(TriggeredOneShot, self).__init__()
        self.msg = msg
        
    def main(self):
        """Main loop"""
        while not self.dataReady("inbox"):
            while self.dataReady("control"):
                msg = self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                    return
            self.pause()
            yield 1
        
        self.recv("inbox")
        self.send(self.msg,"outbox")
        yield 1
        self.send(producerFinished(self),"signal")


__kamaelia_components__ = ( OneShot, TriggeredOneShot, )
