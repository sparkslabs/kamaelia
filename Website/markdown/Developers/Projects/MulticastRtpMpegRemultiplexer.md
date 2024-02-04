---
pagename: Developers/Projects/MulticastRtpMpegRemultiplexer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Multicast RTP MPEG Remultiplexer {#project-task-page-multicast-rtp-mpeg-remultiplexer align="left"}
---------------------------------------------------

::: {.boxright}
**Status:** Blocked *- Performance bottlenecks - code can\'t run fast
enough*\
**Current Developers:** *Matt*\
**Current \"inflight\" dev location:** */Sketches/MH/RTP/*\
**Start Date:** ??\
**Major Milestone date:** n/a\
**Expected End Date:** 22nd December 2006\
**End Date:** *tbd*\
**Date this page last updated:** *27th November 2006*\
**Estimated effort so far:** *9 days*\
:::

Description
-----------

A tool to mix MPEG transport streams received over multicast in RTP
format; and rebroadcast as a new multicast RTP stream.\
\
Internal work on developing live multicast streaming services needs a
way to take data from one stream and mix it into another. The streams
are multicast RTP packets containing MPEG Transport Stream data. The
tool, when deployed should be able to run 24/7, combining a subset of
data from 2 or more streams to generate a new one. This would be used,
for example, to mix existing EPG data into an existing stream containing
audio and video.\
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

User

-   BB

Interested Third Parties\

-   RB (BBC internal)

Requirements (non exhaustive):\

Receive multicast RTP containing MPEG Transport Stream containing H264 @
\~1Mbit/s (MUST)

Simulataneously receive a 2nd multicast RTP containing MPEG Transport
Stream containing EIT data and MPEG2 video @ \~5Mbit/s (MUST)

Combine (demultiplex and remultiplex) EIT data from 2nd stream with
video from the 1st to form a new stream (MUST)\

Transmit the new stream as multicast RTP (MUST)

Adjust stream timestamps (MPEG Transport Stream level, and possibly MPEG
Program Elementary Stream level) if needed (WOULD LIKE)

-   uncertain of this until able to test with various clients
-   Derived from discussions with RB

Relevant Influencing factors:\

-   *eg release of a tool doing the same sort of thing that renders this
    non-relevant*
-   *people joining/leaving project*
-   *change of sponsorship*
-   *growth in users/thirdparties*
-   *tool dependency suitablility*
-   *unexpected complications*
-   *speed of available hardware / speed of Axon/Kamaelia\
    *

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

SDP handling

-   /Sketches/MH/RTP/SDP.py\

DVB/MPEG Transport stream processing

-   /Sketches/MH/DVB\_Remux/ExtractPCR.py

case-insensitivity problem fixed for /trunk/

\...removing filename clash problems for case insensitive filesystems
like that on win32/osx

-   Code/Python/Kamaelia/Kamaelia/Util/passThrough.py\

### Realistic possibilities arising as a result of activity on this task

New/modified components for mainline codebase (RTP, DVB)

-   review and merge some or all of the above components

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

-   [DVB Tools](/Developers/Projects/DVBTools%20)
-   TCP Subsystem\

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
    requested, and awaiting, hardware & info on streams from BB
-   06 December 2006 - Matt : **Task status changed** to running - got
    new hardware
-   11 Decemeber 2006 - Matt : Built initial then \'proper\' SDP parser.
    Time spent 2 days
-   14 December 2006 - Matt : Code doesn\'t run fast enough.
    Investigated options and determined a possible solution involving
    modifying Axon (should be a separate task). **Task status changed**
    to blocked. Time spent 1.5 days\

Discussion
----------

### Stream Synchronisation Timestamps may need regenerating 

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

### CPU load higher than anticipated

CPU load is higher than anticipated - handling a single 1-2Mbit/s stream
takes 50%+ CPU usage on the Mac Mini currently being used for testing. A
faster \"Core Duo\" Mac Mini has been tried, but the system struggles to
keep up with the 4Mbps MPEG2 stream (ie. usage teeters close to
90%/100%).\
\
**Multicast I/O improvements**\
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
**Threaded component bottlenecks**\
\
I\'ve also tried writing\
\
Why? Interactions between a thread and the main thread are
bottlenecked:\

-   the thread (doing the select() calls in the case of the Selector)
    passes addOutbox, deleteOutbox, link and unlink operations to the
    main thread and waits for it to do them. It does this (and has to
    wait) to ensure thread safety. Since Selector makes and removes the
    boxes and linkages used every time it handles a request to wait on a
    socket/file.
-   sending and receiving messages is done via a \'proxy\' microprocess
    running in the main thread. In the case of components like the
    Selector, this extra overhead is probably equal to the time being
    spent in the thread.\

Each component is taking between 10% and 20% CPU. Moving the Selector or
Multicast components themselves into separate threads doesn\'t reduce
the amount of CPU being spent in the main thread. The Mac Mini could
probably cope if it were possible to spread some of the workload across
the 2nd CPU without incurring a penalty in the main thread.\
\
**Proposal: Axon modifications**\
\
I believe there may be mileage in experimenting with modifying Axon such
that threads can perform all tasks themselves, using (hopefully fine
grained) locking to ensure thread safety. This would eliminate the need
for threaded components to have a microprocess running in main thread
handling all its requests. This would substantially reduce the overhead
incurred when making a component threaded. It would potentially also
have the benefit that two components running in threads independant of
the main thread would not be bottlenecked by the needing the main thread
to handle message passing on their behalf.\
\
This would probably qualify as a separate project task, lasting a few
weeks.\
\
**Other routes to try first**\
\
Michael suggests that such a radical approach may well not be necessary.
Instead the following perhaps should be tried first:\

-   converting intensive data manipulation tasks (such as RTP demuxing
    and remuxing) to pyrex code (ie. converting it partially to C). The
    MPEG demuxer is already pyrex\'ed.
-   Grouping data into larger chunks for message passing between
    components - reducing the message passing overheads per mpeg/rtp
    packet

\
