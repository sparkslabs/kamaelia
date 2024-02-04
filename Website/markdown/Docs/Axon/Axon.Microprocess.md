---
pagename: Docs/Axon/Axon.Microprocess
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Microprocess](/Docs/Axon/Axon.Microprocess.html){.reference}
------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Microprocess - A class supporting concurrent execution
======================================================

::: {.container}
-   **class
    [\_NullScheduler](/Docs/Axon/Axon.Microprocess._NullScheduler.html){.reference}**
-   **class
    [microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}**
:::

-   [Basic Usage](#46){.reference}
-   [More detail](#47){.reference}
    -   [Alternative ways of defining the
        generator/thread](#48){.reference}
-   [Microprocess lifecycle in detail](#49){.reference}
-   [Internal flags/state](#50){.reference}
-   [Test documentation](#51){.reference}
:::

::: {.section}
A microprocess is a class supporting parallel execution, provided by
forming a wrapper around a generator. It also provides a place for
context to be stored about the generator.

-   A component is based on a microprocess - giving it its thread of
    execution.
-   The Scheduler runs microprocesses that have been \'activated\'

*This is an Axon internal. If you are writing components you do not need
to understand this as you will normally not use it directly.*

Developers wishing to use Axon in other ways or understand its
implementation shoudl read on with interest!

::: {.section}
[Basic Usage]{#basic-usage} {#46}
---------------------------

Making and using a microprocess is easy:

1.  Subclass microprocess writing your own main() generator method
2.  Create and \'activate\' it
3.  Run the scheduler so it is executed

Specifically, classes that subclass microprocess, and implement a main()
generator function can be activated, and scheduled by the
scheduler/microthread systems. Essentially a microprocess provides a
minimal runtime context for the scheduling & thread handling system.

In more detail:

1.  Subclass a microprocess, overriding the main() generator method to
    make your own that yields non-zero/False values:

    ``` {.literal-block}
    class Loopy(microprocess):
        def __init__(self, num):
            self.num = num
            super(Loopy, self).__init__()
        def main(self):
            yield 1
            while 1:
                print "we loop forever", self.num
                yield 1
    ```

2.  Instantiate and activate a few (note these are two separate steps!):

    ``` {.literal-block}
    mp1=Loopy(1)
    mp1.activate()

    mp2=Loopy(2)
    mp2.activate()

    mp3=Loopy(3).activate()     # a more convenient shorthand
    ```

3.  If you haven\'t already, start the scheduler to cause them to be
    run. The call will return when all microprocesses have finished
    executing (which is *never* in this example case):

    ``` {.literal-block}
    >>> scheduler.run.runThreads()
    we loop forever 1
    we loop forever 2
    we loop forever 3
    we loop forever 1
    we loop forever 2
    we loop forever 3
    we loop forever 1
    we loop forever 2
    ... etc ...
    ```

Pause a microprocess whilst it is running by calling the pause() method.
Wake it up again by calling unpause(). Pausing a microprocess means that
it will cease to be executed until something else unpauses it. When
unpaused it picks up from where it left off.
:::

::: {.section}
[More detail]{#more-detail} {#47}
---------------------------

Essentially a microprocess provides a context for scheduling generators,
and treating them similar to processes/threads. It provides basic
facilities to support the activation (starting), pausing, unpausing and
termination of a generator.

To start a microprocess running, you must create it and then activate
it. Activation is a separate step to allow you to control exactly when
you want a microprocess to actually start running. Once activated,
running the scheduler will cause your generator to be executed along
with all other active microprocesses.

Every yield statement in your generator hands back control, allowing
Axon to schedule other microprocesses that may be running.

You can yield any value you like except zero or False (which are
reserved for future use).

When a microprocess finishes, the scheduler calls its
\_closeDownMicroprocess() method. You can either override this in your
subclass, or specify a closeDownValue when initialising microprocess.
The scheduler will act on the return value if it recognises it - see the
Scheduler module for more details.

::: {.section}
### [Alternative ways of defining the generator/thread]{#alternative-ways-of-defining-the-generator-thread} {#48}

Subclass microprocess and write your generator as a differently named
method, for example foo(), and to then specify the *name* of the
\"mainmethod\" when you ask the microproces to activate:

``` {.literal-block}
class MyMicroprocess(microprocess):
    def foo(self):
        yield 1
        while 1:
            print "we loop forever!"
            yield 1

mp = MyMicroprocess()
mp.activate(mainmethod="foo")
scheduler.run.runThreads()
```

Alternatively, you can instantiate a microprocess providing your own
generator:

``` {.literal-block}
def bar():
    yield 1
    while 1:
        print "we loop forever!"
        yield 1

mp = MyMicroprocess(thread=bar())
mp.activate()
scheduler.run.runThreads()
```

Note that this last approach removes the ability of the microprocess to
be prematurely stopped by calling its stop() method.
:::
:::

::: {.section}
[Microprocess lifecycle in detail]{#microprocess-lifecycle-in-detail} {#49}
---------------------------------------------------------------------

In terms of runtime a microprocess can be viewed to have 2 different
life cycles - that which an external user sees, and that which the
microprocess sees.

In terms of runtime life cycle viewed externally, a microprocess is
created, activated, and then has its next method repeatedly called until
a StopIteration exception is raised, at which point the microprocess is
deleted. In terms of a more traditional approach the next call
approximates to a timeslice being allocated to a process/thread.

The value returned by next() should be non-zero (reserved for future
use). The scheduler calling next() may also recognise some specific
values - see the
[Axon.Scheduler.scheduler](/Docs/Axon/Axon.Scheduler.scheduler.html){.reference}
class for more information.

The runtime life cycle from the view of the microprocess stems from the
fact that a generator wraps a thread of control, by effectively treating
the program counter like a static variable. The following describes this
runtime from the microprocess\'s point of view.

First the \'\_\_init\_\_\' function is called during initialisation at
object creation time. This results in a non-active, non-running
microprocess. Activation has been deliberately separated from creation
and initialisation. At some point in the future, the microprocess\'s
activate method is called, activating the object. When the object is
activated, an internal call to a \'\_microprocessGenerator\' occurs.
This function in fact results in the return object being a generator,
which can then have its next method called repeatedly. This generator is
then stored as an attribute of the microprocess class.

The following describe the flow of control the generator takes when the
generator is provided with a flow of control/time slice via it\'s next
method. Initially, it creates a local generator object - \'pc\' - by
calling the object\'s main method. (This allows the client of the
microprocess class to provide their own generator if they wish.) This is
necessary due to the fact that any function containing a \'yield\'
keyword is a generator - the \'yield\' keyword cannot be abstracted
away. Next, inside a loop, the microprocess calls the next() method of
its local generator object \'pc\' - effectively providing a time slice
to the user of the microprocess class. Any result provided by the
timeslice is then yielded (returned) to the client of the generator.
However if the microprocess has its stopped flag set, the microprocess
generator simply yields a null value, followed by stopping.

This all boils down to checking to see if the microprocess is not
stopped prior to running the body of a generator formed from the main
method of the class. The intent here is that users will inherit from the
microprocess class, and then reimplement the main method, which
periodically yields control. If the user/inheriting class does not
implement a main method, then the system provides a stub that simply
returns.

Pausing and unpausing of microprocesses has been delegated to the
scheduler to allow Axon systems to not consume CPU cycles when idle.
When a microprocess is paused the scheduler simply never calls its
next() method until it is unpaused. As such, calls to pause() and
unpause() are actually relayed to the scheduler.

The microprocess class uses a dummy scheduler \_NullScheduler until it
is actually activated. This is done so pause() and unpause() calls can
be silently absorbed whilst a microprocess is not yet active.

Essentially the microprocess provides a context for scheduling
generators, and treating them similar to processes/threads.

Clients are not expected to use the microprocess class itself directly -
they are expected to subclass the microprocess class. Subclasses do need
however to call the microprocess constructor. A minimal client class
could look like this:

``` {.literal-block}
from microprocess import microprocess
class automaton(microprocess):
    def __init__(self):
        self.Microprocess() # Call superclass constructor
    def main:
        while 1:
        yield 1
        print "Hello Again"
```

This microprocess would then be run by a wrapper as follows:

``` {.literal-block}
import microprocess, scheduler
s = scheduler.scheduler()
a = automaton()
a.activate()
s.runThreads()
```

The component class does this, and adds further facilities for
inter-microprocess communication. Likewise, the scheduler class
subclasses microprocess so that it can be scheduled in parallel with
other tasks.

As noted previously, every microprocess object has access to a debugger,
which is accessed via the local attribute self.debugger, which we shall
return to later. Likewise every microprocess object contains a reference
to a scheduler.
:::

::: {.section}
[Internal flags/state]{#internal-flags-state} {#50}
---------------------------------------------

-   **id** and **name** - unique identifiers. No other Axon entity will
    have the same name or id.
-   **init** - a flag indicating if the microprocess has been correctly
    initialised.
-   **stopped** - Indicates that the microprocess has run and since
    stopped.
-   **\_\_thread** - the generator object that gets executed whenever
    next() is called. Is actually an internally created generator that
    wraps the one created by the main() method.
-   **scheduler** - The scheduler that controls execution of this
    microprocess. When not yet activated a dummy scheduler
    (NullScheduler) is used instead.
-   **tracker** - The coordinating assistant tracker to be used by this
    microprocess.
-   **debugger** - A local debugging object. (See the debug class docs
    for more detail)

Note that the paused/awake state of a microprocess is something
maintained and managed by the scheduler; not the microprocess itself.
:::

Test documentation {#51}
==================

Tests passed:

-   Additional checks over the main overridden main checks to test
    pausing and stopping behaviour.
-   \_\_init\_\_ - Called with no arguments. Creates multiple
    microprocess objects with no arguments and checks they do not have
    matching ids.
-   After being stopped a microprocess returns true to \_isStopped and
    false to \_isRunnable.
-   test\_\_\_str\_\_ (\_\_main\_\_.MicroProcess\_Test)
-   Stub \_closeDownMicroprocess should always return 0
-   Tests the setting of the scheduler class to be used for a subclass
    of microprocess is actually reflected at activation
-   Tests the activation method operates as expected with a chosen
    scheduler
-   Tests that an overridden main is run correctly by repeatedly calling
    next() and that termination occurs at the proper time with the
    proper StopIteration exception.
-   After being paused a microprocess returns false to \_isRunnable.
    Also tests \_isRunnable and \_unpause.
-   Tests setting scheduler class and that the default scheduler is
    Scheduler.scheduler
-   test\_\_\_str\_\_ (test\_\_\_str\_\_.str\_Test)
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Microprocess](/Docs/Axon/Axon.Microprocess.html){.reference}.[\_NullScheduler](/Docs/Axon/Axon.Microprocess._NullScheduler.html){.reference}
======================================================================================================================================================================================

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

[Axon](/Docs/Axon/Axon.html){.reference}.[Microprocess](/Docs/Axon/Axon.Microprocess.html){.reference}.[microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}
=================================================================================================================================================================================

::: {.section}
class microprocess([Axon.Axon.AxonObject](/Docs/Axon/Axon.Axon.AxonObject.html){.reference}) {#symbol-microprocess}
--------------------------------------------------------------------------------------------

::: {.section}
microprocess(\[thread\]\[,closeDownValue\]) -\> new microprocess object

Creates a new microprocess object (not yet activated). You can
optionally specify an alternative generator to be used instead of the
one the microprocess would ordinarily create for itself.

Keyword arguments:

-   thread \-- None, or an alternative generator to be the thread of
    execution in this microprocess.
-   closeDownValue \-- Value to be returned when the microprocess has
    finished and \_closeDownMicroprocess() is called (default=0)
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, thread\]\[, closeDownValue\]\[, tag\])]{#symbol-microprocess.__init__}

Microprocess initialiser.

Subclasses must call this using the idiom super(TheClass,
self).\_\_init\_\_()
:::

::: {.section}
#### [\_\_str\_\_(self)]{#symbol-microprocess.__str__}

Standard function for rendering the object as a string.
:::

::: {.section}
#### [\_closeDownMicroprocess(self)]{#symbol-microprocess._closeDownMicroprocess}

Stub method that is overridden internally in Axon but not clients

Called by scheduler to ask microprocess to perform any desired shutdown
tasks. The scheduler also processes any IPC objects in the return value.
:::

::: {.section}
#### [\_isRunnable(self)]{#symbol-microprocess._isRunnable}

Returns True if the microprocess is active and awake, or paused.

This query is actually passed on to this microprocess\'s scheduler.
:::

::: {.section}
#### [\_isStopped(self)]{#symbol-microprocess._isStopped}

Returns True if this microprocess has been running but has since been
halted or terminated of its own accord. Otherwise returns False.
:::

::: {.section}
#### [\_microprocessGenerator(self, someobject\[, mainmethod\])]{#symbol-microprocess._microprocessGenerator}

This contains the mainloop for a microprocess, returning a generator
object. Creates the thread of control by calling the class\'s main
method, then in a loop repeatedly calls the resulting generator\'s next
method providing the object with time slices. After each time slice, the
\_microprocessGenerator yields control back to its caller.

Keyword arguments:

-   someobject \-- the object containing the main method (usually
    \'self\')
-   mainmethod \-- *name* of the method that is the generator to be run
    as the thread.
:::

::: {.section}
#### [\_unpause(self)]{#symbol-microprocess._unpause}

DEPRECATED - use M.unpause() instead
:::

::: {.section}
#### [activate(self\[, Scheduler\]\[, Tracker\]\[, mainmethod\])]{#symbol-microprocess.activate}

Call to activate this microprocess, so it can start to be executed by a
scheduler. Usual usage is to simply call x.activate()

You can optionally specify a specific scheduler or tracker to use
(instead of the defaults). You can also specify that a different method
is the \'main\' generator.

Keyword arguments:

-   Scheduler \-- None to use the default scheduler; or an alternate
    scheduler.
-   Tracker \-- None to use the default coordinating assistant tracker;
    or an alternative one.
-   mainmethod \-- Optional. The name of the \'main\' method of this
    microprocess (default=\"main\")
:::

::: {.section}
#### [main(self)]{#symbol-microprocess.main}

\'main\' thread of execution stub function. Client classes are expected
to override this.

Write your replacement as a generator (a method with \'yield\'
statements in it). \'Yield\' any non-zero values you like regularly to
hand control to the scheduler so other microprocesses can get a turn at
executing. Your code must therefore not block - eg. waiting on a system
call or event.

If you miss this off a class that directly subclass\'s microprocess,
your program will run, but it will not do what you want!
:::

::: {.section}
#### [next(self)]{#symbol-microprocess.next}

Calls next() of the internal generator - lets you drop a microprocess in
somewhere where you\'d ordinarily stick a generator.

Internally this calls self.\_\_thread.next() to pass the timeslice down
to the actual generator
:::

::: {.section}
#### [pause(self)]{#symbol-microprocess.pause}

Pauses the microprocess.

If done by the microprocess itself, the microprocess will pause at the
next point it \'yields\'.

Internally, the request is forwarded to this microprocesses scheduler.
:::

::: {.section}
#### [run(self)]{#symbol-microprocess.run}

run - starts the scheduler for this microprocess and runs it.

This is a convenient shortcut to activate and run this microprocess and
any other microprocesses that have already been activated (with the same
scheduler).
:::

::: {.section}
#### [stop(self)]{#symbol-microprocess.stop}

Halts the microprocess, no way to \"unstop\"
:::

::: {.section}
#### [unpause(self)]{#symbol-microprocess.unpause}

Un-pauses the microprocess.

This is provided to allow other microprocesses to \'wake up\' this one.
This can only be performed by an external microprocess - if you are
paused there is no way you can unpause yourself!

Does nothing if microprocess has been stopped.

Internally, the request is forwarded to this microprocess\'s scheduler.
:::
:::

::: {.section}
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
