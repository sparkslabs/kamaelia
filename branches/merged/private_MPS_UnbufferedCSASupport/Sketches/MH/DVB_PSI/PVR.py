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

# A program designed to record a programme, by specifying its name and channel name
# it is on. It records any programmes it sees that match the name - so if there is,
# for example, more than one episode they'll all get recorded back to back in the
# one file
#
# Note:
# * must be tuned to the right multiplex (the one containing the channel) for
#   it to work.
# * Channel names and programme names must be exact
# * channel names are case sensitive


import dvb3.frontend

FREQUENCY = 505833330/1000000.0
FE_PARAMS = { "inversion" : dvb3.frontend.INVERSION_AUTO,
              "constellation" : dvb3.frontend.QAM_16,
              "coderate_HP" : dvb3.frontend.FEC_3_4,
              "coderate_LP" : dvb3.frontend.FEC_3_4,
            }
            
programmes_to_record = [
       #  Channel     programme   filename
       ( "BBC ONE", "Neighbours", "/data/neighbours.ts" ),
       ( "BBC TWO", "Newsnight",  "/data/Newsnight.ts" ),
    ]
    
# ------------------------------------------------------------------------------

from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Backplane import Backplane,PublishTo,SubscribeTo

from Kamaelia.Device.DVB.Parse.ParseServiceDescriptionTable import SDT_PID, ParseServiceDescriptionTable_ActualTS
from Kamaelia.Device.DVB.Parse.ParseProgramAssociationTable import PAT_PID, ParseProgramAssociationTable
from Kamaelia.Device.DVB.Parse.ParseProgramMapTable import ParseProgramMapTable
from Kamaelia.Device.DVB.Parse.ParseEventInformationTable import EIT_PID, ParseEventInformationTable_Subset, SimplifyEIT

from Kamaelia.Device.DVB.NowNext import NowNextProgrammeJunctionDetect
from Kamaelia.Device.DVB.PSITables import FilterOutNotCurrent

from Kamaelia.Experimental.Services import RegisterService, Subscribe, ToService

from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.File.Writing import SimpleFileWriter

import time


