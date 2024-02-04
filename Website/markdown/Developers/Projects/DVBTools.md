---
pagename: Developers/Projects/DVBTools
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: DVBTools
===========================

::: {.boxright}
**Status:** Stasis *- No other tasks currently requiring further
development of these components*\
**Current Developers:** *Matt*\
**Current \"inflight\" dev location:**\

-   /Code/Python/Kamaelia/Kamaelia/Devices/DVB/
-   /Code/Python/Kamaelia/Kamaelia/Support/DVB/\

**Start Date:** 06 May 2006\
**Major Milestone date:**

-   09 June 2006 : Code to enable Macro demonstrator complete.\

**Expected End Date:** *n/a*\
**End Date:** *??*\
**Date this page last updated:** *28th November 2006*\
**Estimated effort so far:** \~ 50 days (estimate)\
:::

**\
**

**Description**
---------------

Components and example code and tools for receiving Digital Video
Broadcasting (DVB) transmissions and parsing and handling the MPEG
transport stream (TS) contained in it. Particularly with a mind to the
creation of television timeshifting tools.\
\
Using these components it should be relatively simple to instantiate
Kamaelia systems capable of using a PC based DVB tuner device to receive
an off-air broadcast in real time; extracting audio and video or
additional meta data such as \"now and next\" or \"electronic programme
guide\" (EPG) from the stream.\
\
Simple examples or tools will demonstrate and explain the ways these
components can be used to achieve tasks such as recording programmes.\
\
Benefits:\

-   Substantial set of extra components providing interesting and useful
    capabilities (receiving and handling digital TV broadcasts)
-   Motivation for optimising the throughput of Kamaelia systems to
    handle the high data rates (up to 10s of Mbits/s)
-   Enables [Kamaelia Macro](/Developers/Projects/KamaeliaMacro) work\

Inputs
------

Task Sponsor: TL (BBC internal)\
Task Owner: Michael (MPS), Matt (MH)\
Developers:\

-   Michael\
-   Matt\

Users:\

-   MPS, MH (direct users of components)
-   TL, etc (users of systems incorporating them)

Interested third parties:\

-   MB, PC (BBC internal)\

Requirements:\

MUST be able to operate in real time

MUST be able to tune and receive transport stream from a terrestrial
(receive through aerial) DVB PCI or USB tuner.

MUST support Linux

MUST be able to extract transport stream packets with specific packet
IDs (PIDs)

MUST be able to extract Event Information Table (EIT) data containing
\"now & next\" information

WOULD LIKE to be able to extract additional meta data, making it
possible to:

-   determine the PIDs containing a given service (channel)
-   map channel names to service IDs
-   locate and extract subtitling data
-   extract EPG data for the next 7 days (as broadcast in the UK)\

WOULD LIKE to support Mac, Windows\

\
Relevant Influencing factors:\

*\"python-dvb3\" bindings (to Linux DVB API) donated by MB & PC\
*

Relevant standards documentation: (all are publicly available at no
charge to the best of my knowledge \-- Matt)

-   *ISO/IEC 13818-1* (aka \"MPEG: Systems\") \"Generic Coding of Moving
    Pictures and Associated Audio: Systems\" ISO / Motion Picture
    Experts Group
-   *ETSI EN 300 468* \"Digital Video Broadcasting (DVB): Specification
    for Service Information (SI) in DVB systems\" ETSI / EBU (DVB group)
-   *\"Digitial Terrestrial Television: Requirements for
    Interoperability\"* Issue 4.0+ (aka \"The D book\") UK Digital
    Television Group (DTG)\

Outputs
-------

### Expected

Code in /Code/Python/Kamaelia/Kamaelia/Device/DVB/:\

-   control a DVB device under Linux (tuning and receiving transport
    stream packets)
-   demultiplex transport stream packets (using DVB card facilities)
-   demultiplex transport stream packets (in software)
-   extract and parse information tables from the stream

Small example code fragments demonstrating functionality provided by
components

Example \'tools\' demonstrating applications (eg. recording a channel or
programme)

Tutorial webpages

### Actual 

First iteration code (for Kamaelia Macro initial demonstrator):

Example tools:

-   /Code/Python/Kamaelia/Examples/DVB\_Systems/SingleChannelTransportStreamCapture.py
-   /Code/Python/Kamaelia/Examples/DVB\_Systems/TransportStreamCapture.py
-   /Code/Python/Kamaelia/Examples/DVB\_Systems/TransportStreamDemuxer.py

Components for controlling tuner device and demultiplexing:\

-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Core.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/SoftDemux.py

Components for parsing stream metadata:

-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/NowNext.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/PSITables.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/EIT.py

Second iteration code (post Macro):

Example tools:

/Code/Python/Kamaelia/Examples/DVB\_Systems/PersonalVideoRecorder.py

