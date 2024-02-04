---
pagename: Developers/Projects/AxonBoxDeliveryOptimisations
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Axon Box Delivery Optimisations 
--------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** *MH*\
**Current \"inflight\" dev location:**
*/branches/*private\_MH\_axon\_optimisations\
**Start Date:** *March 2006*\
**Expected End Date:** n/a\
**End Date:** *April 2006*\
**Date this page last updated:** *22 February 2007*\
**Estimated effort so far:** *20 days*\
:::

\
\

**Description**
---------------

Modifying axon to optimise delivery of messages along linkages -
especially chains of linkages - by delivering a message immediately and
directly to the final destination inbox as soon as it is sent to an
outbox. This would remove the need for a separate \"postman\"
microprocess to transfer the message along each linkage, from outbox to
inbox.\
\
This will substantially improve responsiveness and performance of Axon
systems - there will be less microprocesses in a running system; and
where components are nested delivery take a single hop rather than as
many hops as there are linkages in the chain.\
\
Needed to make practical high data throughput Kamaelia systems, such as
[KamaeliaMacro](/Developers/Projects/KamaeliaMacro).\

Inputs
------

Task Sponsor: Michael (MS)\

Task Owner: Michael, Matt (MH)\

Developers: Michael (initial experiments & final merge), Matt (final
code)\

Users: Michael, Matt\

Interested third parties: none\

Requirements

-   MUST improve rate of message delivery along linkages
-   MUST deliver messages in a single hop along a chain (2 or more
    joined) linkages
-   SHOULD not cause substantive perormance decreases elsewhere in the
    system
-   SHOULD pass the existing Axon test suite\

Relevant Influencing factors:\

-   *Needed for Kamaelia Macro*
-   *Preferable to temporarily drop Axon\'s ability to \'wake up\'
    producer components when message delivery occurs if this is
    necessary to implement these performance improvements*

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

CVS branch: private\_MH\_axon\_optimisations

Mainline code: /Code/Python/Axon/Axon/

-   Modified: most/all source files\
-   Added: Box.py
-   Removed: Postman.py

Mainline code: /Code/Python/Axon/Axon/Tests

-   Tests removed that were now inapplicable
-   New tests added

Updated components in mainline:\

-   /Code/Python/Kamaelia/Kamaelia/Chassis/Carousel.py
-   /Code/Python/Kamaelia/Kamaelia/Internet/Selector.py
-   /Code/Python/Kamaelia/Kamaelia/Util/Splitter.py
-   /Sketches/MH/ircShakespeare.py

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

-   February 2006 : Added developer Michael
-   March 2006 : **Task status changed** to running.
-   March 2006 : Michael : worked on inital sketches\
-   March 2006 : Added developer Matt
-   March 2006 : Matt : worked on private\_MH\_axon\_optimisations
    branch for Axon
-   12 April 2006 : Matt : completed development
-   18 April 2006 : Michael : Allocated to merge branch into mainline
-   27 April 2006 : Michael : Merge completed
-   27 April 2006 : **Task status changed** to completed\
-   28 April 2006 : Removed developers, Michael, Matt
-   28 April 2006 : Minor updates to components to match API change\
-   21 February 2007 : Matt : Project Task Page created\

Discussion
----------

These optimisations led to a massive performance improvement; but at the
price of Axon losing some functionality (namely the ability to wake
components when message deliveries take place).\
\
The modifications and additions to the axon testsuite were not initially
merged when the main code was merged from the branch to the mainline
codebase. This was because the decision was taken to move the tests from
/Code/Python/Axon/Axon/test to /Tests/Python/Axon/. They were later
merged when other optimisations were merged later in Summer 2006.\
\
A minor Axon API change was made (other that the removal of support for
waking due to deliveries) to make things more uniform for component
writers - a new unlink() method superceeds deRegisterLinkage() - this
mirrors the existing link() method.\
\
\-- Matt Hammond, 22 February 2007\
