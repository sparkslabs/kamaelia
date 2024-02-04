---
pagename: Developers/Projects/MobileReframer
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: MobileReframer
---------------------------------

Description 
-----------

::: {.boxright}
**Status:** Blocked - awaiting demonstration server to install onto**\
Current Developers:** *Matt***\
Current \"inflight\" dev location:** */Sketches/MH/MobileReframe***\
Start Date:** *12 October 2006***\
Major Milestone date:** \--**\
Expected End Date:** 5 December 2006**\
End Date:** *\-\--***\
Date this page last updated:** *30 November 2006***\
Estimated effort so far:** *21*.25\
:::

The aim is to create a back-end tool that decodes a video clip; applies
edit decisisions (cutting, cropping and scaling); and re-encodes it. The
idea is to cut and crop video to make it suitable for playback on a
small screen mobile device.\

This will slot in as a back-end for a web based video reframing internal
BBC demonstrator. A flash based web front end will be used to generate
the edit decision list as XML data. This reframer tool will then be run
by the server to apply those edit decisions to a video clip. A user will
be able to upload a video; reframe it using the front end; then download
the reframed video.\
\
Benefits include:\
\

-   A good test for the Axon bugfix of enabling components to be woken
    when data is consumed at a destination\'s inbox.
-   Creation of video and audio file parsing and writing components
-   Creation of video processing components (cropping and scaling)

Inputs
------

Task Sponsor: SJ (BBC internal)\
Task Owner: Matt (MH)\
Developers:\

-   Matt

Users:\

-   SJ (BBC internal)\

Interested Third Parties:\

-   n/a

Requirements (non exhaustive):\

-   MUST be launchable from the command line (MUST)\
-   accept edit decisions as an XML file matching a defined schema
    (MUST)\
-   Edit decisions may include only a subset of the original clip
    (MUST)\
-   Edit decisions may sequence clips in a different order to that of
    the riginal video (WOULD LIKE)\
-   Self rate limiting (so CPU and memory usage are held in check)
    (MUST)\
-   Use ffmpeg/mencoder to decode and encode video (SHOULD)

Relevant Influencing factors:\

-   *eg release of a tool doing the same sort of thing that renders this
    non-relevant*
-   *people joining/leaving project*
-   *change of sponsorship*
-   *growth in users/thirdparties*
-   *tool dependency suitablility*
-   *unexpected complications*

Outputs
-------

### Expected

Code in /Sketches\

New Video processing components

New Video and Audio file parsing and writing components

New XML parsing components\

Experimental modifications to existing components to handle noSpaceInBox
exceptions

-   Pipeline, Graphline, Carousel, etc\...

Webpages describing:

-   architecture
-   how to use

Feature in presentation to Mobile SIG (BBC internal)\

### Actual

Code

Mobile reframer specific:\

/Sketches/MH/MobileReframe/MobileReframer.py

-   The mobile reframer application itself\

```{=html}
<!-- -->
```
-   /Sketches/MH/MobileReframe/EDL.py

```{=html}
<!-- -->
```
-   Parsing of tokenised XML containing the Edit Decision List\

Video components

/Sketches/MH/Video/YUV4MPEG.py

-   YUV4MPEG file format parsing/generation\

/Sketches/MH/Video/CropAndScale.py

-   Cropping and scaling of video frames\

Audio components:

/Sketches/MH/audio/WAV.py

-   WAV file format parsing\

/Sketches/MH/audio/ToWAV.py

-   WAV file format generation\

General purpose components:

/Sketches/MH/MobileReframe/TagWithSequenceNumber.py\

-   Tagging data with sequence numbers\

/Sketches/MH/MobileReframe/OneShot.py\

-   Sending one-off messages\

/Sketches/MH/MobileReframe/PromptedTurnstile.py\

-   Buffering of data until needed\

/Sketches/MH/MobileReframe/FirstOnly.py\

-   Extracting the first item of data\

/Sketches/MH/MobileReframe/Chunk.py\

-   chunking of data to match a required chunkrate\

/Sketches/MH/MobileReframe/Sync.py\

-   waiting for \'n\' items before continuing\

/Sketches/MH/MobileReframe/Collate.py\

-   collate all data together\

/Sketches/MH/MobileReframe/RangeFilter.py\

-   filter items not within specified ranges\

/Sketches/MH/MobileReframe/Max.py

-   select the maximum value from a list\

Chassis-style components:

/Sketches/MH/MobileReframe/InboxControlledCarousel.py\

-   Variation of Carousel component\

/Sketches/MH/MobileReframe/Chassis.py\

-   box size limit setting versions of Carousel,Pipeline,Graphline\

/Sketches/MH/MobileReframe/Seq.py\

-   runs one component then the next, then the next\...\

Process components:

/Sketches/MH/MobileReframe/UnixProcess.py\

-   Variant of UnixProcess component with multiple I/O pipes and
    noSpaceInBox handling

XML components:

/Sketches/MH/MobileReframe/SAXPromptedParser.py

-   Parsing of a stream of XML data using SAX, outputting only when
    prompted for more data

Webpages

-   [Explanation of how to use the mobile reframer](/MobileReframer%20)\

### Realistic possibilities arising as a result of activity on this task

New components for the mainline codebase

-   review and merge some or all of the above components

Writing a video player able to play anything that ffmpeg/mencoder/other
tools can play\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

-   [Axon bugfix](/Developers/Projects/AxonWakingProducersBugfix) to
    re-introduce the waking of components if they have an outbox linked
    to an inbox from which an item has just been consumed.
-   Conversion of YUV to RGB pixel data (VideoSurface component)\

### Sub Tasks

Modifying/rewriting UnixProcess to:

not throw away data

support named pipes for input and output\

to allow rate limiting by boxes becoming full

-   leave data in inbox(es) until the process can accept it
-   not accept data until the destination outbox is not full

Writing components

Deployment onto demonstration server\

\

Task Log
--------

-   12 October 2006 - Added developer Matt\
-   20 October 2006 - Matt : development to date: Time spent 5 days.
    **Task status changed** to blocked - need to complete [Axon
    bugfix](/Developers/Projects/AxonWakingProducersBugfix) (development
    begins in branch private\_MH\_axon\_outboxwakeups)\
-   26 October 2006 - Matt : **Task status changed** to running -
    resumed development
-   10 November 2006 - Matt : Time spent 11 days. **Task status
    changed** to stasis - secondment for BBC internal project
-   20 November 2006 - Matt : **Task status changed** to running -
    resumed development\
-   27 November 2006 - Matt : development complete. Most code documented
    Time spent 4 days. **Task status changed** to blocked - awaiting
    demonstration server to install onto
-   29 November 2006 - Matt : Minor bugs come to attention and are
    fixed. Adding to documentation. Time spend 1/2 day
-   15 December 2006 - Matt : Added [webpage describing how to use
    it](/MobileReframer%20) . Time spent 1/4 day.\

Discussion
----------

Coping with size limited boxes:\

-   Creation of components that cope sensibly with noSpaceInBox
    exceptions and still can shutdown as soon as appropriate, without
    deadlocking/livelocking, has proved much harder than anticipated.
-   Similarly, parsing stream data from inboxes, whilst only taking from
    the inbox when actually needed was non trivial to code too.
-   In particular developing and debugging the revised UnixProcess
    component took much longer than expected.\
-   The least unpleasant approach developed can be seen in components
    such as *YUV4MPEGToFrame* and *MaxSpeedFileReader*.
-   Either further approaches need trying out, or perhaps the existing
    approaches might be worth wrapping into a mixin. Either way, further
    review and discussion is required.\

\
