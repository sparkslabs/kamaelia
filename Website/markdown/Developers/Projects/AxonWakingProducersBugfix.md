---
pagename: Developers/Projects/AxonWakingProducersBugfix
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Axon Waking Producers Bugfix 
-----------------------------------------------

::: {.boxright}
**Status:** Running\
**Current Developers:** *MH*\
**Current \"inflight\" dev location:**
/branches/private\_MH\_axon\_outboxwakeups\
**Start Date:** 20 October 2006\
**Expected End Date:** *31 November 2006*\
**End Date:** *???*\
**Date this page last updated:** *23 February 2007*\
**Estimated effort so far:** 5 days\
:::

**\
**

**Description**
---------------

To get Axon to wake up producer components when a message they have sent
out is consumed. This used to be a feature of axon, but was removed when
[Axon box delivery
optimisations](/Developers/Projects/AxonBoxDeliveryOptimisations) were
implemented. This is therefore effectively a bugfix.\
\
This allows producers to sleep if an inbox they are trying to send to
becomes full (because it is size limited) and then be woken when it
becomes non-full.\
\
Needed by the [Mobile reframer](/Developers/Projects/MobileReframer).\
\
Benefits:\

-   Reintroducing feature that was removed during earlier optimisations
-   Axon systems can self rate limit when a consumer runs slower than a
    producer\

Inputs
------

This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\

Task Sponsor: MH, MS\

Task Owner: MH\

Developers involved: MH (development), MS (merge)\

Users: MH, MS

Interested third parties: MH, MS, SJ (bbc internal)\

Requirements

-   MUST wake producer component when a message it sent is consumed
-   MUST wake producer component\
-   SHOULD not require API or behaviour changes (components should not
    need to be rewritten)
-   MUST have some test suite coverage\

\
Relevant Influencing factors:\

-   Need for rate limiting in Mobile Reframer
-   Status as an outstanding bug\

Outputs
-------

### Expected

-   Modifications to Axon (initially in branch then merged into mainline
    code)
-   \...including modifications and additions to the Axon test suite\

### Actual

Code:

CVS branch: private\_MH\_axon\_threads

Mainline code: /Code/Python/Axon/Axon/

-   Modified: Microprocess, Component and Scheduler\
-   Added: threadedadaptivecommscomponent to ThreadedComponent.py\

Mainline code: /Code/Python/Axon/Axon/Tests

-   Tests removed that were now inapplicable
-   New tests added

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

-   20 October 2006 : Added developer Matt
-   20 October 2006 : **Task status changed** to running.
-   20 October 2006 : Matt : working on private\_MH\_axon\_outboxwakeups
    branch
-   24 October 2006 : Matt : bulk of development and tests complete.
    Days spent: 5. Work switches back to [Mobile
    reframer](/Developers/Projects/MobileReframer) to adapt components
    to use these facilities.
-   Added developer Michael
-   December 2006 : Michael : Allocated to merge branch into mainline
-   21 February 2006 : Matt : takes over responsibility for merge\

\

Discussion
----------

This bug-fix brings Axon up to equivalent, but not semantically
identical, functionality to the original capabilities of Axon 1.0.\
\

#### Changes to behaviour/semantics

The original semantics worked for a model where both inbox *and* outbox
sizes could be limited, and a postman microprocess would transfer data
along linkages from outboxes to inboxes. In that model:\

-   a consumer is woken when the postman delivers
-   a producer is woken when the postman collects

However, the [box delivery
optimisations](/Developers/Projects/AxonBoxDeliveryOptimisations)
removed the concept of messages being left in an outbox and a postman to
carry them. Instead they are immediately and directly put into the final
destination inbox.\
\
The differences can therefore be summarised as:\

-   only inboxes can be size limited
-   all producers linked to an inbox are woken whenever a message is
    consumed from that inbox

In practical terms, this means that from the perspective of a component
developer, behaviour has changed in the following way:\

-   a producer may be woken only to find the destination it is trying to
    send to is still full (because another producer send a message
    there)

It was not deemed practical to perfectly replicate the old behaviour
(without reverting to a postman style model) because of the lack of a
concept of messages waiting for dispatch in the outbox.\

#### Performance issues 

It could be argued that this strategy of waking *all* producers may
cause a significant performance hit to some Axon based systems as all
producers linked to a consumer will be woken every time the consumer
collects from that inbox.

An alternative would be to only wake producers when the inbox
transitions from being full to becoming not-full. Alternatively,
producers could only be woken if they explicitly request it.\

However these ideas constitue a more fundamental change in behaviour
that component developers would have to take into account, rather than
being a simple bug-fix.

\

\-- Matt Hammond, 23 February 2007\

\
