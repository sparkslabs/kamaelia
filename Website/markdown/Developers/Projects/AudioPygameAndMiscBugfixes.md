---
pagename: Developers/Projects/AudioPygameAndMiscBugfixes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: PyMedia Audio, Pygame and misc bugfixes 
----------------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*, MS\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070423\_kamaelia\_bugfixes\
**Start Date:** *23 April 2007*\
**Expected End Date:** 30 April 2007\
**End Date:** 27 April 2007\
**Date this page last updated:** *30 April 2007*\
**Estimated effort so far:** 2.0\
:::

**\
**

**Description**
---------------

**Bugfixes** to fix following:

-   Kamaelia.Audio.PyMedia.Input - not working under win32 (noSpaceInBox
    exceptions) ([see mailing
    list](http://sourceforge.net/mailarchive/forum.php?thread_name=96d4cf580704181815u6b99f9acyef8d65e98b72633f%40mail.gmail.com&forum_name=kamaelia-list))\
-   Kamaelia.UI.Pygame.Display - not working under win32 and MacOSX
    (freezes/unresponsive to keyboard/mouse interaction) ([see IRC
    logs](http://koala.ilog.fr/twikiirc/bin/irclogger_log/kamaelia?date=2007-04-23,Mon&sel=15#l11))\
-   Kamaelia.Util.Chooser - not quiescent
-   Kamaelia example \"Show.py\" raises exception on startup: ([see IRC
    logs](http://koala.ilog.fr/twikiirc/bin/irclogger_log/kamaelia?date=2007-04-23,Mon&sel=226#l222))

Inputs
------

Task Sponsor: MH

Task Owner: MH\

Developers: MH, MS\

Users: MH, \_eris (IRC), David Montgomery\

Interested third parties: MS

Requirements

-   MUST fix the bugs so the problem doesn\'t occur
-   SHOULD not result in any foreseeable regressions\

Outputs
-------

### Expected

Modifications to:

-   /Code/Python/Kamaelia/Kamaelia/UI/Pygame/Display.py
-   /Code/Python/Kamaelia/Kamaelia/Audio/PyMedia/Input.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Chooser.py
-   /Code/Python/Kamaelia/Kamaelia/Tools/Show.py

### Actual

Branch /branches/private\_MH\_20070423\_kamaelia\_bugfixes/

\...containing modifications to:

-   /Code/Python/Kamaelia/Kamaelia/Audio/Input/PyMedia/Input.py
-   /Code/Python/Kamaelia/Kamaelia/UI/Pygame/Display.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Chooser.py\
-   /Code/Python/Kamaelia/Tools/Show/GraphSlides.py
-   /Code/Python/Kamaelia/Kamaelia/Support/Data/Experimental.py

\... which were merged into /trunk\

### Realistic possibilities arising as a result of activity on this task

none\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

none\

### Sub Tasks

-   Branch containing modifications
-   Merge of branch

Task Log
--------

-   2007 04 22 : **Task status changed** to running
-   2007 04 22 : Added developer MH
-   2007 04 22 : Fixed PyMedia Input code in private Sketches area.
    Tested by MH under win32.\
-   2007 04 23 : Created branch
    /branches/private\_MH\_20070423\_kamaelia\_bugfixes/
-   2007 04 23 : Fixed PyGame Display bug. Verified working on win32 by
    MH and MacOSX by eris\_
-   2007 04 23 : Imported fixed PyMedia Input code from Sketches
-   2007 04 23 : Fixed quiescence in Chooser - tested by MH in Show.py
    tool\
-   2007 04 25 : Time spent 1.5 days
-   2007 04 22 : **Task status changed** to stasis - waiting for test
    feedback from David Montgomery
-   2007 04 27 : Removed developer MH
-   2007 04 27 : Added developer MS
-   2007 04 27 : **Task status changed** to running - decided to proceed
    anyway (MH has already tested on win32)
-   2007 04 27 : Branch merged
-   2007 04 27 : **Task status changed** to completed
-   2007 04 27 : Time spend 0.5 days\

Discussion
----------

Note this branch was renamed (logged by svn as a copy operation). **The
original branch point is revision r2887**. The renaming occurred at
revision r2899.\
\

PyMedia Input bug was two-fold:

-   Not handling when pymedia returns \"None\" instead of string like
    (not actually string) data; or empty strings
-   Not handling noSpaceInBox exceptions - more likely if pumping out
    small fragments of data, and never really pausing/waiting\

PyGame Display bug:

-   win32 and MacOSX limitations in pygame/SDL require the display to be
    initialised, and event handling to be done in the application\'s
    main thread - not a child thread. Fixed by moving everything into
    the main thread, but still keeping the child thread as a passive
    observer that makes sure the main component gets woken up if events
    are waiting.

show.py bug:\

-   misunderstood use of the xml.sax.make\_parser call - should have
    provided a list of strings as an argument rather than a string.
    Seems to work on Linux on test machines used by MS and MH, but
    problem shows up on win32 and MacOSX.\

\-- Matt, 25 April 2007\
\
