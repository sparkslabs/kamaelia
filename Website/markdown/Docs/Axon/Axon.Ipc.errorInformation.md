---
pagename: Docs/Axon/Axon.Ipc.errorInformation
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[errorInformation](/Docs/Axon/Axon.Ipc.errorInformation.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class errorInformation(ipc) {#symbol-errorInformation}
---------------------------

::: {.section}
errorInformation(caller\[,exception\]\[,message\]) -\> new
errorInformation ipc message.

A message to indicate that a non fatal error has occured in the
component. It may skip processing errored data but should respond
correctly to future messages.

Keyword arguments:

-   caller \-- the source of the error information. Assigned to
    self.caller
-   exception \-- Optional. None, or the exception that caused the
    error. Assigned to self.exception
-   message \-- Optional. None, or a message describing the problem.
    Assigned to self.message
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, caller\[, exception\]\[, message\])]{#symbol-errorInformation.__init__}
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
