---
pagename: Docs/Axon/Axon.Ipc.shutdownMicroprocess
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class shutdownMicroprocess(ipc) {#symbol-shutdownMicroprocess}
-------------------------------

::: {.section}
shutdownMicroprocess(\*microprocesses) -\> new shutdownMicroprocess ipc
message.

Message used to indicate that the component recieving it should
shutdown. Or to indicate to the scheduler a shutdown knockon from a
terminating microprocess.

Arguments:

-   the microprocesses to be shut down (when used as a knockon)
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*microprocesses)]{#symbol-shutdownMicroprocess.__init__}
:::

::: {.section}
#### [microprocesses(self)]{#symbol-shutdownMicroprocess.microprocesses}

Returns the list of microprocesses to be shut down
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
