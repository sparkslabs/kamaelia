---
pagename: Developers/Projects/DeprecationFixes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Fixing references to deprecated components in Examples and Tools 
-----------------------------------------------------------------------------------

::: {.boxright}
**Status:** Running\
**Current Developers:** *MH*\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070424\_deprecationsfixes\
**Start Date:** *24 April 2007*\
**Expected End Date:** 30 April 2007\
**End Date:** 27 April 2007\
**Date this page last updated:** *30 April 2007*\
**Estimated effort so far:** 1.5\
:::

**\
**

**Description**
---------------

Several of the example programmes in Code/Python/Kamaelia/Examples and
Code/Python/Kamaelia/Tools import components that are now deprecated
(eg. Kamaelia.Util.Pipeline). This generates deprecation warnings but
does not stop the programs from running.

Easily fixed by modifying to point to the new names/locations of the
components.\

Inputs
------

Task Sponsor: MH

Task Owner: MH\

Developers: MH,MS

Users: none

Interested third parties: none\

Requirements

-   MUST fix so deprecation warnings no longer occur\
-   SHOULD not result in any foreseeable regressions\

Outputs
-------

### Expected

Modifications to:

-   various bits of code in /Code/Python/Kamaelia/Examples and
    /Code/Python/Kamaelia/Tools

### Actual

Branch /branches/private\_MH\_20070424\_deprecationfixes/

\...containing modifications to:

-   /Code/Python/Kamaelia/Tools/Show.py
-   /Code/Python/Kamaelia/Tools/Whiteboard/Whiteboard.py
-   /Code/Python/Kamaelia/Examples/SoC2006/RJL/TorrentSeeder/torrentseeder.py
-   /Code/Python/Kamaelia/Examples/SoC2006/RJL/HTTPSpider/HTTPSpider.py
-   /Code/Python/Kamaelia/Examples/SoC2006/RJL/P2PStreamPeer/p2pstreampeer.py
-   /Code/Python/Kamaelia/Examples/SoC2006/RJL/P2PStreamSeed/p2pstreamseed.py

\...merged into /trunk\

### Realistic possibilities arising as a result of activity on this task

none\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

-   /branches/private\_MH\_20070423\_kamaelia\_bugfixes branch *should*
    be merged first, as this branch is based on it - it will make
    merging simpler if done this way.\

### Sub Tasks

-   Branch containing modifications
-   Merge of branch

Task Log
--------

-   2007 04 24 : **Task status changed** to running
-   2007 04 24 : Added developer MH
-   2007 04 24 : Created branch
    /branches/private\_MH\_20070424\_deprecationfixes/
-   2007 04 24 : Found deprecation uses; fixed; tested\
-   2007 04 25 : Ready for merging into /trunk\
-   2007 04 25 : Time spent 1 day
-   2007 04 27 : Removed developer MH
-   2007 04 27 : Added developer MS
-   2007 04 27 : Merged branch
-   2007 04 27 : **Task status changed** to completed
-   2007 04 27 : Time spend 0.5 days\

Discussion
----------

Important note: this branch was (retrospectively, stupidly) based on the
/branches/private\_MH\_20070423\_kamaelia\_bugfixes branch - it
therefore includes all changes made in that branch up to the moment at
which is was branched from it. When merging, it is therefore recommended
to merge that branch before this one (in order to simplify the process)\

\-- Matt, 25 April 2007\

\
