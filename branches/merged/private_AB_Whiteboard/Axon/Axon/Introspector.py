#!/usr/bin/env python

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
===============================================
Detecting the topology of a running Axon system
===============================================

The Introspector is a component that introspects the current local topology of
an Axon system - that is what components there are and how they are wired up.

It continually outputs any changes that occur to the topology.



Example Usage
-------------

Introspect and display whats going on inside the system::
    
    MyComplexSystem().activate()
    
    pipeline( Introspector(),
              AxonVisualiserServer(noServer=True),
            )



More detail
-----------

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
is output through the "outbox" outbox. Each line may be one of the following:

* `"DEL ALL"`

  - the first thing sent immediately after activation - to ensure that
    the receiver of this data understand that we are starting from nothing

* `"ADD NODE <id> <name> randompos component"`
* `"ADD NODE <id> <name> randompos inbox"`
* `"ADD NODE <id> <name> randompos outbox"`

  - an instruction to add a node to the topology, representing a component,
    inbox or outbox. <id> is a unique identifier. <name> is a 'friendly'
    textual label for the node.

* `"DEL NODE <id>"`

  - an instruction to delete a node, specified by its unique id
    
* `"ADD LINK <id1> <id2>"`

  - an instruction to add a link between the two identified nodes. The link is
    deemed to be directional, from <id1> to <id2>

* `"DEL LINK <id1> <id2>"`

  - an instruction to delete any link between the two identified nodes. Again,
    the directionality is from <id1> to <id2>.

the <id> and <name> fields may be encapsulated in double quote marks ("). This
will definitely be so if they contain space characters.

If there are no topology changes then nothing is output.

This component ignores anything arriving at its "inbox" inbox.

If a shutdownMicroprocess message is received on the "control" inbox, it is sent
on to the "signal" outbox and the component will terminate.



How does it work?
-----------------

Every execution timeslice, Introspector queries its scheduler to obtain a list
of all components. It then queries the postoffice in each component to build a
picture of all linkages between components. It also builds a list of all inboxes
and outboxes on each component.

This is mapped to a list of nodes and linkages. Nodes being components and
postboxes; and linkages being what postboxes belong to what components, and what
postboxes are linked to what postboxes.

This is compared against the nodes and linkages from the previous cycle of
processing to determine what has changed. The changes are then output as a 
sequence of "ADD NODE", "DEL NODE", "ADD LINK" and "DEL LINK" commands.

"""


import Component
import Scheduler
import Ipc

class Introspector(Component.component):
    """\
    Introspector() -> new Introspector component.

    Outputs topology (change) data describing what components there are, and
    how they are wired inside the running Axon system.
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
                if isinstance(data, Ipc.shutdownMicroprocess):
                    self.send(data, "signal")
                    return
        
            if isinstance(self.scheduler, Scheduler.scheduler):
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
                delnodemsgs = ""
                addlinkmsgs = ""
                dellinkmsgs = ""
                                        
                # build topology nodes - one node per component, one per postbox on each component
                for id in components.iterkeys():
                    if not nodes.has_key(id):         # incase component activated twice (twice in scheduler.threads)
                        name = components[id]
                        nodes[ id ] = name
                        if oldNodes.has_key( id ):
                            del oldNodes[id]
                        else:
                            addnodemsgs += 'ADD NODE "'+str(id)+'" "'+str(name)+'" randompos component\n'

                # build nodes for postboxes, and also link them to the components to which they belong
                for id in postboxes:
                    if not nodes.has_key(id):
                        nodes[ id ] = name
                        if oldNodes.has_key( id ):
                            del oldNodes[id]
                        else:
                            (cid, io, name) = id
                            addnodemsgs += 'ADD NODE "'+str(id)+'" "'+str(name)+'" randompos '
                            if io=="i":
                                addnodemsgs += "inbox\n"
                            else:
                                addnodemsgs += "outbox\n"
                            addnodemsgs += 'ADD LINK "'+str(cid)+'" "'+str(id)+'"\n'
                            
                # now addmsgs contains msgs to create new nodes
                # and oldNodes only contains nodes that no longer exist
                
                for id in oldNodes.iterkeys():
                    delnodemsgs += 'DEL NODE "'+str(id)+'"\n'
                
                # now go through inter-postbox linkages and do the same as we did for nodes
                # note, we check not only that the link exists, but that it still goes to the same thing!
                # otherwise leave the old link to be destroyed, and add a new one
                for (src,dst) in linkages.iterkeys():
                    if oldLinkages.has_key((src, dst)): 
                        del oldLinkages[(src,dst)]
                    else:
                        addlinkmsgs += 'ADD LINK "'+str(src)+'" "'+str(dst)+'"\n'
                        
                # delete linkages that no longer exist
                for (src,dst) in oldLinkages.iterkeys():
                    dellinkmsgs += 'DEL LINK "'+str(src)+'" "'+str(dst)+'"\n'

                # note: order of the final messages is important - delete old things
                # before adding new
                # and del links before nodes and add nodes before links
                msg = dellinkmsgs + delnodemsgs + addnodemsgs + addlinkmsgs
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
        
        # fetch components currently active with the scheduler
        # (note that this is not necessarily all components - as they may have only just been 
        #  activated, in which case they may not register yet)
        threads = self.scheduler.listAllThreads()
        components = dict([ (p,(p.id,p.name)) for p in threads if isinstance(p, Component.component) ])
        
        # go through all components' postoffices and find all linkages
        linkages = {}
        components_to_scan = components.keys()  # list
        for postoffice in [ c.postoffice for c in components_to_scan ]:
            for link in postoffice.linkages:
                src = (link.source.id, Introspector.srcBoxType[link.passthrough], link.sourcebox)
                dst = (link.sink.id  , Introspector.dstBoxType[link.passthrough], link.sinkbox)
                linkages[(src,dst)] = 1
                # some components may not have been detected from the scheduler
                # but maybe linked to, so we need to detect them now
                # 1) append to the list we're scanning now
                # 2) add to the dictionary of components we're building
                if not components.has_key(link.source):
                    components_to_scan.append(link.source)
                    components[link.source] = (link.source.id, link.source.name)
                if not components.has_key(link.sink):
                    components_to_scan.append(link.sink)
                    components[link.sink] = (link.sink.id, link.sink.name)
                           
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

__kamaelia_components__  = ( Introspector, )


if __name__ == '__main__':

   i = Introspector()
   i.activate()
   from Kamaelia.Util.ConsoleEcho import consoleEchoer
   e = consoleEchoer()
   e.activate()
   i.link((i,"outbox"), (e, "inbox"))
   
   print "You should see the Introspector find that it and a consoleEchoer component exist."
   print "We both have inbox, control, signal and outbox postboxes"
   print "The Introspector's outbox is linked to the consoleEchoer's inbox"
   print
   Scheduler.scheduler.run.runThreads(slowmo=0)
