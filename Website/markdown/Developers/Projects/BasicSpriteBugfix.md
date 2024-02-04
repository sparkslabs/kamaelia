---
pagename: Developers/Projects/BasicSpriteBugfix
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Bugfix to BasicSprite component 
--------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*, MS\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070425\_spritebugfix\
**Start Date:** *25 April 2007*\
**Expected End Date:** 30 April 2007\
**End Date:** *26 April 2007*\
**Date this page last updated:** *26 April 2007*\
**Estimated effort so far:** 0.75\
:::

**\
**

**Description**
---------------

**Bugfix** to BasicSprite class - clashed with
Axon.Microprocess.microprocess since both defined pause() and unpause()
methods.

**Effect of bug:**\

-   when running
    Code/Python/Kamaelia/Examples/SimpleGraphicalApps/BouncingCatGame/SimpleGame.py
-   program is non responsive, and the shapes don\'t bounce around.
    clicking doesn\'t cause shapes to appear or disappear.\

Inputs
------

Task Sponsor: MH

Task Owner: MH\

Developers: MH, MS\

Users: none

Interested third parties: MS

Requirements

-   MUST fix the bug so the problem doesn\'t occur
-   SHOULD not result in any foreseeable regressions\

Outputs
-------

### Expected

Modifications to:

-   /Code/Python/Kamaelia/Kamaelia/UI/Pygame/BasicSprite.py\

### Actual

Branch /branches/private\_MH\_20070425\_spritebugfix/

\...containing modifications to:

-   /Code/Python/Kamaelia/Kamaelia/UI/Pygame/BasicSprite.py
-   /Code/Python/Kamaelia/Examples/SimpleGraphicalApps/BouncingCatGame/Sprites/BasicSprite.py
-   /Code/Python/Kamaelia/Examples/SimpleGraphicalApps/BouncingCatGame/SimpleGame.py

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

-   2007 04 25 : **Task status changed** to running
-   2007 04 25 : Added developer MH
-   2007 04 25 : Created branch
    /branches/private\_MH\_20070425\_spritebugfix/
-   2007 04 25 : Fixed the bug and tested fixes work
-   2007 04 25 : Ready for merging into /trunk\
-   2007 04 25 : Time spent 0.5 days
-   2007 04 25 : Removed developer MH
-   2007 04 26 : Added developer MS
-   2007 04 26 : Merged with /trunk
-   2007 04 26 : Time spend 0.25 days
-   2007 04 26 : **Task status changed** to completed\

Discussion
----------

Turned out that the BasicSprite.py code existed both in the codebase,
and in a subdir in the examples directory. Both were modified to fix the
bug.

For consistency, the messages passed/understood were changed from
\"pause\" terminology to match the new \"freeze\" terminology too - so
SimpleGame.py needed modification too.\

\-- Matt, 25 April 2007\

\
