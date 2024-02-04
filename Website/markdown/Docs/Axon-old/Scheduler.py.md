---
pagename: Docs/Axon-old/Scheduler.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Scheduler.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

[TODO: ]{style="font-weight:600"}Needs better test suite

You provide the scheduler with microthreads of microprocesses, and it
runs them, clean and simple. This is usually handled by the component
system via returning a newComponent value. An alternative is to call the
component\'s activate method.

It also has a slow motion mode designed to help with debugging &
testing.

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class scheduler(Axon.Microprocess.microprocess)

Method resolution order:

-   scheduler
-   Axon.Microprocess.microprocess
-   Axon.Axon.AxonObject
-   \_\_builtin\_\_.object

Data and other attributes defined here:

-   run = \<Axon.Scheduler.scheduler object\> - this is the default
    scheduler

Methods defined here:

[\_\_init\_\_(self)]{style="font-weight:600"}

Creates a scheduler object. If scheduler.run has not been set, sets it.
Class initialisation ensures that this object/class attribute is
initialised - client modules always have access to a standalone
scheduler.\
Internal attributes:

-   time = time when this object was last active.
-   threads = list of threads to run.

<div>

Whilst there can be more than one scheduler active in the general case
you will NOT want to create a custom scheduler.

</div>

[main(self, slowmo=0)]{style="font-weight:600"}

This is the meat of the scheduler - this actively loops round the
threads that it has available to run, and runs them. The only control
over the scheduler at present is a means to slow it down - ie run in
slow motion.

<div>

The way this is run is as follows:

</div>

<div>

</div>

<div>

where delay is in seconds. If the delay is 0, the the system runs all
the threads as fast as it can. If the delay is non zero - eg 0.5, then
the system runs all the threads for one \"cycle\", waits until the delay
has passed, and then times again. Note : the delay is between the start
points of cycles, and not between the start and end points of cycles.
The delay is NOT 100% accurate nor guaranteed and can be extended by
threads that take too long to complete. (Think of it as a \"hello
world\" of soft-real time scheduling)

</div>

[runThreads(self, slowmo=0)]{style="font-weight:600"}

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

Needs major work. (See todo above!)

Michael, December 2004
