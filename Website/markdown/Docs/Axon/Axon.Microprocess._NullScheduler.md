---
pagename: Docs/Axon/Axon.Microprocess._NullScheduler
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Microprocess](/Docs/Axon/Axon.Microprocess.html){.reference}.[\_NullScheduler](/Docs/Axon/Axon.Microprocess._NullScheduler.html){.reference}
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Microprocess.html){.reference}

------------------------------------------------------------------------

::: {.section}
class \_NullScheduler(object) {#symbol-_NullScheduler}
-----------------------------

::: {.section}
A dummy scheduler, used by microprocess when it has not yet been
activated (and therefore isn\'t yet assigned to a real scheduler).

Provides dummy versions of the methods a microprocess may wish to call
to get stuff done.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [isThreadPaused(self, mprocess)]{#symbol-_NullScheduler.isThreadPaused}

Dummy method - does nothing.
:::

::: {.section}
#### [pauseThread(self, mprocess)]{#symbol-_NullScheduler.pauseThread}

Dummy method - does nothing.
:::

::: {.section}
#### [wakeThread(self, mprocess)]{#symbol-_NullScheduler.wakeThread}

Dummy method - does nothing.
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