class ChannelNameLookupService(AdaptiveCommsComponent):
    """\
    I'm a service you can subscribe to to be told the service_id and transport
    stream id under which a given named channel is being broadcast, eg "BBC ONE"
    
    If that mapping changes, you'll get an update message letting you know.
    
    The messages I send you are of the form:
        (channel_name, service_id, transport_stream_id)
    """
    
    Inboxes = { "inbox" : "sdt tables",
                "request" : "prod here to get output",
                "control" : "",
              }
        
    def __init__(self):
        super(ChannelNameLookupService,self).__init__()
        
        # key,value = channelname, [outboxnames]
        self.destinations = {}
        
        # key,value = (component, inbox),(outboxname, linkage, [channelnames])
        self.subscriptions = {}
        
        
    def shutdown(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            self.send(msg,"signal")
            if isinstance(msg,(producerFinished,shutdownMicroprocess)):
                return True
        return False
        
        
    def handleSubscribeUnsubscribe(self, msg):
        cmd, names, dest = msg
        
        if cmd=="ADD":
            # add (or fetch existing) outbox going to this destination
            try:
                recipientOutbox, linkage, subscribedToNamess = self.subscriptions[dest]
            except KeyError:
                recipientOutbox = self.addOutbox("outbox")
                linkage = self.link( (self, recipientOutbox), dest)
                subscribedToNames = []
                self.subscriptions[dest] = recipientOutbox, linkage, subscribedToNames
                
            for name in names:
                # add (or fetch existing) routing for this channel name
                try:
                    recipientOutboxes = self.destinations[name]
                except KeyError:
                    recipientOutboxes = []
                    self.destinations[name] = recipientOutboxes
                    
                # for this name, make sure our outbox is one of the recipients
                if recipientOutbox not in recipientOutboxes:
                    recipientOutboxes.append(recipientOutbox)
                    
                # for this outbox, add to the list of names it receives
                if name not in subscribedToNames:
                    subscribedToNames.append(name)
                    
                # might as well send now
                lookup = self.lookup(name)
                if lookup:
                    self.send( lookup, recipientOutbox)
                
        elif cmd=="REMOVE":
            # work out which outbox we must be using
            try:
                recipientOutbox, linkage, subscribedToNames = self.subscriptions[dest]
            except KeyError:
                return
                
            for name in names:
                if name in subscribedToNames:
                    subscribedToNames.remove(pid)
                    self.destinations[name].remove(recipientOutbox)
                    
                    # if nobody is subscribed to this name anymore, clean up
                    if not self.destinations[name]:
                        del self.destinations[name]
                        
                        
            # if no longer subscribed to any names on this destination, then clean it up
            if not subscribedToNames:
                self.unlink(thelinkage = linkage)
                self.deleteOutbox(recipientOutbox)
                del self.subscriptions[dest]
    
    
    def main(self):
        self.sdt_table = None
        
        while not self.shutdown():
            
            while self.dataReady("request"):
                self.handleSubscribeUnsubscribe(self.recv("request"))
                    
            while self.dataReady("inbox"):
                self.sdt_table = self.recv("inbox")
                
                for channelname in self.destinations.keys():
                    lookup = self.lookup(channelname)
                    if lookup:
                        for boxname in self.destinations[channelname]:
                            self.send(lookup,boxname)

            self.pause()
            yield 1

    
    def lookup(self, channelname):
        if self.sdt_table == None:
            return None
        
        # enumerate all channels
        for (sid,service) in self.sdt_table['services'].items():
            for (dtype,descriptor) in service['descriptors']:
                if descriptor['type'] == "service":
                    if descriptor['service_name'] == channelname:
                        service_id = sid
                        transport_stream_id = self.sdt_table['transport_stream_id']
                        return (channelname, service_id, transport_stream_id)

        


class ProgrammeDetector(component):
    """\
    I take in simplified now and next data and look for the programme name on the
    specified channel. When I see it, I send a "START" message. When I see that
    channel but with a differently named programme, I send a "STOP" message.
    
    I use a channel lookup service to map the channel name to the service_id for
    that channel.
    """
    Inboxes = { "inbox" : "sdt tables",
                "_fromChannelLookup" : "",
                "control" : "",
              }
                            
    # watches programme junction data, and decides when to start recording a channel
    def __init__(self, channel_name, programme_name, fromChannelLookup):
        super(ProgrammeDetector,self).__init__()

        self.channel_name = channel_name
        self.programme_name = programme_name.lower().strip()
        self.fromChannelLookup = fromChannelLookup
        
    def main(self):
        # first, get the service ID for this channel
        #
        channelLookup = Subscribe(self.fromChannelLookup, [self.channel_name]).activate()
        self.link( (channelLookup,"outbox"), (self, "_fromChannelLookup") )
        while not self.dataReady("_fromChannelLookup"):
            self.pause()
            yield 1
        
        channel_name, service_id, ts_id = self.recv("_fromChannelLookup")
        assert(channel_name == self.channel_name)
        assert(service_id)
        
        
        while 1:
            
            recording=False
            while not recording:
                if self.dataReady("inbox"):
                    newNowEvent = self.recv("inbox")
                    if newNowEvent['service'] == service_id:
                        recording = newNowEvent['name'].lower().strip() == self.programme_name
                else:
                    self.pause()
                yield 1
                    
            # start recording
            service_id = newNowEvent['service']
            self.send("START", "outbox")
                    
            while recording:
                if self.dataReady("inbox"):
                    newNowEvent = self.recv("inbox")
                    if newNowEvent['service'] == service_id:
                        recording = newNowEvent['name'].lower().strip() == self.programme_name
                else:
                    self.pause()
                yield 1
            
            # stop recording
            self.send("STOP", "outbox")




class ControllableRecorder(component):
    """\
    I output audio and video transport stream packets for the named channel,
    controlled by "START" and "STOP" messages sent to my inbox.
    
    I use a channel name lookup service to map the channel name to the service_id
    I create components to parse the "Programme Association Table" and "Programme
    Map Table" in the data stream in order to work out what the packet IDs (PIDs)
    are that contain the channel's audio and video.
    
    I use the demuxer service to obtain streams of the audio and video packets
    and I forward them on out of my outbox.
    """
    Inboxes = { "inbox" : "",
                "_fromChannelLookup" : "",
                "_fromPAT" : "",
                "_fromPMT" : "",
                "_av_packets" : "",
                "control" : "",
              }
              
    Outboxes = { "outbox" : "",
                 "_toDemuxer" : "",
                 "signal" : "",
               }
               
    def __init__(self, channel_name, fromDemuxer, fromPSI, fromChannelLookup):
        super(ControllableRecorder,self).__init__()
        
        self.channel_name = channel_name
        self.fromDemuxer = fromDemuxer
        self.fromPSI = fromPSI
        self.fromChannelLookup = fromChannelLookup
        
    def main(self):
        # first, get the service ID for this channel
        #
        channelLookup = Subscribe(self.fromChannelLookup, [self.channel_name]).activate()
        self.link( (channelLookup,"outbox"), (self, "_fromChannelLookup") )
        while not self.dataReady("_fromChannelLookup"):
            self.pause()
            yield 1
        
        channel_name, service_id, ts_id = self.recv("_fromChannelLookup")
        assert(channel_name == self.channel_name, service_id)
        
        # stage 2, find out which PID contains the PMT for the service,
        # so we'll query the PAT
        pat_parser = Pipeline( Subscribe(self.fromPSI, [PAT_PID]),
                               ParseProgramAssociationTable()
                             ).activate()
        
        fromPAT_linkage = self.link( (pat_parser,"outbox"),(self,"_fromPAT") )
        
        # wait until we get data back from the PAT
        PMT_PID = None
        while PMT_PID == None:
            while not self.dataReady("_fromPAT"):
                self.pause()
                yield 1
        
            pat_table = self.recv("_fromPAT")
            # see if we can find our service's PMT
            for transport_stream_id in pat_table['transport_streams']:
                ts_services = pat_table['transport_streams'][transport_stream_id]
                if service_id in ts_services:
                    PMT_PID = ts_services[service_id]
                    break
            
        print "Found PMT PID for this service:",PMT_PID
            
        # stage 3, find out which PIDs contain AV data, so we'll query this
        # service's PMT
        pmt_parser = Pipeline( Subscribe(self.fromPSI, [PMT_PID]),
                               ParseProgramMapTable()
                             ).activate()
        
        fromPMT_linkage = self.link( (pmt_parser,"outbox"),(self,"_fromPMT") )
        
        # wait until we get data back from the PMT
        audio_pid = None
        video_pid = None
        while audio_pid == None and video_pid == None:
            while not self.dataReady("_fromPMT"):
                self.pause()
                yield 1

            pmt_table = self.recv("_fromPMT")
            if service_id in pmt_table['services']:
                service = pmt_table['services'][service_id]
                for stream in service['streams']:
                    if   stream['type'] in [3,4] and not audio_pid:
                        audio_pid = stream['pid']
                    elif stream['type'] in [1,2] and not video_pid:
                        video_pid = stream['pid']

        print "Found audio PID:",audio_pid
        print "Found video PID:",video_pid
        print "Waiting to start recording..."
        
        yield 1
        
        # get the demuxer service
        cat = CAT.getcat()
        service = cat.retrieveService(self.fromDemuxer)
        self.link((self,"_toDemuxer"),service)
        
        while 1:
            # now wait for the go signal
            recording = False
            while not recording:
                if self.dataReady("inbox"):
                    recording = self.recv("inbox") == "START"
                else:
                    self.pause()
                yield 1
        
        
            # request audio and video data
            self.send( ("ADD",[audio_pid,video_pid], (self,"_av_packets")), "_toDemuxer")
            print time.asctime(), "Recording ",audio_pid,video_pid
            
            while recording:
                while self.dataReady("_av_packets"):
                    packet = self.recv("_av_packets")
                    self.send(packet,"outbox")
                    
                while self.dataReady("inbox"):
                    recording = not ( self.recv("inbox") == "STOP" )
                    
                if recording:
                    self.pause()
                yield 1
                
            self.send( ("REMOVE", [audio_pid,video_pid], (self,"_av_packets")), "_toDemuxer")
            print time.asctime(), "Stopped",audio_pid,video_pid


# ==============================================================================

from Kamaelia.Device.DVB.Receiver import Receiver

# DVB tuner and demultiplexer as a service, so other components can wire up
# and request transport stream packets containing the pids they need
RegisterService( Receiver( FREQUENCY, FE_PARAMS, 0 ),
                 {"DEMUXER":"inbox"},
               ).activate()


# ------------------------------------------------------------------------------
# PSI table service - so other services, such as looking up channel names, mappings
# of services to their audio & video pids etc. can get their tables from somewhere.
#
# Connects to the demuxer service, so it can request the relevant bits of data

from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITablesService

RegisterService( \
     Graphline( PSI     = ReassemblePSITablesService(),
                DEMUXER = ToService("DEMUXER"),
                linkages = {
                    ("PSI", "pid_request") : ("DEMUXER", "inbox"),
                    ("",    "request")     : ("PSI",     "request"),
                }
              ),
     {"PSI_Tables":"request"}
).activate()


# ------------------------------------------------------------------------------
# now and next data on a backplane

Pipeline( Subscribe("PSI_Tables", [EIT_PID]),
          ParseEventInformationTable_Subset( True, False, False, False),
          FilterOutNotCurrent(),
          SimplifyEIT(),
          NowNextProgrammeJunctionDetect(),
          PublishTo("now&next"),
        ).activate()

Backplane("now&next").activate()


# ------------------------------------------------------------------------------
# A service to map textual channel names to service_id's

RegisterService( \
    Graphline( TABLE_SOURCE = Subscribe("PSI_Tables", [SDT_PID]),
               PARSING = ParseServiceDescriptionTable_ActualTS(),
               LOOKUP = ChannelNameLookupService(),
               linkages = {
                   ("","inbox")               : ("LOOKUP", "request"),
                   ("TABLE_SOURCE", "outbox") : ("PARSING", "inbox"),
                   ("PARSING", "outbox")      : ("LOOKUP", "inbox"),
               }
             ),
    {"LookupChannelName" : "inbox"}
).activate()
        

# ------------------------------------------------------------------------------
# bringing it all together into a programme recorder

def recordForMe(channel, programme, filename):
    return \
        Pipeline( SubscribeTo("now&next"),
                  ProgrammeDetector( channel_name=channel, programme_name=programme,
                                     fromChannelLookup="LookupChannelName"),
                  ControllableRecorder( channel_name=channel,
                                        fromDemuxer="DEMUXER",
                                        fromPSI="PSI_Tables",
                                        fromChannelLookup="LookupChannelName"),
          SimpleFileWriter(filename),
        )

# ------------------------------------------------------------------------------

for (channel, programme,filename) in programmes_to_record:
    recordForMe(channel,programme,filename).activate()

from Axon.Scheduler import scheduler
scheduler.run.runThreads()
