#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
==========================================
Publishing and Subscribing with Backplanes
==========================================

Backplanes provide a way to 'publish' data under a name, enabling other parts
of the system to 'subscribe' to it on the fly, without having to know about the
actual component(s) the data is coming from.

It is a quick and easy way to distribute or share data. Think of them like
backplane circuit boards - where other circuit boards can plug in to send or
receive any signals they need.



Example usage
-------------

A system where several producers publish data, for consumers to pick up::

    Pipeline( Producer1(),
              PublishTo("DATA")
            ).activate()

    Pipeline( Producer2(),
              PublishTo("DATA")
            ).activate()

    Pipeline( SubscribeTo("DATA"),
              Consumer1(),
            ).activate()
            
    Pipeline( SubscribeTo("DATA"),
              Consumer2(),
            ).activate()
            
    Backplane("DATA").run()

A server where multiple clients can connect and they all get sent the same data
at the same time::
    
    Pipeline( Producer(),
              PublishTo("DATA")
            ).activate()

    SimpleServer(protocol=SubscribeTo("DATA"), port=1500).activate()

    Backplane("DATA").run()



More detail
-----------

The Backplane component collects data from publishers and sends it out to
subscribers.

You can have as many backplanes as you like in a running system - provided they
all register under different names.

A backplane can have multiple subscribers and multiple publishers. Publishers
and subscribers can be created and destroyed on the fly.

To shut down a PublishTo() component, send a producerFinished() or
shutdownMicroprocess() message to its "control" inbox. This does *not* propagate
and therefore does *not* cause the Backplane or any subscribers to terminate.

To shut down a SubscribeTo() component, send a producerFinished() or
shutdownMicroprocess() message to its "control" inbox. It will then immediately
forward the mesage on out of its "signal" outbox and terminate.

To shut down the Backplane itself, send a producerFinished() or
shutdownMicroprocess() message to its "control" inbox. It will then immediately
terminate and also propagate this message onto any subscribers (SubscribeTo
components), causing them to also terminate.



Implementation details
----------------------

Backplane is actually based on a Kamaelia.Util.Splitter.PlugSplitter component,
and the SubscribeTo component is a wrapper around a Kamaelia.Util.Splitter.Plug.

The Backplane registers itself with the coordinating assistant
tracker.
 
* Its "inbox" inbox is registered under the name "Backplane_I_<name>"
* Its "configuration" inbox is registered under the name "Backplane_O_<name>"

PublishTo components look up the "Backplane_I_<name>" service and simply forward
data sent to their "inbox" inboxes direct to the "inbox" inbox of the
PlugSplitter - causing it to be distributed to all subscribers.

SubscribeTo components look up the "Backplane_O_<name>" service and request to
have their "inbox" and "control" inboxes connected to the PlugSplitter.
SubscribeTo then forwards on any messages it receives out of its "outbox" and
"signal" outboxes respectively.

The PlugSplitter component's "control" inbox and "signal" outbox are not
advertised as services. To shut down a Backplane you must therefore send a
shutdownMicroprocess() or producerFinished() message directly to its "control"
inbox. When this happens, the shutdown message will be forwarded on to all
subscribers - causing SubscribeTo components to also shut down.

"""
import Axon
from Axon.Ipc import newComponent, producerFinished, shutdownMicroprocess
from Kamaelia.Util.Splitter import PlugSplitter as Splitter
from Kamaelia.Util.Splitter import Plug
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
from Kamaelia.Util.PassThrough import PassThrough

class Backplane(Axon.Component.component):
    """\
    Backplane(name) -> new Backplane component.

    A named backplane to which data can be published for subscribers to pick up.
    
    * Use PublishTo components to publish data to a Backplane.
    * Use SubscribeTo components to receive data published to a Backplane.

    Keyword arguments:

    - name  -- The name for the backplane. publishers and subscribers connect to this by using the same name.
    """

    Inboxes = { "inbox"   : "NOT USED",
                "control" : "Shutdown signalling (shuts down the backplane and all subscribers",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling",
               }
    
    def __init__(self, name):
        super(Backplane,self).__init__()
        assert name == str(name)
        self.name = name
        self.splitter = Splitter()

        splitter = self.splitter
        cat = CAT.getcat()
        try:
            cat.registerService("Backplane_I_"+self.name, splitter, "inbox")
            cat.registerService("Backplane_O_"+self.name, splitter, "configuration")
        except Axon.AxonExceptions.ServiceAlreadyExists, e:
            print "***************************** ERROR *****************************"
            print "An attempt to make a second backplane with the same name happened."
            print "This is incorrect usage."
            print 
            traceback.print_exc(3)
            print "***************************** ERROR *****************************"


            raise e
    def main(self):
        """Main loop."""
        self.link((self,"control"),(self.splitter,"control"), passthrough=1)
        self.link((self.splitter,"signal"),(self,"signal"), passthrough=2)
        
        yield newComponent(self.splitter)
        self.addChildren(self.splitter)
        self.splitter = None
        # FIXME: If we had a way of simply getting this to "exec" a new component in our place,
        # FIXME: then this while loop here would be irrelevent, which would be cool.
        while not self.childrenDone():
            self.pause()
            yield 1
            
        cat = CAT.getcat()
        cat.deRegisterService("Backplane_I_"+self.name)
        cat.deRegisterService("Backplane_O_"+self.name)

    def childrenDone(self):
        """\
        Unplugs any children that have terminated, and returns true if there are no
        running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())


