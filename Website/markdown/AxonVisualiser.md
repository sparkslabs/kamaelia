---
pagename: AxonVisualiser
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon Visualiser]{style="font-size:23pt;font-weight:600"}

[Looking inside running systems]{style="font-size:15pt"}

In [Tools]{style="font-style:italic"} in the Kamaelia distribution, we
have the Axon Visualiser. This allows you to look inside running
Kamaelia based systems and see what your system is currently doing, what
components are active and linked to what.

[Starting the Axon Visualiser]{style="font-size:13pt;font-weight:600"}

::: {.boxright}
The Axon visualiser can be found in the
[Tools]{style="font-family:Courier"} directory of the Kamaelia
distribution, named [AxonVisualiser.py]{style="font-family:Courier"}. In
the following run through, we\'ll use [bold
italic]{style="font-family:Courier;font-style:italic;font-weight:600"}
to indicate something the user types.
:::

Start the Axon Visualiser:

If all goes well, an empty visualiser window will appear (empty except
for a logo).

Press [ESCAPE]{style="font-style:italic;font-weight:600"} or
[Q]{style="font-style:italic;font-weight:600"} to quit.

You can see the full command line options for this tool:

[Simple Navel gazing]{style="font-size:13pt;font-weight:600"}

But that isn\'t very interesting. Let\'s get the visualiser to navel
gaze a little and introspect itself:

Once the display has settled down, things should look a little more
interesting. The visualiser is now showing the components it consists
of:

[![](screenshots/thumbnail/AxonVisualiser_navelgaze.gif)](screenshots/AxonVisualiser_navelgaze.gif)

[Axon Visualiser Introspecting itself (Click to
enlarge)]{style="font-style:italic"}

[What am I seeing?]{style="font-style:italic;font-weight:600"}

Each grey \'blob\' is a component. A component\'s inboxes and outboxes
are labels that hover round the edge of the blob. Linkages between
components are the green and orange lines. The direction arrows show the
which way data flows. Orange linkages are \'passthrough\' linkages -
where a component forwards an inbox to a child\'s inbox or an outbox to
a child\'s outbox.

The name labels for all compoents, inboxes and outboxes are abbreviated.

What you are seeing may not look quite this tidy. But don\'t worry, you
can re-arrange the blobs!

[Manipulating the view]{style="font-style:italic;font-weight:600"}

[Drag ]{style="font-weight:600"}components, inboxes or outboxes with the
mouse to move them around. As you drag things, the topology visualiser
physics model will cause things to move around, trying to rearrange
themselves to not get in the way.

[Click ]{style="font-weight:600"}a component, inbox or outbox and it
will be highlighted. Its full, unabbreviated, name will also be
displayed at the top. In the screenshot above, the Introspector
component (the source of this introspection data) is highlighted.

Use the [arrow keys]{style="font-weight:600"} to pan the view left,
right, up and down.

[Introspecting Another Program]{style="font-size:13pt;font-weight:600"}

The Axon Visualiser, by default, receives introspection data from a TCP
socket. Lets plug introspection code into another system and watch what
is going on.

[Adding Introspection]{style="font-style:italic;font-weight:600"}

Take the SimpleStreamer.py example. The code added to provide
introspection is highlighted in green:

::: {.boxright}
This example can be found in
[Kamaelia/Examples/example3/SimpleStreamer.py]{style="font-family:courier"}
:::

<div>

[import Axon as \_Axon]{style="font-family:Courier"}

</div>

<div>

[import Kamaelia.ReadFileAdaptor]{style="font-family:Courier"}

</div>

<div>

[from Kamaelia.SimpleServerComponent import
SimpleServer]{style="font-family:Courier"}

</div>

<div>

</div>

<div>

[file\_to\_stream =
\"/usr/share/wesnoth/music/wesnoth-1.ogg\"]{style="font-family:Courier"}

</div>

<div>

</div>

<div>

[def AdHocFileProtocolHandler(filename):]{style="font-family:Courier"}

</div>

<div>

[class
klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):]{style="font-family:Courier"}

