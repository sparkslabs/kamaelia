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

# introspector component

import Axon as _Axon

from Axon.Component import component as axonComponent
from Axon.Postman   import postman   as axonPostman
from Axon.Scheduler import scheduler as axonScheduler

from Axon.Ipc import producerFinished, shutdownMicroprocess

class Introspector(_Axon.Component.component):
    """This component introspects the current local topology of an axon system.
    
    Local? This component examines its scheduler to find components and postmen.
    It then examines them to determine their inboxes and outboxes and the linkages
    between them.
    
    If this component is not active, then it will see no scheduler and will report nothing.
    
    The output is a description of the a graph topology, where components and postboxes
    are the nodes, and their relationships/linkages form the links between them. As the
    shape of the graph changes, this component relays only the changes.
    
    The output format is a stream of strings, designed to be fed to an AxonVisualiserServer
    component.
    """

    # passthrough==0 -> outbox > inbox
    # passthrough==1 -> inbox > inbox
    # passthrough==2 -> outbox > outbox
    srcBoxType = { 0:"o", 1:"i", 2:"o" }
    dstBoxType = { 0:"i", 1:"i", 2:"o" }
        
    def main(self):
        # reset the receiving 'axon visualiser'
        self.send("DEL ALL\n", "outbox")
        yield 1
        
        nodes = dict()
        linkages = dict()
        while 1:
            # shutdown if requested
            if self.dataReady("control"):
                data = self.recv("control")
                if isinstance(data, shutdownMicroprocess):
                    return
        
            if isinstance(self.scheduler, axonScheduler):
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
        """returns the current set of components, postboxes and interpostbox linkages"""
        
        # fetch components currently active with the scheduler
        # (note that this is not necessarily all components - as they may have only just been 
        #  activated, in which case they may not register yet)
        components = dict([ (p,(p.id,p.name)) for p in self.scheduler.threads if isinstance(p, axonComponent) ])
        
        # go through all postmen and find all linkages
        linkages = {}
        for postman in [ p for p in self.scheduler.threads if isinstance(p, axonPostman) ]:
            for link in postman.linkages:
                src = (link.source.id, Introspector.srcBoxType[link.passthrough], link.sourcebox)
                dst = (link.sink.id  , Introspector.dstBoxType[link.passthrough], link.sinkbox)
                linkages[(src,dst)] = 1
                # some components may not have been detected from the scheduler
                # but maybe linked to, so we need to detect them now
                if not components.has_key(link.source):
                    components[link.source] = (link.source.id, link.source.name)
                if not components.has_key(link.sink):
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
            
                    

if __name__ == '__main__':
   from Axon.Scheduler import scheduler
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
   scheduler.run.runThreads(slowmo=0)

