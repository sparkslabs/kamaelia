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

import Axon

class OnDemandIntrospector(Axon.Component.component):
    Inboxes  = { "inbox"   : "Wake me!",
                 "control" : "Shutdown signalling",
               }
    Outboxes = { "outbox" : "Topology dump",
                 "signal" : "Shutdown signalling",
               }

    srcBoxType = { 0:"o", 1:"i", 2:"o" }
    dstBoxType = { 0:"i", 1:"i", 2:"o" }
    
    def main(self):
        """Main loop."""
        while 1:
            yield 1
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                output = ""
                components, postboxes, linkages = self.introspect()
                for comp in components.iterkeys():
                    output += str(comp.name)
                    if comp._isStopped():
                        output += " STOPPED "
                    elif not comp._isRunnable():
                        output += " PAUSED "
                    else:
                        output += " ACTIVE "
                    output += "\n"
                self.send(output, "outbox")
            else:
                self.pause()

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
        components = dict([ (p,(p.id,p.name)) for p in threads if isinstance(p, Axon.Component.component) ])
        
        # go through all components' postoffices and find all linkages
        linkages = {}
        components_to_scan = components.keys()  # list
        for postoffice in [ c.postoffice for c in components_to_scan ]:
            for link in postoffice.linkages:
                src = (link.source.id, OnDemandIntrospector.srcBoxType[link.passthrough], link.sourcebox)
                dst = (link.sink.id  , OnDemandIntrospector.dstBoxType[link.passthrough], link.sinkbox)
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
        #cdict = dict([ components[c] for c in components.iterkeys() ])
        
        return components, postboxes, linkages