</div>

<div>

[def \_\_init\_\_(self,\*argv,\*\*argd):]{style="font-family:Courier"}

</div>

<div>

[return klass]{style="font-family:Courier"}

</div>

<div>

</div>

<div>

[clientServerTestPort=1500]{style="font-family:Courier"}

</div>

<div>

</div>

<div>

[from Kamaelia.Util.PipelineComponent import
pipeline]{style="font-family:Courier;font-weight:600;color:#008002"}

</div>

<div>

[from Kamaelia.Internet.TCPClient import
TCPClient]{style="font-family:Courier;font-weight:600;color:#008002"}

</div>

<div>

[from Kamaelia.Util.Introspector import
Introspector]{style="font-family:Courier;font-weight:600;color:#008002"}

</div>

<div>

</div>

<div>

[pipeline( Introspector(), TCPClient(\"127.0.0.1\",1501)
).activate()]{style="font-family:Courier;font-weight:600;color:#008002"}

</div>

<div>

</div>

<div>

[SimpleServer(protocol=AdHocFileProtocolHandler(file\_to\_stream),]{style="font-family:Courier"}

</div>

As you can see, all you need to do is create an Introspector, and
TCPClient (to send the data) and pipeline them together.

By default the Axon Visualiser expects the client to connect on port
1500, however this example program already uses that port. We therefore
arbitrarily choose port 1501 instead.

[Performing the
Introspection]{style="font-style:italic;font-weight:600"}

We must start the Axon Visualiser before the system we are
introspecting. Why? Because the Introspector component only sends the
changes it sees in the system it is introspecting and the TCPClient
component will want to connect to the visualiser immediately. If we were
to start up the streaming server first, then the visualiser would not be
in sync with the data and the TCPClient would have given up trying to
connect to it.

Lets start the visualiser, remembering to ask it to listen on port 1501,
rather than its default of port 1500:

Now we can start the streaming system:

After a brief pause, the visualiser will gradually be populated with the
components, postboxes and linkages currently in SimpleServer. Once it
has settled down and you have moved things around to tidy it up, you
should see something like this:

[![](screenshots/thumbnail/AxonVisualiser_SimpleStreamer.gif)](screenshots/AxonVisualiser_SimpleStreamer.gif)

[A view inside SimpleStreamer.py (Click to
enlarge)]{style="font-style:italic"}

[What am I seeing?]{style="font-style:italic;font-weight:600"}

Why are there so many components, when the SimpleStreamer surely only
consists of a few? The simple answer is that you\'re not only seeing the
SimpleServer components, but also the ones you added to perform the
introspection.

::: {.boxright}
Introspector (5) is the source of introspection data. Pipeline (5) joins
it to TCPClient (7) which is using ConnectedSocketAdapter (17) to send
the data to the visualiser.
:::

The highlighted Selector component represents the unix \'select\'
statement, waiting for events on all socket bindings. Notice that both
the introspection \'system\' and the server share the Selector.
Obviously, the moral of the story is that you can\'t observe a system
without modifying and affecting it.

[Watching a changing system]{style="font-size:13pt;font-weight:600"}

Lets see what happens when a client connects to our streaming server.

First, check that the client (SimpleStreamingClient.py) is going to
connect to the machine we\'re running SimpleStreamer.py on:

<div>

[from Kamaelia.Internet.TCPClient import
TCPClient]{style="font-family:courier"}

</div>

<div>

[from Kamaelia.vorbisDecodeComponent import VorbisDecode,
AOAudioPlaybackAdaptor]{style="font-family:courier"}

</div>

<div>

[from Kamaelia.Util.PipelineComponent import
pipeline]{style="font-family:courier"}

</div>

<div>

</div>

<div>

[clientServerTestPort=1500]{style="font-family:courier"}

</div>

<div>

[pipeline(TCPClient(]{style="font-family:courier"}[\"127.0.0.1\"]{style="font-family:courier;font-weight:600;color:#008002"}[,clientServerTestPort),]{style="font-family:courier"}

</div>

<div>

[).run()]{style="font-family:courier"}

</div>

[Now lets run the client\...]{style="font-family:verdana"}

\...and see what happens:

[![](screenshots/thumbnail/AxonVisualiser_SimpleStreamerWithClient.gif)](screenshots/AxonVisualiser_SimpleStreamerWithClient.gif)

[A view inside SimpleStreamer.py when a client has connected (Click to
enlarge)]{style="font-style:italic"}

For the duration of the streaming connection, you can see new
components, postboxes and linkages created (circled in blue in the above
screenshot).

[Limitations]{style="font-style:italic;font-weight:600"}

You may find that the components appear and disappear too quickly for
you to be able to see what is happening. This is because you are
remotely viewing what is happening in a live running system, rather than
stepping through execution in a debugger. It takes time for data to flow
from introspector to visualiser; and it takes time for the visualiser\'s
physics model to sort out the visual mess into a semblance of order.

Also bear in mind that the visualiser will batch process data from the
introspector if it comes in particularly fast, redrawing the view less
frequently. You may have noticed this when you first started up the
streaming server. Consequently, if a change to the system has a very
short duration, you may not see it at all.

If you want to freeze the state of a system to inspect it properly, you
must cut off the flow of introspection data to the visualiser - either
by in some may pausing your program, or by simply killing it (pressing
[ctrl-c]{style="font-weight:600"} in unix systems).

[Visualisation as a debugging
aid]{style="font-size:13pt;font-weight:600"}

We\'ve found this tool to be useful as a debugging aid. We\'ve spotted
the following when introspecting running systems:

[The Linkages are all wrong!]{style="font-style:italic;font-weight:600"}

Introspection lets you see whether the linkages you think you coded have
actually been made. You can also follow the arrows to check that the
data-flow of your system makes sense.

[Components left dangling]{style="font-style:italic;font-weight:600"}

A component has finished doing its task and should have been unwired
(linkages removed) and/or disappeared.

-   Linkages are \'owned\' by the component you called the link() method
    on. Only that component\'s postman can destroy that linkage. Check
    that all components that created the linkages are destroying them
    \... correctly.
-   A component will remain \'active\' (and be called by the scheduler)
    until it exits its main() generator. Check that the component is
    shutting down properly.

[One outbox linked to multiple
inboxes]{style="font-style:italic;font-weight:600"}

Axon only supports many-to-one or one-to-one linkages. One-to-many are
not supported.

-   If one outbox is linked to many inboxes, only one will receive any
    data sent. Which one receives the data is undefined.

[Non-sensical introspection visualisation / far too many
components]{style="font-style:italic;font-weight:600"}

If a component\'s microprocess is activated more than once, the
scheduler will register it multiple times. The Introspector cannot
guarantee being able to make sense of such situations!

-   Check that you are not, for example, activating a component, then
    placing it in a pipeline and activating that too.

[How it works]{style="font-size:13pt;font-weight:600"}

This is a specialisation of the Topology Visualiser for viewing the
components, and linkages between them, in a running system. This is a
quick tutorial to give you an understanding of how to use this tool and
what you can do with it.

The actual introspection into a running system is performed separately -
by the Introspector component. The visualiser waits to receive this data
over a TCP socket connection.

[Further information]{style="font-size:13pt;font-weight:600"}

You can obtain help on the full command line options for the Axon
Visualiser:

The Axon visualiser is a specialisation of the generic Topology
visualiser system. Set it to navelgaze or \'loop back\' to understand
what components it is built from:

[or:]{style="font-family:verdana"}

[Summary]{style="font-size:13pt;font-weight:600"}

This page has shown how to use the Axon Visualiser program and how to
add introspection code to a Kamaelia system. You should also have a
flavour of how this can be used to aid understanding the runtime
properties of your system and to aid debugging.
