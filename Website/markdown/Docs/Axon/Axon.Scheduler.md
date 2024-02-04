---
pagename: Docs/Axon/Axon.Scheduler
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Scheduler](/Docs/Axon/Axon.Scheduler.html){.reference}
------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Scheduler - runs things concurrently
====================================

::: {.container}
-   **[\_sort](/Docs/Axon/Axon.Scheduler._sort.html){.reference}**(somelist)
-   **class
    [scheduler](/Docs/Axon/Axon.Scheduler.scheduler.html){.reference}**
:::

-   [Using the scheduler](#26){.reference}
-   [Pausing and Waking microprocesses](#27){.reference}
-   [\'yielding\' new components for activation and replacement
    generators](#28){.reference}
-   [What happens when a microprocess finishes?](#29){.reference}
-   [Querying the scheduler (Introspection)](#30){.reference}
-   [Slowing down execution (for debugging)](#31){.reference}
-   [How does it work internally?](#32){.reference}
-   [Test documentation](#33){.reference}
:::

::: {.section}
The Scheduler runs active microprocesses - giving a regular timeslice to
each. It also provides the ability to pause and wake them; allowing an
Axon based system to play nicely and relinquish the cpu when idle.

-   The Scheduler runs microprocesses that have been \'activated\'
-   The Scheduler is itself a microprocess

::: {.section}
[Using the scheduler]{#using-the-scheduler} {#26}
-------------------------------------------

The simplest way is to just use the default scheduler
`scheduler.run`{.docutils .literal}. Simply activate components or
microprocesses then call the runThreads() method of the scheduler:

``` {.literal-block}
from Axon.Scheduler import scheduler
from MyComponents import MyComponent, AnotherComponent

c1 = MyComponent().activate()
c2 = MyComponent().activate()
c3 = AnotherComponent().activate()

scheduler.run.runThreads()
```

Alternatively you can create a specific scheduler instance, and activate
them using that specific scheduler:

``` {.literal-block}
mySched = scheduler()

c1 = MyComponent().activate(Scheduler=mySched)
c2 = MyComponent().activate(Scheduler=mySched)
c3 = AnotherComponent().activate(Scheduler=mySched)

mySched.runThreads()
```

The runThreads() method is the way of bootstrapping the scheduler. Being
a microprocess, it needs something to schedule it! The runThreads()
method does exactly that.

The activate() method is fully thread-safe. It can handle multiple
simultaneous callers from different threads to the one the scheduler is
running in.
:::

::: {.section}
[Pausing and Waking microprocesses]{#pausing-and-waking-microprocesses} {#27}
-----------------------------------------------------------------------

The Scheduler supports the ability to, in a thread safe manner, pause
and wake individual microprocesses under its control. Because it is
thread safe, any thread of execution can issue pause and wake requests
for any scheduled microprocess.

The pauseThread() and wakeThread() methods submit requests to pause or
wake microprocesses. The scheduler will process these when it is next
able to - the requests are queued rather than processed immediately.
This is done to ensure thread safety. It can handle multiple
simultaneous callers from different threads to the one the scheduler is
running in.

Pausing a microprocess means the scheduler removes it from its \'run
queue\'. This means that it no longer executes that microprocess. Waking
it puts it back into the \'run queue\'.

If no microprocesses are awake then the scheduler relinquishes cpu usage
by blocking.

If however this scheduler is itself being scheduled by another
microprocess then it does not block. Ideally it should ask its scheduler
to pause it, but instead it busy-waits - self pausing functionality is
not yet implemented.
:::

::: {.section}
[\'yielding\' new components for activation and replacement generators]{#yielding-new-components-for-activation-and-replacement-generators} {#28}
-------------------------------------------------------------------------------------------------------------------------------------------

In general, the main() generator in a microprocess (its thread of
execution) can return any values it likes when it uses the
`yield`{.docutils .literal} statement. It is recommended to not yield
zeros or other kinds of \'false\' value as these are reserved for
possible future special meaning.

However, this scheduler does understand certain values that can be
yielded:

-   **[Axon.Ipc.newComponent](/Docs/Axon/Axon.Ipc.newComponent.html){.reference}** -
    a microprocess can yield this to ask the scheduler to activate a new
    component or microprocess:

    ``` {.literal-block}
    def main(self):
        ...
        x=MyComponent()
        yield Axon.Ipc.newComponent(x)
        ...
    ```

    This is simply an alternative to calling x.activate().

-   **[Axon.Ipc.WaitComplete](/Docs/Axon/Axon.Ipc.WaitComplete.html){.reference}** -
    this is a way for a microprocess to substitute itself (temporarily)
    with another one that uses a new generator. For example:

    ``` {.literal-block}
    def main(self):
        ...
        yield Axon.Ipc.WaitComplete(self.waitOneSecond())
        ...

    def waitOneSecond(self):
        t=time.time()
        while time.time() < t+1.0:
            yield 1
    ```

    This is a convenient way to modularise parts of your main() code.
    But there is an important limitation with the current
    implementation:

    -   self.pause() will not cause the replacement generator to pause.
        (Where \'self\' is the original microprocess - as in the example
        code above)
:::

::: {.section}
[What happens when a microprocess finishes?]{#what-happens-when-a-microprocess-finishes} {#29}
----------------------------------------------------------------------------------------

The scheduler will stop running it! It will call the microprocess\'s
stop() method. It will also call the \_closeDownMicroprocess() method
and will act on the return value if it is one of the following:

-   **[Axon.Ipc.shutdownMicroprocess](/Docs/Axon/Axon.Ipc.shutdownMicroprocess.html){.reference}** -
    the specified microprocess will also be stopped. Use with caution as
    the implementation is currently untested and likely to fail,
    possibly even crash the scheduler!
-   **[Axon.Ipc.reactivate](/Docs/Axon/Axon.Ipc.reactivate.html){.reference}** -
    the specified microprocess will be (re)activated. The scheduler uses
    this internally to pick up where it left off when a
    [Axon.Ipc.WaitComplete](/Docs/Axon/Axon.Ipc.WaitComplete.html){.reference}
    instigated detour finishes (see above).
:::

::: {.section}
[Querying the scheduler (Introspection)]{#querying-the-scheduler-introspection} {#30}
-------------------------------------------------------------------------------

The listAllThreads() method returns a list of all activated
microprocesses - both paused and awake.

The isThreadPaused() method lets you determine if an individual
microprocess is paused. Note that the result returned by this method is
conservative (the default assumption is that a thread is probably
awake). the result will vary depending on the exact moment it is called!

Both these methods are thread safe.
:::

::: {.section}
[Slowing down execution (for debugging)]{#slowing-down-execution-for-debugging} {#31}
-------------------------------------------------------------------------------

It also has a slow motion mode designed to help with debugging &
testing. Call runThreads() with the slowmo argument set to the number of
seconds the scheduler should pause after each cycle of executing all
microprocesses. For example, to wait half a second after each cycle of
execution:

``` {.literal-block}
scheduler.run.runThreads(slowmo=0.5)
```
:::

::: {.section}
[How does it work internally?]{#how-does-it-work-internally} {#32}
------------------------------------------------------------

The scheduler keeps the following internal state:

-   **time** - updated to time.time() every execution cycle - can be
    inspected by microprocesses instead of having to call time.time()
    themselves.
-   **threads** - a dictionary containing the state of activated
    microprocesses (whether they are awake or not)
-   **wakeRequests** and **pauseRequests** - the thread safe queues of
    requests to wake and pause individual microprocesses
-   Internal to the main() generator:
    -   **runqueue** - the list of active and awake microprocesses being
        run
    -   **nextrunqueue** - the list of microprocesses to be run next
        time round

The scheduler uses a simple round robin approach - it walks through its
run queue and calls the next() method of each microprocess in turn. As
it goes, it builds a new run queue, ready for the next cycle. If a
microprocess terminates (raises a StopIteration exception) then it is
not included in the next cycle\'s run queue.

After it has gone through all microprocesses, the scheduler then
processes messages in its wakeRequests and sleepRequests queues. Sleep
requests are processed first; then wake requests second. Suppose there
is a sleep and wake request queued for the same microprocess; should it
be left awake or put to sleep? By processing wake requests last, the
scheduler can err on the side of caution and prefer to leave it awake.

Microprocesses are all in one of three possible states (recorded in the
`threads`{.docutils .literal} dictionary):

-   **ACTIVE** - the microprocess is awake. It should be in the run
    queue being prepared for the next execution cycle.
-   **SLEEPING** - the microprocess is asleep/paused. It should *not* be
    in the run queue for the next cycle.
-   **GOINGTOSLEEP** - the microprocess has been requested to be put to
    sleep.

A request to put a microprocess to sleep is handled as follows:

-   If the microprocess is already *sleeping*, then nothing needs to
    happen.

-   If the microprocess is *active*, then it is changed to \"going to
    sleep\". It is not removed from the run queue immediately. Instead,
    what happens is:

    > -   on the next cycle of execution, as the scheduler goes through
    >     items in the run queue, it doesn\'t execute any that are
    >     \"going to sleep\" and doesn\'t include them in the next run
    >     queue it is building. It also sets them to the \"sleeping\"
    >     state,

Wake requests are used to both wake up sleeping microprocesses and also
to activate new ones. A request to wake a microprocess is handled like
this:

-   If the microprocess is already *active*, then nothing needs to
    happen.
-   If the microprocess is *sleeping* then it is added to the next run
    queue and changed to be *active*.
-   If the microprocess is *going to sleep* then it is only changed to
    be *active* (it will already be in the run queue, so doesn\'t need
    to be added)

If the request contains a flag indicating that this is actually an
activation request, then this also happens:

-   If the microprocess is not in the `threads`{.docutils .literal}
    dictionary then it is added to both the run queue and
    `threads`{.docutils .literal}. It is set to be *active*.

This three state system is a performance optimisation: it means that the
scheduler does not need to waste time searching through the next run
queue to remove items - they simply get removed on the next cycle of
execution.

Wake requests and sleep requests are handled through thread-safe queues.
This enables other threads of execution (eg. threaded components) to
safely make requests to wake or pause components.
:::

Test documentation {#33}
==================

Tests passed:

-   \_\_init\_\_ - Called with no arguments \...
-   By default, if all microprocesses are paused, the scheduler will
    immediately yield back - it will not block.
-   test\_importsuccess (\_\_main\_\_.scheduler\_Test)
-   The isThreadPaused() method will return True for micropocesses not
    scheduled with this scheduler.
-   The isThreadPaused() method returns True if a thread is currently
    paused, or False is it is active.
-   The listAllThreads() method returns a list of all activated
    microprocesses whether paused or awake.
-   If one microprocess is paused, the scheduler continues to run other
    microprocesses.
-   If a microprocess pauses and immediately terminates (without further
    yields) it will still terminate properly.
-   If a microprocess is paused, calling sheduler.wakeThread() will
    unpause it.
-   A microprocess is run until paused, by calling
    scheduler.pauseThread(). The microprocess is then no longer \'run\'.
-   Specifying slowMo\>0 argument to runThreads() causes a delay of the
    specified number of seconds between each pass through all
    microprocesses. During the delay it will yield.
-   If run using the runThreads method, then the scheduler may/will
    block for short periods, relinquishing processor time, if all
    microprocesses are paused.
-   When run with a single microprocess, the scheduler microprocess only
    terminates once the scheduled microprocess has terminated.
-   When run with multiple microprocesses, the scheduler microprocess
    only terminates once all scheduled microprocesses have terminated.
-   When run, the scheduler microprocess terminates immediately if there
    are no microprocesses to schedule.
-   Waking or pausing a microprocess that is already awake or paused
    (respectively) has no effect.
-   Waking or pausing a microprocess that has not yet been activated has
    no effect.
-   Waking a paused microprocess will not wake other paused
    microprocesses.
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Scheduler](/Docs/Axon/Axon.Scheduler.html){.reference}.[\_sort](/Docs/Axon/Axon.Scheduler._sort.html){.reference}
===========================================================================================================================================================

::: {.section}
[\_sort(somelist)]{#symbol-_sort}
---------------------------------
:::

[Axon](/Docs/Axon/Axon.html){.reference}.[Scheduler](/Docs/Axon/Axon.Scheduler.html){.reference}.[scheduler](/Docs/Axon/Axon.Scheduler.scheduler.html){.reference}
==================================================================================================================================================================

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