-   uses EPG and other metadata tables to record programmes, specified
    by programme name and channel name\

/Code/Python/Kamaelia/Examples/DVB\_Systems/RecordNamedChannel.py

-   uses metadata tables to record a channel, specified by channel name\

Components for controlling tuner device and demultiplexing:

-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Receiver.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Tuner.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/DemuxerService.py

Compoents for parsing stream metadata:

-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseEventInformationTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseProgramAssociationTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseNetworkInformationTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseProgramMapTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseServiceDescriptionTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseTimeAndDateTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ParseTimeOffsetTable.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/PrettifyTables.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/Parse/ReassemblePSITables.py

Support code (CRC checks & parsing data formats/structures)\

-   /Code/Python/Kamaelia/Kamaelia/Support/DVB/CRC.py
-   /Code/Python/Kamaelia/Kamaelia/Support/DVB/DateTime.py
-   /Code/Python/Kamaelia/Kamaelia/Support/DVB/Descriptors.py

Experimental code for making it easier to create and access CAT
registered services:\

-   /Code/Python/Kamaelia/Kamaelia/Experimental/Services.py\

### Realistic possibilities arising as a result of activity on this task

-   Build an Electronic Programme Guide browsing interface
-   Build a \'traditional\' PVR style application, by combining an EPG
    browsing interface into a UI for scheduling programmes to record for
    later viewing
-   Devise code to capable of retuning to a different broadcast
    multiplex to get to a required TV channel
-   Build a radio recorder/PVR\

\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   Axon optimisations to message passing along linkages.\

### Sub Tasks

For Kamaelia Macro initial demonstrator:\

-   Incorporation of python-dvb3 bindings into mainline

```{=html}
<!-- -->
```
-   Write tuner and demultiplexer components

```{=html}
<!-- -->
```
-   Write Program Status Info (PSI) table parser (enables access to
    metadata tables)\

```{=html}
<!-- -->
```
-   Write EIT parser to extract Now & Next information\

```{=html}
<!-- -->
```
-   Write optimised software demuliplexer (doesn\'t use DVB device
    facilities)\

Further work:

Write parsers for remaining metadata table types:

-   Network Information Table (NIT)
-   Program Association Table (PAT)
-   Program Map Table (PMT)
-   Service Description Table (SDT)
-   Time and Date Table (TDT)
-   Time Offset Table (TOT)

Write prettifiers to make output from table parsers more human readable
(for debugging & diagnostic purposes)\

Rewrite PSI parser to behave as a \'service\' able to dynamically serve
table data to multiple table parsers, as requested

Refactor tuner and demultiplexing components to behave as a \'service\'
able to dynamically serve packets with particular PIDs, as requested\

Task Log
--------

Retrospectively generated entries (no guarantees of completeness!)\
\

-   19 January 2006 - Added developer Michael. Checked in experiments
    into /Sketches/MPS/DVB\
-   23 January 2006 - Michael : Checked in donated python-dvb3 bindings
-   17 March 2006 - Michael : Improvements to experiments\
-   06 May 2006 - Michael : **Task status changed** to running.
    Developing in /Sketches/MPS/DVB/\
-   06 May 2006 - Added developer Matt. Developing in
    /Sketches/MH/DVB\_EIT
-   09 June 2006 - Matt : **Task status changed** to stasis - code
    necesary for Macro demonstrator complete and working(!)
-   19 June 2006 - Matt : **Task status changed** to running - Matt
    continuing work on table parsing.
-   13 July 2006 - Matt : **Task status changed** to blocked - uncertain
    what to do next + other stuff: holidays, providing Google SoC
    support, pymedia components, etc.\
-   11 September 2006 - Matt : **Task status changed** to running -
    documenting components and preparing for merge into mainline
-   13 September 2006 - Matt : \'PVR\' example app checked into
    /Sketches/MH/DVB\_PSI\
-   03 October 2006 - Matt : **Task status changed** to stasis -
    components documented and merged into mainline

Live entries\

-   28 November 2006 - Matt : created this task page\
-   07 December 2006 - Matt : Fixed long standing software MPEG TS
    demuxer bug. Time spent 1/2 day.

Discussion
----------

Upon investigating how to handle metadata tables containing information
such as audio and video PID values, channel names etc. it turned out
that often the packet IDs containing tables are dynamically set - you
need to look it up in another table first.\
\
This generated the need to modify the demultiplexing components to be
able to change what PIDs they extract, and where they send them to, at
runtime. Similarly, Matt decided to apply the same logic to the
packet-\>table data conversion (PSI parsing) step.\
\
The EIT parsing code was rewritten (1 day) to match the same code design
used for parsing all the other tables, and to add the ability to extract
the full 7 day programme guide data.\
\
\
