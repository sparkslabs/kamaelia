---
pagename: Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Console](/Components/pydoc/Kamaelia.Util.Console.html){.reference}.[ConsoleEchoer](/Components/pydoc/Kamaelia.Util.Console.ConsoleEchoer.html){.reference}
============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Console.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ConsoleEchoer([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ConsoleEchoer}
-----------------------------------------------------------------------------------------------------

ConsoleEchoer(\[forwarder\]\[,use\_repr\]\[,tag\]) -\> new ConsoleEchoer
component.

A component that outputs anything it is sent to standard output (the
console).

Keyword arguments:

-   forwarder \-- incoming data is also forwarded to \"outbox\" outbox
    if True (default=False)
-   use\_repr \-- use repr() instead of str() if True (default=False)
-   tag \-- Pre-pend this text tag before the data to emit

::: {.section}
### [Inboxes]{#symbol-ConsoleEchoer.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Stuff that will be echoed to standard output
:::

::: {.section}
### [Outboxes]{#symbol-ConsoleEchoer.Outboxes}

-   **outbox** : Stuff forwarded from \'inbox\' inbox (if enabled)
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
#### [\_\_init\_\_(self\[, forwarder\]\[, use\_repr\]\[, tag\])]{#symbol-ConsoleEchoer.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-ConsoleEchoer.main}

Main loop body.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ConsoleEchoer.shutdown}
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
