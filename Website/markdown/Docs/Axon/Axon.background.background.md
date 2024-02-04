---
pagename: Docs/Axon/Axon.background.background
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[background](/Docs/Axon/Axon.background.html){.reference}.[background](/Docs/Axon/Axon.background.background.html){.reference}
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.background.html){.reference}

------------------------------------------------------------------------

::: {.section}
class background(threading.Thread) {#symbol-background}
----------------------------------

::: {.section}
A python thread which runs the Axon Scheduler. Takes the same arguments
at creation that Axon.Scheduler.scheduler.run.runThreads accepts.

Create one of these and start it running by calling its start() method.

After that, any components you activate will default to using this
scheduler.

Only one instance can be used within a given python interpreter.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, slowmo\]\[, zap\])]{#symbol-background.__init__}
:::

::: {.section}
#### [run(self)]{#symbol-background.run}
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