class PublishTo(Axon.Component.component):
    """\
    PublishTo(destination) -> new PublishTo component

    Publishes data to a named Backplane. Any data sent to the "inbox" inbox is
    sent to all (any) subscribers to the same named Backplane.

    Keyword arguments:

    - destination  -- the name of the Backplane to publish data to
    """
    
    Inboxes = { "inbox"   : "Send to here data to be published to the backplane",
                "control" : "Shutdown signalling (doesn't shutdown the Backplane)",
              }
    Outboxes = { "outbox" : "NOT USED",
                 "signal" : "Shutdown signalling",
               }
    
    def __init__(self, destination):
        super(PublishTo, self).__init__()
        self.destination = destination
    def main(self):
        """Main loop."""
        cat = CAT.getcat()
        service = cat.retrieveService("Backplane_I_"+self.destination)
        self.link((self,"inbox"), service, passthrough=1)
        # FIXME: If we had a way of simply getting this to "exec" a new component in our place,
        # FIXME: then this while loop here would be irrelevent, which would be cool.
        # FIXME: especially if we could exec in such a way that passthrough linkages
        # FIXME: still operated as you'd expect.
        shutdown=False
        while not shutdown:
            while self.dataReady("control"):
                msg=self.recv("control")
                self.send(msg,"signal")
                if isinstance(msg, (producerFinished,shutdownMicroprocess)):
                    shutdown=True
                    
            if not shutdown:
                self.pause()
                yield 1            
            
            
class SubscribeTo(Axon.Component.component):
    """\
    SubscribeTo(source) -> new SubscribeTo component

    Subscribes to a named Backplane. Receives any data published to that
    backplane and sends it on out of its "outbox" outbox.

    Keyword arguments:

    - source  -- the name of the Backplane to subscribe to for data
    """
    
    Inboxes = { "inbox"   : "NOT USED",
                "control" : "Shutdown signalling (doesn't shutdown the Backplane)",
              }
    Outboxes = { "outbox" : "Data received from the backplane (that was published to it)",
                 "signal" : "Shutdown signalling",
               }
    
    def __init__(self, source):
        super(SubscribeTo, self).__init__()
        self.source = source
    def main(self):
        """Main loop."""
        cat = CAT.getcat()
        splitter,configbox = cat.retrieveService("Backplane_O_"+self.source)
        p = PassThrough()
        plug = Plug(splitter, p)
        self.link( (self, "control"), (plug, "control"), passthrough=1)
        self.link( (plug,"outbox"), (self,"outbox"), passthrough=2)
        self.link( (plug,"signal"), (self,"signal"), passthrough=2)
        self.addChildren(plug)
        yield newComponent(plug)
        # wait until all child component has terminated
        # FIXME: If we had a way of simply getting this to "exec" a new component in our place,
        # FIXME: then this while loop here would be irrelevent, which would be cool.
        # FIXME: especially if we could exec in such a way that passthrough linkages
        # FIXME: still operated as you'd expect.
        while not self.childrenDone():
            self.pause()
            yield 1


    def childrenDone(self):
        """\
        Unplugs any children that have terminated, and returns true if there are no
        running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())


__kamaelia_components__ = ( Backplane, PublishTo, SubscribeTo, )
            
# deprecation stubs

import Kamaelia.Support.Deprecate as Deprecate

publishTo = Deprecate.makeClassStub(
    PublishTo,
    "Use Kamaelia.Util.Backplane:PublishTo instead of Kamaelia.Util.Backplane:publishTo",
    "WARN"
    )

subscribeTo = Deprecate.makeClassStub(
    SubscribeTo,
    "Use Kamaelia.Util.Backplane:SubscribeTo instead of Kamaelia.Util.Backplane:subscribeTo",
    "WARN"
    )




















