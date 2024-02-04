---
pagename: Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[WakeableIntrospector](/Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector.html){.reference}
=================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [WakeableIntrospector](/Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector.WakeableIntrospector.html){.reference}**
:::

-   [On Demand/Wakeable Introspector](#71){.reference}
    -   [Example Usage](#72){.reference}
    -   [How does it work?](#73){.reference}
    -   [Termination](#74){.reference}
    -   [TODO](#75){.reference}
:::

::: {.section}
On Demand/Wakeable Introspector {#71}
===============================

This component grabs a list of all running/runnable components whenever
it receives a message on its inbox \"inbox\". This list is then sorted,
and noted to a logfile.

::: {.section}
[Example Usage]{#example-usage} {#72}
-------------------------------

This component is intended to be used with PeriodicWakeup, as follows:

``` {.literal-block}
Pipeline(
     PeriodicWakeup(interval=20),
     WakeableIntrospector(logfile="/tmp/trace"),
)
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#73}
--------------------------------------

This component uses the fact that we can ask the scheduler for a list of
running componenents, takes this, sorts it and dumps the result to a
logfile.

It then sits quietly waking for a message (any message) on the inbox
\"inbox\".
:::

::: {.section}
[Termination]{#termination} {#74}
---------------------------

This component is not well behaved regarding termination, in that it
does not have any shutdown conditions.
:::

::: {.section}
[TODO]{#todo} {#75}
-------------

In retrospect, it may\'ve been nicer to split the introspection from the
logging. Better termination/shutdown would be a good idea.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Apps](/Components/pydoc/Kamaelia.Apps.html){.reference}.[Grey](/Components/pydoc/Kamaelia.Apps.Grey.html){.reference}.[WakeableIntrospector](/Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector.html){.reference}.[WakeableIntrospector](/Components/pydoc/Kamaelia.Apps.Grey.WakeableIntrospector.WakeableIntrospector.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class WakeableIntrospector([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-WakeableIntrospector}
------------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-WakeableIntrospector.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-WakeableIntrospector.Outboxes}
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [main(self)]{#symbol-WakeableIntrospector.main}
:::

::: {.section}
#### [noteToLog(self, line)]{#symbol-WakeableIntrospector.noteToLog}
:::
:::

::: {.section}
:::
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
