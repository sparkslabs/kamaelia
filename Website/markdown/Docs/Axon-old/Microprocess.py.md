---
pagename: Docs/Axon-old/Microprocess.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Microprocess.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

[TODO: ]{style="font-weight:600"}Test suite needs changing to emit API
docs (which is why testdocs below look odd)

A microprocess is a class supporting parallel execution, provided by
forming a wrapper around a generator. It also provides a place for
context to be stored about the generator. In terms of runtime a
microprocess can be viewed to have 2 different life cycles - that which
an external user sees, and that which the microprocess sees.

In terms of runtime life cycle viewed externally, a microprocess is
created, activated, and then has its next method repeatedly called until
a false value is returned, at which point the microprocess is deleted.
In terms of a more traditional approach the next call approximates to a
timeslice being allocated to a process/thread.

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
away. Next, inside a loop, the microprocess checks to see if it is
runnable. If the microprocess is runnable, the local generator object
\'pc\' has it\'s next method called - effectively providing a time slice
to the user of the microprocess class. Any result provided by the
timeslice is then yielded (returned) to the client of the generator.
After this, if the microprocess has its stopped flag set, the
microprocess generator simply yields a null value, followed by stopping.

This all boils down to checking to see if the microprocess is not
stopped and runnable prior to running the body of a generator formed
from the main method of the class. The intent here is that users will
inherit from the microprocess class, and then reimplement the main
method, which periodically yields control. If the user/inheriting class
does not implement a main method, then the system provides a stub that
simply returns.

Essentially the microprocess provides a context for scheduling
generators, and treating them similar to processes/threads.

Clients are not expected to use the microprocess class itself directly -
they are expected to subclass the microprocess class. Subclasses do need
however to call the microprocess constructor. A minimal client class
could look like this:

<div>

[class]{style="font-family:Courier 10 Pitch;font-weight:600"}[
automaton(microprocess):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
\_\_init\_\_(self):]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[def]{style="font-family:Courier 10 Pitch;font-weight:600"}[
main:]{style="font-family:Courier 10 Pitch"}

</div>

<div>

[while]{style="font-family:Courier 10 Pitch;font-weight:600"}[
1:]{style="font-family:Courier 10 Pitch"}

</div>

This microprocess would then be run by a wrapper as follows:

The component class does this, and adds further facilities for
inter-microprocess communication. Likewise, the postman class subclasses
microprocess so that it can be scheduled in parallel with other tasks.

As noted previously, every microprocess object has access to a debugger,
which is accessed via the local attribute self.debugger, which we shall
return to later. Likewise every microprocess object contains a reference
to a scheduler.

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

[\_\_init\_\_(self)]{style="font-weight:600"}

-   Microprocess constructor. Subclasses must call this using the idiom
    self.\_\_super.\_\_init\_\_()

[\_\_str\_\_(self)]{style="font-weight:600"}

-   Standard function for rendering the object as a string.

[activate(self, Scheduler=None, Tracker=None)]{style="font-weight:600"}

-   calls the \_microprocessGenerator function to create a generator
    object, places this into the thread attribute of the microprocess
    and appends the component to the scheduler\'s run queue.

[main(self)]{style="font-weight:600"}

-   \'M.main()\' - stub function. Client classes are expected to
    override this. If you miss this off a class that directly
    subclass\'s microprocess, your program will run, but it will not do
    what you want!

[next(self)]{style="font-weight:600"}

-   M.next() - This is to provide a microprocess object with the ability
    to be dropped in largely wherever a generator object can be put.
    Internally this calls self.thread.next() to pass the timeslice down
    to the actual generator.

[pause(self)]{style="font-weight:600"}

-   \'M.pause()\' - Pauses the microprocess.S ets the runnable flag to
    false - thus pausing the microprocess.

[stop(self)]{style="font-weight:600"}

-   \'M.stop()\' -
-   Halts the microprocess, no way to \"unstop\"

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

\_\_init\_\_ - Called with no arguments. Creates multiple microprocess
objects with no arguments and checks they do not have matching ids.

Tests that after being stopped a microprocess returns true to
\_isStopped and false to \_isRunnable.

test\_\_\_str\_\_ (\_\_main\_\_.MicroProcess\_Test)

\_activityCreator should return False as the basic microprocess does not
inititate any usefule work.

Stub \_closeDownMicroprocess should always return 0

Tests the setting of the scheduler class to be used for a subclass of
microprocess is actually reflected at activation

Tests the activation method operates as expected with a chosen scheduler

Tests that an overridden main is run correctly by repeatedly calling
next() and that termination occurs at the proper time with the proper
StopIteration exception.

Tests that after being pause a microprocess returns false to
\_isRunnable. Also tests \_isRunnable and \_unpause.

Tests setting scheduler class and that the default scheduler is
Scheduler.scheduler

test\_\_\_str\_\_ (test\_\_\_str\_\_.str\_Test)

Michael, December 2004
