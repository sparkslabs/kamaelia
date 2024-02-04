---
pagename: Developers/Projects/UnbufferedCSASupport
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Unbuffered CSA Support (bugfix?) 
---------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** MPS, MH\
**Current \"inflight\" dev location:**
*/branches/private\_MPS\_UnbufferedCSASupport*\
**Start Date:** *Aug 2007*\
**Expected End Date:** Aug 2007\
**End Date:** *11 Aug 2007*\
**Date this page last updated:** 5 Aug 2007\
**Estimated effort so far:** 0.75\
:::

**\
**

**Description**
---------------

This change removes the internal buffering sendQueue in
ConnectedSocketAdaptor.\
\
This enables a producer sending data into the CSA to mark its linkage
synchronous. This allows the producer to create and send data as fast as
the socket can handle the data being sent.\
\
This is a legacy bugfix, and can be considered an optimisation.\

Inputs
------

Task Sponsor: MS

Task Owner: MS

Developers involved in the task at some point\

-   MS
-   MH\

Users:

-   MS, RJL (RJL did something similar as part of SOC but was mixed in
    with a bunch of other changes in a sub optimal way)\

Interested third parties

-   MS, RJL\

Requirements

-   Remove the internal buffering in the CSA.\

Outputs
-------

### Expected

-   An improved CSA that has no internal buffering\

### Actual

-   /Code/Python/Kamaelia/Kamaelia/Internet/ConnectedSocketAdaptor.py
    has been patched to remove buffering\
-   This is in branch private\_MPS\_UnbufferedCSASupport\

### Realistic possibilities arising as a result of activity on this task

See the general description above.\

Related Tasks
-------------

None.\

Task Log
--------

-   **Output:** 5 Aug 2007 : MPS: Branch changes completed. Time spent
    1/2 day\
-   5 Aug 2007 : List mailed asking for merger.\
-   5 Aug 2007 : Created the PTP page for the project, and brainstormed
    how to get started. Michael. November 27th 2006. Time spent 1/4 day
-   11 Aug 2007 : Added developer MH
-   11 Aug 2007 : MH : Branch merged into trunk
-   11 Aug 2007 : **Task status changed** to completed\

Discussion
----------

\....\
