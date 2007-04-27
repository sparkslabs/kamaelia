#!/usr/bin/env python

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
This is a modification to detect only components registered as children, or
deeper descendants of a specified component. But note - that component is
not adopted as a child (yet)

===============================================
Detecting the topology of a running Axon system
===============================================

The Introspector component introspects the current local topology of an Axon
system - that is what components there are and how they are wired up.

It continually outputs any changes that occur to the topology.



Example Usage
-------------
Introspect and display whats going on inside the system::
    MyComplexSystem().activate()
    
    pipeline( Introspector(),
              AxonVisualiserServer(noServer=True),
            )



How does it work?
-----------------

Once activated, this component introspects the current local topology of an Axon
system.

Local? This component examines its scheduler to find components and postmen.
It then examines them to determine their inboxes and outboxes and the linkages
between them. In effect, it determines the current topology of the system.
    
If this component is not active, then it will see no scheduler and will report
nothing.

What is output is how the topology changes. Immediately after activation, the
topology is assumed to be empty, so the first set of changes describes adding
nodes and linkages to the topology to build up the current state of it.

Subsequent output just describes the changes - adding or deleting linkages and
nodes as appropriate.

Nodes in the topology represent components and postboxes. A linkage between
a component node and a postbox node expresses the fact that that postbox belongs
to that component. A linkage between two postboxes represents a linkage in the
Axon system, from one component to another.

This topology change data is output as string containing one or more lines. It
is output through the "outbox" outbox. Each line may be one of the following::

* "DEL ALL\n"
  - the first thing sent immediately after activation - to ensure that
    the receiver of this data understand that we are starting from nothing

* "ADD NODE <id> <name> randompos component\n"
  "ADD NODE <id> <name> randompos inbox\n"
  "ADD NODE <id> <name> randompos outbox\n"
  - an instruction to add a node to the topology, representing a component,
    inbox or outbox. <id> is a unique identifier. <name> is a 'friendly'
    textual label for the node.

* "DEL NODE <id>"
  - an instruction to delete a node, specified by its unique id
    
* "ADD LINK <id1> <id2>"
  - an instruction to add a link between the two identified nodes. The link is
    deemed to be directional, from <id1> to <id2>

* "DEL LINK <id1> <id2>"
  - an instruction to delete any link between the two identified nodes. Again,
    the directionality is from <id1> to <id2>.

