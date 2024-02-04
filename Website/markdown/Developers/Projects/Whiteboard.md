---
pagename: Developers/Projects/Whiteboard
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Whiteboard
-----------------------------

::: {.boxright}
**Status:** Stasis *-* This tool is currently useful, so no effort
allocated, future work possible however\
**Current Developers:** *na*\
**Current \"inflight\" dev location:**
/Code/Python/Kamaelia/Tools/Whiteboard\
**Start Date:** 16 Apr 2006\
**Expected End Date:** n/a\
**End Date:** n/a\
**Date this page last updated:** 3 December 2006\
**Estimated effort so far:** 15 (estimate based on logs)\
:::


**Description**
---------------

This whiteboard application is designed to allow two or more people
using tablet PCs (or similar devices) to collaborate effectively at a
distance, and also to make good use of the fact they\'re using tablet
PCs.\
\
Two users should be able to talk and scribble to each other. It should
not matter who starts up first allowing connections in either direction.
It would be useful if any client could be a server. Having a history is
also useful and how this can be used is worth exploring.\
\
This tasks sits in the context that the Kamaelia team inside the BBC
(Michael/Matt) is now split site, and a tool was needed to assist with
collaboration. Since Kamaelia is network friendly, this tasks started
opportunistically - to see if something worthwhile could come of this.
This has turned out to be an extremely useful tool since then.\
\
Direct benefits as a result of this task:\

-   A useful tool for split/multi -site co-operation.
-   There\'s been a number of ancilliary / unexpected benefits as well.
-   Tools for sending audio across the network\

**Current issue:**\

-   Audio quality is not as good as it could be hampering usage.
    (probably due to initial sampling rate being too low)

Inputs
------

This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\

Task Sponsor: Michael/Matt

Task Owner: Matt (varies)\

Developers involved in the task at some point\

-   Michael
-   Matt\

Users:

-   MPS, MH

Interested third parties

-   HW - is interested in a version for Mac OS X
-   fo.am collaborators
-   Linux Format\

Requirements

-   MUST allow for the ability to draw in pictures (MH)
-   MUST allow pictures to be shared over a network connection and
    collaboratively editted in realtime - really shared (MH)
-   MUST allow a client server set up (MH)
-   WOULD LIKE the ability to send audio over the same connection (MH)
-   WOULD LIKE the ability to send video over the same connection (MH)
-   WOULD LIKE low bandwidth audio (eg speex) (MH)
-   WOULD LIKE page histories (MPS)
-   WOULD LIKE synchronised changing of page histories for presentations
    (MPS)
-   WOULD LIKE the ability to scribble over synchronised video (HW)\
-   WOULD LIKE the underlying events plane extracted (MPS)
-   WOULD LIKE the ability to record and playback sessions (MPS/MH)\

The people listed here should be real people. Unless you have agreement
however, this this should be their initials rather than name.\
\
Relevant Influencing factors:\

-   Summer of code student playing with speex made it clear that speex
    is sufficient stable for use
-   Collaborator on kamaelia-list experimenting with pymedia made it
    look like pymedia was worth another look
-   A simple paint program had already been written.
-   The tool has a certain \"wow\" factor when running on a laptop for
    people since users aged 3 - 60 are able to understand how to use it.
    Part of this \"wow\" comes from keeping out of the way.\

Outputs
-------

### Expected

-   A simple to use tool for scribbling at each other over a distance\

### Actual

Code sits here:\

-   /Code/Python/Kamaelia/Tools/Whiteboard
-   This has been tested and is used successfully on Linux based
    machines\

Documentation\

-   An article on the whiteboard was written for Linux Format - it
    appeared in the December 2006 issue. It will appear on this site
    shortly.\

Event\

-   The whiteboard was the focus (due to interest) of a Kamaelia Open
    Space event in Brussels immediately following Euro OSCON 2006

### Realistic possibilities arising as a result of activity on this task

Two potentially highly interesting possibilities arising as a result of
work on the whiteboard were discussed in Summer of Code 2006 project
applications:

-   [Generalised network events
    backplane](/Projects/Soc2006/GeneralisedEventsBackplane)\
-   [Peer to Peer streaming](/Projects/Soc2006/PeerToPeerStreaming) (The
    audio aspects of the whiteboard if removed have potential)

Other\

-   It would be useful to work on improving audio capture, and audio
    filtering & resampling to improve low bit rate audio to desirable
    levels. (current approach is non-optimal)

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   Backplane
-   Pluggable Splitter
-   TCP Subsystem
-   Pygame Display Subsystem
-   Speex work from SoC
-   Axon Service facility\
-   Audio mixing code from Collaborative Community Radio Rapid
    Prototyping

### Sub Tasks

-   na - written after the fact - Probably useful to flesh out at some
    point.\

Task Log
--------

*Written after the fact, so only key highlights\
*

*This is a list of time indexed day to day item. There should ideally be
an entry here every time you work on this task. Ideally the time taken
relating to each entry should be listed as well, preferably in man days,
down to 1/4 day granuarity. (ie 2 hours). Sanity is expected to prevail
when noting this down. They should be annotated by who made the entry,
when, and any status changes.*\

***When a task is running, then this is where most updates will
occur.**\
\
Please put **Output** in bold prior to any entries where an output was
produced\
Please put **Task status changed** in bold when the entry relates to a
task status change.\
Example entries:*\

-   Matt - April 2006 - Initial version created
-   Michael - July 2006 - History/pagination & remote control of
    whiteboard added\
-   Matt - August 2006 - Audio added by Matt
-   Michael - August 2006 - Video whiteboard sketch created
-   Matt - August 2006 - Audio improvements
-   Michael - September 2006 - Merge of improved code into mainline &
    released
-   Michael - September 2006 - Tutorial on whiteboard written
-   Michael - 27th November 2006 - PTP Page created

Discussion
----------

The whiteboard was started to solve a particular problem caused by split
site working. History & Pagination was added due to a need for these
features at OSCON for note taking. As a result the whiteboard has a very
minimalist UI to keep out of the way of the user.\

\-- Michael Sparks, December 3rd 2006

\
