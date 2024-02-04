---
pagename: Docs/Axon/Axon.Microprocess.microprocess
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Microprocess](/Docs/Axon/Axon.Microprocess.html){.reference}.[microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Microprocess.html){.reference}

------------------------------------------------------------------------

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
