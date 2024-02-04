---
pagename: Docs/Axon/Axon.Scheduler.scheduler
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Scheduler](/Docs/Axon/Axon.Scheduler.html){.reference}.[scheduler](/Docs/Axon/Axon.Scheduler.scheduler.html){.reference}
------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Scheduler.html){.reference}

------------------------------------------------------------------------

::: {.section}
class scheduler([Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}) {#symbol-scheduler}
-------------------------------------------------------------------------------------------------------------

::: {.section}
Scheduler - runs microthreads of control.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, \*\*argd)]{#symbol-scheduler.__init__}

Creates a scheduler object. If scheduler.run has not been set, sets it.
Class initialisation ensures that this object/class attribute is
initialised - client modules always have access to a standalone
scheduler. Internal attributes:

> -   time = time when this object was last active.
> -   threads = set of threads to be run, including their state -
>     whether active or sleeping(paused)

Whilst there can be more than one scheduler active in the general case
you will NOT want to create a custom scheduler.
:::

::: {.section}
#### [\_addThread(self, mprocess)]{#symbol-scheduler._addThread}

A Microprocess adds itself to the runqueue using this method, using the
mannerism scheduler.run.\_addThread(). Generally component writers
should *not* use this method to activate a component - use the
component\'s own activate() method instead.
:::

::: {.section}
#### [handleMicroprocessShutdownKnockon(self, knockon)]{#symbol-scheduler.handleMicroprocessShutdownKnockon}
:::

::: {.section}
#### [isThreadPaused(self, mprocess)]{#symbol-scheduler.isThreadPaused}

Returns True if the specified microprocess is sleeping, or the scheduler
does not know about it.
:::

::: {.section}
#### [listAllThreads(self)]{#symbol-scheduler.listAllThreads}

Returns a list of all microprocesses (both active and sleeping)
:::

::: {.section}
#### [main(self\[, slowmo\]\[, canblock\])]{#symbol-scheduler.main}

main(\[slowmo\]\[,canblock\]) - Scheduler main loop generator

Each cycle through this generator does two things: \* one pass through
all active microprocesses, giving executing them. \* processing of
wake/sleep requests

You can optionally slow down execution to aid debugging. You can also
allow the scheduler to block if there are no active, awake
microprocesses.

Keyword arguments:

-   slowmo \-- slow down execution by waiting this number of seconds
    each cycle (default=0)
-   canblock \-- if True, then will block (waiting for wake requests) if
    all microprocesses are sleeping (default=False)

slowmo specifies a delay (in seconds) before the main loop is run.
slowmo defaults to 0.

If canblock is True, this generator will briefly) block if there are no
active microprocesses, otherwise it will return immediately (default).

This generator terminates when there are no microprocesses left (either
sleeping or awake) because they\'ve all terminated. (or because there
were none to begin with!)
:::

::: {.section}
#### [pauseThread(self, mprocess)]{#symbol-scheduler.pauseThread}

pauseThread(mprocess) - request to put a mprocess to sleep.

If active, or already sleeping, the specified microprocess will be put
to leep on the next cycle through the scheduler.
:::

::: {.section}
#### [runThreads(self\[, slowmo\])]{#symbol-scheduler.runThreads}

Runs the scheduler until there are no activated microprocesses left
(they\'ve all terminated).

Think of this as bootstrapping the scheduler - after all it is a
microprocess like any other, so needs something to run it!

Keyword arguments:

-   slowmo \-- Optional. Number of seconds to wait between each cycle of
    executing microprocesses. (default=0 - no wait)
:::

::: {.section}
#### [stop(self)]{#symbol-scheduler.stop}
:::

::: {.section}
#### [waitForOne(self)]{#symbol-scheduler.waitForOne}
:::

::: {.section}
#### [wakeThread(self, mprocess\[, canActivate\])]{#symbol-scheduler.wakeThread}

Request to wake a sleeping mprocess, or activate a new one.

If sleeping or already active, the specified microprocess will be
ensured to be active on the next cycle through the scheduler.

If the microprocess is not running yet then it will be woken if (and
only if) canActivate is set to True (the default is False).
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._closeDownMicroprocess){.reference}(self)
-   [pause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.pause){.reference}(self)
-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [\_\_str\_\_](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.__str__){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [activate](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
:::
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
