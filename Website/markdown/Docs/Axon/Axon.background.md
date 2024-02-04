---
pagename: Docs/Axon/Axon.background
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[background](/Docs/Axon/Axon.background.html){.reference}
--------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Running an Axon system in a separate thread
===========================================

::: {.container}
-   **class
    [background](/Docs/Axon/Axon.background.background.html){.reference}**
:::

-   [Example Usage](#59){.reference}
-   [Behavour](#60){.reference}
:::

::: {.section}
The background class makes it easy to run an Axon system in a separate
thread (in effect: in the background).

This simplifies integration of Axon/Kamaelia code into other python
code. See also [Axon.Handle](/Docs/Axon/Axon.Handle.html){.reference}
for a simple way to wrap a component in a thread safe way to access its
inboxes and outboxes.

::: {.section}
[Example Usage]{#example-usage} {#59}
-------------------------------

At its simplest, you could run a Kamaelia task independently in the
background - such as a simple network connection, that dumps received
data into a thread safe queue, after de-chunking it into lines of text.

NOTE: This example can be achieved more simply by using
[Axon.Handle](/Docs/Axon/Axon.Handle.html){.reference}. See the
documentation of [Axon.Handle](/Docs/Axon/Axon.Handle.html){.reference}
to find out more.

1.  We implement a simple component to collect the data:

    ``` {.literal-block}
    from Axon.background import background
    from Axon.Component import component

    class Receiver(component):
        def __init__(self, queue):
            super(Bucket,self).__init__()
            self.q = queue

        def main(self):
            while 1:
                while self.dataReady("inbox"):
                    self.q.put(self.recv("inbox"))
                self.pause()
                yield 1
    ```

2.  Then we create a background object and call its start() method:

    ``` {.literal-block}
    from Axon.background import background

    background().start()
    ```

3.  Finally, we create and activate our Kamaelia pipeline of components,
    including the receiver component we\'ve just written, passing it a
    thread-safe queue to put the data into:

    ``` {.literal-block}
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Visualisation.PhysicsGraph import chunks_to_lines
    from Queue import Queue

    queue = Queue()

    Pipeline(
        TCPClient("my.server.com", 1234),
        chunks_to_lines(),
        Receiver(queue)
    ).activate()
    ```

We can now fetch items of data, from the queue when they arrive:

``` {.literal-block}
received_line = queue.get()
```
:::

::: {.section}
[Behavour]{#behavour} {#60}
---------------------

Create one of these and start it running by calling its start() method.

After that, any components you activate will default to using this
scheduler.

Only one instance can be used within a given python interpreter.

The background thread is set as a \"daemon\" thread. This means that if
your program exits, this background thread will be killed too. If it
were not a daemon, then it would prevent the python interpreter
terminating until the components running in it had all terminated too.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[background](/Docs/Axon/Axon.background.html){.reference}.[background](/Docs/Axon/Axon.background.background.html){.reference}
=======================================================================================================================================================================

::: {.section}
class background(threading.Thread) {#symbol-background}
----------------------------------

::: {.section}
A python thread which runs the Axon Scheduler. Takes the same arguments
at creation that Axon.Scheduler.scheduler.run.runThreads accepts.

Create one of these and start it running by calling its start() method.

After that, any components you activate will default to using this
scheduler.

Only one instance can be used within a given python interpreter.
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, slowmo\]\[, zap\])]{#symbol-background.__init__}
:::

::: {.section}
#### [run(self)]{#symbol-background.run}
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
