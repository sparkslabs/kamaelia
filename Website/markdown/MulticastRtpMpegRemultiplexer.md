---
pagename: MulticastRtpMpegRemultiplexer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Multicast RTP MPEG Remultiplexer
===================================================

::: {.boxright}
**Status:** Blocked *- Awaiting hardware purchase authorisation*\
**Current Developers:** *Matt*\
**Current \"inflight\" dev location:** */Sketches/MH/RTP/*\
**Start Date:** ??\
**Major Milestone date:** n/a\
**Expected End Date:** 22nd December 2006\
**End Date:** *tbd*\
**Date this page last updated:** *27th November 2006*\
**Estimated effort so far:** *??*\
:::

### Description

A tool to mix MPEG transport streams received over multicast in RTP
format; and rebroadcast as a new multicast RTP stream.\
\
Internal work on developing live multicast streaming services needs a
way to take data from one stream and mix it into another. The streams
are multicast RTP packets containing MPEG Transport Stream data. The
tool, when deployed should be able to run 24/7, combining a subset of
data from 2 or more streams to generate a new one.\
\
Benefits:\

-   RTP packetising/depacketising components
-   Possibly more MPEG components
-   Seleector and multicast component optimisations\

\

Inputs
------

Task Sponsor: BB (BBC internal)\
Task Owner: Matt (MH)\
Developers:\

-   Matt

Users:\

-   BB

Interested Third Parties\

-   RB (BBC internal)

Requirements (non exhaustive):\

Receive multicast RTP containing MPEG Transport Stream containing H264 @
\~1Mbit/s (MUST)

Simulataneously receive a 2nd multicast RTP containing MPEG Transport
Stream containing EIT data and MPEG2 video @ \~5Mbit/s (MUST)

Combine EIT data from 2nd stream with video from the 1st to form a new
stream (MUST)\

Transmit the new stream as multicast RTP (MUST)

Adjust stream timestamps (MPEG Transport Stream level, and possibly MPEG
Program Elementary Stream level) if needed (WOULD LIKE)

-   uncertain of this until able to test with various clients
-   Derived from discussions with RB\

Outputs
-------

### Expected

Components to parse and create RTP packets

Command line tool, as described

-   /Sketches/MH/RTP/RTPMux.py

Webpages describing:

-   architecture
-   usage\

### Actual

Code

RTP handling

-   /Sketches/MH/RTP/RTPFramer.py
-   /Sketches/MH/RTP/RTPDeFramer.py

Internet components (uprades/modifications)\

-   /Sketches/MH/RTP/Multicast\_transceiver.py
-   /Sketches/MH/RTP/Selector.py
-   /Sketches/MH/RTP/ConnectedSocketAdaptor.py

DVB/MPEG Transport stream processing

-   /Sketches/MH/DVB\_Remux/ExtractPCR.py\

Realistic possibilities arising as a result of activity on this task

New/modified components for mainline codebase (RTP, DVB)

-   review and merge some or all of the above components

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

-   n/a\

### Subtasks

Improved throughput of multicast component and Selector in general

-   rewrite multicast\_transceiver to use Selector
-   modified Selector to be instantly woken if a component requests to
    add a reader/writer/exceptional

Develop code\

Task Log
--------

-   05 October 2006 - Matt : Added developer Matt. **Task status
    changed** to Running\
-   11 October 2006 - Matt : development to date: Time spent 5 days.
    **Task status changed** to stasis\
-   12 November 2006 - Matt : Code modifications: Time spent 1/2 day.
-   20 November 2006 - Matt : **Task status changed** to blocked -
    requested, and awaiting, hardware & info on streams from BB\

Discussion
----------

Need to determine, experimentally, if timestamp resynchronisation
algorithms will be neededIf resynchronisation algorithms are needed.
Technically remultiplexing severely jitters the timestamps on the
transport stream packets.\

-   For a traditional Set-top-box style receiver device, these
    timestamps are used to regenerate the precise bitrate of the
    original data stream. They do this for the purposes of generating
    their own timing clocks for video and audio output. (RB)\
-   Computer based video players are probably less likely to use this as
    they don\'t have access or control over very accurate clocks, or the
    precise timing of their local sound and video subsystems. Instead
    they are more likely to simply buffer data and play it at their own
    rate. (Matt)
-   This may be a substantial piece of work, as MPEG PES packets will
    need decoding from transport stream packets and an algorithm would
    have to be identified or devised to calculate the new timestamps.
    This may be problematic as the original streams appear to be highly
    variable bitrate.\

CPU load is higher than anticipated - handling a single 1-2Mbit/s stream
takes 50%+ CPU usage on the Mac Mini currently being used for testing.
Faster hardware, and possibly further optimisations, are required.\
\
Selector component has been improved (local copy in the working dir) to
increase responsiveness. Specifically, instead of requests to select on
file handles queueing up at its inbox until the current select() call
timeout fires; a separate filehandle is used to wake it immediately if
there are pending requests.\
\
The Multicast components have been optimised (local copy in the working
dir) to sleep when inactive, using the Selector component to wake them.\
\