the <id> and <name> fields may be encapsulated in double quote marks ("). This
will definitely be so if they contain space characters.

If there are no topology changes then nothing is output.

This component ignores anything arriving at its "inbox" inbox.

If a shutdownMicroprocess message is received on the "control" inbox, it is sent
on to the "signal" outbox and the component will terminate.
"""


import Axon

class Introspector(Axon.Component.component):
    """\
    Introspector(*components) -> new Introspector component.

    Outputs topology (change) data describing the specified component and its
    descendants and how they are wired inside a running Axon system.
    """

    Inboxes  = { "inbox"   : "NOT USED",
                 "control" : "Shutdown signalling",
               }
    Outboxes = { "outbox" : "Topology (change) data describing the Axon system",
                 "signal" : "Shutdown signalling",
               }
    
    # passthrough==0 -> outbox > inbox
    # passthrough==1 -> inbox > inbox
    # passthrough==2 -> outbox > outbox
    srcBoxType = { 0:"o", 1:"i", 2:"o" }
    dstBoxType = { 0:"i", 1:"i", 2:"o" }

    def __init__(self, *components):
        """x.__init__(...) initializes component. See x.__class__.__doc__ for signature"""
        super(Introspector,self).__init__()
        self.targets = list(components)
    
    def main(self):
        """Main loop."""
        # reset the receiving 'axon visualiser'
        self.send("DEL ALL\n", "outbox")
        yield 1
        
        nodes = dict()
        linkages = dict()
        while 1:
            # shutdown if requested
            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data, Axon.Ipc.shutdownMicroprocess):
                    self.send(data, "signal")
                    return
        
            oldNodes    = nodes
            oldLinkages = linkages
            
            nodes    = dict()
            linkages = dict()
        
            components, postboxes,linkages = self.introspect()
            # now it is safe to yield if we wish to, since we've not snapshotted all system state we need

            # now go through building the new set of nodes
            # if we find one already in oldNodes, delete it from there,
            # so that at the end oldNodes contains only 'differences'
            # if not already there, then add it to the 'addmsgs' output
            
            # if the node being added is a postbox, then also build the
            # 'add link' message to join it to its parent component
            addnodemsgs = ""
            rennodemsgs = ""
            delnodemsgs = ""
            addlinkmsgs = ""
            dellinkmsgs = ""
                                    
            # build topology nodes - one node per component, one per postbox on each component
            for id in components.iterkeys():
                if not nodes.has_key(id):         # incase component activated twice (twice in scheduler.threads)
                    name = components[id]
                    name = name[:name.rfind("_")] # strip off trailing "_XX" where XX is numerical UID
                    nodes[id] = name
                    if oldNodes.has_key( id ):
                        # if node previously existed, but has changed in some way...
                        if oldNodes[id] != name:
                            rennodemsgs += 'UPDATE_NAME NODE "'+self.esc(str(id))+'" "'+self.esc(str(name))+'"\n'
                        del oldNodes[id]
                    else:
                        addnodemsgs += 'ADD NODE "'+self.esc(str(id))+'" "'+self.esc(str(name))+'" randompos component\n'

            # build nodes for postboxes, and also link them to the components to which they belong
            for id in postboxes:
                if not nodes.has_key(id):
                    nodes[ id ] = name
                    if oldNodes.has_key( id ):
                        del oldNodes[id]
                    else:
                        (cid, io, name) = id
                        addnodemsgs += 'ADD NODE "'+self.esc(str(id))+'" "'+self.esc(str(name))+'" randompos '
                        if io=="i":
                            addnodemsgs += "inbox\n"
                        else:
                            addnodemsgs += "outbox\n"
                        addnodemsgs += 'ADD LINK "'+self.esc(str(cid))+'" "'+self.esc(str(id))+'"\n'
                        
            # now addmsgs contains msgs to create new nodes
            # and oldNodes only contains nodes that no longer exist
            
            for id in oldNodes.iterkeys():
                delnodemsgs += 'DEL NODE "'+self.esc(str(id))+'"\n'
            
            # now go through inter-postbox linkages and do the same as we did for nodes
            # note, we check not only that the link exists, but that it still goes to the same thing!
            # otherwise leave the old link to be destroyed, and add a new one
            for (src,dst) in linkages.iterkeys():
                if oldLinkages.has_key((src, dst)): 
                    del oldLinkages[(src,dst)]
                else:
                    addlinkmsgs += 'ADD LINK "'+self.esc(str(src))+'" "'+self.esc(str(dst))+'"\n'
                    
            # delete linkages that no longer exist
            for (src,dst) in oldLinkages.iterkeys():
                dellinkmsgs += 'DEL LINK "'+self.esc(str(src))+'" "'+self.esc(str(dst))+'"\n'

            # note: order of the final messages is important - delete old things
            # before adding new
            # and del links before nodes and add nodes before links
            msg = dellinkmsgs + delnodemsgs + addnodemsgs + rennodemsgs + addlinkmsgs
            if msg.strip() != "":
                self.send(msg, "outbox")
                
            yield 1

    def introspect(self):
        """\
        introspect() -> components, postboxes, linkages

        Returns the current set of components, postboxes and interpostbox linkages.

        - components  -- a dictionary, containing components as keys
        - postboxes   -- a list of (component.id, type, "boxname") tuples, where type="i" (inbox) or "o" (outbox)
        - linkages    -- a dictionary containing (postbox,postbox) tuples as keys, where postbox is a tuple from the postboxes list
        """
        
        # starting with the specified component, enumerate its children, then
        # its childrens' children etc...
        components = self.targets[:]
        for c in components:
            components.extend(c.childComponents())
        
        components = dict([ (p,(p.id,p.name)) for p in components])
        
        
        # go through all postmen and find all linkages
        linkages = {}
        for postman in [ p.postoffice for p in components.iterkeys() ]:
            for link in postman.linkages:
                # some components may not be within the scope of the children
                # we are concerned with, so we need to not include those
                # linkages
                if components.has_key(link.source):
                    if components.has_key(link.sink):
                        src = (link.source.id, Introspector.srcBoxType[link.passthrough], link.sourcebox)
                        dst = (link.sink.id  , Introspector.dstBoxType[link.passthrough], link.sinkbox)
                        linkages[(src,dst)] = 1
        
        # now we have a comprehensive list of all components (not just those the scheduler
        # admits to!) we can now build the list of all postboxes
        postboxes = []
        for c in components.iterkeys():
            postboxes += [ (c.id, "i", boxname) for boxname in c.inboxes.keys()  ]
            postboxes += [ (c.id, "o", boxname) for boxname in c.outboxes.keys() ]
        
        # strip the direct reference to component objects from the dictionary, leaving
        # just a mapping from 'id' to 'name'
        cdict = dict([ components[c] for c in components.iterkeys() ])
        
        return cdict, postboxes, linkages
        
    def esc(self, s):
        s=s.replace('\\','\\\\')
        s=s.replace('"','\\"')
        s=s.replace("'","\\'")
        return s

if __name__ == '__main__':

   c1 = Axon.Component.component().activate()
   c2 = Axon.Component.component().activate()
   c1.link( (c1,"outbox"), (c2,"inbox") )
   i = Introspector(c1,c2)
   i.activate()
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   e = consoleEchoer()
   e.activate()
   i.link((i,"outbox"), (e, "inbox"))
   
   print "You should see the Introspector finds only a 'Component'."
   print "With standard inbox, control, signal and outbox postboxes"
   print
   Axon.Scheduler.scheduler.run.runThreads(slowmo=0)
