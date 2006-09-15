#!/usr/bin/env python

# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
Components for filtering and processing *simplified* event information table
data containing now and next information.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess


class NowNextServiceFilter(component):
    """\
    Filters now/next event data for only specified services.
    """
    def __init__(self, *services):
        super(NowNextServiceFilter,self).__init__()
        self.services = services
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        while not self.shutdown():
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                if event['service'] in self.services:
                    self.send(event,"outbox")
            self.pause()
            yield 1


class NowNextProgrammeJunctionDetect(component):
    """\
    Distinguishes between updates to the details of an event;
    and a change in running status of an event.
    
    Only works for NOW and NEXT events. Schedule events are ignored and sunk.
    
    If the running status has changed, the event is output
    """
    Outboxes = { "outbox"      : "new NOW events, at programme junctions only",
                 "now"         : "same as for 'outbox' outbox",
                 "now_update"  : "NOW events, when details change, but its still the same programme",
                 "next"        : "new NEXT events, at programme junctions only",
                 "next_update" : "NEXT events, when details change, but its still the same programme",
                 "signal"      : "Shutdown signalling",
               }
    
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        outbox_mappings = {
                ("NOW",True)   : ["now","outbox"],
                ("NOW",False)  : ["now_update"],
                ("NEXT",True)  : ["next"],
                ("NEXT",False) : ["next_update"],
            }
        
        event_ids = {}   # indexed by (service_id, and 'NOW'/'NEXT')
        
        while not self.shutdown():
            
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                
                service_id = event['service']
                when       = event['when']
                
                if not (when=="NOW" or when=="NEXT"):
                    continue
                
                # its a junction if the event_id has changed
                index = (service_id,when)
                if event['event_id'] != event_ids.get(index, -1):
                    event_ids[index] = event['event_id']
                    isJunction=True
                else:
                    isJunction=False
                    
                sendto = outbox_mappings[(when,isJunction)]
                for boxname in sendto:
                    self.send(event, boxname)
            
            self.pause()
            yield 1

