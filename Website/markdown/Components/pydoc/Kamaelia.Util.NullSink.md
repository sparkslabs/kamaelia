---
pagename: Components/pydoc/Kamaelia.Util.NullSink
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[NullSink](/Components/pydoc/Kamaelia.Util.NullSink.html){.reference}
======================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [nullSinkComponent](/Components/pydoc/Kamaelia.Util.NullSink.nullSinkComponent.html){.reference}**
:::
:::

::: {.section}
Null sink component. To ignore a component\'s outbox connect it to this
component and the box will be emptied but not used in any way. This will
be necessary with syncronized linkages.
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[NullSink](/Components/pydoc/Kamaelia.Util.NullSink.html){.reference}.[nullSinkComponent](/Components/pydoc/Kamaelia.Util.NullSink.nullSinkComponent.html){.reference}
=======================================================================================================================================================================================================================================================================================

::: {.section}
class nullSinkComponent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-nullSinkComponent}
---------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-nullSinkComponent.Inboxes}

-   **(\'inbox\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
-   **(\'control\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
:::

::: {.section}
### [Outboxes]{#symbol-nullSinkComponent.Outboxes}

-   **(\'outbox\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
-   **(\'signal\', \'\')** : Code uses old style inbox/outbox
    description - no metadata available
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
#### [mainBody(self)]{#symbol-nullSinkComponent.mainBody}
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
