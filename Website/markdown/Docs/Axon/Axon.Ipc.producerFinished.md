---
pagename: Docs/Axon/Axon.Ipc.producerFinished
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[producerFinished](/Docs/Axon/Axon.Ipc.producerFinished.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class producerFinished(ipc) {#symbol-producerFinished}
---------------------------

::: {.section}
producerFinished(\[caller\]\[,message\]) -\> new producerFinished ipc
message.

Message to indicate that the producer has completed its work and will
produce no more output. The receiver may wish to shutdown.

Keyword arguments:

-   caller \-- Optional. None, or the producer who has finished.
    Assigned to self.caller
-   message \-- Optional. None, or a message giving any relevant info.
    Assigned to self.message
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, caller\]\[, message\])]{#symbol-producerFinished.__init__}
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
