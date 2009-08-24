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
=======================================================
DVB-T (Digital Terrestrial TV) Tuner & Demuxing Service
=======================================================

Tunes to the specified frequency, using the specified parameters, using a DVB
tuner device; then demultiplexes packets by packet ID (PID) from DVB/MPEG
transport streams. Provides this as a service, to which other components can
subscribe as clients, requesting to receive packets with certain PIDs.

This is a prefab component built out of a Tuner and DemuxerService component.



Example Usage
-------------

(Using experimental Kamaelia.Experimental.Services components)

Set up receiver as a named public service, then subscribe to specific PIDs for
recording a stream and some event information::
    
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    RegisterService( Receiver(505.833330, feparams),
                     {"DEMUXER":"inbox"}
                   ).activate()
                   
    Pipeline( Subscribe("DEMUXER", [600,601]),
              SimpleFileWriter("recording_of_600_and_601.ts"),
            ).activate()
    
    Pipeline( Subscribe("DEMUXER", [18]),
              SimpleFileWriter("event_information_data.ts")
            ).run()



How does it work?
-----------------

This component is a prefab combining a Tuner and a DemuxerService component.

Use this component in exactly the same way as you would use the
Kamaelia.Device.DVB.DemuxerService component. The only difference is that
requests should be sent to the "inbox" inbox, instead of a different one.

To request to be sent packets with particular PIDs, send messages of the form:

    ("ADD",    (dest_component, dest_inboxname), [pid, pid, ...])
    ("REMOVE", (dest_component, dest_inboxname), [pid, pid, ...])

For more details, see Kamaelia.Device.DVB.DemuxerService.

Internally, the DemuxerService component is wired so that its requests for PIDs
go straight back to the Tuner component. When a client makes a request, the
DemuxerService therefore automatically asks the Tuner to give it only the
packets it needs to satisfy all its current clients.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.

"""

import os
import dvb3.frontend
import dvb3.dmx
import time
import struct

from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import shutdownMicroprocess,producerFinished
from Kamaelia.Chassis.Graphline import Graphline

from Tuner import Tuner
from DemuxerService import DemuxerService

def Receiver(frequency, feparams, card=0):
    return Graphline( TUNER = Tuner(frequency, feparams, card),
                      DEMUX = DemuxerService(),
                      linkages = {
                          ("self", "inbox")       : ("DEMUX","request"),
                          ("DEMUX","pid_request") : ("TUNER","inbox"),
                          ("TUNER","outbox")      : ("DEMUX","inbox"),
                          
                          # propagate shutdown messages
                          ("self",  "control") : ("TUNER", "control"),
                          ("TUNER", "signal")  : ("DEMUX", "control"),
                          ("DEMUX", "signal")  : ("self",  "signal"),
                      }
                    )


__kamaelia_prefabs__ = ( Receiver, )

if __name__=="__main__":
    
    import random
    from Axon.Component import component
    from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT
    from Axon.AxonExceptions import ServiceAlreadyExists

    class Subscriber(component):
        def __init__(self, servicename, spacing, *pids):
            super(Subscriber,self).__init__()
            self.notsubscribed = list(pids)
            self.subscribed = []
            self.spacing = " "*spacing
            self.servicename = servicename
            
        def takesomefrom(self,source):
            items = []
            if len(source):
                qty = 1+random.randrange(0,len(source))
                for _ in range(0,qty):
                    i = random.randrange(0,len(source))
                    items.append(source[i])
                    del source[i]
            return items
                
        def changeSubscription(self):
            if random.randrange(0,2) == 1:
                pids = self.takesomefrom(self.notsubscribed)
                self.send( ("ADD",pids,(self,"inbox")), "outbox")
                self.subscribed.extend(pids)
            else:
                pids = self.takesomefrom(self.subscribed)
                self.send( ("REMOVE",pids,(self,"inbox")), "outbox")
                self.notsubscribed.extend(pids)
            print self.spacing,"Now subscribed to pids:"
            print self.spacing,"  ",self.subscribed
                
        def main(self):
            cat = CAT.getcat()
            service = cat.retrieveService(self.servicename)
            self.link((self,"outbox"),service)
            
            nextchangetime = self.scheduler.time + random.randrange(5,10)
            self.notyetreceived = self.subscribed[:]
            while 1:
                while self.dataReady("inbox"):
                    packet = self.recv("inbox")
                    pid = ((ord(packet[1]) << 8) + ord(packet[2])) & 0x1fff
                    if pid not in self.subscribed:
                        print self.spacing,"Shouldn't have received pid:",pid
                    else:
                        if pid in self.notyetreceived:
                            print self.spacing,"Received 1st of pid:",pid
                            self.notyetreceived.remove(pid)
                        
                if self.scheduler.time >= nextchangetime:
                    nextchangetime = self.scheduler.time + random.randrange(10,20)
                    self.changeSubscription()
                    self.notyetreceived = self.subscribed[:]
                
                if self.subscribed:
                    self.pause()
                yield 1


    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Experimental.Services import RegisterService
    
    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }

    print "Tunes to UK Crystal palace transmitter MUX 1"
    print "Subscribers subscribe to PIDs that should contain data"
    print "May take several seconds before you see any activity..."
    print "---1st subscriber:------|---2nd subscriber:------"
    
    Subscriber("MUX1", 0,  0,0x11,0x12,600,601).activate()
    Subscriber("MUX1", 25, 0,0x11,0x12,600,601).activate()

    demux = Receiver(505833330.0/1000000.0, feparams)
                     
    RegisterService(demux,{"MUX1":"inbox"}).run()

