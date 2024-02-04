---
pagename: Cookbook/DVB/TransportStreamDemuxer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Separating out lots of channels from a recorded DVB broadcast 
========================================================================

Find this code here:\
[/Code/Python/Kamaelia/Examples/DVB\_Systems/TransportStreamDemuxer.py](http://svn.sourceforge.net/viewvc/kamaelia/trunk/Code/Python/Kamaelia/Examples/DVB_Systems/TransportStreamDemuxer.py?view=markup)

This simple example shows how to read back in a recorded transport
stream from a file and separate out (demultiplex) several channels from
it:

>     from Kamaelia.Device.DVB.Core import DVB_Demuxer
>     from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
>     from Kamaelia.Chassis.Graphline import Graphline
>     from Kamaelia.File.Writing import SimpleFileWriter
>
>     Graphline(
>         SOURCE=ReadFileAdaptor("BBC_MUX_1.ts"),
>         DEMUX=DVB_Demuxer({
>             640: ["NEWS24"],
>             641: ["NEWS24"],
>             600: ["BBCONE"],
>             601: ["BBCONE"],
>             610: ["BBCTWO"],
>             611: ["BBCTWO"],
>             620: ["CBBC"],
>             621: ["CBBC"],
>             18:  ["NEWS24", "BBCONE"],# "BBCTWO", "CBBC"],
>         }),
>         NEWS24=SimpleFileWriter("news24.data"),
>         BBCONE=SimpleFileWriter("bbcone.data"),
>         BBCTWO=SimpleFileWriter("bbctwo.data"),
>         CBBC=SimpleFileWriter("cbbc.data"),
>         linkages={
>            ("SOURCE", "outbox"):("DEMUX","inbox"),
>            ("DEMUX", "NEWS24"): ("NEWS24", "inbox"),
>            ("DEMUX", "BBCONE"): ("BBCONE", "inbox"),
>            ("DEMUX", "BBCTWO"): ("BBCTWO", "inbox"),
>            ("DEMUX", "CBBC"): ("CBBC", "inbox"),
>         }
>     ).run()

The *DVB\_Demuxer* component takes, at initialization, a dictionary
mapping packet IDs (PIDs) to outbox names. Each of those outboxes has
been linked to a *SimpleFileWriter* component to write it to a file.\

For all the channels there are two PIDs - one for the audio and one for
the video. For two of them, we also include PID 18 which carries Event
Information Tables (tables containing now & next and EPG data)\
