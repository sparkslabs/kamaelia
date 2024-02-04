---
pagename: Docs/Axon/Axon.ThreadedComponent.threadedcomponent
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[ThreadedComponent](/Docs/Axon/Axon.ThreadedComponent.html){.reference}.[threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.ThreadedComponent.html){.reference}

------------------------------------------------------------------------

::: {.section}
class threadedcomponent([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-threadedcomponent}
---------------------------------------------------------------------------------------------------------

::: {.section}
threadedcomponent(\[queuelengths\]) -\> new threadedcomponent

Base class for a version of an Axon component that runs main() in a
separate thread (meaning it can, for example, block). Subclass to make
your own.

Internal queues buffer data between the thread and the Axon inboxes and
outboxes of the component. Set the default queue length at
initialisation (default=1000).

A simple example:

``` {.literal-block}
class IncrementByN(Axon.ThreadedComponent.threadedcomponent):

    Inboxes = { "inbox" : "Send numbers here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Incremented numbers come out here",
                 "signal" : "NOT USED",
               }

    def __init__(self, N):
        super(IncrementByN,self).__init__()
        self.n = N

    def main(self):
        while 1:
            while self.dataReady("inbox"):
                value = self.recv("inbox")
                value = value + self.n
                self.send(value,"outbox")

            if not self.anyReady():
                self.pause()
```
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, queuelengths, \*\*argd)]{#symbol-threadedcomponent.__init__}
:::

::: {.section}
#### [\_do\_threadsafe(self, cmd, argL, argD)]{#symbol-threadedcomponent._do_threadsafe}

Internal method for ensuring a method call takes place in the main
scheduler\'s thread.
:::

::: {.section}
#### [\_handlemessagefromthread(self, msg)]{#symbol-threadedcomponent._handlemessagefromthread}

Unpacks a message containing a request to run a method of the form
(objectToCall, argList, argDict) then calls it and places the result in
the axontothreadqueue queue.

Used to execute methods on behalf of the separate thread. Results are
returned to it via the return queue.
:::

::: {.section}
#### [\_localmain(self)]{#symbol-threadedcomponent._localmain}

Do not overide this unless you reimplement the pass through of the boxes
to the threads, and state management.
:::

::: {.section}
#### [\_threadmain(self)]{#symbol-threadedcomponent._threadmain}

Exception trapping wrapper for main().

Runs in the separate thread. Catches any raised exceptions and attempts
to pass them back to \_localmain() to be re-raised.
:::

::: {.section}
#### [activate(self\[, Scheduler\]\[, Tracker\]\[, mainmethod\])]{#symbol-threadedcomponent.activate}

Call to activate this microprocess, so it can start to be executed by a
scheduler. Usual usage is to simply call x.activate().

See
[Axon.Microprocess.microprocess.activate](/Docs/Axon/Axon.Microprocess.microprocess.activate.html){.reference}()
for more info.
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-threadedcomponent.closeDownComponent}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [dataReady(self\[, boxname\])]{#symbol-threadedcomponent.dataReady}

Returns true if data is available in the requested inbox.

Used by the main() method of a component to check an inbox for ready
data.

Call this method to periodically check whether you\'ve been sent any
messages to deal with!

You are unlikely to want to override this method.
:::

::: {.section}
#### [forwardInboxToThread(self, box)]{#symbol-threadedcomponent.forwardInboxToThread}
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-threadedcomponent.initialiseComponent}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [link(self, source, sink\[, passthrough\])]{#symbol-threadedcomponent.link}

Creates a linkage from one inbox/outbox to another.

\-- source - a tuple (component, boxname) of where the link should start
from \-- sink - a tuple (component, boxname) of where the link should go
to

Other optional arguments:

-   passthrough=0 - (the default) link goes from an outbox to an inbox
-   passthrough=1 - the link goes from an inbox to another inbox
-   passthrough=2 - the link goes from an outbox to another outbox

See Axon.Postoffice.link(\...) for more information.
:::

::: {.section}
#### [main(self)]{#symbol-threadedcomponent.main}

Override this method, writing your own main thread of control as an
ordinary method. When the component is activated and the scheduler is
running, this what gets executed.

Write it as an ordinary method. Because it is run in a separate thread,
it can block.

If you do not override it, then a default main method exists instead
that will:

1.  Call self.initialiseComponent()
2.  Loop forever calling self.mainBody() repeatedly until mainBody()
    returns a False/zero result.
3.  Call self.closeDownComponent()
:::

::: {.section}
#### [mainBody(self)]{#symbol-threadedcomponent.mainBody}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [pause(self\[, timeout\])]{#symbol-threadedcomponent.pause}

Pauses the thread and blocks - does not return until the something
happens to re-awake it, or until it times out (if the optional timeout
is specified)

Must only be called from within the main() method - ie. from within the
separate thread.

Keyword arguments:

-   timeout \-- Optional. None, or the number of seconds after which
    this call should unblock itself (default=None)
:::

::: {.section}
#### [recv(self\[, boxname\])]{#symbol-threadedcomponent.recv}

returns the first piece of data in the requested inbox.

Used by the main() method to recieve a message from the outside world.
All comms goes via a named box/input queue

You will want to call this method to actually recieve messages you\'ve
been sent. You will want to check for new messages using dataReady first
though.

You are unlikely to want to override this method.
:::

::: {.section}
#### [send(self, message\[, boxname\])]{#symbol-threadedcomponent.send}

appends message to the requested outbox.

Used by the main() method to send a message to the outside world. All
comms goes via a named box/output queue

You will want to call this method to send messages.

Raises
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
if this outbox is linked to a destination inbox that is full, or if your
component is producing messages faster than Axon can pass them on.

You are unlikely to want to override this method.
:::

::: {.section}
#### [sync(self)]{#symbol-threadedcomponent.sync}

Call this from main() to synchronise with the main scheduler\'s thread.

You may wish to do this to throttle your component\'s behaviour This is
akin to posix.sched\_yield or shoving extra \"yield\" statements into a
component\'s generator.
:::

::: {.section}
#### [unlink(self\[, thecomponent\]\[, thelinkage\])]{#symbol-threadedcomponent.unlink}

Destroys all linkages to/from the specified component or destroys the
specific linkage specified.

Only destroys linkage(s) that were created *by* this component itself.

Keyword arguments:

-   thecomponent \-- None or a component object
-   thelinakge \-- None or the linkage to remove
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [\_deliver](/Docs/Axon/Axon.Component.html#symbol-component._deliver){.reference}(self,
    message\[, boxname\])
-   [removeChild](/Docs/Axon/Axon.Component.html#symbol-component.removeChild){.reference}(self,
    child)
-   [Inbox](/Docs/Axon/Axon.Component.html#symbol-component.Inbox){.reference}(self\[,
    boxname\])
-   [addChildren](/Docs/Axon/Axon.Component.html#symbol-component.addChildren){.reference}(self,
    \*children)
:::

::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
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
