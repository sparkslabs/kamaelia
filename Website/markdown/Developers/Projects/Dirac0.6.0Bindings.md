---
pagename: Developers/Projects/Dirac0.6.0Bindings
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Dirac 0.6.0 Bindings 
---------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*, MS\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070425\_dirac0.6.0bindings\
**Start Date:** 11 October 2006\
**Expected End Date:** 30 April 2007\
**End Date:** 27 April 2007\
**Date this page last updated:** *25 April 2007*\
**Estimated effort so far:** 5\
:::

**\
**

**Description**
---------------

Dirac python bindings are for dirac version 0.5.4. Dirac has moved onto
0.6.0 and there have been API changes which make the bindings
incompatible ([see IRC
logs](http://koala.ilog.fr/twikiirc/bin/irclogger_log/kamaelia?date=2006-10-11,Wed&sel=31#l27))

Update the bindings for compatibility with 0.6.0. If possible find a way
to maintain compatibility with 0.5.4.\

Inputs
------

Task Sponsor: MH

Task Owner: MH\

Developers: MH, MS\

Users: lawouach (IRC handle)\

Interested third parties: MS, lawouach (IRC handle)

Requirements

-   MUST provide compability with Dirac 0.6.0 release\
-   WOULD LIKE to maintain the option of still working with Dirac 0.5.4\

Outputs
-------

### Expected

New/updated bindings in\

-   /Code/Python/Bindings/Dirac\

### Actual

Branch /branches/private\_MH\_20070425\_dirac0.6.0bindings/

\...containing modifications to:

-   /Code/Python/Bindings/Dirac ( renamed to
    /Code/Python/Bindings/Dirac-0.5.4 )\
-   /Code/Python/Bindings/Dirac-0.6.0 (added)
-   /Code/Python/Kamaelia/Kamaelia/Codecs/Dirac.py
-   /Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/SimpleDiracPlayer.py
-   /Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.dirac.drc
    ( renamed to Dirac/snowboard-jump-352x288x75.0.5.4.drc )
-   /Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.0.6.0.drc

Modifications merged into /trunk\

### Realistic possibilities arising as a result of activity on this task

-   /trunk/Sketches/MH/dirac still contains yet another set of bidings
    reflecting even more recent changes currently in dirac cvs (but not
    yet in a release) \... when this release is made, a new set of
    bindings should be issued.\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

none\

### Sub Tasks

-   Development and testing of new bindings
-   Branch containing modifications
-   Merge of branch

Task Log
--------

-   2006 10 11 : **Task status changed** to running\
-   2007 10 11 : Added developer MH
-   2007 10 17 : Tested and checked new bindings into
    /Sketches/MH/dirac/
-   2007 04 25 : Time spent 4 days
-   2007 10 18 : **Task status changed** to stasis\
-   2007 04 25 : **Task status changed** to running\
-   2007 04 25 : Created branch
    /branches/private\_MH\_20070425\_dirac0.6.0bindings/
-   2007 04 25 : Ready for merging into /trunk\
-   2007 04 25 : Time spent 0.5 days
-   2007 04 27 : Removed developer MH
-   2007 04 27 : Added developer MS
-   2007 04 27 : Merge complete
-   2007 04 27 : Time spend 0.5 days
-   2007 04 27 : **Task status changed** to completed\

Discussion
----------

Discovered it was possible to simply keep two sets of bindings - for
0.5.4 and 0.6.0. Pyrex does not yet support conditional compilation, so
two sets of bindings is an alternative simple solution.\
\
Added a version number attribute to 0.6.0 which the component now tests
for so it knows how to behave differently depending on which bindings it
has available.\

Note that there was a change in bitsam syntax between 0.6.0 and 0.5.4 so
files compressed with one cannot be played back by the other.

Modified examples so there are two example compressed files - one for
0.5.4 and one for 0.6.0. \'simple playback\' example program modified to
take a command line argument to specify which.\

\-- Matt, 25 April 2007\
