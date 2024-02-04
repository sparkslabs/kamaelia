---
pagename: Developers/Projects/AxonThreadedComponentAPIChange
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Axon ThreadedComponent API Change 
----------------------------------------------------

::: {.boxright}
**Status:** *Completed*\
**Current Developers: ** *MH*\
**Current \"inflight\" dev location:**
/branches/private\_MH\_axon\_threads\
**Start Date:** *13 April 2006*\
**Expected End Date:** *n/a*\
**End Date:** *4 May 2006*\
**Date this page last updated:** *22 February 2007*\
**Estimated effort so far:** *15*\
:::

**\
**

**Description**
---------------

To change the design of ThreadedComponent so that when writing a
component based on it, it is almost identical to writing a normal
component (just leaving out the yield statements).

The existing design required the component writer to access queue
objects to send and receive data, rather than use the
*self.dataReady()*, *self.send* and *self.recv()* methods they would use
for a normal component.

In the process, thread safety should also be improved, and the ability
to add and remove inboxes and outboxes on the fly (ala
AdaptiveCommsComponent) should be implemented.

Benefits:

-   Much easier to write threaded components
-   Very easy to convery a normal component to/from being a threaded
    one\
-   Possible to write threaded components that dynamically change their
    inboxes and outboxes (eg. Selector service component)\

Inputs
------

Task Sponsor: Michael (MS)\

Task Owner: Matt (MH)\

Developers involved: Matt (development), Michael (merging)\

Users: Matt, Michael\

Interested third parties: none\

Requirements

Just like for a normal component, when writing a threaded one\...\

-   MUST be able to use *self.dataReady()*, *self.send()* and
    *self.recv()\
    *
-   SHOULD be able to call the main body code main()\

MUST be thread safe for:

-   sending messages
-   receiving messages
-   adding inboxes & outboxes
-   removing inboxes & outboxes
-   creating linkages
-   destroying linkages

SHOULD be able to trap exceptions and throw them back to the main thread
so an Axon system can correctly terminate.\

Relevant Influencing factors:\

-   *Need to implement \'Selector\' as a threaded component (for
    throughput optimisations)\
    *

Outputs
-------

### Expected

-   Modifications to Axon (initially in branch, then merged into
    mainline code)
-   Modifications and additions to Axon test suite

### Actual

Code:

CVS branch: private\_MH\_axon\_threads

Mainline code: /Code/Python/Axon/Axon/

-   Modified: Microprocess, Component and Scheduler\
-   Added: threadedadaptivecommscomponent to ThreadedComponent.py\

Mainline code: /Code/Python/Axon/Axon/Tests

-   Tests removed that were now inapplicable
-   New tests added

Updated components to use new API:\

-   /Sketches/MPS/backplane.py
-   /Sketches/MPS/control\_mix.py
-   /Sketches/MPS/dj1.py
-   /Sketches/MPS/dj2.py
-   /Sketches/MPS/music.py

### Realistic possibilities arising as a result of activity on this task

Need to make access to CAT threadsafe too.\

Task Log
--------

-   13 April 2006 : Added developer Matt\
-   13 April 2006 : **Task status changed** to running
-   13 April 2006 : Matt : worked on private\_MH\_Axon\_threads branch
    for Axon
-   02 May 2006 : Matt : completed development\
-   03 May 2006 : Added developer Michael : to merge branch into
    mainline
-   04 May 2006 : Michael : Merge completed
-   04 May 2006 : **Task status changed** to completed
-   04 May 2006 : Removed developers Matt, Michael
-   22 February 2007 : Project Task Page created\

Discussion
----------

Distinction between activity-creators and non activity-creator
components removed (the scheduler would stop if there wasn\'t at least
one activity-creator microprocess running). This was no longer necessary
as there was no longer a postman microprocess (a non activity-creator).
Removing support for this from the scheduler simplified things, making
implementing support for the new design threaded components (and later
quiescence optimisations) easier.\
\

\-- Matt Hammond, 22 February 2007\
