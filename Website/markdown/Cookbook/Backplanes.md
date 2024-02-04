---
pagename: Cookbook/Backplanes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook : Backplanes
=====================

Backplanes provide an easy way to distribute data from many sources to
many destinations. For example\

### Serving to multiple clients 

For example, perhaps we want to build a server where each client that
connects receives a copy of a stream of data - perhaps the current time.
First, lets create our source of time data:

>     from Axon.ThreadedComponent import threadedcomponent
>     import time
>
>     class TimeTick(threadedcomponent):
>         def main(self):
>             prev=""
>             while 1:
>                 now = time.asctime() + "\n"
>                 if now!=prev:
>                     self.send(now, "outbox")
>                     prev=now
>                 else:
>                     self.pause(0.1)

We\'re going to use SimpleServer to provide a simple TCP server to
clients. Every time a client connects, we could make a new, private
instance of TimeTick to handle that client. Alternatively we could make
a single TimeTick component that sends (publishes) its messages to a
Backplane:\
\

>     from Kamaelia.Util.Backplane import Backplane
>     from Kamaelia.Util.Backplane import PublishTo
>     from Kamaelia.Chassis.Pipeline import Pipeline
>
>     Backplane("TIME").activate()
>
>     Pipeline( TimeTick(),
>               PublishTo("TIME"),
>             ).activate()

Then for each client that connects, we ask SimpleServer to make a
component that fetches (subscribes) from that same backplane:\
\

>     from Kamaelia.Util.Backplane import SubscribeTo
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     SimpleServer(protocol=lambda : SubscribeTo("TIME"), port=1500).run()

### So what\'s going on? 

Notice we\'ve named the Backplane \"TIME\" to distinguish it from other
Backplanes. You can therefore have as many Backplanes in a system as you
like. The SubscribeTo and PublishTo components connect to the right
backplane because they look it up (by the name) using the Coordinating
Assistant Tracker (CAT). Once the subscribers and publishers are all
linked up, you get something like this:\
\

::: {align="center"}
![PublishTo components send data to the Backplane. The Backplane then
sends it onto ALL SubscribeTo components subscribed to
it.](/images/backplane1.gif)\
:::

\
PublishTo components send anything that arrives at their \"inbox\" inbox
onto the Backplane. SubscribeTo components talk to the backplane and
send on anything they receive from it to their \"outbox\" outbox. The
Backplane itself acts like a splitter component - anything it receives
is sent onto all outputs; in this case - all subscribers.\

### Couldn\'t we have done that more simply? 

For a really simple example like this, there is little or no benefit of
doing it this way \... in fact, it might seem like unnecessary extra
effort and components! However, the real power is that all the clients
are sharing the same data source.

### A simple relay server 

Perhaps, for example, our source of data is actually coming from another
server (say \"foo.bar.com\" on port 1600). Using a backplane, its easy
to build a relay server capable of replicating the data to multiple
clients:

>     from Kamaelia.Internet.TCPClient import TCPClient
>
>     Pipeline( TCPClient("foo.bar.com", port=1600),
>               PublishTo("DATA"),
>             ).activate()
>
>     Backplane("DATA").activate()
>
>     SimpleServer(protocol=lambda : SubscribeTo("DATA"), port=1600).run()

### An aggregating logger\... 

Backplanes aren\'t just useful for distributing data in a one-to-many
fashion; they can also be used for many-to-one or many-to-many. For
example, we can use a Backplane to build a logging server capable of
logging, to a single file, data received from multiple clients. In
effect, a simple aggregating logger:

>     from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
>     from Kamaelia.File.Writing import SimpleFileWriter
>
>     def sendToBackplane():
>         return Pipeline( chunks_to_lines(),
>                           PublishTo("LOGGER"),
>                         )
>
>     SimpleServer(protocol=sendToBackplane, port=1500).activate()
>
>     Pipeline( SubscribeTo("LOGGER"),
>               SimpleFileWriter("log.data"),
>             ).activate()
>
>     Backplane("LOGGER").run()

### \...that can also be a relay 

Because we use a Backplane and a SimpleServer chassis, the client
connections are not hard wired - clients can connect and disconnect
whenever they choose. In fact, we could extend this further, by allowing
clients to connect on a different port to receive a live stream of the
aggregated logging data:

>     SimpleServer(protocol=SubscribeTo("LOGGER"), port=1501).activate()

Our aggregating logger is now also a relay, using the backplane to
distribute messages from many sources to many destinations.

\
\-- Jan 2007, Matt\
