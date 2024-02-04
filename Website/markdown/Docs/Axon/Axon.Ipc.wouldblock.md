---
pagename: Docs/Axon/Axon.Ipc.wouldblock
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[wouldblock](/Docs/Axon/Axon.Ipc.wouldblock.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class wouldblock(ipc) {#symbol-wouldblock}
---------------------

::: {.section}
wouldblock(caller) -\> new wouldblock ipc message.

Message used to indicate to the scheduler that the system is likely to
block now.

Keyword arguments:

-   caller \-- who it is who is likely to block (presumably a
    microprocess). Assigned to self.caller
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, caller)]{#symbol-wouldblock.__init__}
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
