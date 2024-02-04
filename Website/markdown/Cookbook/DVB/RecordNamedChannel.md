---
pagename: Cookbook/DVB/RecordNamedChannel
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Recording a named channel from a DVB broadcast 
=========================================================

*Find the code for this here:\
*[/Code/Python/Kamaelia/Examples/DVB\_Systems/RecordNamedChannel.py](http://svn.sourceforge.net/viewvc/kamaelia/trunk/Code/Python/Kamaelia/Examples/DVB_Systems/RecordNamedChannel.py?view=markup)

Recording a channel from a DVB (digital video broadcasting) broadcast
[is relatively
simple](../../../Cookbook/DVB/SingleChannelTransportStreamCapture)[](../../../Cookbook/DVB/SingleChannelTransportStreamCapture)
if you know the packet IDs (PIDs) for packets containing the audio and
video streams of the service (the channel) you want to record. But what
if you only know the channel\'s name?

In this example the component *DVB\_TuneToChannel* uses various DVB
components to extract and parse the Program Specific Information (PSI)
tables needed to work it out itself. It therefore needs to be able to
talk to the DVB *Receiver* to request packets with varous PIDs as it
realises it needs them.

The top level of the system is therefore this:

        from Kamaelia.Chassis.Graphline import Graphline
        from Kamaelia.File.Writing import SimpleFileWriter
        
        import dvb3.frontend

        feparams = {
            "inversion" : dvb3.frontend.INVERSION_AUTO,
            "constellation" : dvb3.frontend.QAM_16,
            "coderate_HP" : dvb3.frontend.FEC_3_4,
            "coderate_LP" : dvb3.frontend.FEC_3_4,
        }

        from Kamaelia.Device.DVB.Receiver import Receiver
        
        RegisterService( Receiver(505833330.0/1000000.0, feparams),
                         {"MUX1":"inbox"}
                       ).activate()
            
        Pipeline( DVB_TuneToChannel(channel="BBC ONE",fromDemuxer="MUX1"),
                  SimpleFileWriter("bbc_one.ts"),
                ).run()

The DVB *Receiver* component (which contains both a tuner and demuxer)
is registered as a named service \"MUX1\". *DVB\_TuneToChannel* is given
its name, so it can request packets with specific PIDs.\
\
*DVB\_TuneToChannel* is then pipelined with a *SimpleFileWriter* so that
audio and video packets it eventually outputs will be written to a
file.\

What does DVB\_TuneToChannel do?
--------------------------------

The component takes a channel name, and the name of the demuxer service
as arguments:

>     class DVB_TuneToChannel(AdaptiveCommsComponent):
>         ...
>
>         def __init__(self, channel, fromDemuxer):
>             super(DVB_TuneToChannel,self).__init__()
>             self.channelname = channel
>             self.demuxerservice = fromDemuxer

First, *DVB\_TuneToChannel* resolves the demuxer service name it was
given and adds an outbox and linkage to allow it to send requests to it:

        def main(self):
            # get the demuxer service
            toDemuxer = self.addOutbox("toDemuxer")
            cat = CAT.getcat()
            service = cat.retrieveService(self.demuxerservice)
            self.link((self,toDemuxer),service)

Before they can be parsed, PSI tables need to be reconstructed from the
transport stream packets they are carried in. So next it sets up a named
service \"PSI\" to reconstruct them, based on a
*ReassemblePSITablesService* component. It is linked to the demuxer
service so it can requests packets with the PIDs it needs:

            psi = ReassemblePSITablesService()
            psi_service = RegisterService(psi,{"PSI":"request"}).activate()
            self.link( (psi,"pid_request"), service )

### 1. Resolving service name to service id 

The first step is to resolve the service name \"BBC ONE\" in this
example, to the service\'s id. This data is held in the Service
Description Table (SDT), which is carried in a fixed PID. So
*DVB\_TuneToChannel* creates the correct parsing component and
subscribes it to the PSI table service; then adds an inbox and links it
to receive output from the pipeline:

            sdt_parser = Pipeline( Subscribe("PSI", [SDT_PID]),
                                   ParseServiceDescriptionTable_ActualTS()
                                 ).activate()
            
            fromSDT = self.addInbox("fromSDT")
            fromSDT_linkage = self.link( (sdt_parser,"outbox"),(self,fromSDT) )

*DVB\_TuneToChannel* then waits for the parsing component to return a
table and searches it for the matching service ID and transport stream
ID:\

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

The PIDs for the audio and video streams are recorded in a Program Map
Table (PMT). There is one of these for each service in the multiplex.
The PIDs for these are listed in the Program Association Table (PAT)
which is carried in packets with a known PID.\

So the next steps are to examine the Program Association Table, then
find and examine the correct Program Map Table for the service we want.

### 2. Finding the Program Map Table for a given service id

As was done for the Service Description table, *DVB\_TuneToChannel* sets
up a parser for the Program Association Table, and an inbox to collect
the results:

            pat_parser = Pipeline( Subscribe("PSI", [PAT_PID]),
                                   ParseProgramAssociationTable()
                                 ).activate()
            
            fromPAT = self.addInbox("fromPAT")
            fromPAT_linkage = self.link( (pat_parser,"outbox"),(self,fromPAT) )

It then waits for a parsed table to be returned and searches it for the
PID for packets containing the Program Map Table for the service:\

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

### 3. Finding the PIDs containing audio and video 

Nowthe PID for packets containing the Program Map Table is known,
*DVB\_TuneToChannel* can set up a parser that table:\

            pmt_parser = Pipeline( Subscribe("PSI", [PMT_PID]),
                                   ParseProgramMapTable()
                                 ).activate()
            
            fromPMT = self.addInbox("fromPMT")
            fromPMT_linkage = self.link( (pmt_parser,"outbox"),(self,fromPMT) )

It then waits for the parsed table to be returned and searches for the
first PIDs it can find for an audio and a video stream:

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

### 4. Demuxing the audio and video packets 

Now the PIDs for packets containing the service\'s audio and video are
known, the final step is for *DVB\_TuneToChannel* to request to be sent
packets with those PIDs; so they can be sent on out of its \"outbox\"
outbox (to go to the file writer component):

            fromDemuxer = self.addInbox("fromDemuxer")
            self.send( ("ADD",[audio_pid,video_pid], (self,fromDemuxer)), toDemuxer)
            
            while 1:
                while self.dataReady(fromDemuxer):
                    packet = self.recv(fromDemuxer)
                    self.send(packet,"outbox")
                    
                self.pause()
                yield 1

So there you have it. *DVB\_TuneToChannel* uses various parsing
components that are part of Kamaelia to extract and interpret the
Program Specific Information tables available in a DVB multiplex
carrying an MPEG transport stream.\

\-- 04 Jan 2007, Matt\
