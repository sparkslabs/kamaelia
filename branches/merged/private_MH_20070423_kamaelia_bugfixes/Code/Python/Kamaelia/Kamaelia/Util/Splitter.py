#!/usr/bin/env python2.3
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
"""\
=========================
Simple Fanout of messages
=========================

A component that splits a data source, fanning it out to multiple destinations.



Example Usage
-------------

Component connecting to a Splitter::

    class Consumer(Axon.Component.component):
        Outboxes = [ "outbox", "signal", "splitter_config" ]
        
        def main(self):
             self.send( addsink( self, "inbox", "control" ), "splitter_config")
             yield 1
             ... do stuff when data is received on "inbox" inbox

    mysplitter = Splitter()
    Pipeline( producer(), mysplitter ).activate()
    
    myconsumer = Consumer().activate()
    myconsumer.link( (myconsumer, "splitter_config"), ("mysplitter", "configuration") )



How does it work?
-----------------

Any data sent to the component's "inbox" inbox is sent out to multiple
destinations (but not to the "outbox" outbox).

Add a destination by sending an addsink(...) message to the "configuration"
inbox of the component. Splitter will then wire up to the 'sinkbox' inbox
specified in the message, and send it any data sent to its "inbox" inbox.

NOTE: Splitter only does this for the 'sinkbox' inbox, not for the
'sinkcontrol' inbox. If one is specified, it is ignored.

There is no limit on the number of 'sinks' that can be connected to the
splitter. The same component can add itself as a sink multiple times, provided
different named inboxes are used each time.

NOTE: The data is not duplicated - the same item is sent to all destinations.
Care must therefore be taken if the data item is mutable.

If one or more destinations cause a noSpaceInBox exception, the data item will
be queued, and Splitter will attempt to resend it to the destinations in
question until successful. It will stop forwarding any new incoming data until
it has succeeded, thereby ensuring the order of data is not altered.

Stop data being sent to a destination by sending a removesink(...) message to
the "configuration" inbox of the Splitter component. Splitter will then cease
sending messages to the 'sinkbox' inbox specified in the message and will
unwire from it.

Any messages sent to the "control" inbox are ignored. The "outbox" and "signal"
outboxes are not used.

This component does not terminate.



============================
Pluggable Fanout of messages
============================

The PlugSplitter component splits a data source, fanning it out to multiple
destinations. The Plug component allows you to easily 'plug' a destination
into the splitter.



Example Usage
-------------

Two consumers receiving the same data from a single consumer. Producer and
consumers are encapsulated by PlugSplitter and Plug components respectively::

    mysplitter = PlugSplitter( producer() ).activate()
    
    Plug(mysplitter, consumer() ).activate()
    Plug(mysplitter, consumer() ).activate()
    
The same, but the producer and consumers are not encapsulated::

    mysplitter = PlugSplitter()
    Pipeline( producer, mysplitter ).activate()
    
    Pipeline( Plug(mysplitter), consumer() ).activate()
    Pipeline( Plug(mysplitter), consumer() ).activate()
    
    
    
How does it work?
-----------------

Any data sent to the component's "inbox" and "control" inboxes is sent out to
multiple destinations. It is also sent onto the components "outbox" and
"signal" outboxes, respectively.

Alternatively, initialisation you can specify a 'source' component. If you do,
then data to be sent out to multiple destinations is instead received from that
component's "outbox" and "signal" outboxes, respectively. Any data sent to the
"inbox" and "control" inboxes of the PlugSplitter component will be forwarded
to the "inbox" and "control" inboxes of the 'source' component, respectively.

This source component is encapsulated as a child within the PlugSplitter
component, and so must not be separately activated. Activating PlugSplitter
will also activate this child component.

Add a destination by making a Plug component, specifying the PlugSplitter
component to 'plug into'. See documentation for the Plug component for more
information.

Alternatively, you can add and remove destinations manually:

* Add a destination by sending an addsink(...) message to the "configuration"
  inbox of the component.
  
  If a 'sinkbox' inbox is specified in the message, then
  PlugSplitter will wire up to it and forward to it any 'inbox'/'outbox' data.
  If a 'sinkcontrol' inbox is specified, then Plugsplitter will wire up to it
  and forward to it any 'control'/'signal' data.
  
* Stop data being sent to a destination by sending a removesink(...) message to
  the "configuration" inbox of the Splitter component.
  
  Splitter will then cease
  sending messages to the 'sinkbox' inbox specified in the message and will
  unwire from it.

There is no limit on the number of 'sinks' that can be connected to the
splitter. The same component can add itself as a sink multiple times, provided
different named inboxes are used each time.

NOTE: The data is not duplicated - the same item is sent to all destinations.
Care must therefore be taken if the data item is mutable.

If a shutdownMicroprocess or producerFinished message is received on the 
"control" inbox and there is NO 'source' child component, then the message is
forwarded onto all 'control' destinations and the 'signal' outbox. The 
component then immediately terminates, unwiring from all destinations.

If there is a child component then PlugSplitter will terminate when the child
component terminates, unwiring from all destinations.



=====================
Plug for PlugSplitter
=====================

The Plug component 'plugs into' a PlugSplitter as a destination to which the
source data is split.



Example Usage
-------------
See PlugSplitter documentation.



How does it work?
-----------------

Initialise the Plug component by specifying a PlugSplitter component to connect
to and the component that wants to receive the data from the Plugsplitter.

The destination/sink component is encapsulated as a child component, and is
therefore activated by the Plug component when it is activated. Do not activate
it yourself.

The Plug component connects to the PlugSplitter component by wiring its
"splitter_config" outbox to the "configuration" inbox of the PlugSplitter
component and sending it an addsink(...) message. This causes PlugSplitter
to wire up to the Plug's "inbox" and "control" inboxes.

The Plug's "inbox" and "control" inboxes are forwarded to the "inbox" and
"control" inboxes of the child component respectively. The "outbox" and
"signal" outboxes of the child component are forwarded to the "outbox" and
"signal" outboxes of the Plug component respectively.

When the child component terminates, the Plug component sends a removesink(...)
message to the PlugSplitter, causing PlugSplitter to unwire from it. It then
terminates.




Thoughts
--------

PlugSplitter is probably more reliable than Splitter however it *feels* too
complex. However the actual "Splitter" class in this file is not the
preferable option.
"""



