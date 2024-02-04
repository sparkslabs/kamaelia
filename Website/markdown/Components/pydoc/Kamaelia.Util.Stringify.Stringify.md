---
pagename: Components/pydoc/Kamaelia.Util.Stringify.Stringify
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Stringify](/Components/pydoc/Kamaelia.Util.Stringify.html){.reference}.[Stringify](/Components/pydoc/Kamaelia.Util.Stringify.Stringify.html){.reference}
==========================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Stringify.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Stringify([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Stringify}
-------------------------------------------------------------------------------------------------

Stringify() -\> new Stringify.

A component that converts data items received on its \"inbox\" inbox to
strings and sends them on out of its \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-Stringify.Inboxes}

-   **control** : NOT USED
-   **inbox** : Data items to convert to string
:::

::: {.section}
### [Outboxes]{#symbol-Stringify.Outboxes}

-   **outbox** : Data items converted to strings
-   **signal** : NOT USED
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
#### [\_\_init\_\_(self)]{#symbol-Stringify.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [mainBody(self)]{#symbol-Stringify.mainBody}

Main loop body.
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
