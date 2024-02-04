---
pagename: Developers/Projects/MobileReframerAndRTPNewComponents
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Mobile Reframer and RTP New Components 
---------------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MPS*\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070429\_newcomponents\
**Start Date:** 29 April 2007\
**End Date:** *5 Aug 2007*\
**Date this page last updated:** *5 Aug 2007*\
**Estimated effort so far:** 14\
:::

**\
**

**Description**
---------------

Merging of *new* components developed for RTP and Mobile Reframer work
(in /trunk/Sketches/MH ) into the main Kamaelia codebase thereby
increasing Kamaelia\'s capabilities and facilitating the incorporation
of the Mobile Reframe and RTP work as official examples or tools.

Note that this *does not* include components that were developed as
modifications or rewrites of existing components that are not essential
to the operation of the mobile reframer - such as the Multicast and
Selector modifications. It does include the \'new\' UnixProcess
component and modifications to the Carousel.\

Inputs
------

Task Sponsor: MH,MPS

Task Owner: MPS

Developers: MH,MPS

Users: n/a\

Interested third parties: MPS

Requirements

-   MUST add new components to main codebase in trunk\
-   SHOULD not cause regressions\

Outputs
-------

### Expected

New sourcefiles in\

-   /Code/Python/Kamaelia/Kamaelia
-   /Code/Python/Kamaelia/Tools\

### Actual

Branch /branches/private\_MH\_20070429\_newcomponents/

\...containing new components:

-   /Code/Python/Kamaelia/Kamaelia/File/MaxSpeedFileReader.py
-   /Code/Python/Kamaelia/Kamaelia/File/UnixProcess2.py
-   /Code/Python/Kamaelia/Kamaelia/Experimental/Chassis.py
-   /Code/Python/Kamaelia/Kamaelia/Chassis/Seq.py
-   /Code/Python/Kamaelia/Kamaelia/Chassis/Carousel.py
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/SoftDemux.py
-   /Code/Python/Kamaelia/Kamaelia/XML/\_\_init\_\_.py
-   /Code/Python/Kamaelia/Kamaelia/XML/SimpleXMLParser.py
-   /Code/Python/Kamaelia/Kamaelia/Protocol/RTP/\_\_init\_\_.py
-   /Code/Python/Kamaelia/Kamaelia/Protocol/RTP/RTP.py
-   /Code/Python/Kamaelia/Kamaelia/Protocol/RecoverOrder.py
-   /Code/Python/Kamaelia/Kamaelia/Protocol/SDP.py
-   /Code/Python/Kamaelia/Kamaelia/Video/CropAndScale.py
-   /Code/Python/Kamaelia/Kamaelia/Video/DetectShotChanges.py
-   /Code/Python/Kamaelia/Kamaelia/Video/PixFormatConversion.py
-   /Code/Python/Kamaelia/Kamaelia/Video/\_\_init\_\_.py
-   /Code/Python/Kamaelia/Kamaelia/Codec/WAV.py
-   /Code/Python/Kamaelia/Kamaelia/Codec/YUV4MPEG.py
-   /Code/Python/Kamaelia/Kamaelia/UI/Pygame/VideoSurface.py
-   /Code/Python/Kamaelia/Kamaelia/Util/PromptedTurnstile.py
-   /Code/Python/Kamaelia/Kamaelia/Util/RateChunker.py
-   /Code/Python/Kamaelia/Kamaelia/Util/OneShot.py
-   /Code/Python/Kamaelia/Kamaelia/Util/TwoWaySplitter.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Max.py
-   /Code/Python/Kamaelia/Kamaelia/Util/FirstOnly.py
-   /Code/Python/Kamaelia/Kamaelia/Util/RangeFilter.py
-   /Code/Python/Kamaelia/Kamaelia/Util/TagWithSequenceNumber.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Sync.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Collate.py
-   .

Removed (moved elsewhere)\