import Axon.AdaptiveCommsComponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, ipc
from Axon.Linkage import linkage
from Axon import Ipc


class addsink(ipc):
    """\
    addsink(sink[,sinkbox][,sinkcontrol][passthrough]) -> new addsink message.
    
    Message specifying a target component and inbox(es), requesting they be
    wired to receive a data source (to be the data sink).
    
    Keywork arguments:
    
    - sink         -- target component
    - sinkbox      -- target component's inbox name (default="inbox")
    - sinkcontrol  -- None, or target component's 'control' inbox name (default=None)
    - passthrough  -- 0, or 1 if linkage is inbox-inbox, or 2 if outbox-outbox (default=0)
    """
    def __init__(self, sink, sinkbox="inbox", sinkcontrol = None, passthrough=0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.sink = sink
        self.sinkbox = sinkbox
        self.sinkcontrol = sinkcontrol
        self.passthrough = passthrough


class removesink(ipc):
    """\
    removesink(sink[,sinkbox][,sinkcontrol]) -> new removesink message.
    
    Message specifying a target component and inbox(es), requesting they be
    unwired from a data source (no longer act as a data sink)
    """
    def __init__(self, sink, sinkbox="inbox", sinkcontrol = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.sink = sink
        self.sinkbox = sinkbox
        self.sinkcontrol = sinkcontrol



class Splitter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
   """\
   Splitter() -> new Splitter component.
   
   Splits incoming data out to multiple destinations. Send addsink(...) and
   removesink(...) messages to the 'configuration' inbox to add and remove
   destinations.
   """
   #inbox is the box for data too be split.  control is for future use to also split the signal/control data
   #associated with the main data.  configuration is the port to send requests for extra outward connections
   #and for deletions.
      
   Inboxes = { "inbox"   : "Source of data items", 
               "control" : "NOT USED", 
               "configuration" : "addsink(...) and removesink(...) request messages",
             }
   Outboxes = { "outbox" : "NOT USED",
                "signal" : "NOT USED",
              }

   def __init__(self):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      super(Splitter,self).__init__()
      #outlist is for tuples of (sinkcomponent, sinkbox) to a tuple of (outboxname, linkage)
      self.outlist = {}
   
   def mainBody(self):
         """Main loop body."""
         postponedmesage = None
         self.delayedboxlist = []
         dontpause = False # Assumption is that we should be able to pause after finishing
         if self.dataReady("configuration"):
            mes = self.recv("configuration")
            dontpause = True
            if isinstance(mes, addsink):
               self.createsink(mes.sink,mes.sinkbox, mes.passthrough)
            elif isinstance(mes,removesink):
               self.deletesink(mes)
         if postponedmesage:
            mes,bl = postponedmesage, self.delayedboxlist
            postponedmesage, self.delayedboxlist = None, []
            for box in bl:
                try:
                    self.send(mes,self.outlist[box][0])
                except noSpaceInBox:
                    postponedmesage = mes
                    self.delayedboxlist.append(box)
         if self.dataReady() and not postponedmesage:
            mes = self.recv()
            dontpause = True
            for box in self.outlist:
               try:
                  self.send(mes,self.outlist[box][0])
               except noSpaceInBox:
                  postponedmesage = mes
                  self.delayedboxlist.append(box)
         if postponedmesage or not dontpause:
            self.pause()
         return 1

   def createsink(self, sink, sinkbox="inbox", passthrough=0):
      """\
      Set up a new destination for data.
      
      Creates an outbox, links it to the target (component,inbox) and records
      it in self.outlist.
      """
      name = self.addOutbox(sink.name + '-' + sinkbox)
      lnk = linkage(source = self, sourcebox = name, sink = sink, sinkbox = sinkbox, postoffice = self.postoffice, passthrough=passthrough)
      self.outlist[(sink,sinkbox)] = (name, lnk)
   
   def deletesink(self, oldsink):
      """\
      Removes the specified (component, inbox) as a destination for data
      where (component, inbox) = (oldsink.sink, oldsink.sinkbox).
      
      Unlinks the target, destroys the corresponding outbox, and removes the
      corresponding record from self.outlist.
      """
      sink = self.outlist[(oldsink.sink,oldsink.sinkbox)]
      del self.outlist[(oldsink.sink,oldsink.sinkbox)]
      self.unlink(thelinkage=sink[1])
      self.deleteOutbox(sink[0])
      try:
        self.delayedboxlist.remove(sink[0])
      except ValueError:
        pass # Common occurence, not an error.


   
class PlugSplitter(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    PlugSplitter([sourceComponent]) -> new PlugSplitter component.
    
    Splits incoming data out to multiple destinations. Send addsink(...) and
    removesink(...) messages to the 'configuration' inbox to add and remove
    destinations.
    
    Keyword arguments:
    
    - sourceComponent  -- None, or component to act as data source
    """

    Inboxes = { "inbox"         : "Data items to be fanned out.",
                "control"       : "Shutdown signalling, and signalling to be fanned out.",
                "configuration" : "addsink(...) and removesink(...) request messages",
                "_inbox"        : "Internal inbox for receiving from the child source component (if it exists)",
                "_control"      : "Internal inbox for receiving from the child source component (if it exists)",
              }
    Outboxes = { "outbox" : "Data items received on 'inbox' inbox.",
                 "signal" : "Shutdown signalling, and data items received on 'control' inbox.",
               }

    def __init__(self, sourceComponent = None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PlugSplitter,self).__init__()

        # set of wired in destinations (other than std 'outbox' and 'signal'
        self.outboxsinks = {}   #  (component, inboxname) --> splitter outboxname
        self.signalsinks = {}   #  (component, inboxname) --> splitter outboxname

        if sourceComponent != None:
            self.addChildren(sourceComponent)
            self.link( (self, "inbox"), (sourceComponent, "inbox"), passthrough=1)
            self.link( (self, "control"), (sourceComponent, "control"), passthrough=1)
            self.link( (sourceComponent, "outbox"), (self, "_inbox") )
            self.link( (sourceComponent, "signal"), (self, "_control") )
            self.inboxname = "_inbox"
            self.controlname = "_control"
            self.usingChild = True
        else:
            self.inboxname = "inbox"
            self.controlname = "control"
            self.usingChild = False


    def main(self):
        """Main loop."""

        # activate the child (if we have one)
        yield Ipc.newComponent( *(self.childComponents()) )

        done=False
        while not done:

            # check for requests to add/remove destinations
            while self.dataReady("configuration"):
                config = self.recv("configuration")
                if isinstance(config, addsink):
                    self._addSink(config.sink, config.sinkbox, config.sinkcontrol)
                elif isinstance(config, removesink):
                    self._delSink(config.sink, config.sinkbox, config.sinkcontrol)

            # pass anything received on 'inbox' inbox
            while self.dataReady(self.inboxname):
                data = self.recv(self.inboxname)
                self.send(data, "outbox")
                for (boxname, linkage) in self.outboxsinks.values():
                    self.send(data, boxname)

            # pass anything received on 'control' inbox
            while self.dataReady(self.controlname):
                msg = self.recv(self.controlname)
                self.send(msg, "signal")
                for (boxname, linkage) in self.signalsinks.values():
                    self.send(msg, boxname)

                # if we don't have a child component, we should shutdown in
                # response to msgs
                if not self.usingChild:
                    if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                        done = True


            # if we have a child, we'll shutdown when the child dies
            if self.usingChild:
                if self.childrenDone():
                    done=True

            # if we don't have a child, we know we'll be shutting down outselves
            # in response to a message received on 'control', so we can block
            # awaiting new data on inboxes
            if not self.usingChild:
                if not done:
                    self.pause()

            yield 1

        # unlink and cleanup on exit - unwire any destinations still connected
        for (sink, box) in self.outboxsinks.keys():
            self._delSink(sink, box, None)
        for (sink, box) in self.signalsinks.keys():
            self._delSink(sink, None, box)


    def childrenDone(self):
        """\
        Unplugs any children that have terminated, and returns true if there are no
        running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())


    def _addSink(self, sink, sinkinbox=None, sinkcontrol=None):
        """\
        Add a new destination for data.
        
        Specify target component (sink), and target inbox (sinkinbox) and/or 
        target shutdown signalling inbox (sinkcontrol).
        """
        if sinkinbox != None:
            dst = (sink,sinkinbox)
            if dst not in self.outboxsinks:
                outboxname = self.addOutbox("outbox")
                linkage = self.link( (self, outboxname), dst )
                self.outboxsinks[dst] = outboxname, linkage

        if sinkcontrol != None:
            dst = (sink, sinkcontrol)
            if dst not in self.signalsinks:
                outboxname = self.addOutbox("signal")
                linkage = self.link( (self, outboxname), dst )
                self.signalsinks[dst] = outboxname, linkage


    def _delSink(self, sink, sinkinbox=None, sinkcontrol=None):
        """\
        Remove a destination for data.
        
        Specify target component (sink), and target inbox (sinkinbox) and/or
        target shutdown signalling inbox (sinkcontrol).
        """
        if sinkinbox != None:
            dst = (sink,sinkinbox)
            try:
                boxname, linkage = self.outboxsinks[dst]
                self.unlink(thelinkage = linkage)
                self.deleteOutbox(boxname)
                del self.outboxsinks[dst]
            except KeyError:
                pass

        if sinkcontrol != None:
            dst = (sink, sinkcontrol)
            try:
                boxname, linkage = self.signalsinks[dst]
                self.unlink(thelinkage = linkage)
                self.deleteOutbox(boxname)
                del self.signalsinks[dst]
            except KeyError:
                pass



class Plug(Axon.Component.component):
    """\
    Plug(splitter,component) -> new Plug component.
    
    A component that 'plugs' the specified component into the specified
    splitter as a destination for data.
    
    Keyword arguments:
    
    - splitter   -- splitter component to plug into (any component that accepts addsink(...) and removesink(...) messages on a 'configuration' inbox
    - component  -- component to receive data from the splitter
    """
    Inboxes = { "inbox"   : "Incoming data for child component",
                "control" : "Incoming control data for child component, and shutdown signalling",
              }
    Outboxes = { "outbox"          : "Outgoing data from child component",
                 "signal"          : "Outgoing control data from child component, and shutdown signalling",
                 "splitter_config" : "Used to communicate with the target splitter",
               }

    def __init__(self, splitter, component):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Plug, self).__init__()

        # wire up to the splitter and remember it
        self.pluglinkage = self.link( (self, "splitter_config"),
                                      (splitter, "configuration") )

        self.addChildren(component)

        # wire in the child component
        self.link( (self, "inbox"),   (component, "inbox"),   passthrough = 1)
        self.link( (self, "control"), (component, "control"), passthrough = 1)
        self.link( (component, "outbox"), (self, "outbox"),  passthrough = 2)
        self.link( (component, "signal"), (self, "signal"),  passthrough = 2)


    def main(self):
        """Main loop."""
        self.send( addsink( self, "inbox", "control" ), "splitter_config")

        # activate the child
        for child in self.childComponents():
            child.activate()

        # wait until all child component has terminated
        while not self.childrenDone():
            self.pause()
            yield 1

        # unplug from the splitter
        self.send( removesink( self, "inbox", "control" ), "splitter_config")
        yield 1  # allow the msg to be sent
        self.unlink(thelinkage = self.pluglinkage)


    def childrenDone(self):
        """\
        Unplugs any children that have terminated, and returns true if there are no
        running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us

        return 0==len(self.childComponents())

__kamaelia_components__  = ( Splitter, PlugSplitter, Plug, )
