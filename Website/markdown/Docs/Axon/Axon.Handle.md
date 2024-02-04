---
pagename: Docs/Axon/Axon.Handle
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Handle](/Docs/Axon/Axon.Handle.html){.reference}
------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Communicating with components from non Axon code
================================================

::: {.container}
-   **class [Handle](/Docs/Axon/Axon.Handle.Handle.html){.reference}**
:::

-   [Still Experimental](#11){.reference}
-   [Example Usage](#12){.reference}
-   [Behaviour](#13){.reference}
-   [Limitations](#14){.reference}
    -   [Limited to standard inboxes and outboxes](#15){.reference}
    -   [CPU Usage](#16){.reference}
-   [Design rationale and history](#17){.reference}
:::

::: {.section}
The Handle component wraps another component and allows data to be sent
to and received from its standard inboxes (\"inbox\" and \"control\")
and standard outboxes (\"outbox\" and \"signal\"). It provides this via
thread safe, non-blocking get() and put() methods.

This is particularly useful in combination with
[Axon.background](/Docs/Axon/Axon.background.html){.reference} -
allowing communication with components running in the background of a
non Axon based piece of code.

::: {.section}
[Still Experimental]{#still-experimental} {#11}
-----------------------------------------

This code is currently experimental - we\'d welcome reports of any
issues you may encounter when using this code.
:::

::: {.section}
[Example Usage]{#example-usage} {#12}
-------------------------------

Here, Axon/Kamaelia is used to connect to a server then receive text,
chunking it into individual lines. This is done by using Axon in the
background (since other code in this hypothetical system is not Axon
based).

NOTE: To see how this could be done without using
[Axon.Handle](/Docs/Axon/Axon.Handle.html){.reference}, see the examples
in the documentation for
[Axon.background](/Docs/Axon/Axon.background.html){.reference}.

1.  We create a background object and call its start() method:

    ``` {.literal-block}
    from Axon.background import background

    background().start()
    ```

2.  We create and activate our Kamaelia pipeline of components, wrapped
    in an instance of the Handle class:

    ``` {.literal-block}
    from Axon.Handle import Handle
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Visualisation.PhysicsGraph import chunks_to_lines

    queue = Queue()

    connection = Handle(
        Pipeline(
            TCPClient("my.server.com", 1234),
            chunks_to_lines()
        )
    ).activate()
    ```

We can now fetch items of data when they arrive, using the Handle, from
the \"outbox\" outbox of the pipeline:

``` {.literal-block}
from Queue import Empty

while 1:
   try:
       received_line = connection.get("outbox")
       print "Received line:", received_line
   except Empty:
       # no data yet
       time.sleep(0.1)
```

We can also send data, back to the server, by sending it to the
\"inbox\" inbox of the pipeline:

``` {.literal-block}
connection.put("Bytes to send to server\n", "inbox")
```
:::

::: {.section}
[Behaviour]{#behaviour} {#13}
-----------------------

Handle is a threaded component. It does not have the standard inboxes
(\"inbox\" and \"control\") or standard outboxes (\"outbox\" and
\"signal\"). The only way to communicate with Handle is via its get()
and put() methods.

Instantiate Handle, passing it a component to wrap. Upon activation,
Handle automatically wires inboxes and outboxes of its own to the
\"inbox\" and \"control\" inboxes and \"outbox\" and \"signal\" outboxes
of the component it is wrapping. Handle then activates the wrapped
component.

To send data to the wrapped component\'s \"inbox\" or \"control\"
inboxes, call the put() method, specifying, as arguments, the item of
data and the name of the inbox it is destined for. The data is queued
and sent at the next opportunity.

To retrieve data sent out by the wrapped component\'s \"outbox\" or
\"signal\" outboxes, call the get() method, specifying, as an argument,
the name of the outbox in question. This method is *non blocking* - if
there is data waiting, then the oldest item of data is returned,
otherwise a Queue.Empty exception is immediately thrown.

When the wrapped component terminates, Handle will immediately
terminate. Handle does not respond to shutdown messages received from
the wrapped component. Handle cannot be sent shutdown messages since it
has no \"control\" inbox on which to receive them.
:::

::: {.section}
[Limitations]{#limitations} {#14}
---------------------------

::: {.section}
### [Limited to standard inboxes and outboxes]{#limited-to-standard-inboxes-and-outboxes} {#15}

Handle currently only provides access to the standard \"inbox\" and
\"control\" inboxes and standard \"outbox\" and \"signal\" outboxes of
the component it wraps.

If access is required to a different inbox or outbox, try wrapping the
component within a Kamaelia.Chassis.Graphline component and specifying
linkages to connect the inbox or outbox in question to one of the
standard inboxes or outboxes of the Graphline.
:::

::: {.section}
### [CPU Usage]{#cpu-usage} {#16}

The current implememntation of Handle involves a degree of polling.
However it does use a slight (approximately 1 centisecond) delay between
pollings.

Therefore when idle, CPU usage of this component will be slightly
greater than zero.
:::
:::

::: {.section}
[Design rationale and history]{#design-rationale-and-history} {#17}
-------------------------------------------------------------

This component is the successor to the earlier \"likefile\" component.
Likefile suffered from some design issues that resulted in occassional
race conditions.

We dropped the name \"LikeFile\" since whilst it derives from the
concept of a file handle, it doesn\'t use the same API as file() for
some good reasons we\'ll come back to.

A file handle is an opaque thing that you can .write() data to, and
.read() data from. This is a very simple concept and belies a huge
amount of parallel activity happening concurrently to your application.
The file system is taking your data and typically buffering it into
blocks. Those blocks then may need padding, and depending on the file
system, may actually be written immediately to the end of a cyclone
buffer in a journal with some write operations. Then periodically those
buffers get flushed to the actual disk.

Based on the fact that file handles are a very natural thing for people
to work with, based on their ubiquity, and the fact that it masks the
fact you\'re accessing a concurrent system from a linear one, that\'s
why we\'ve taken this approach for integrating Kamaelia components
(which are naturally parallel) with non-Kamaelia code, which is
typically not parallel.

For simplicity of implementation, initially the implementation of Handle
supports only the equivalent of non-blocking file handles. This has two
implications:

-   Reading data from a Handle may fail, since there may not be any
    ready yet. This is chosen in preference to a blocking operation
-   Writing data to a Handle may also fail, since the component may not
    actually be ready to receive data from us.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Handle](/Docs/Axon/Axon.Handle.html){.reference}.[Handle](/Docs/Axon/Axon.Handle.Handle.html){.reference}
===================================================================================================================================================

::: {.section}
class Handle([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-Handle}
------------------------------------------------------------------------------------------------------------------------------

::: {.section}
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self, someComponent)]{#symbol-Handle.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_get(self)]{#symbol-Handle._get}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Handle.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [get(self\[, boxname\])]{#symbol-Handle.get}

Return an item of data sent to an outbox of the wrapped component.

This method is non blocking and always returns immediately. If there is
no data to return, then the exception Queue.Empty is thrown

Arguments:

-   boxname \-- (optional) the name of the outbox of the wrapped
    component from which the data should be collected
    (default=\"outbox\", should be either \"outbox\" or \"signal\")
:::

::: {.section}
#### [main(self)]{#symbol-Handle.main}

Main loop.
:::

::: {.section}
#### [put(self, \*args)]{#symbol-Handle.put}

Send an item of data to one of the inboxes of the wrapped component.

The item of data is queued and sent to the inbox as soon as possible.

Arguments:

-   the item of data
-   the name of the inbox it is destined for (either \"inbox\" or
    \"control\")
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference} :

-   [initialiseComponent](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.initialiseComponent){.reference}(self)
-   [\_handlemessagefromthread](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._handlemessagefromthread){.reference}(self,
    msg)
-   [activate](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [mainBody](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.mainBody){.reference}(self)
-   [recv](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.recv){.reference}(self\[,
    boxname\])
-   [forwardInboxToThread](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.forwardInboxToThread){.reference}(self,
    box)
-   [closeDownComponent](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.closeDownComponent){.reference}(self)
-   [unlink](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.unlink){.reference}(self\[,
    thecomponent\]\[, thelinkage\])
-   [sync](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.sync){.reference}(self)
-   [send](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.send){.reference}(self,
    message\[, boxname\])
-   [\_threadmain](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._threadmain){.reference}(self)
-   [pause](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.pause){.reference}(self\[,
    timeout\])
-   [\_localmain](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._localmain){.reference}(self)
-   [\_do\_threadsafe](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent._do_threadsafe){.reference}(self,
    cmd, argL, argD)
-   [link](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.link){.reference}(self,
    source, sink\[, passthrough\])
-   [dataReady](/Docs/Axon/Axon.ThreadedComponent.html#symbol-threadedcomponent.dataReady){.reference}(self\[,
    boxname\])
:::

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
