---
pagename: Components/pydoc/Kamaelia.Util.TwoWaySplitter.TwoWaySplitter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[TwoWaySplitter](/Components/pydoc/Kamaelia.Util.TwoWaySplitter.html){.reference}.[TwoWaySplitter](/Components/pydoc/Kamaelia.Util.TwoWaySplitter.TwoWaySplitter.html){.reference}
===================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.TwoWaySplitter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class TwoWaySplitter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-TwoWaySplitter}
------------------------------------------------------------------------------------------------------

TwoWaySplitter() -\> new TwoWaySplitter component

Anything sent to the \"inbox\" or \"control\" inboxes is sent on out of
the \"outbox\" and \"outbox2\" or \"signal\" and \"signal2\" outboxes
respectively.

::: {.section}
### [Inboxes]{#symbol-TwoWaySplitter.Inboxes}

-   **control** : Shutdown signalling (also sent to the \'signal\' and
    \'signal2\' outboxes
-   **inbox** : Message to be sent to the \'outbox\' and \'outbox2\'
    outboxes
:::

::: {.section}
### [Outboxes]{#symbol-TwoWaySplitter.Outboxes}

-   **outbox2** : Messages sent to the \'inbox\' inbox
-   **outbox** : Messages sent to the \'inbox\' inbox
-   **signal** : Messages sent to the \'control\' inbox
-   **signal2** : Messages sent to the \'control\' inbox
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
#### [canStop(self)]{#symbol-TwoWaySplitter.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-TwoWaySplitter.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-TwoWaySplitter.main}
:::

::: {.section}
#### [mustStop(self)]{#symbol-TwoWaySplitter.mustStop}
:::

::: {.section}
#### [waitSendMultiple(self, \*things)]{#symbol-TwoWaySplitter.waitSendMultiple}
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
