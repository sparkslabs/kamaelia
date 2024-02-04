---
pagename: Components/pydoc/Kamaelia.Util.PromptedTurnstile.PromptedTurnstile
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.html){.reference}.[PromptedTurnstile](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.PromptedTurnstile.html){.reference}
==================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.PromptedTurnstile.html){.reference}

------------------------------------------------------------------------

::: {.section}
class PromptedTurnstile([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PromptedTurnstile}
---------------------------------------------------------------------------------------------------------

PromptedTurnstile() -\> new PromptedTurnstile component.

Buffers all items sent to its \"inbox\" inbox, and only sends them out,
one at a time when requested.

::: {.section}
### [Inboxes]{#symbol-PromptedTurnstile.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
-   **next** : Requests to send out items
:::

::: {.section}
### [Outboxes]{#symbol-PromptedTurnstile.Outboxes}

-   **outbox** : Data items
-   **signal** : Shutdown signalling
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
#### [checkShutdown(self)]{#symbol-PromptedTurnstile.checkShutdown}
:::

::: {.section}
#### [main(self)]{#symbol-PromptedTurnstile.main}
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
