---
pagename: Components/pydoc/Kamaelia.File.UnixProcess.UnixProcess
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.html){.reference}.[UnixProcess](/Components/pydoc/Kamaelia.File.UnixProcess.UnixProcess.html){.reference}
====================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.File.UnixProcess.html){.reference}

------------------------------------------------------------------------

::: {.section}
class UnixProcess([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-UnixProcess}
---------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-UnixProcess.Inboxes}

-   **control** : We receive shutdown messages here
-   **stdinready** : We\'re notified here when we can write to the
    sub-process
-   **inbox** : Strings containing data to send to the sub process
-   **stderrready** : We\'re notified here when we can read errors from
    the sub-process
-   **stdoutready** : We\'re notified here when we can read from the
    sub-process
:::

::: {.section}
### [Outboxes]{#symbol-UnixProcess.Outboxes}

-   **outbox** : data from the sub command is output here
-   **signal** : not used
-   **selectorsignal** : To send control messages to the selector
-   **selector** : We send messages to the selector here, requesting it
    tell us when file handles can be read from/written to
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
#### [\_\_init\_\_(self, command)]{#symbol-UnixProcess.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-UnixProcess.main}
:::

::: {.section}
#### [openSubprocess(self)]{#symbol-UnixProcess.openSubprocess}
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
