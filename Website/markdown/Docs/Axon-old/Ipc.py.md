---
pagename: Docs/Axon-old/Ipc.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Ipc.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

\...

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

Class hierarchy

[\_\_builtin\_\_.object]{style="font-family:Courier 10 Pitch"}

[ipc]{style="font-family:Courier 10 Pitch"} - Message base class

[errorInformation]{style="font-family:Courier 10 Pitch"} - A message to
indicate that a non fatal error has occured in the component. It may
skip processing errored data but should respond correctly to future
messages.

-   \_\_init\_\_(self, caller, exception=None, message=None)

[newComponent]{style="font-family:Courier 10 Pitch"} - Message used to
inform the scheduler of a new component that needs a thread of control
and activating

-   \_\_init\_\_(self, \*components)
-   components(self)

[notify]{style="font-family:Courier 10 Pitch"} - Message used to notify
the system of an event

-   \_\_init\_\_(self, caller, payload)

[producerFinished]{style="font-family:Courier 10 Pitch"} - Message to
indicate that the producer has completed its work and will produce no
more output.

-   \_\_init\_\_(self, caller=None, message=None)

[shutdownMicroprocess]{style="font-family:Courier 10 Pitch"} -

-   \_\_init\_\_(self, \*microprocesses)
-   microprocesses(self)

[status]{style="font-family:Courier 10 Pitch"} - General Status message

-   \_\_init\_\_(self, status)
-   status(self)

[wouldblock]{style="font-family:Courier 10 Pitch"} - Message used to
indicate to the scheduler that the system is likely to block now, why,
and reasons to awaken the system

-   \_\_init\_\_(self, caller)

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[errorInformation.\_\_init\_\_]{style="font-weight:600"}

-   An exception & message (any object) in addition to the caller to
    provide a more meaningful errorInformation message where
    appropriate. ttbw
-   Called without arguments fails - must include caller.
-   Takes the supplied caller, and creates an errorInformation object.
    Checks errorInformation object is an instance of ipc.

[ipc]{style="font-weight:600"}

-   Should be derived from object.

[newComponent.\_\_init\_\_]{style="font-weight:600"}

-   Groups all the arguments as a tuple of components that need to be
    activated/added to the run queue. Order is unimportant, scheduler
    doesn\'t care.
-   Should work without problems.

[newComponent.components]{style="font-weight:600"}

-   Returns a tuple of components that need to be added to the run
    queue/activated. Same test as for \_\_init\_\_ as they are
    counterparts.

[notify.\_\_init\_\_]{style="font-weight:600"}

-   Called without arguments fails.
-   Creates a message from a specific caller with some data payload to
    notify part of the system of an event.

[producerFinished.\_\_init\_\_]{style="font-weight:600"}

-   Called without arguments defaults to a caller of None, message of
    None. Checks producerFinished is a subclass of ipc

[shutdownMicroprocess.\_\_init\_\_]{style="font-weight:600"}

-   Should work without problems.
-   Treats all the arguments as a tuple of microprocesses that need to
    be shutdown. \<br\>

[shutdownMicroprocess.microprocesses]{style="font-weight:600"}

-   Returns the list of microprocesses that need to be shutdown. This is
    essentially the counterpart to the \_\_init\_\_ test.

[status.\_\_init\_\_]{style="font-weight:600"}

-   Called without arguments fails.
-   Stores the status message - for extraction by the recipient of the
    message. Checks object is instance of ipc.

[status.status]{style="font-weight:600"}

-   Returns the status message stored inside the status object.
    Counterpart to \_\_init\_\_ test.

[test\_SmokeTest.\_\_init\_\_]{style="font-weight:600"}

-   Creates a producerFinished message with specified caller & shutdown
    \'last\' message.

[wouldblock.\_\_init\_\_]{style="font-weight:600"}

-   Called without arguments fails.
-   Stores the caller in the wouldblock message. Allows the scheduler to
    make a decision. Checks wouldblock is a subclass of ipc.

Michael, December 2004
