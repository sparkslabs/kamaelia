---
pagename: AxonShell
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon Shell]{style="font-size:28pt;font-weight:600"}

[Interactive Kamaelia]{style="font-size:18pt"}

In [Tools]{style="font-style:italic"} in the Kamaelia distribution, we
have the Axon Shell. This is an integration of IPython with Axon, with
Axon running in a secondary shell, thus you can build Axon systems in
the same way you build unix systems - interactively from the command
line.

[Starting the Axon Shell]{style="font-size:16pt;font-weight:600"}

::: {.boxright}
The Axon shell can be found in the [Tools]{style="font-family:Courier"}
directory of the Kamaelia distribution, named
[axonshell.py]{style="font-family:Courier"}. In the following run
through, we\'ll use [bold
italic]{style="font-family:Courier;font-style:italic;font-weight:600"}
to indicate something the user types.
:::

First of all, start up the Axon Shell:

You\'re then greeted by the IPython default command line prompt. (This
is the line labeled \'[In \[1\]]{style="font-family:Courier"}:\' )

If you want, you can confirm that Axon is indeed already loaded and
available:

[In \[1\]:
]{style="font-family:Courier"}[Axon]{style="font-family:Courier;font-style:italic;font-weight:600"}[\
]{style="font-family:Courier;font-style:italic;font-weight:400"}[Out\[1\]:
\<module \'Axon\' from
\'/usr/lib/python2.4/site-packages/Axon/\_\_init\_\_.pyc\'\>]{style="font-family:Courier"}

The line starting \"[Out \[1\]]{style="font-family:Courier"}\' is output
from IPython, in this case displaying where the Axon module was loaded
from.

[Loading and Running a
Component]{style="font-size:16pt;font-weight:600"}

The next thing we might want to know is how to load and run a component.
This is pretty much as you would do with a component in a running
system, the difference is as soon as we activate the component it starts
immediately - this is due to the scheduler running in a separate thread:

This shows the creation of a component, which we can now activate:

At this point in time a pygame window appears with a blank (white on
white) ticker. We can then send a message to the tickers main inbox as
follows:

This text then appears - but it does so instantaneously - too quick to
notice\...

[Sending a Component Data]{style="font-size:16pt;font-weight:600"}

OK, so that\'s relatively interesting, but let\'s make this more
visible. We\'ll grab a chunk of text, split it into words, and deliver
those every tenth of a second. One source of text is documentation, so
let\'s check the size of the docstring for the pydoc module:

This looks like a reasonable size, but how many chunks would this split
into, if we do a [rough]{style="font-style:italic"} word split?

217 words seems reasonable - if we have this displayed at a rate of 10
words per second this will take about 20 seconds - nice for testing, not
too long, not too short. OK, so lets just deliver these every 0.1
seconds apart:

<div>

[In \[10\]: ]{style="font-family:Courier"}[import
time]{style="font-family:Courier;font-style:italic;font-weight:600"}[\
In \[11\]: ]{style="font-family:Courier"}[for i in
pydoc.\_\_doc\_\_.split():]{style="font-family:Courier;font-style:italic;font-weight:600"}

</div>

And key presto - we have a working ticker controlled from the command
line :)

[Building and using Pipelines]{style="font-size:16pt;font-weight:600"}

OK, so that\'s nice, what else can we do?

[Making the pipeline]{style="font-style:italic;font-weight:600"}

Let\'s try the graph viewer. For this we need to build a simple
pipeline, because it\'s a lot simpler to send text strings to the graph
viewer rather than data structures (though we could send data
structures). First of all we need to import the components we\'re going
to use:

Then we can build the pipeline, activate it and take a reference to it.
This is however relatively simple:

<div>

[In \[15\]: ]{style="font-family:Courier"}[myvis =
pipeline(lines\_to\_tokenlists(),]{style="font-family:Courier;font-style:italic;font-weight:600"}

</div>

And just as before, the topology viewer appears instantaneously.

[Using the pipeline]{style="font-style:italic;font-weight:600"}

This topology viewer understands messages sent to it of the following
two forms:

-   ADD NODE [id label]{style="font-style:italic"} auto -
-   ADD LINK [id id]{style="font-style:italic"}
-   DEL ALL

So let\'s try it! Let\'s draw a simple producer consumer system. First
of all, let\'s create a producer node \...

\... and it appears. So let\'s create a consumer node \...

\... and that appears. Creating a link between then is then also simple:

And the link appears. The topology viewer is then still interactive, so
you can move the nodes around etc.

[Using the pipeline to visualise something more
complex]{style="font-style:italic;font-weight:600"}

OK, that\'s fairly interesting - let\'s try visualising the systems
described in [Simple Reliable
Multicast](SimpleReliableMulticast.html).So we start off by wiping the
display:

We can then add on the 4 components in the server piple line as nodes.
For convenience I\'m giving them ids \"1\", \"2\", \"3\" and \"4\".

Then we simply add in the links:

Similarly, we can add in the client side components \...

\... and add in their links:

[Summary]{style="font-size:16pt;font-weight:600"}

This page has shown how you can use IPython and Kamaelia together to run
the Axon shell. It\'s shown how you can build simple pipelines on the
command line to do interesting tasks interactively - even things
involving external event loops such as pygame based systems.
