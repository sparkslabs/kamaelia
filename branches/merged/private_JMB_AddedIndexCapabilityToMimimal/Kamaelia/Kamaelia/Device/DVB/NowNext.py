#!/usr/bin/env python

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
==================================================
Processing Simplified Now & Next Event Information
==================================================

These components filter or process simplified events, derived from Event
Information Table data containing now and next information.

Convert a parsed EIT table to simplified individual events using the
Kamaelia.Devices.DVB.Parse.ParseEventInformationTable.SimplifyEIT component.

NowNextServiceFilter selects information relating to only particular services
(channels) in the data.

NowNextProgrammeJunctionDetect detects the point at which one programme ends
and another begins - known as the "programme junction". It distinguishes
between programme junctions and ammendments to a programme's details.



Example Usage
~~~~~~~~~~~~~

Tuning to a particular broadcast multiplex and detecting when a new programme
starts on service 4164, outputting the information about the new programme::
    
    frequency = 505833330.0/1000000.0
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }

    EIT_PID = 0x12
    BBC_ONE = 4164       # the 'service id' on this particular multiplex

    Pipeline( DVB_Multiplex(505833330.0/1000000.0, [EIT_PID], feparams),
              DVB_Demuxer({ EIT_PID:["outbox"]}),
              ReassemblePSITables(),
              ParseEventInformationTable_Subset(True,False,False,False), # now and next for this mux only
              SimplifyEIT(),
              NowNextProgrammeJunctionDetect(),
              NowNextServiceFilter(BBC_ONE),
              ConsoleEchoer(),

The above code receives the broadcast multiplex, reconstructs and parses the
Event Information Table in it, then simplifies it to a stream of events.
These events are then filtered and processed.



NowNextServiceFilter
~~~~~~~~~~~~~~~~~~~~

NowNextServiceFilter selects information relating to only particular services
(channels) in the data.



Behaviour
---------

At initialisation, specify the service id's of the services to be detected as
arguments.

Send the parsed and simplified events to this component's "inbox" inbox.
Those which match the service id's specified at initialisation will immediately
be sent on out of the "outbox" outbox. Those which do not match are discarded.

If a shutdownMicroprocess or producerFinished message is sent to this
component's "control" inbox, it will immediately be sent on out of the "signal"
outbox. The component will then immediately terminate.



NowNextProgrammeJunctionDetect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NowNextProgrammeJunctionDetect detects the point at which one programme ends
and another begins - known as the "programme junction". It distinguishes
between programme junctions and ammendments to a programme's details.



Behaviour
---------

Send the parsed and simplified events to this component's "inbox" inbox.
This component then distinguishes between ammendments to a programme (such as
(a change to to how long it is, or its description) and actual programme
junctions (the end of one programme and the start of the next).

A single NowNextProgrammeJunctionDetect instance can handle the events for
an unlimited number of services concurrently.

When a programme junction is detected, the event describing the programme that
has just started is sent out of the "outbox" and "now" outboxes. Any event
describing the 'next' programme that will follow it is sent out the "next"
outbox.

If the details of a programme have just been ammended (it is not a junction),
then the new event information is sent out of the "now_update" outbox if it
relates to the current programme on air; or the "next_update" outbox if it
relates to the programme that will follow it.

NowNextProgrammeJunctionDetect only handles 'now' and 'next' events. Events
for schedule (electronic programme guide) details are ignored.

If a shutdownMicroprocess or producerFinished message is sent to this
component's "control" inbox, it will immediately be sent on out of the "signal"
outbox. The component will then immediately terminate.



How does it work?
-----------------

NowNextProgrammeJunction detect keeps a record of the ids of the 'now' and
'next' events each service.

When an event is received, it is looked up in this table. If the event id
matches, then it is assumed to be an ammendment of details. If it does not
then it is assumed that a programme junction must be taking place.

"""

from Axon.Component import component
from Axon.Ipc import producerFinished,shutdownMicroprocess


class NowNextServiceFilter(component):
    """\
    NowNextServiceFilter(\*services) -> new NowNextServiceFilter component.

    Filters simplified events from Event Information Tables, only letting
    through those that match the service ids specified.    
    
    Argument list is a list of service id's to be let through by the filter.
    """
    def __init__(self, *services):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(NowNextServiceFilter,self).__init__()
        self.services = services
        
    def shutdown(self):
        """Shutdown handling."""
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False

    def main(self):
        """Main loop."""
        while not self.shutdown():
            while self.dataReady("inbox"):
                event = self.recv("inbox")
                if event['service'] in self.services:
                    self.send(event,"outbox")
            self.pause()
            yield 1


class NowNextProgrammeJunctionDetect(component):
    """\
    NowNextProgrammeJunctionDetect() -> new NowNextJunctionDetect component.
    
    Takes simplified events derived from parsed Event Information Table data
    and sorts them according to whether they simply ammend/correct details or
    whether they represent the start of a new programme (a junction).
    """
    Outboxes = { "outbox"      : "new NOW events, at programme junctions only",
                 "now"         : "same as for 'outbox' outbox",
                 "now_update"  : "NOW events, when details change, but its still the same programme",
                 "next"        : "new NEXT events, at programme junctions only",
                 "next_update" : "NEXT events, when details change, but its still the same programme",
                 "signal"      : "Shutdown signalling",
               }
    
    def shutdown(self):
        """Shutdown handling"""
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True
        return False
    
    def main(self):
        """Main loop"""
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

__kamaelia_components__ = ( NowNextServiceFilter,
                            NowNextProgrammeJunctionDetect, )
