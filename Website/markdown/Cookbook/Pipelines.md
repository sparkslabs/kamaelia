---
pagename: Cookbook/Pipelines
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Pipelines
====================

Pipelines are one of the simplest ways to wire components together. A
Pipeline wires components together in a long chain.\
\
Here\'s a simple pipeline we want to build that sends a file over
multicast, using a simple protocol to ensure reliable transmission:\
\

::: {align="center"}
![We want to wire a set of components together in a long chain (a
pipeline)](/images/pipeline1_idea.gif)
:::

\
We could build this by writing a new component with a whole bunch of
self.link() calls to link each outbox to the next inbox. But that is a
lot of code to write and rather tedious! \... surely there must be an
easier way?\
\
\... And so the Pipeline component comes to the rescue! No need to write
a whole new component, simply use a Pipeline component like this:\

>     from Kamaelia.Chassis.Pipeline import Pipeline
>
>     from Kamaelia.Internet.Multicast_transceiver import Multicast_transceiver
>     from Kamaelia.Protocol.SimpleReliableMulticast import Annotator
>     from Kamaelia.Protocol.SimpleReliableMulticast import _Framer
>     from Kamaelia.Protocol.SimpleReliableMulticast import _DataChunker
>     from Kamaelia.Protocol.Packetise import MaxSizePacketiser
>     from Kamaelia.File.Reading import RateControlledFileReader
>
>     Pipeline( RateControlledFileReader("myaudio.mp3",readmode="bytes",rate=128000/8),
>               Annotator(),
>               _Framer(),
>               _DataChunker(),
>               MaxSizePacketiser(),
>               Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
>             ).run()

You can find this code in
` Kamaelia/Examples/Multicast/SimpleReliableMulticast `\

So what did Pipeline actually do?

![Pipeline component does this for us](/images/pipeline1_intention.gif)

It wires the components into a chain inside itself - linking outboxes to
inboxes. When we call the run() method, the Kamaelia system starts, and
the pipeline component is activated. It in turn, activates all the
components inside.\

### How are the components linked together?

::: {.boxright}
**Just like unix pipes**\
\"inbox\" and \"outbox\" are a lot like standard-input and
standard-output for command line programs. When you pipe programs
together on a unix shell, the standard-output of one program gets sent
to the standard-input of the next.\
\
\"control\" and \"signal\" are analogous to standard-error. In practice
Kamaelia components use it to signal when they are finished.\
:::

\
More specifically, Pipeline links one component to the next in the
chain. It links the \"outbox\" and \"signal\" outboxes of one component
to the \"inbox\" and \"control\" inboxes on the next one:\

-   The \"inbox\" and \"outbox\" boxes are the ones most components use
    to take in and send out data. So for example, whatever the
    RateControlledFileReader component reads gets sent to the Annotator
    component.\
    \
-   The \"control\" and \"signal\" boxes are used to send the shutdown
    message when a component has finished, and wants to tell the next.

So, if we look at precisely what linkages are made, we see something
like this:\
\

::: {align="center"}
![Pipeline component links ](/images/pipeline1_inside.gif)
:::

\

### Pipeline is a component too \... time to go modular! 

The Pipeline also links its own inboxes and outboxes to the start and
the end (respectively) of the chain. Pipeline is, after all, a component
too, so it makes sense to be able to send and receive messages to/from
the pipeline of components within using its inboxes and outboxes. Think
of it as a kind of container.\
\
You can therefore use a Pipeline as a way to wrap up a useful pipelined
set of components into a single bundle that you can then reuse
elsewhere.\
\
For example, we could separate the components that make the multicast
reliability protocol into another Pipeline, and simply include it like
another component:\

>     Pipeline( RateControlledFileReader("myaudio.mp3",readmode="bytes",rate=128000/8),
>               Pipeline( Annotator(),
>                          _Framer(),
>                          _DataChunker(),
>                        ),
>               MaxSizePacketiser(),
>               Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
>             ).run()

We don\'t have to call the run() or activate() method of the inner
pipeline since, just like the other components, they\'ll all be
activated by the main pipeline when it starts.\
\
In fact, we could actually move that into a completely separate
function, that simply returns the pipeline:\

>     def SRM_Sender():
>        return Pipeline( Annotator(),
>                         _Framer(),
>                         _DataChunker(),
>                       )

Now we can call that function to put the sub pipeline into the chain:\

>     Pipeline( RateControlledFileReader("myaudio.mp3",readmode="bytes",rate=128000/8),
>               SRM_Sender(),
>               MaxSizePacketiser(),
>               Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
>             ).run()

We can now, for the most part, use SRM\_Sender just like any other
component.\
\
This hopefully makes the design of the system more modular and clearer,
and also give us a re-usable component for applying our multicast
reliability protocol - which we previously didn\'t have. In fact, this
has already been done so you can simply import it and use it:\

>     from Kamaelia.Protocol.SimpleReliableMulticast import SRM_Sender
>
>     Pipeline( RateControlledFileReader("myaudio.mp3",readmode="bytes",rate=128000/8),
>               SRM_Sender(),
>               MaxSizePacketiser(),
>               Multicast_transceiver("0.0.0.0", 0, "224.168.2.9", 1600),
>             ).run()

### Need more flexibility?

Pipelines are not the only quick and easy way to link up components.
Perhaps you need to make different links? Try a
[Graphline](/Cookbook/Graphlines%20) instead.\
\
\-- 18 Dec 2006 - Matt Hammond\
\
