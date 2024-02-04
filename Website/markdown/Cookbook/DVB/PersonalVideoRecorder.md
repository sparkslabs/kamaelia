---
pagename: Cookbook/DVB/PersonalVideoRecorder
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Recording named programmes from a DVB broadcast {#cookbook-recording-named-programmes-from-a-dvb-broadcast align="left"}
==========================================================

Find the code for this here:\
[/Code/Python/Kamaelia/Examples/DVB\_Systems/PersonalVideoRecorder.py](http://svn.sourceforge.net/viewvc/kamaelia/trunk/Code/Python/Kamaelia/Examples/DVB_Systems/PersonalVideoRecorder.py?view=markup)\

So we can record a [whole
broadcast](../../../Cookbook/DVB/TransportStreamCapture), or a single
channel [determined by its
name](../../../Cookbook/DVB/RecordNamedChannel); but what about
recording individual programmes?\

[]{#recordForMe} recordForMe component 
--------------------------------------

We can create a component to handle each recording we want to make.The
*recordForMe* component takes a channel name, programme name, and
filename and will record anything broadcast on that channel with that
name:

>     programmes_to_record = [
>            #  Channel     programme   filename
>            ( "BBC ONE", "Neighbours", "/data/neighbours.ts" ),
>            ( "BBC TWO", "Newsnight",  "/data/Newsnight.ts" ),
>         ]
>
>     ...
>
>     for (channel, programme,filename) in programmes_to_record:
>         recordForMe(channel,programme,filename).activate()
>
>     ...
>
>     scheduler.run.runThreads()

What does *recordForMe* need to do:

-   work out when the programme starts and stops (programme junctions)
-   work out what packet IDs contain the audio and video for the named
    channel
-   ask to be sent packets with those IDs
-   write the packets to a file\

The *recordForMe* component is therefore a simple pipeline:

>     def recordForMe(channel, programme, filename):
>         return \
>             Pipeline( SubscribeTo("nowEvents"),
>                       ProgrammeDetector( channel_name=channel, programme_name=programme,
>                                          fromChannelLookup="LookupChannelName"),
>                       ControllableRecorder( channel_name=channel,
>                                             fromDemuxer="DEMUXER",
>                                             fromPSI="PSI_Tables",
>                                             fromChannelLookup="LookupChannelName"),
>                       SimpleFileWriter(filename),
>             )

It does the following:\

1.  It subscribes to a source of events that happen at junctions, when
    one programme finishes and another begins;
2.  *[ProgrammeDetector](#ProgrammeDetector)* examines the events to see
    whether it indicates the start or end of the programme and sends out
    \"START\" and \"STOP\" messages;
3.  [*ControllableRecorder*](#ControllableRecorder) works out what
    packet IDs contain the audio and video for the channel so it can
    request them from the demuxer. It can then respond to the \"START\"
    and \"STOP\" by requesting the audio and video packets and sending
    them on;
4.  *SimpleFileWriter* simply dumps the packets it receives to a file.

Already we can see that each *recordForMe* instance will need to share
access to the received DVB broadcast - specifically to do the
following:\

-   Get programme junction events information
    ([\"nowEvents\"](#nowEvents) named service)
-   Convert channel names to service IDs
    ([\"LookupChannelName\"](#LookupChannelName) named service)
-   Ask to be sent audio and video packets ([\"DEMUXER\"](#DEMUXER)
    named service)
-   Possibly reconstruct other broadcast data tables
    ([\"PSI\_Tables\"](#PSI_Tables) named service)\

Supporting services: demuxer, PSI tables, & channel names
---------------------------------------------------------

The supporting services are implemented as named services that
components can talk to.

### []{#DEMUXER} Demuxing packets from the broadcast

The most basic service needed is the ability to request to be sent
packets (with specific IDs) that have been received from the broadcast
stream:

>     import dvb3.frontend
>
>     FREQUENCY = 505833330/1000000.0
>     FE_PARAMS = { "inversion" : dvb3.frontend.INVERSION_AUTO,
>                   "constellation" : dvb3.frontend.QAM_16,
>                   "coderate_HP" : dvb3.frontend.FEC_3_4,
>                   "coderate_LP" : dvb3.frontend.FEC_3_4,
>                 }
>     ...
>
>     from Kamaelia.Device.DVB.Receiver import Receiver
>
>     ...
>
>     RegisterService( Receiver( FREQUENCY, FE_PARAMS, 0 ),
>                      {"DEMUXER":"inbox"},
>                    ).activate()

The *Receiver* component is a combined tuner and demulipliexer service,
capable of handling requests from multiple client components asking to
be sent packets. Its \"inbox\" inbox is registered as a named service
for clients to access it by.\

Note that this system is hard wired to tune to a single broadcast
multiplex. If the programmes you want to record are on a different
channel, then its tough luck!\

### []{#PSI_Tables} Reconstruction of Program Specific Information (PSI) tables

PSI tables, containing information about the broadcast stream, will be
needed by several parts of the system. The *ReassemblePSITablesService*
component can provide this as a service that other components can
subscribe to:\

>     from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITablesService
>
>     RegisterService( \
>          Graphline( PSI     = ReassemblePSITablesService(),
>                     DEMUXER = ToService("DEMUXER"),
>                     linkages = {("PSI", "pid_request") : ("DEMUXER", "inbox"),
>                                 ("",    "request")     : ("PSI",     "request"),
>                     }
>                   ),
>          {"PSI_Tables":"request"}
>     ).activate()

The component is linked to the \"DEMUXER\" service so it can request
packets as it needs them to be able to service requests for tables from
clients. Its \"request\" inbox is then registered as a named service for
clients to access it by.\

### []{#nowEvents} \'Now\' event information

We are now in a position to extract and parse the Event Information
Tables (EIT), process it down to individual events for when programmes
start, and make them available on a \"nowEvent\" Backplane:\

>     Pipeline( Subscribe("PSI_Tables", [EIT_PID]),
>               ParseEventInformationTable_Subset( True, False, False, False),
>               FilterOutNotCurrent(),
>               SimplifyEIT(),
>               NowNextProgrammeJunctionDetect(),
>               PublishTo("nowEvents"),
>             ).activate()
>
>     Backplane("nowEvents").activate()

The steps involved, above, are:

1.  Requesting to be sent Event Information Tables\
2.  Parsing them (only those containing \'now & next\' information for
    all services - channels - on [this]{.underline} multiplex)
3.  Ignoring any tables that are not currently applicable
4.  Simplifying the tables down to messages containing individual events
5.  Filtering down to only those events that indicate the start of a new
    programme (a programme junction)
6.  Making the events available to other components via a Backplane\

### []{#LookupChannelName} Looking up channel names

The final service needed is one for mapping a channel name to its
numeric service ID. Again, this is implemented as a named service:\

>     RegisterService( \
>         Graphline( TABLE_SOURCE = Subscribe("PSI_Tables", [SDT_PID]),
>                    PARSING =ParseServiceDescriptionTable_ActualTS(),
>                    LOOKUP = ChannelNameLookupService(),
>                    linkages = {
>                        ("","inbox")               : ("LOOKUP", "request"),
>                        ("TABLE_SOURCE", "outbox") : ("PARSING", "inbox"),
>                        ("PARSING", "outbox")      : ("LOOKUP", "inbox"),
>                    }
>                  ),
>         {"LookupChannelName" : "inbox"}
>     ).activate()

The mappings needed are in the Service Description Table, so that table
is requested from the \"PSI\_Tables\" reconstruction service and is
parsed by an *ParseServiceDescriptionTable\_ActualTS* component.

*ChannelNameLookupService* component is fed the parsed tables, and keeps
a note of the most recent, so it can perform lookups when requested by
clients.

The key aspects of the ChannelNameLookupService component is its main
loop, for handling requests and receiving new tables:

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

\... and how it resolves the channel name to its corresponding service
ID and transport stream ID:

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

\

The rest of the code for this component handles adding and removing
subscribers. Client subscribe, rather than issue a single-shot request,
because it is always possible the mappings may change during the
broadcast.\

[]{#ProgrammeDetector} ProgrammeDetector component
--------------------------------------------------

Needed by [*recordForMe*](#recordForMe), this component examines the
programme junction events it is sent, and determines when to start and
stop recording.

It looks up the channel name it has been given using the [channel name
lookup service](#LookupChannelName), so it can know which events to
watch for:\

        def main(self):

            ...
            
            channelLookup = Subscribe(self.fromChannelLookup, [self.channel_name]).activate()
            self.link( (channelLookup,"outbox"), (self, "_fromChannelLookup") )
            while not self.dataReady("_fromChannelLookup"):
                self.pause()
                yield 1
            
            channel_name, service_id, ts_id = self.recv("_fromChannelLookup")

It can then go into a loop, waiting until it sees an event for the start
of a programme with the right programme name and service ID. It can then
send on a message to instruct the recorder to start:\

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

The component then waits for an event signalling the start of another
programme with the same service ID but a different programme name. It
can then signal the recorder to stop:\

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

[]{#ControllableRecorder} ControllableRecorder component 
--------------------------------------------------------

Needed by [*recordForMe*](richtextframe.html#recordForMe), this
component works out what packet IDs contain the audio and video data for
the channel, then waits to be instructed to start or stop. It requests
the audio and video packets from the demuxer whilst it is supposed to be
recording.\

First it looks up the channel name it has been given using the [channel
name lookup service](richtextframe.html#LookupChannelName):

        def main(self):
            ...

            channelLookup = Subscribe(self.fromChannelLookup, [self.channel_name]).activate()
            self.link( (channelLookup,"outbox"), (self, "_fromChannelLookup") )
            while not self.dataReady("_fromChannelLookup"):
                self.pause()
                yield 1
            
            channel_name, service_id, ts_id = self.recv("_fromChannelLookup")

Armed with the service ID, it can then look in the Program Association
Table (PAT) to find the packet ID for the corresponding Program Map
Table (PMT). The PMT lists what packet IDs contain the audio and video
data.\

A ParseProgramAssociationTable component is fed the table from the
[\"PSI\_Tables\"](#PSI_Tables) service, to parse it: (the service name
is in *self.fromPSI*)\

            pat_parser = Pipeline( Subscribe(self.fromPSI, [PAT_PID]),
                                   ParseProgramAssociationTable()
                                 ).activate()
            
            fromPAT_linkage = self.link( (pat_parser,"outbox"),(self,"_fromPAT") )

The parsed table is collected, then searched for the packet ID of the
PMT for the given service ID:\

            # wait until we get data back from the PAT
            PMT_PID = None
            while PMT_PID == None:
                while not self.dataReady("_fromPAT"):
                    self.pause()
                    yield 1
            
                pat_table = self.recv("_fromPAT")
                
                for transport_stream_id in pat_table['transport_streams']:
                    ts_services = pat_table['transport_streams'[]transport_stream_id]
                    if service_id in ts_services:
                        PMT_PID = ts_services[service_id]
                        break

It then sets up another parser component to parse the right PMT:

            pmt_parser = Pipeline( Subscribe(self.fromPSI, [PMT_PID]),
                                   ParseProgramMapTable()
                                 ).activate()
            
            fromPMT_linkage = self.link( (pmt_parser,"outbox"),(self,"_fromPMT") )

            print "Found PMT PID for this service:",PMT_PID

The parsed table is collected, then searched for the packet IDs for the
audio and video:\

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

*ControllableRecorder* is now ready, so it links up to the [\"DEMUXER\"
service](#DEMUXER), and waits to receive the \"START\" order:

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

To start recording, it sends a request to the demultiplexer, asking to
be sent the audio and video packets for the service:

                # request audio and video data
                self.send( ("ADD",[audio_pid,video_pid], (self,"_av_packets")), "_toDemuxer")

And forwards them out of its \"outbox\" outbox until it receives the
\"STOP\" command:

                while recording:
                    while self.dataReady("_av_packets"):
                        packet = self.recv("_av_packets")
                        self.send(packet,"outbox")
                        
                    while self.dataReady("inbox"):
                        recording = not ( self.recv("inbox") == "STOP" )
                        
                    if recording:
                        self.pause()
                    yield 1

Once it has been told to stop, it sends another request to the
demultiplexer, asking to stop being sent audio and video packets:

                self.send( ("REMOVE", [audio_pid,video_pid], (self,"_av_packets")), "_toDemuxer")

This is quite a long example, but demonstrates that you can build quite
complex systems, like a PVR in quite a modular fashion.
