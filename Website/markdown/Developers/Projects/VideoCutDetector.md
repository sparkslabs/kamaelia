---
pagename: Developers/Projects/VideoCutDetector
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Video Cut Detector
==================

::: {.boxright}
**Status:** Completed\
**Current Developers:** *Matt*\
**Current \"inflight\" dev location:** */Sketches/MH/Video/CutDetector*\
**Start Date:** *01 December 2006*\
**Major Milestone date:** (met/slipped/missed) *(optional)*\
**Expected End Date:** *n/a*\
**End Date:** *10 December 2006*\
**Date this page last updated:** *10 December 2006*\
**Estimated effort so far:** 3.25\
:::

**\
**

**Description**
---------------

A tool to analyse a video file and output a list of (probable) locations
of cuts/shot-changes in the video.\
\
This will serve as useful input data to user controlled video
manipulation applications, such as the intended front end for the mobile
reframer.\
\
This work was requested as a follow on from the Mobile Reframer - to
support the front end interface being developed (a BBC internal
project).\
\
This adds a simple shot change detection capability.

Inputs
------

\
Task Sponsor: SJ (BBC internal)\
Task Owner: Matt\
Developers: Matt\
Users: SJ\
Interested third parties: None\
Requirements:\

-   MUST Analyse video files of a range of formats for shot changes/cuts
-   Use ffmpeg/mencoder to decode the video
-   MUST Output a list of frame numbers of likely shot changes
-   MUST Output as XML conforming to a schema
-   MAY output additional information, such as a confiden value for each
    shot change detection

Relevant Influencing factors:\

-   *JE (BBC internal) has open sourced a simple shot change algorithm
    [now on
    sourceforge](http://sourceforge.net/projects/shot-change%20)\
    *

Outputs
-------

Expected

Video shot change detector command line application\

XML Schema defining the output format

New components:

-   shot change detector, reimplementing JE\'s algorithm\

### Actual

Code

-   /Sketches/MH/Video/CutDetector/ComputeMAD.c
-   /Sketches/MH/Video/CutDetector/Makefile
-   /Sketches/MH/Video/CutDetector/DetectedCuts.xsd\
-   /Sketches/MH/Video/CutDetector/CutDetector.py\

XML Schema:

-   /Sketches/MH/Video/CutDetector/ComputeMeanAbsDiff.pyx

Webpages:

-   [explanation of how to use it](/VideoCutDetector)\

### Realistic possibilities arising as a result of activity on this task

\-\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   [Mobile Reframer](/Developers/Projects/MobileReframer) (YUV4MPEG
    components)\

### Sub Tasks

-   Seek permission to reimplement algorithm from JE\'s project
-   Develop shot change detection component
-   Write schema
-   Develop application\

Task Log
--------

-   01 December 2006 - Matt : Added developer Matt. Permission obtained
    to re-implement algorithm and to relicence as part of Kamaelia
    distribution
-   02 December 2006 - Matt : **Task status changed** to Running.
-   10 December 2006 - Matt : Code complete. **Task status changed** to
    Completed.
-   14 December 2006 - Matt : Added [webpage describing how to use
    it](/VideoCutDetector) . Time spent: 1/4 day\

Discussion
----------

Developed during weekends.\
