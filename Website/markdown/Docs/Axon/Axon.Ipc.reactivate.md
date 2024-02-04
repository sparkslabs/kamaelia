---
pagename: Docs/Axon/Axon.Ipc.reactivate
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Ipc](/Docs/Axon/Axon.Ipc.html){.reference}.[reactivate](/Docs/Axon/Axon.Ipc.reactivate.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Ipc.html){.reference}

------------------------------------------------------------------------

::: {.section}
class reactivate(ipc) {#symbol-reactivate}
---------------------

::: {.section}
reactivate(original) -\> new reactivate ipc message.

Returned by
[Axon.Microprocess.microprocess.\_closeDownMicroprocess](/Docs/Axon/Axon.Microprocess.microprocess._closeDownMicroprocess.html){.reference}()
to the scheduler to get another microprocess reactivated.

Keyword arguments:

-   original \-- The original microprocess to be resumed. Assigned to
    self.original
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, original)]{#symbol-reactivate.__init__}
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
