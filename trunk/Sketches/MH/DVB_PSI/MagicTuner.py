#!/usr/bin/env python

# automagic channel tuner
# you set up a DVB_Multiplex component tuned to the right multiplex
#
# then create one of these, saying which channel you want and it'll try to
# find the audio and video streams for it

from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.AxonExceptions import ServiceAlreadyExists
from Axon.CoordinatingAssistantTracker import coordinatingassistanttracker as CAT

from Kamaelia.Chassis.Pipeline import pipeline

from PSIPacketReconstructor import PSIPacketReconstructorService
import dvb3.frontend

from ParseSDT import ParseSDT_ActualTS
from ParsePAT import ParsePAT
from ParsePMT import ParsePMT

from sys import path
path.append("..")
from ServiceWrapper import Service, Subscribe


PAT_PID = 0x00
SDT_PID = 0x11

class DVB_TuneToChannel(AdaptiveCommsComponent):
    """Uses tuner services to find and start getting the audio and video pids
    for the specified channel"""

    def __init__(self, channel, fromDemuxer):
        super(DVB_TuneToChannel,self).__init__()
        self.channelname = channel
        self.demuxerservice = fromDemuxer
        

    def main(self):
        # get the demuxer service
        toDemuxer = self.addOutbox("toDemuxer")
        cat = CAT.getcat()
        service = cat.retrieveService(self.demuxerservice)
        self.link((self,toDemuxer),service)
        
        # create a PSI packet reconstructor, and wire it so it can ask
        # the demuxer for PIDs as required.
        psi = PSIPacketReconstructorService()
        psi_service = Service(psi,{"PSI":"request"}).activate()
        self.link( (psi,"pid_request"), service )
        
        # stage 1, we need to get the service ID, so we'll query the SDT
        sdt_parser = pipeline( Subscribe("PSI", [SDT_PID]),
                               ParseSDT_ActualTS()
                             ).activate()
        
        fromSDT = self.addInbox("fromSDT")
        fromSDT_linkage = self.link( (sdt_parser,"outbox"),(self,fromSDT) )
        
        # wait until we get data back from the SDT
        # note that we wait until we find our service, there's no timeout
        service_id = None
        while service_id == None:
            while not self.dataReady(fromSDT):
                self.pause()
                yield 1
        
            sdt_table = self.recv(fromSDT)
            
            transport_stream_id = sdt_table['transport_stream_id']
            
            # see if we can find our services channel name
            for (sid,service) in sdt_table['services'].items():
                for (dtype,descriptor) in service['descriptors']:
                    if descriptor['type'] == "service":
                        if descriptor['service_name'].lower() == self.channelname.lower():
                            service_id = sid
                            break
        
        print "Found service id:",service_id
        print "Its in transport stream id:",transport_stream_id
            
            
        # stage 2, find out which PID contains the PMT for the service,
        # so we'll query the PAT
        pat_parser = pipeline( Subscribe("PSI", [PAT_PID]),
                               ParsePAT()
                             ).activate()
        
        fromPAT = self.addInbox("fromPAT")
        fromPAT_linkage = self.link( (pat_parser,"outbox"),(self,fromPAT) )
        
        # wait until we get data back from the PAT
        PMT_PID = None
        while PMT_PID == None:
            while not self.dataReady(fromPAT):
                self.pause()
                yield 1
        
            sdt_table = self.recv(fromPAT)
            # see if we can find our service's PMT
            ts_services = sdt_table['transport_streams'][transport_stream_id]
            if service_id in ts_services:
                PMT_PID = ts_services[service_id]
                break
            
        print "Found PMT PID for this service:",PMT_PID
            
        # stage 3, find out which PIDs contain AV data, so we'll query this
        # service's PMT
        pmt_parser = pipeline( Subscribe("PSI", [PMT_PID]),
                               ParsePMT()
                             ).activate()
        
        fromPMT = self.addInbox("fromPMT")
        fromPMT_linkage = self.link( (pmt_parser,"outbox"),(self,fromPMT) )
        
        # wait until we get data back from the PMT
        audio_pid = None
        video_pid = None
        while audio_pid == None and video_pid == None:
            while not self.dataReady(fromPMT):
                self.pause()
                yield 1

            pmt_table = self.recv(fromPMT)
            if service_id in pmt_table['services']:
                service = pmt_table['services'][service_id]
                for stream in service['streams']:
                    if   stream['type'] in [3,4] and not audio_pid:
                        audio_pid = stream['pid']
                    elif stream['type'] in [1,2] and not video_pid:
                        video_pid = stream['pid']

        print "Found audio PID:",audio_pid
        print "Found video PID:",video_pid
        
        yield 1
        # now set up to receive those pids and forward them on for all eternity
        
        fromDemuxer = self.addInbox("fromDemuxer")
        self.send( ("ADD",[audio_pid,video_pid], (self,fromDemuxer)), toDemuxer)
        
        while 1:
            while self.dataReady(fromDemuxer):
                packet = self.recv(fromDemuxer)
                self.send(packet,"outbox")
                
            self.pause()
            yield 1
        

if __name__ == "__main__":
    
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.File.Writing import SimpleFileWriter
    
    from MakeHumanReadable import MakeSDTHumanReadable

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "coderate_HP" : dvb3.frontend.FEC_3_4,
        "coderate_LP" : dvb3.frontend.FEC_3_4,
    }

    from Multiplex import DVB_Receiver
    
    Service( DVB_Receiver(505833330.0/1000000.0, feparams),
             {"MUX1":"inbox"}
           ).activate()
    
    
    from Kamaelia.Util.Introspector import Introspector
    from Kamaelia.Internet.TCPClient import TCPClient
    
    pipeline( DVB_TuneToChannel(channel="BBC ONE",fromDemuxer="MUX1"),
              SimpleFileWriter("bbc_one.ts"),
            ).run()