-   /Code/Python/Bindings/MpegTsDemux/\* *(moved into \"SupportCode\")*\
-   .\

New bindings/pyrex based optimised library

-   /Code/Python/Bindings/SupportCode/Kamaelia/Support/Optimised/Video/\_PixFormatConvertCore.c
-   /Code/Python/Bindings/SupportCode/Kamaelia/Support/Optimised/Video/\_\_init\_\_.py
-   /Code/Python/Bindings/SupportCode/Kamaelia/Support/Optimised/Video/Kamaelia.Support.Optimised.Video.PixFormatConvert.pyx
-   /Code/Python/Bindings/SupportCode/Kamaelia/Support/Optimised/Video/Kamaelia.Support.Optimised.Video.ComputeMeanAbsDiff.pyx
-   /Code/Python/Bindings/SupportCode/Kamaelia/Support/Optimised/\_\_init\_\_.py
-   /Code/Python/Bindings/SupportCode/Kamaelia/Support/Optimised/Kamaelia.Support.Optimised.MpegTsDemux.pyx
-   .\

New tests

-   /Tests/Python/Kamaelia/Chassis/test\_Carousel.py
-   .

New tool: Video player:\

-   /Code/Python/Kamaelia/Tools/VideoPlayer.py
-   .\

New tool: Video Reframer:\

-   /Code/Python/Kamaelia/Tools/VideoReframer/VideoReframer.py
-   /Code/Python/Kamaelia/Tools/VideoReframer/MobileReframe.xsd
-   /Code/Python/Kamaelia/Tools/VideoReframer/EDL.py
-   /Code/Python/Kamaelia/Tools/VideoReframer/StopSelector.py
-   .\

New tool: Video shot change detector:\

-   /Code/Python/Kamaelia/Tools/VideoShotChangeDetector/DetectShotChanges.xsd
-   /Code/Python/Kamaelia/Tools/VideoShotChangeDetector/ShotChangeDetector.py
-   /Code/Python/Kamaelia/Tools/VideoShotChangeDetector/StopSelector.py
-   .

New examples: RTP:

-   /Code/Python/Kamaelia/Examples/UDP\_Systems/RTP\_G711\_microphone\_sender.py
-   /Code/Python/Kamaelia/Examples/UDP\_Systems/RTP\_G711\_receiver.py
-   .\

Modified

-   /Code/Python/Kamaelia/CHANGELOG
-   /Code/Python/Kamaelia/Kamaelia/Device/DVB/SoftDemux.py *(adjusted
    imports to match moved support pyrex lib)*\
-   /Code/Python/Kamaelia/Kamaelia/Chassis/Carousel.py *(Carousel
    rewrite to fix shutdown behaviour bugs)*
-   /Code/Python/Bindings/SupportCode/setup.py
-   .\

### Realistic possibilities arising as a result of activity on this task

-   Merging of mobile reframer itself\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

-   [Development of Mobile
    Reframer](/Developers/Projects/MobileReframer)
-   [Development of RTP
    Remuxing](/Developers/Projects/MulticastRtpMpegRemultiplexer)

### Sub Tasks

-   Branch containing modifications
-   Merge of branch

Task Log
--------

-   2007 04 29 : **Task status changed** to running\
-   2007 04 29 : Added developer MH
-   2007 05 17 : Branch ready for merge. Time spent: 13 days
-   2007 05 22 : MH : Some last minute additions (merge not commenced
    yet)
-   2007 08 01 : MPS Eventually merged (sorry for delay)\

Discussion
----------

I originally opted to separate the merging of these completely new
components from the merging of ones that modify/rewrite existing
components. These components independently add new functionality that
should not have any knockon impact on existing Kamaelia components and
systems. Modifications/rewrites may do.\
\
I eventually decided it made sense to bundle everything to get mobile
reframer (renamed Video Reframer) working, including the reframer itself
into one branch. In practice most components are new. There is only one
rewrite - the Carousel - which I\'ve tested and added a long overdue
test suite for that illustrates how it improves on the existing Carousel
design. Finally, I\'ve added the reframer itself and supplementary video
player tool.\
\
It made sense to **rename the Mobile Reframer to Video Reframer** since
the first name implies an unnecessary limitation on the range of
applications it could be used for. In reality it could be used to
process any re-editing and reframing of video for any purpose.\
\
This is taking longer than originally anticipated becuase various small
bugs and fixes have been identified along the way - both due to the
reframer and also asides from helping Google SoC students. In addition
it took longer to rationalise these components; tidy up and fix
documentation; and figure out how to neatly fit them into the main
codebase.\
\
The **SupportCode** pyrex based library was introduced (and the
**SoftDemux** one deprecated) because several of the components
introduced for the video reframer, video player and cut detector require
various optimised alogirthms (image difference comparisons, YUV-\>RGB
conversion, etc). It feels sensible to bundle these together as generic
support code as they have no dependencies on external libraries. I also
chose to get them to appear under the Kamaelia.Support.Optimised
namespace - as opposed to allowing them to litter the top level.
SoftDemux naturally fitted into the category and so was rolled in too.
Perhaps this should have been done as a separate branch. If so, it is
relatively easy to separate out from this set of changes.\

\-- Matt, 16 May 2007\
