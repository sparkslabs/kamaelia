---
pagename: Docs/Axon/Axon.Component.component
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Component](/Docs/Axon/Axon.Component.html){.reference}.[component](/Docs/Axon/Axon.Component.component.html){.reference}
------------------------------------------------------------------------------------------------------------------------------------------------------------------
:::

For examples and more explanations, see the [module level
docs.](/Docs/Axon/Axon.Component.html){.reference}

------------------------------------------------------------------------

::: {.section}
class component([Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}) {#symbol-component}
-------------------------------------------------------------------------------------------------------------

::: {.section}
Base class for an Axon component. Subclass to make your own.

A simple example:

``` {.literal-block}
class IncrementByN(Axon.Component.component):

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

            yield 1
```
:::

::: {.section}
### Methods defined here

::: {.section}
#### [Inbox(self\[, boxname\])]{#symbol-component.Inbox}
:::

::: {.section}
#### [\_\_addChild(self, child)]{#symbol-component.__addChild}

Register component as a child.

This takes a child component, and adds it to the children list of this
component. It also registers to be woken up by the child if it
terminates.

This has a number of effects internally, and includes registering the
component as capable of recieving and sending messages. It doesn\'t give
the child a thread of control however!

You will want to call this function if you create child components of
your component.
:::

::: {.section}
#### [\_\_init\_\_(self, \*args, \*\*argd)]{#symbol-component.__init__}

You want to overide this method locally.

You MUST remember to call the superconstructor for things to work
however. The way you do this is: super(YourClass,self).\_\_init\_\_()
:::

::: {.section}
#### [\_\_str\_\_(self)]{#symbol-component.__str__}

Provides a useful string representation of the component. You probably
want to override this, and append this description using something like:
\'component.\_\_str\_\_(self)\'
:::

::: {.section}
#### [\_closeDownMicroprocess(self)]{#symbol-component._closeDownMicroprocess}

Overrides original in microprocess class.

Ensures callbacks are deregistered, and all linkages created by this
component are destroyed.
:::

::: {.section}
#### [\_deliver(self, message\[, boxname\])]{#symbol-component._deliver}

For tests and debugging ONLY - delivers message to an inbox.
:::

::: {.section}
#### [addChildren(self, \*children)]{#symbol-component.addChildren}

Register the specified component(s) as children of this component

This component will be woken if any of its children terminate.

Note that any children still need to be activated!
:::

::: {.section}
#### [anyReady(self)]{#symbol-component.anyReady}

Returns true if *any* inbox has any data waiting in it.

Used by a component to check an inbox for ready data.

You are unlikely to want to override this method.
:::

::: {.section}
#### [childComponents(self)]{#symbol-component.childComponents}

Returns list of child components
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-component.closeDownComponent}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [dataReady(self\[, boxname\])]{#symbol-component.dataReady}

Returns true if data is available in the requested inbox.

Used by a component to check an inbox for ready data.

Call this method to periodically check whether you\'ve been sent any
messages to deal with!

You are unlikely to want to override this method.
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-component.initialiseComponent}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [link(self, source, sink, \*optionalargs, \*\*kwoptionalargs)]{#symbol-component.link}

Creates a linkage from one inbox/outbox to another.

\-- source - a tuple (component, boxname) of where the link should start
from \-- sink - a tuple (component, boxname) of where the link should go
to

Other optional arguments:

-   passthrough=0 - (the default) link goes from an outbox to an inbox
-   passthrough=1 - the link goes from an inbox to another inbox
-   passthrough=2 - the link goes from an outbox to another outbox

See
[Axon.Postoffice.postoffice.link](/Docs/Axon/Axon.Postoffice.postoffice.link.html){.reference}()
for more information.
:::

::: {.section}
#### [main(self)]{#symbol-component.main}

Override this method, writing your own main thread of control as a
generator. When the component is activated and the scheduler is running,
this what gets executed.

Write it as a python generator with regular yield statements returning a
non zero value.

If you do not override it, then a default main method exists instead
that will:

1.  Call self.initialiseComponent()
2.  Loop forever calling self.mainBody() yielding the return value each
    time until mainBody() returns a False/zero result.
3.  Call self.closeDownComponent()
:::

::: {.section}
#### [mainBody(self)]{#symbol-component.mainBody}

Stub method. **This method is designed to be overridden.**
:::

::: {.section}
#### [recv(self\[, boxname\])]{#symbol-component.recv}

returns the first piece of data in the requested inbox.

Used by a component to recieve a message from the outside world. All
comms goes via a named box/input queue

You will want to call this method to actually recieve messages you\'ve
been sent. You will want to check for new messages using dataReady first
though.

You are unlikely to want to override this method.
:::

::: {.section}
#### [removeChild(self, child)]{#symbol-component.removeChild}

Deregister component as a child.

Removes the child component, and deregisters it from notifying us when
it terminates. Also removes any linkages this component has made that
involve this child.

You probably want to do this when you enter a closedown state of some
kind for either your component, or the child component.
:::

::: {.section}
#### [send(self, message\[, boxname\])]{#symbol-component.send}

appends message to the requested outbox.

Used by a component to send a message to the outside world. All comms
goes via a named box/output queue.

You will want to call this method to send messages.

Raises
[Axon.AxonExceptions.noSpaceInBox](/Docs/Axon/Axon.AxonExceptions.noSpaceInBox.html){.reference}
if this outbox is linked to a destination inbox that is full.

You are unlikely to want to override this method.
:::

::: {.section}
#### [setInboxSize(self, boxname, size)]{#symbol-component.setInboxSize}

boxname - some boxname, must be an inbox ; size - maximum number of
items we\'re happy with
:::

::: {.section}
#### [unlink(self\[, thecomponent\]\[, thelinkage\])]{#symbol-component.unlink}

Destroys all linkages to/from the specified component or destroys the
specific linkage specified.

Only destroys linkage(s) that were created *by* this component itself.

Keyword arguments:

-   thecomponent \-- None or a component object
-   thelinkage \-- None or the linkage to remove

See
[Axon.Postoffice.postoffice.unlink](/Docs/Axon/Axon.Postoffice.postoffice.unlink.html){.reference}()
for more information.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [pause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.pause){.reference}(self)
-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
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
