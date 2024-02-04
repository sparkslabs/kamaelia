---
pagename: Developers/Projects/AxonOneToManyDetection
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Making Axon Detect One-to-many linkage creation 
------------------------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*, MPS\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070509\_axonwarnings\
**Start Date:** 09 May 2007\
**End Date:** *5 Aug 2007*\
**Date this page last updated:** *5 Aug 2007*\
**Estimated effort so far:** 0.5 days\
:::

**\
**

**Description**
---------------

Axon cannot handle one-to-many linkages - where a postbox is wired to
more than one destination. However, when creating linkages, Axon
currently makes no attempt to detect this and flag the error.\
\
Getting Axon to alert the developer/user that this has happened will aid
debugging and development.\
\

Inputs
------

This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\

Task Sponsor: MH\

Task Owner: MH, MPS\

Developers involved: MH (development), MPS (merge)\

Users: MH, MPS\

Interested third parties: MH, MS, Patrick (SoC 2007)\

Requirements

-   MUST flag to the developer or user when the problem occurs\
-   SHOULD not cause any regressions\
-   MUST have some test suite coverage\

Outputs
-------

### Expected

-   Modifications to Axon (initially in branch then merged into mainline
    code)
-   \...including modifications and additions to the Axon test suite\

### Actual

Code:

SVN branch: private\_MH\_20070509\_axonwarnings

Mainline code: /Code/Python/Axon/Axon/

-   Modified: Box.py, PostOffice.py, AxonExceptions.py

Mainline code: /Tests/Python/Axon/

-   Modified: test\_Postoffice.py\

### Realistic possibilities arising as a result of activity on this task

none\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies)

-   none\

### Sub Tasks

-   Development
-   Testing
-   Test suite additions\

Task Log
--------

-   09 May 2007 : Added developer Matt
-   09 May 2007 : **Task status changed** to running.
-   09 May 2007 : Matt : working on private\_MH\_20070509\_axonwarnings
    branch
-   10 May 2007 : Matt : bulk of development and tests complete. Days
    spent: 0.75
-   10 May 2007 : Matt : branch ready for merge
-   1 AUG 2007 : MPS : merged (sorry for the delay)\

Discussion
----------

To my mind this could be deemed a bugfix. It is certainly not really a
tangible API or feature-set change.\
\
I\'ve added an appropriately named exception that is thrown if the
problem occurs.\
\
\-- Matt Hammond, 09 May 2007\

\
