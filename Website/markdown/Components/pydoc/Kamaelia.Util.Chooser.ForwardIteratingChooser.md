---
pagename: Components/pydoc/Kamaelia.Util.Chooser.ForwardIteratingChooser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chooser](/Components/pydoc/Kamaelia.Util.Chooser.html){.reference}.[ForwardIteratingChooser](/Components/pydoc/Kamaelia.Util.Chooser.ForwardIteratingChooser.html){.reference}
================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Chooser.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ForwardIteratingChooser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ForwardIteratingChooser}
---------------------------------------------------------------------------------------------------------------

Chooser(\[items\]) -\> new Chooser component.

Iterates through an iterable set of items. Step by sending \"NEXT\"
messages to its \"inbox\" inbox.

Keyword arguments: - items \-- iterable source of items to be chosen
from (default=\[\])

::: {.section}
### [Inboxes]{#symbol-ForwardIteratingChooser.Inboxes}

-   **control** : shutdown messages
-   **inbox** : receive commands
:::

::: {.section}
### [Outboxes]{#symbol-ForwardIteratingChooser.Outboxes}

-   **outbox** : emits chosen items
-   **signal** : shutdown messages
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
#### [\_\_init\_\_(self\[, items\])]{#symbol-ForwardIteratingChooser.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [getCurrentChoice(self)]{#symbol-ForwardIteratingChooser.getCurrentChoice}

Return the current choice
:::

::: {.section}
#### [gotoNext(self)]{#symbol-ForwardIteratingChooser.gotoNext}

Advance the choice forwards one.

Returns True if successful or False if unable to (eg. already at end).
:::

::: {.section}
#### [main(self)]{#symbol-ForwardIteratingChooser.main}

Main loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ForwardIteratingChooser.shutdown}

Returns True if a shutdownMicroprocess message was received.
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
