---
pagename: Developers/Projects/AxonQuiescenceOptimisation
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.bodytext}
Project Task Page: Axon Quiescence Optimisation 
-----------------------------------------------
:::

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*\
**Current \"inflight\" dev location:**
*/branches/*private\_MH\_axon\_flowcontrolinversion\
**Start Date:** *May 2006*\
**Expected End Date:** n/a\
**End Date:** *May 2006*\
**Date this page last updated:** *22 February 2007*\
**Estimated effort so far:** *20 days*\
:::

\
\

**Description**
---------------

Modifying axon so that components are not scheduled (ie. run) when they
are paused. If all components are paused, then the whole Axon system
sleeps until woken - it goes quiescent. As it stands, Axon does not do
this - the scheduler keeps all microprocesses in a single list and polls
all of them continually.\
\
This is also an \"inversion of flow control\" - since it enables an Axon
based system to become reactive to events, rather than polling.\
\
Benefits:\

-   General performance and responsiveness improvement - processor
    cycles will not be wasted on idle microprocesses
-   Better cooperation with other processes on a computer - Axon based
    systems will no longer hog processor cycles, even when inactive

Needed to make practical high data throughput Kamaelia systems, such as
[KamaeliaMacro](../../../Developers/Projects/KamaeliaMacro).\

Inputs
------

Task Sponsor: Michael (MS)\

Task Owner: Michael, Matt (MH)\

Developers: Matt (initial sketches and final code dev), Michael (final
merge)\

Users: Michael, Matt\

Interested third parties: none\

Requirements

-   MUST cause an Axon system to relinquish the cpu when idle
-   MUST not change the behaviour of an Axon system from the perspective
    of individual components
-   MUST be threadsafe
-   SHOULD only schedule and run microprocesses that are actually active
    at a given time (scheduler should properly pause() microprocesses
    and also unpause() them)
-   SHOULD not noticeably impact performance
-   SHOULD be responsive to external stimuli when quiescent (eg.
    Selector component gets woken when data is available)\

Relevant Influencing factors:\

-   *Needed for Kamaelia Macro*

\

Outputs
-------

### Expected

-   Modifications to Axon (initially in branch, then merged into
    mainline code)
-   Modifications and additions to Axon test suite
-   Improved performance\

### Actual

Code:

Experiments (in order):

-   /Sketches/MH/Inversion/miniaxon.py
-   /Sketches/MH/Inversion/cleverscheduling.py
-   /Sketches/MH/Inversion/aggregatedevents.py

CVS branch: private\_MH\_axon\_flowcontrolinversion

Mainline code: /Code/Python/Axon/Axon/

-   Modified: most/all source files\

Mainline code: /Code/Python/Axon/Axon/Tests

-   Tests removed that were now inapplicable
-   New tests added

Bugfixes for components in mainline: (turned out several components did
not use self.pause() properly)\

-   /Code/Python/Kamaelia/Kamaelia/Internet/Selector.py - made threaded
    and pausing
-   /Code/Python/Kamaelia/Kamaelia/Internet/TCPServer.py
-   /Code/Python/Kamaelia/Kamaelia/Chassis/ConnectedServer.py
-   /Code/Python/Kamaelia/Examples/example2/SimpleStreamingSystem.py
-   /Sketches/MPS/Macro/UnixPipe.py
-   /Code/Python/Kamaelia/Kamaelia/File/\*
-   /Code/Python/Kamaelia/Kamaelia/Util/passThrough.py
-   /Code/Python/Kamaelia/Kamaelia/Visualisation/PhysicsGraph/lines\_to\_tokenlists.py
-   /Code/Python/Kamaelia/Kamaelia/UI/\*
-   /Code/Python/Kamaelia/Examples/example11/Ticker.py
-   /Sketches/MH/Sketcher/\*
-   /Sketches/MPS/Paint/Paint.py
-   /Sketches/MH/Editor2/Sandbox.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Introspector.py
-   \

### Realistic possibilities arising as a result of activity on this task

Axon\'s support for the following was removed; and needed to be added
back in again:\

-   limited \"pipewidths\" - linkages that could only carry a limited
    number of items data before becoming \'full\' - (a rate limiting
    mechanism)\
-   waking a component when a message leaves on of its outboxes (free
    space to send to)

Task Log
--------

-   4 May 2006 : Added developer Matt
-   4 May 2006 : **Task status changed** to running.
-   4 May 2006 : Matt : worked on inital sketches/experiments\
-   4 May 2006 : Matt : work commenced on
    private\_MH\_axon\_flowcontrolinversion branch
-   7 May 2006 : Matt : finished sketches/experiments
-   14 May 2006 : Matt : began retrofitting new threading and pausing
    support to key Kamaelia components\
-   31 May 2006 : Matt : completed development
-   31 May 2006 : Michael : Allocated to merge branch into mainline
-   1 June 2006 : Michael : Merge completed
-   1 June 2006 : **Task status changed** to completed\
-   1 June 2006 : Removed developers, Michael, Matt
-   22 February 2007 : Matt : Project Task Page created\

Discussion
----------

This work mainly centred on modifications to the scheduler - replacing
its main loop with on that wouldn\'t iterate through inactive
microprocesses, and providing a thread safe mechanism for submitting
requests to it to activate, pause and unpause microprocesses.\
\
Two variants were experimented on in /Sketches/MH/Inversion.
*cleverscheduling.py* used queues for the pause/unpause/activate
requests. *aggregatedevents.py* attempted to improve efficiency by
building a table of changes, rather than simply queuing repeat requests.
The former approach was adopted as it was slightly simpler to
implement.\
\
The following components notably underwent substantial overhauls to take
advantage of the new quiescence capability, and in some cases, fixing
buggy uses of self.pause():\

-   Selector - made into a threaded component that blocked on select
    calls and would pause when idle
-   Pipeline/Graphline/Carousel - improved handling for child shutdown
    on termination
-   Pygame components - separated event polling into a threaded
    component to allow pausing when inactive; and modified existing
    components to explicitly send a request when they need to be
    redrawn, rather than assuming it happens continuously.
-   Introspector - new method calls were added to the scheduler for it
    to use, so it could introspect without knowing too much about the
    scheduler\'s internal structure.

\
\-- Matt Hammond, 22 February 2007
