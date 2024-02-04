---
pagename: Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextProgrammeJunctionDetect
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Device](/Components/pydoc/Kamaelia.Device.html){.reference}.[DVB](/Components/pydoc/Kamaelia.Device.DVB.html){.reference}.[NowNext](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}.[NowNextProgrammeJunctionDetect](/Components/pydoc/Kamaelia.Device.DVB.NowNext.NowNextProgrammeJunctionDetect.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Device.DVB.NowNext.html){.reference}

------------------------------------------------------------------------

::: {.section}
class NowNextProgrammeJunctionDetect([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-NowNextProgrammeJunctionDetect}
----------------------------------------------------------------------------------------------------------------------

NowNextProgrammeJunctionDetect() -\> new NowNextJunctionDetect
component.

Takes simplified events derived from parsed Event Information Table data
and sorts them according to whether they simply ammend/correct details
or whether they represent the start of a new programme (a junction).

::: {.section}
### [Inboxes]{#symbol-NowNextProgrammeJunctionDetect.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-NowNextProgrammeJunctionDetect.Outboxes}

-   **signal** : Shutdown signalling
-   **next** : new NEXT events, at programme junctions only
-   **now\_update** : NOW events, when details change, but its still the
    same programme
-   **outbox** : new NOW events, at programme junctions only
-   **next\_update** : NEXT events, when details change, but its still
    the same programme
-   **now** : same as for \'outbox\' outbox
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
#### [main(self)]{#symbol-NowNextProgrammeJunctionDetect.main}

Main loop
:::

::: {.section}
#### [shutdown(self)]{#symbol-NowNextProgrammeJunctionDetect.shutdown}

Shutdown handling
:::
:::

::: {.section}
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
