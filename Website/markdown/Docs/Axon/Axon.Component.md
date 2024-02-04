---
pagename: Docs/Axon/Axon.Component
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Component](/Docs/Axon/Axon.Component.html){.reference}
------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Components - the basic building block
=====================================

::: {.container}
-   **class
    [component](/Docs/Axon/Axon.Component.component.html){.reference}**
:::

-   [The basics of writing a component](#18){.reference}
-   [Running a component](#19){.reference}
-   [Communicating with other components - creating
    linkages](#20){.reference}
-   [Child components](#21){.reference}
-   [Going to sleep (pausing)](#22){.reference}
-   [Old style main thread](#23){.reference}
-   [Internal Implementation](#24){.reference}
-   [Test documentation](#25){.reference}
:::

::: {.section}
A component is a microprocess with a microthread of control and
input/output queues (inboxes and outboxes) which can be connected by
linkages to other components. Ie. it has code that runs whilst the
component is active, and mechanisms for sending and receiving data to
and from other components.

-   A component is based on a microprocess - giving it its thread of
    execution.

There are other variants on the basic component:

-   [Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}
-   [Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}
-   [Axon.ThreadedComponent.threadedadaptivecommscomponent](/Docs/Axon/Axon.ThreadedComponent.threadedadaptivecommscomponent.html){.reference}

If your component needs to block - eg. wait on a system call; then make
it a \'threaded\' component. If it needs to change what inboxes or
outboxes it has at runtime, then make it an \'adaptive\' component.

::: {.section}
[The basics of writing a component]{#the-basics-of-writing-a-component} {#18}
-----------------------------------------------------------------------

Here\'s a simple example:

``` {.literal-block}
class MyComponent(Axon.Component.component):

    Inboxes = { "inbox"   : "Send the FOO objects to here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Emits BAA objects from here",
                 "signal" : "NOT USED",
               }

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                result = ... do something to msg ...
                self.send(result, "outbox")

            yield 1
```

Or, more specifically:

1.  **Subclass the component class**. Don\'t forget to call the
    superclass initializer if you write your own \_\_init\_\_ method:

    ``` {.literal-block}
    class MyComponent(Axon.Component.component):

        def __init__(self, myArgument, ...):
            super(MyComponent, self).__init__()
            ...
    ```

2.  **Declare any inboxes or outboxes you expect it to have** - do this
    as static members of the class called \"Inbox\" and \"Outbox\". They
    should be dictionaries where the key is the box name and the value
    serves as documentation describing what the box is for:

    ``` {.literal-block}
    Inboxes = { "inbox"   : "Send the FOO objects to here",
                "control" : "NOT USED",
              }
    Outboxes = { "outbox" : "Emits BAA objects from here",
                 "signal" : "NOT USED",
               }
    ```

    You can also do this as lists, but doing it as a dictionary with
    documentation values is much more useful to people wanting to use
    your component.

    If you don\'t specify any then you get the default \"inbox\" and
    \"control\" inboxes and \"outbox\" and \"signal\" outboxes.

3.  **Write the main() method** - it must be a generator - namely just
    like an ordinary method or function, but with \'yield\' statements
    regularly interspersed through it. This is the thread of execution
    in the component - just use yield statements regularly so other
    components get time to execute.

    If you need to know more, these might help you:

    -   [A tutorial on \"How to write
        components\"](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1113495151){.reference}
    -   [the Mini Axon
        tutorial](http://kamaelia.sourceforge.net/MiniAxon/){.reference}
    -   the
        [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference}
        class
:::

::: {.section}
[Running a component]{#running-a-component} {#19}
-------------------------------------------

Once you have written your component class; simply create instances and
activate them; then start the scheduler to begin execution:

``` {.literal-block}
x = MyComponent()
y = MyComponent()
z = AnotherComponent()
x.activate()
y.activate()
z.activate()

scheduler.run.runThreads()
```

If the scheduler is already running, then simply activating a component
will start it executing.
:::

::: {.section}
[Communicating with other components - creating linkages]{#communicating-with-other-components-creating-linkages} {#20}
-----------------------------------------------------------------------------------------------------------------

Components have inboxes and outboxes. The main() thread of execution in
a component communicates with others by picking up messages that arrive
in its inboxes and sending out messages to its outboxes. For example
here is a simple block of code for the main() method of a component that
echoes anything it receives to the console and also sends it on:

``` {.literal-block}
if self.dataReady("inbox"):
    msg = self.recv("inbox")
    print str(msg)
    self.send(msg,"outbox")

yield 1
```

Use the dataReady() method to find out if there is (one or more items
of) data waiting at the inbox you name. recv() lets you collect a
message from an inbox. Use the send() method to send a message to the
outbox you name. There is also an anyReady() method that will tell you
if *any* inbox has data waiting in it.

A message gets from one component\'s outbox to another one\'s inbox if
there is a linkage between them (going from the outbox to the inbox). A
component can create and destroy linkages by using the link() and
unlink() methods.

For example, we could create a linkage from a component\'s outbox called
\"outbox\" to a different component\'s inbox called \"inbox\":

``` {.literal-block}
theLink = self.link( (self, "outbox"), (otherComponent, "inbox") )
```

Using the handle that we were given, we can destroy that linkage later:

``` {.literal-block}
self.unlink(theLinkage = theLink)
```

Linkages normally go from an outbox to an inbox - after all the whole
idea is to get messages that one component sends to its own outbox to
arrive at another component\'s inbox. However you can also create
\'passthrough\' linkages from an inbox to another inbox; or from an
outbox to another outbox.

This is particularly useful if you want to encapsulate a child component
- hide it from view so other components only need to be wired up to you.

For example, your component may want any data being sent to one of its
inboxes to be forwarded automatically onto an inbox on the child. This
is a type \'1\' passthrough linkage:

``` {.literal-block}
thelink = self.link( (self,"inbox"), (myChild,"inbox"), passthrough=1 )
```

Or if you want anything a child sends to its outbox to be sent out of
one of your own outboxes, which is a type \'2\' passthrough:

``` {.literal-block}
thelink = self.link( (myChild,"outbox"), (self,"outbox"), passthrough=2 )
```

The alternative, of course, is to add extra inboxes and outboxes to
communicate with the child, and to write a main() method that simply
passes the data on. Passthrough linkages are more efficient and quicker
to code!

There is no performance penalty for delivering a message along a such a
chain of linkages (eg. outbox \-\--\> outbox \-\--\> inbox \-\--\> inbox
\-\--\> inbox). Axon resolves the chain and delivers straight to the
final destination inbox!
:::

::: {.section}
[Child components]{#child-components} {#21}
-------------------------------------

Components can create and activate other components. They can adopt them
as children:

``` {.literal-block}
newComponent = FooComponent()
self.addChildren(newComponent)
newComponent.activate()
```

Making a component your child means that:

-   you will be woken (if asleep) when your child terminates
-   the removeChild() method provides a convenient way to make sure any
    linkages you have made involving that child are destroyed.
-   calling childComponents() lists all children you currently have

Whether another component is your child or not, you can tell if it has
terminated yet by calling its \_isStopped() method.

For example, a component might want to create a child component, make a
linkage to it then wait until that child terminates before cleaning it
up. Achieve this by writing code like this in the main() body of the
component:

``` {.literal-block}
src = RateControlledFileReader("myTextFile",readmode="lines")
dst = ConsoleEchoer()

lnk = self.link( (src,"outbox"), (dst,"inbox") )

self.addChildren(src,dst)    # we will be woken if they terminate
src.activate()
dst.activate()

while not dst._isStopped() and not src._isStopped():
    self.pause()
    yield 1

self.unlink(thelinkage = lnk)
self.removeChild(src)
self.removeChild(dst)
```
:::

::: {.section}
[Going to sleep (pausing)]{#going-to-sleep-pausing} {#22}
---------------------------------------------------

When a component has nothing to do it can pause. This means it will not
be executed again until it is woken up. Pausing is a good thing since it
relinquishes cpu time for other parts of the system instead of just
wasting it.

**When would you want to pause?** - usually when there is nothing left
waiting in any of your inboxes and there is nothing else for your
component to do:

``` {.literal-block}
class Echoer(Axon.Component.component):

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                print str(msg)
                self.send(msg,"outbox")

            if not self.anyReady():
                self.pause()

            yield 1
```

Calling the pause() method means that *at the next yield statement* your
component will be put to sleep. It doesn\'t happen as soon as you call
pause() - only when execution reaches the next `yield`{.docutils
.literal}.

**What will wake up a paused component?** - any of the following:

-   a message arriving at any inbox (even one with messages already
    waiting in it)
-   a message being collected from an inbox that is linked to one of our
    outboxes
-   a child component terminating

Your component *cannot* wake itself up - only the actions of other
components can cause it to be woken. Why? You try writing some code that
stops executing (pauses) yet can issue a method call to ask to be woken!
:-)
:::

::: {.section}
[Old style main thread]{#old-style-main-thread} {#23}
-----------------------------------------------

Components also currently support an \'old\' style for writing their
main thread of execution.

**This way of writing components is likely to be deprecated in the near
future. We suggest you write a main() method as a generator instead.**

To do old-style; instead of writing a generator you write 3 functions -
one for initialisation, main execution and termination. The thread of
execution for the component is therefore effectively this:

``` {.literal-block}
self.initialiseComponent()

while 1:
    result = self.mainBody()
    if not result:
        break

self.closeDownComponent()
```

initialiseComponent() is called once when the component first starts to
execute.

mainBody() is called every execution cycle whilst it returns a non zero
value. If it returns a zero value then the component starts to shut
down.

closeDownComponent() is called when the component is about to shut down.

A simple echo component might look like this:

``` {.literal-block}
class EchoComponent(Axon.Component.component):

    def initialiseComponent(self):
        # We can perform pre-loop initialisation here!
        # In this case there is nothing really to do
        return 1

    def mainBody(self):
        # We're now in the main loop
        if self.dataReady("inbox"):
            msg = self.recv("inbox")
            print msg
            self.send(msg,"outbox")

        if not self.anyReady():
            self.pause()

        # If we wanted to exit the loop, we return a false value
        # at the end of this function
        # If we want to continue round, we return a true, non-None,
        # value. This component is set to run & run...
        return 1

  def closeDownComponent(self):
        # We can't get here since mainLoop above always returns true
        # If it returned false however, we would get sent here for
        # shutdown code.
        # After executing this, the component stops execution
        return
```
:::

::: {.section}
[Internal Implementation]{#internal-implementation} {#24}
---------------------------------------------------

Component is a subclass of microprocess (from which it inherits the
ability to have a thread of execution). It includes its own postoffice
object for creating and destroying linkages. It has a collection of
inboxes and outboxes.

Attributes:

-   **Inboxes** and **Outboxes** - static members defining the list of
    names for inboxes and outboxes a component should be given when it
    is created.
-   **inboxes** and **outboxes** - the actual collections of inboxes and
    outboxes that are set up when the component is initialised.
    Implemented as dictionaries mapping names to the postbox objects.
-   **postoffice** - a postoffice object, used to create, destroy and
    manage linkages.
-   **children** - list of components registered as children of this
    component.
-   **\_callOnCloseDown** - list of callback functions to be called when
    this component terminates. Used to notify parents of children that
    their child has terminated.
:::

Test documentation {#25}
==================

Tests passed:

-   \_\_init\_\_ - Class constructor is expected to be called without
    arguments.
-   \_\_addChild - Registers the component as a child of the component.
    Internal function. ttbw
-   \_\_str\_\_ - Returns a string that contains the fact that it is a
    component object and the name of it.
-   \_\_str\_\_ - Returns a string representation of the component-
    consisting of Component,representation of inboxes, representation of
    outboxes.
-   \_closeDownMicroprocess - Checks the message returned is None (no
    knockons).
-   \_closeDownMicroprocess - Returns a shutdownMicroprocess. Internal
    Function.
-   addChildren - All arguments are added as child components of the
    component.
-   childComponents - Returns the list of children components of this
    component.
-   closeDownComponent - stub method, returns 1, expected to be
    overridden by clients.
-   dataReady - Returns true if the supplied inbox has data ready for
    processing.
-   initialiseComponent - Stub method, returns 1, expected to be
    overridden by clients.
-   link - Creates a link, handled by the component\'s postoffice, that
    links a source component to it\'s sink, honouring passthrough,
    pipewidth and synchronous attributes.
-   The \_closeDownMicroprocess method ensures any linkages the
    component has made that still exist are removed.
-   mainBody - stub method, returns None, expected to be overridden by
    clients as the main loop.
-   main - This ensures that the closeDownComponent method is called at
    the end of the loop. It also repeats the above test.
-   main - Returns a generator that implements the documented behaviour
    of a highly simplistic approach component statemachine.
-   recv - Takes the first item available off the specified inbox, and
    returns it.
-   removeChild - Removes the specified component from the set of child
    components and deregisters it from the postoffice.
-   send - Takes the message and places it into the specified outbox.
-   In a chain of linkages, all owners of outboxes are notified when a
    message is picked up.
-   In a chain of linkages with more than one inbox, only the final
    destination is woken when a message is sent.
-   In a chain of linkages, only the owners of outboxes are notified
    when a message is picked up.
-   A paused component is unpaused when a message is delivered to its
    inbox.
-   If the linkage chain breaks before a message is collected, the
    owners of outboxes that are no longer in the chain are not notified.
-   If a message is sent, then a new linkage added before a message is
    collected, the owner of the newly linked in outbox will notified
    too.
-   If the linkage chain breaks and is then re-established before a
    message is collected, the owners of outboxes that are no longer in
    the chain are not notified, but ones that are will be.
-   A paused component stays paused if nothing happens
-   A paused component is not unpaused when it sends a message.
-   A paused component is unpaused when a consumer picks up a message it
    has sent.
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Component](/Docs/Axon/Axon.Component.html){.reference}.[component](/Docs/Axon/Axon.Component.component.html){.reference}
==================================================================================================================================================================

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
