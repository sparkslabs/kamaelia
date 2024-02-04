---
pagename: Developers/Projects/AxonThreadedComponentTerminationBugfix
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Axon ThreadedComponent termination bugfix 
------------------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*, MPS\
**Current \"inflight\" dev location:**
/branches/private\_MH\_20070522\_threadedcomponent\_bugfixes\
**Start Date:** 22 May 2007\
**End Date:** *5 Aug 2007*\
**Date this page last updated:** *5 Aug 2007*\
**Estimated effort so far:** 1 day\
:::

**\
**

**Description**
---------------

\
Casual inspection of Axon.ThreadedComponent identified a
bug:threadedcomponent may never properly terminate if, when the thread
(main() method) terminates, one of the inqueues in full and there are
still messages waiting at the corresponding inbox.\
\
This branch adds test suite coverage of this issues and fixes the bug.\

Inputs
------

This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\

Task Sponsor: MH\

Task Owner: MH\

Developers involved: MH (development)\

Users: MH, Patrick\`\

Interested third parties: MH, Patrick\`\

Requirements

-   MUST fix the bug!\
-   SHOULD not cause any regressions\
-   MUST have some test suite coverage to catch the bug if it arises
    again in future\

Outputs
-------

### Expected

-   Modifications to Axon (initially in branch then merged into mainline
    code)
-   \...including modifications and additions to the Axon test suite\

### Actual

Code:

SVN branch: private\_MH\_20070522\_threadedcomponent\_bugfixes

Mainline code: /Code/Python/Axon/Axon/

-   Modified: ThreadedComponent.py

Mainline code: /Tests/Python/Axon/

-   Modified: test\_ThreadedComponent.py\

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

-   22 May 2007 : Added developer Matt
-   22 May 2007 : **Task status changed** to running.
-   22 May 2007 : Matt : working on
    private\_MH\_20070522\_threadedcomponent\_bugfixes branch
-   23 May 2007 : Matt : bulk of development and tests complete. Days
    spent: 1.0\
-   23 May 2007 : Matt : branch ready for merge
-   1 Aug 2007: MPS : merged\

Discussion
----------

To my mind this could be deemed a bugfix. It is certainly not really a
tangible API or feature-set change.\
\
I\'ve added to the docstrings to provide clarification around shutdown
behaviour to people writing threaded components. Its basically
documenting the situation as-is, rather than being a change in behaviour
(aside from the bugfix aspect!)\
\
\-- Matt Hammond, 23 May 2007\

\
