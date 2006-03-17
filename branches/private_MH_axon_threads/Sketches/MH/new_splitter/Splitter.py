#!/usr/bin/env python
#
# Moved to: Kamaelia.Util.Splitter.
# class Splitter --> class PlugSplitter
#


import Axon
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, ipc
from Axon import Ipc


class addsink(ipc):
    """Message specifying a target component and inbox(es) to be wired to data sources"""
    def __init__(self, sink, sinkbox="inbox", sinkcontrol = None):
        self.sink = sink
        self.sinkbox = sinkbox
        self.sinkcontrol = sinkcontrol

class removesink(ipc):
    """Message specifying a target component and inbox(es) to be unwired from data sources"""
    def __init__(self, sink, sinkbox="inbox", sinkcontrol = None):
        self.sink = sink
        self.sinkbox = sinkbox
        self.sinkcontrol = sinkcontrol


class PlugSplitter(AdaptiveCommsComponent):
    """Experimental version of Splitter (written from scratch)

       Provides fan-out of incoming messages on both 'inbox' and 'control' to
       component's that request it (they specify which inbox(es) to send the data
       to.

       Also supports encapsulation of the source of its data - specifying a component
       in the initialiser for this class will wire that component in as the source
       feeding the splitter. This has been done to experiment with ways of expressing
       the wiring up of your system in a readable but neat fashion.
       
       This version is used by the pipe builder tool at present.
    """
    Inboxes = { "inbox":"",
                "control":"",
                "configuration":"",
                "_inbox":"Internal inbox for receiving from the child source component (if it exists)",
                "_control":"Internal inbox for receiving from the child source component (if it exists)",
              }

    def __init__(self, sourceComponent = None):
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
        """Unplugs any children that have terminated, and returns true if there are no
            running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us
    
        return 0==len(self.childComponents())


    def _addSink(self, sink, sinkinbox, sinkcontrol):
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


    def _delSink(self, sink, sinkinbox, sinkcontrol):
        if sinkinbox != None:
            dst = (sink,sinkinbox)
            try:
                boxname, linkage = self.outboxsinks[dst]
                self.postoffice.deregisterlinkage(thelinkage = linkage)
                self.deleteOutbox(boxname)
                del self.outboxsinks[dst]
            except KeyError:
                pass
            
        if sinkcontrol != None:
            dst = (sink, sinkcontrol)
            try:
                boxname, linkage = self.signalsinks[dst]
                self.postoffice.deregisterlinkage(thelinkage = linkage)
                self.deleteOutbox(boxname)
                del self.signalsinks[dst]
            except KeyError:
                pass



class Plug(Axon.Component.component):
    """A 'plug' for getting another component to 'plug-into' a splitter.
    
    A splitter is any component with a 'configuration' inbox that will accept
    addSink and removeSink messages.

    This component provides encapsulation for that which you wish to plug in.

    Usage:
        mysplitter = PlugSplitter(...)
        plug = Plug(mysplitter, Destination)

        mysplitter.activate()
        plug.activate()
    """
    Inboxes = { "inbox":"",
                "control":"",
              }
    Outboxes = { "outbox":"",
                 "signal":"",
                 "splitter_config":"Used to communicate with the target splitter"
               }
                
    def __init__(self, splitter, component):
        """Initialisation.
           splitter = the splitter you want to plug 'component' into
           component = the component to be plugged into 'splitter'
        """
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
        self.send( addsink( self, "inbox", "control" ), "splitter_config")

        # activate the child
        yield Ipc.newComponent( *(self.childComponents()) )
    
        # wait until all child component has terminated
        while not self.childrenDone():
            # can't self.pause() as child may not immediately terminate after
            # sending/receiving final piece of data
            yield 1

        # unplug from the splitter
        self.send( removesink( self, "inbox", "control" ), "splitter_config")
        yield 1  # allow the msg to be sent
        self.postoffice.deregisterlinkage(thelinkage = self.pluglinkage)


    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
            running child components left (ie. their microproceses have finished)
        """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)   # deregisters linkages for us
    
        return 0==len(self.childComponents())
            



        