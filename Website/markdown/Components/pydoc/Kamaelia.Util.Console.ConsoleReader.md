---
pagename: Components/pydoc/Kamaelia.Util.Console.ConsoleReader
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Console](/Components/pydoc/Kamaelia.Util.Console.html){.reference}.[ConsoleReader](/Components/pydoc/Kamaelia.Util.Console.ConsoleReader.html){.reference}
============================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Console.html){.reference}

------------------------------------------------------------------------

::: {.section}
class ConsoleReader([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-ConsoleReader}
-------------------------------------------------------------------------------------------------------------------------------------

ConsoleReader(\[prompt\]\[,eol\]) -\> new ConsoleReader component.

Component that provides a console for typing in stuff. Each line is
output from the \"outbox\" outbox one at a time.

Keyword arguments:

-   prompt \-- Command prompt (default=\"\>\>\> \")
-   eol \-- End of line character(s) to put on end of every line
    outputted (default is newline)

::: {.section}
### [Inboxes]{#symbol-ConsoleReader.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-ConsoleReader.Outboxes}

-   **outbox** : Lines that were typed at the console
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
#### [\_\_init\_\_(self\[, prompt\]\[, eol\])]{#symbol-ConsoleReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-ConsoleReader.main}

Main thread loop.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ConsoleReader.shutdown}
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
