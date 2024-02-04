---
pagename: KamaeliaOverview
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Kamaelia - Networking Using
Generators]{style="font-size:15pt;font-weight:600"}

Michael Sparks

BBC Research & Development

[ABSTRACT]{style="font-weight:600"}

+-----------------------------------------------------------------------+
| Scalable concurrent systems do not have to be hard - this is a        |
| fundamental aim of the Kamaelia project. The real world contains      |
| large numbers of items we interact with daily on a concurrent basis,  |
| be it every electronic item we own - from kettles to computers        |
| through to simple things like roads, office workers and dance         |
| partners.                                                             |
|                                                                       |
| Concurrency in software often takes 3 approaches - process, thread or |
| state machine based. For portability and scalability, state machine   |
| based systems are normally the preferred approach. However, even best |
| of breed systems often have a steep learning curve and can hard for   |
| beginners to learn, and can be difficult to debug.                    |
|                                                                       |
| Kamaelia represents concurrency as components communicating along     |
| unidirectional linkages. Components are python generators embedded    |
| into a class augmented by inboxes and outboxes. New components can be |
| written sequentially, and then made concurrent slowly and simply in a |
| controlled fashion.                                                   |
|                                                                       |
| Building systems is pretty much like using good old fashioned unix    |
| pipelines. You choose the components that do the work and string      |
| their outputs and inputs together. You can build pipelines or graphs  |
| which may also change dynamically. Components also nest simplifying   |
| systems. This approach also encourages high levels of reuse.          |
|                                                                       |
| Using python generators seems to result in performance similar to     |
| that of traditional state machines, with an ease of use similar to    |
| that of process based concurrency. BBC R&D is building Kamaelia as a  |
| testbed for developing open large scale internet media delivery       |
| protocols. This paper provides an overview of the core technology     |
| allowing others to use the technology for other uses.                 |
+-----------------------------------------------------------------------+

[Kamaelia]{style="font-size:17pt;font-weight:600"}

Kamaelia is a project aimed at exploring long term systems for large
scale media delivery. At its core is a concurrency toolkit, focussed
mainly on experimenting with network protocols. This toolkit has 2 key
portions - Axon and Kamaelia.

Axon itself is the core component infrastructure aimed at making
concurrent systems easy to work with. It is written in the python,
though a simplistic C++ version also exists. In python terms it
implements components using generators, and systems are make by setting
up communications between components.

The Kamaelia portion is the larger of the two sections, which is why it
is named after the main project - since it is a collection of components
that use Axon. These range from components for building network servers
and clients through to music playback, audio codec decode through to
components suitable for viewing network topologies.

Howver, one key aim of the project is to enable even novices programmers
to create scalable, safe concurrent systems quickly and easily.

The Kamaelia project has been released as an open source project
licensed under the MPL/GPL/LGPL trilicense. This is the same licensing
scheme as dirac and is intended to allow the use of Kamaelia by as wide
an audience as possible.

This paper will discuss the current status of the project, the
project\'s motivations, the background to Kamaelia\'s core concurrency
technology, provide a simple example of building systems and components
using Axon, and finally finish with some possible options for longer
term work, and an invitation to work with us!

[Status]{style="font-weight:600"}

The current status of the project is that Axon itself has been deemed
feature stable, and currently stands at version 1.0.3. Axon runs on
Windows, Mac OS X, Linux and Series 60 mobile phones.

As noted above Kamaelia can already be used for a wide variety of tasks
from network servers, through to interactive systems, but we feel has a
long way to go before the system can be considered reaching a 1.0
release. As a result the current version number reflects this and
currently stands at 0.1.2.

That said, like Axon, it runs on Windows, Mac OS X, Linux and Series 60
mobile phones, and has also been used to test our ease of use hypothesis
on 1 pre-university trainee, with promising results.

[Motivations]{style="font-weight:600"}

The motivations for the Kamaelia project stem from 3 main points:

-   What does the BBC do currently with regard to large scale streaming?
-   How might demand change in future?
-   [What happens if\...
    ]{style="font-style:italic;font-weight:600"}[(say) the BBC opened
    the entire archive online and everyone in the UK had
    broadband?]{style="font-style:italic"}

Currently the BBC streams a large amount of content to the UK audience.
This currently amounts to several million streams per day to tens of
thousands of concurrent viewers. That said, given the 3 points above it
is prudent to plan for the day when the BBC may be handling millions of
concurrent viewers online.

As a thought experiment, we can also imagine [what might happen if
]{style="font-style:italic;font-weight:600"}(say) 10 years from now, the
BBC opened up the entire archive to the entire UK audience online? The
creative archive is not that ambitious - after all it is based around
what we have the rights to, and the BBC does not currently have those
right, but what if legislation happened allowing this? Beyond that
copyright does expire eventually, meaning that significant chunks may
become available in 10 - 20 years?

Thankfully such a scenario is not a total unknown - there are online
stores with thousands upon thousands of items of content, and people\'s
choice tends to follow a well known curve - called a zipf distribution.
This is also known as a long tailed distribution due to the shape of the
graph that you get if you plot the number of requests for an object (eg
10 million people watching east enders) vs chart position (eg number 10,
number 100, number 10000 in the charts).

It turns out that with long tail distributions the bulk of traffic and
work is done in this immensely long tail - not in the head. Put another
way, the most popular programmes are a fraction of the amount of work
you have to do, because given the choice, people tend to choose from the
entire range of content available.

ie you can have 20 million homes watching 20 million different things,
which is completely different from 20 million people all watching the
same thing on TV!

Other issues arise when you scale up to these levels as well. The only
open protocol currently in heavy use for streaming is the Realtime
Transport Protocol (RTP). However, RTP was originally concieved for
internet based Audio/Video conferencing/telephony, which means certain
aspects don\'t scale well for large scale unidirectional streaming.

As a result we needed a platform for designing, implementing and testing
new open standards to scale in this way. Unfortunately, scalability and
ability to experiment often conflict, which is why we needed to write
our own system. Furthermore large scale means highly parallel, and
scalable concurrency often has a high barrier to entry. From our
perspective this was a real problem since a high barrier to entry can
limit the ability to take in new ideas, and limits areas of
collaboration. After all those most capable of implementing an idea may
not be the same people capable of imagining the idea.

[Axon\'s Design Background]{style="font-size:17pt;font-weight:600"}

As previously noted, Axon forms the core concurrency subsystem in
Kamaelia, is largely aimed at providing those core concurrency elements.
It tries to provide the smallest useful toolset for concurrency needed
for Kamaelia components, but no smaller (By comparison it is possible to
produce smaller systems, which are useful for exploring various ideas,
but tend to be incomplete).

The keys aims in Axon\'s basic design were as follows:

-   It should first and foremost use a scalable approach, which is also
    portable between operating systems.
-   It should naturally encourage re-use.
-   It should be simple. That is it should be sufficiently simple novice
    programmers can learn the system and quickly find it easy to use to
    produce useful systems. This is partly because we want to experiment
    with new ides and [novices see possibilities, not
    problems.]{style="font-style:italic"}
-   It sould provide a [safe ]{style="font-style:italic"}environment for
    building concurrent systems. Users should not have to worry unduly
    (or preferably at all) about race hazards, and ideally the user
    should not have to worry about locks. ie we want a non-locking
    architecture.

Many of these points will seem contradictory to many used to dealing
with scalable concurrent systems - after all even experienced
professionals can find scalable concurrency difficult.

Before we discuss the design decisions in Axon we simply note that we
believe we have achieved these goals.

[Scaling Concurrency]{style="font-weight:600"}

Let\'s start at the beginning - methods for scaling concurrent systems
in a portable manner. There are essentially 3 well understood and
commonly used methods for handling concurrency: processes, threads, and
\"build your own\".

Processes and threads are very well known approaches to handling
concurrency, and indeed are tools built into the operating system
allowing it to provide programs with the illusion of sole control of the
system. Threads differ from processes in that they reside within a
process, and share data within that process.

Unfortunately the scalabilty of process and thread based concurrency
does not tend to scale equally across different platforms. Furthermore
code written using processes and to a lesser extent threads suffers from
a key problem from our perspective - the operating system has no way of
determining that these processes and threads are working together
towards a common goal, rather than competing. Also, under heavy loads
context switching can also severely hamper scalability using processes
or threads, depending on the operating system or even version of
operating system.

As a result the majority of large scale network software, and hence
large scale concurrent systems tends to use a \"build your own\"
approach to handling concurrency. In practice, this normally means using
state machines.

An interesting question therefore arises - what about the people who
can\'t program state machines? This is a serious question - we are
targeting as wide a group of people as possible and aiming to include
novices within that group.

[State Machines]{style="font-weight:600"}

-   [A state machine is a piece of sequential processing that can
    release control half way and be restarted retaining
    state]{style="font-style:italic"}

What really is the problem with state machines? Unfortunately, they are
hard to get right 100% right even when you\'re pretty certain you are
doing the right thing, and this fact is especially true for novices.
Also we want to allow people to be able to pick up other people\'s code
and reuse it. This increases the likelihood that someone maintaining
code will not be the original author, and unfortunately debugging
someone else\'s state machine is at least twice as hard as designing the
state machine in the first place.

In practice there are a variety of frameworks that exist that try to
make creating systems like this alot simpler. In python the twisted
framwork is probably the best of breed framework for dealing with single
threaded scalable concurrency, and often betrays this state machine
heritage. However despite being a very good framework provide lots of
high quality assistance it still has a barrier to entry that is very
high for the novice.

[Scalability or ease?]{style="font-weight:600"}

At this point we begin to wonder - if we want ease we would normally
choose process based approaches and for scalability we would choose
state machine approaches. Do we really have to choose between these two,
or is there an alternative?

Consider:

-   [A ]{style="font-style:italic"}[state
    machine]{style="font-style:italic;font-weight:600"}[ is a piece of
    sequential processing that can release control half way and be
    restarted retaining state]{style="font-style:italic"}
-   [A
    ]{style="font-style:italic"}[generator]{style="font-style:italic;font-weight:600"}[
    is a piece of sequential processing that can release control half
    way and be restarted retaining state]{style="font-style:italic"}

A generator however also looks single threaded - much like process based
code - so is this what we want? It\'s worth noting that Twisted itself
also recognises that generators might be useful, providing the
twisted.flow module.

The key different between twisted.flow and Axon lies in the way we
compose systems. Our hypothesis is that it is this approach for
composition that limits the complexity that the programmer has to deal
with rather than increasing.

By using generators, we can allow novices to write small pieces of code
completely single threaded to test their ideas. After this they can then
modify their code to work in a parallel manner by simply adding a few
yield statements in the right places, and changing their interaction
with other systems and users. This transition from single threaded to
working cleanly with the concurrency toolkit is something that can be
done slowly and incrementally, often without radical code restructuring.

[Opportunity for collaboration with Twisted?]{style="font-weight:600"}

Whilst we developed Axon independently of the Twisted codebase, this was
a deliberate decision - we wanted to explore a variety of ideas, and the
use of generators was made late in the design process. It is entirely
likely that Axon would be a good fit to integrate with Twisted - largely
because both systems are single threaded, and Axon does not require
control of any main event loop - it simply requires CPU time
periodically.

Furthermore Twisted is a stable, mature system and suitable for
production systems, whereas at present Kamaelia is not mature, and as a
result not suitable for use in production systems. Kamaelia is however
highly suitable now for experimentation even by novices, and bringing
this alternative approach into Twisted might be beneficial to both
projects.

[Concurrency is Easy?]{style="font-weight:600"}

Creating code that can run concurrently is one thing. Actually making
systems that are concurrent, naturally concurrent and easy to use is not
considered common. Indeed, concurrency is often considered hard to work
with.

However, there is one field of IT and computing that uses simple, easy
to use concurrency day in day out and does so on a regular basis - unix
systems administration. Many unix systems admins would find the
following small script simple to understand and very similar to the sort
of shell script they write on a regular basis:

-   [find -type f . \|]{style="font-family:Courier"}

Nominally this can be argued to have 4 processing units, with 3
concurrent units, one of which consists of 2 serialised processing
units. The find statement runs in concurrently to the egrep statement
which runs in parallel to the while statement. The while statement
itself is controlled by the read statement, and dependent on the value
controls execution of the cp statement.

This is a relatively complex parallel computing task that many systems
admins would find natural to write and would naturally take good
advantage of a 3 core/CPU system. However whilst many systems admins
would not consider themselves the world\'s best parallel systems
programmers, it is probably true that they are the world\'s most common
parallel programmers and highly proficient at it.

Axon models itself on hardware systems that follow a very similar model
to Unix pipelines. What are the key characteristics of a unix pipelines
then?

-   They\'re essentially concurrent sequential processes - both in
    practice, and also in the manner of the classic paper on the topic
    (CSP). One major limitation of unix pipelines is that they are
    essentially linear - largely only allowing data flow in one
    direction inside the pipeline.
-   Items have no concept of what might be next in the pipeline - if
    they are even inside a pipeline.
-   Items in the pipeline simply communicate with 3 local file handles :
    stdin, stdout, stderr.

These 3 points are often considered sufficient for any CSP style system,
however there are a couple of further details which are worth noting:

-   How data passes between processes. In Unix pipelines processes can
    send data to the pipeline whenever they want, and will simply block
    when the hidden intermediate buffers between processes are full.
    This allows to operating system to handle race hazards between
    processes. (Consider a program that produces data faster than
    another that consumes and uses that data)
-   The system environment. This allows processes to place information
    in a standard place for notification of standard resources. The most
    commonly used standard resource for example is where to find other
    commands - specifically the PATH variable in the standard
    environment. At it\'s most basic though the system environment forms
    a basic key/value lookup tool.

[Axon]{style="font-size:17pt;font-weight:600"}

Having discussed the background to the key decisions made during Axon\'s
design we now discuss the key features of Axon, what they do and how to
use them. The key classes in Axon are as follows:

-   [Component]{style="font-weight:600"}. A component is a self pausing
    sequential objects - typically a generator - that sends data to
    local interfaces
-   [Linkage]{style="font-weight:600"}. A linkage is a facility for
    joining interfaces, allowing system composition
-   [Scheduler]{style="font-weight:600"}. The scheduler is a mechanism
    for giving components CPU time. The current scheduler is relatively
    primitive, however schedulers may also schedule other schedulers
    however allowing more complex priority mechanisms to be built if
    desired.
-   [Postman]{style="font-weight:600"}. The postmas is a facility for
    tracking linkages, and handling data transferral. It is expected
    that the postman will decrease in importance with time and end up
    simply tracking linkages.
-   [Co-ordinating Assistant/Tracker]{style="font-weight:600"} (cat).
    The co-ordinating assistant tracker provides environmental
    facilities for the same reasons as the unix environment. In
    practical terms this is similar to a Linda tuple space, and could
    evolve towards that sort of general facility.

[Axon: Component]{style="font-weight:600"}

A component in axon is a class that has a generator method called
\"main\". The fact that this generator is a method means that the
generator has access to a local object state. Furthermore, this local
object state is accessible by code that manipulates the object, forming
a mechanism for comunicating with the generator.

Axon provides a standardised mechanism for communicating with the
generator meaning that components do not need to share data, other than
to hand off ownership of data between themselves. (Much like unix
processes do not share data, but can hand off data between processes by
sending data to stdout/stderr)

Specifically, component classes are augmented by a list of named inboxes
and a list of named outboxes. Both inboxes and outboxes form queues for
sending data to/from a component, and a component only communicates with
inboxes and outboxes.

The exception to this is components that communicate with the outside
world in some manner - such as read from files, network sockets,
displaying information. Such components are often named adaptors by
convention to simplify identifying such components since testing these
can be more complex.

The default set of inboxes are named \"inbox\" and \"control\".
\"inbox\" is expected to recieve bulk data - much like stdin for
processes. \"control\" is expected to recieve signalling information
which may control the component. An example message that may be recieved
on a control inbox is \"producerFinished\". This allows the component to
know that the component sending data on the inbox has finished. (eg end
of file)

The default set of outboxes are named \"outbox\" and \"signal\".
\"outbox\" is expected to be sent bulk data - much like stdout for
processes. \"signal\" is expected to be sent signalling information that
may or may not control another component. A file reader for example may
read data from a file and send the data to its \"outbox\", and wen it
reaches the end of file may send a \"producerFinished\" message to
\"signal\".

The simplest example component that is useful is probably as follows:

class Echo(component):

<div>

def main(self):

</div>

<div>

if self.dataReady(\"inbox\"):

</div>

<div>

yield 1

</div>

The logic of this component should be clear - when data is ready in the
inbox \"inbox\", the component takes that data from that inbox, and
sends it to its outbox \"outbox\".

Whilst this may seem like a simple \"pass through\" (which is is)
component with no clear benefit, it forms an extremely useful tool.
Since it is a component, we can also use it as a basic network protocol
- one that echoes back to the client what they send, extremely useful
when testing systems.

[Axon: Scheduler]{style="font-weight:600"}

The scheduler provides components with the CPU periodically. Essentially
its general process of operation is as follows:

-   Holds a run queue containing activated components
-   Calls the generator for each component sequentially, which may yield
    a variety of possible values for communication to the scheduler

There are essentially 3 different return values that hold meaning at
present.

Continue Running

-   If the value yielded by a component\'s generator is true then the
    component is deemed to still be active, but to have relinquished
    control for some reason. (For example it may be waiting for
    information from other components, a network socket or the user)

Component Activation

-   If the value yielded is a newComponent object, the components
    contained within that object are activated (essentially their main()
    method is called, and the resulting generator stored in the run
    queue).

Component Deactivation

-   If the value yielded is false, the component is removed from the run
    queue
-   If the component allows an exception to emerge from the generator
    for whatever reason it is also deemed to have exited.

[Scheduler: Scheduling policy]{style="font-weight:600"}

The scheduler in Axon is in practice currently a very primitive
linear/roundrobin scheduler. If the scheduler has 10 things to run,
currently it runs them all one after another repeatedly with no change
in order. This particular policy is not however guaranteed to stay the
same but was chosen for simplicity and fairness.

[Axon: Linkages]{style="font-weight:600"}

Given the components may run in parallel we need a mechanism for
enabling connections between components. Linkages form this mechanism,
and unlike components and the scheduler are traditional passive objects.

Linkages normally join outboxes to inboxes between components. However
when dealing with connections to sub-/nested/child components
outbox-outbox and inbox-inbox connections make sense. In the case where
there is a link between a component and a nested component the parent
components inbox (or outbox) associated with the name of that box is
prefixed by an underscore by convention to indicate an internal linkage.

Linkages can currently only be created inside a component. Therefore in
order to create a pipeline of 5 components, that pipeline must itself be
a component.

Linkages are therefore our mechanism for forming composition of
components, and this approach or components not knowing who they are
linked to tends to encourage reuse of components.

[Linkage: Example]{style="font-weight:600"}

Take for example the following simple streaming client:

<div>

class SimpleStreamingClient(component):

</div>

<div>

def main(self):

</div>

<div>

client = TCPClient(\"127.0.0.1\", 1500)

</div>

<div>

decoder = VorbisDecode()

</div>

<div>

player = AOAudioPlaybackAdaptor()

</div>

<div>

self.link((client, \"outbox\"), (decoder, \"inbox\"))

</div>

<div>

self.link((decoder, \"outbox\"), (player, \"inbox\"))

</div>

<div>

</div>

<div>

self.addChildren(decoder, player, client)

</div>

<div>

yield newComponent(decoder, player, client)

</div>

<div>

while 1:

</div>

Since it is contructed from a number of components, it too must be a
component. The component creates 3 components - one for connecting to
the server, one for decoding and one for playback. These are then linked
together, and activated by yielding them back to the scheduler. After
that, the only purpose of this component is to acts as a shell. As a
result, it returns control to the scheduler and hints
([self.pause()]{style="font-family:Courier"}) that it no longer needs
any CPU time.

Similarly a server capable of serving an adhoc file to this simple
client might look like this:

<div>

def AdHocFileProtocolHandler(filename):

</div>

<div>

class klass(Kamaelia.ReadFileAdaptor.ReadFileAdaptor):

</div>

<div>

def \_\_init\_\_(self, \*argv, \*\*argd):

</div>

<div>

return klass

</div>

<div>

class SimpleStreamingServer(component):

</div>

<div>

def main(self):

</div>

<div>

server = SimpleServer(protocol=AdHocFileProtocolHandler(\"foo.ogg\"),

</div>

<div>

port=clientServerTestPort)

</div>

<div>

self.addChildren(server)

</div>

<div>

yield \_Axon.Ipc.newComponent(server)

</div>

<div>

while 1:

</div>

What this example does is to use the generic simple server component for
the bulk of the network handling. When a client connects however the
server needs to be able to create components for handling the
connection. Specifically these components handle the actual protocol for
speaking to the client over the network connection. As a result the
protocol argument takes a class reference to allow protocol objects to
be created.

In this particular case, the protocol class is created dynamically and
will always create a component that reads the file foo.ogg, and sends it
at a constant bit rate to it\'s outbox.

What this means is in practice when a client connects to the port the
server is listening on, the specified protocol component will be created
and recieve network data on it\'s inbox and any data it sends to it\'s
outbox will be sent to the client. This enables a wide range of
behaviours to take place and to be tested in complete isolation from the
network.

[Linkage Example: Re-use]{style="font-weight:600"}

Suppose however that rather than connecting to a TCP based server, we
wanted to modify out simple streaming component to connect to a
multicast session instead, decode and play that back. The following code
snippet shows in bold the required changes to the program:

<div>

class SimpleStreamingClient(component):

</div>

<div>

def main(self):

</div>

<div>

[client = Multicast\_transceiver(\"0.0.0.0\", 1600, \"224.168.2.9\",
0)]{style="font-weight:600"}

</div>

<div>

[adapt = detuple(1)]{style="font-weight:600"}

</div>

<div>

decoder = VorbisDecode()

</div>

<div>

player = AOAudioPlaybackAdaptor()

</div>

<div>

self.link((client, \"outbox\"), ([adapt]{style="font-weight:600"},
\"inbox\"))

</div>

<div>

self.link(([adapt]{style="font-weight:600"}, \"outbox\"), (decoder,
\"inbox\"))

</div>

<div>

self.link((decoder, \"outbox\"), (player, \"inbox\"))

</div>

<div>

</div>

<div>

self.addChildren(decoder, [adapt, ]{style="font-weight:600"}player,
client)

</div>

<div>

yield newComponent(decoder, [adapt, ]{style="font-weight:600"}player,
client)

</div>

<div>

while 1:

</div>

<div>

yield 1

</div>

Essentially we have simply done the following:

-   Instead of creating a TCPClient, we have created a
    Multicast\_transceiver component
-   The multicast\_transceiver component sends tuples of (sender, data)
    to its output. This is largely because data recieved over a
    multicast socket is a UDP socket which isn\'t connected.
-   In order to extract the data from this tuple as part of the decode
    chain we simply chain the data from the Multicast\_transceiver into
    a detuple component.
-   The rest of the decode chain then remains the same

As a result, not only have we been able to largely reuse the bulk of the
streaming server client, but also we have used the decoding and playback
components unchanged.

[Co-ordinating Assistant Tracker]{style="font-weight:600"}

Finally we have the co-ordinating assistant tracker. Essentially this
tracks two distinct types of values in an Axon system: values and
services.

[Values]{style="font-weight:600"}

The cat tracks values associated with keys. This provides facilities
[similar]{style="font-style:italic"} to environment variables (or a
linda tuple space) and is intended to facilitate the collection of stats
in network servers. At present not many components make use of this
facility, but experience with similar systems imply that this is needed.

[Services]{style="font-weight:600"}

A service is a name given to a [(component,
inbox)]{style="font-family:Courier"} tuple. This allows a component to
advertise a service upon which it may expect values to be sent. This
facility is deliberately modelled on the concept of named ports in
AmigaOS and can be viewed as similar to services in a rendevous/zero
conf environment.

Components can contact request access to a service via the CAT by name
and then make use of the service. If the component requires
communication back to itself from the service, it can send the service a
service.

Whilst sounding hideously recursive and theoretical, services were borne
out of a very specific realworld usecase:

-   Suppose we have 2 server components in a system.
-   Both of these will have a number of active sockets, which are
    traditionally managed via a select call. In Axon this maps directory
    to a selector component that simply tracks sockets and sends
    components managing those sockets \"data ready\" messages in order
    activate them.
-   Clearly if we have 2 (or more) servers in a system they could all
    share the same selector component.
-   At this point in time we have the problem about how we will find
    this single selector component. We
    [could]{style="font-style:italic"} enforce this on users of the
    selector component using a singleton pattern, but we want components
    to be generic. The alternative is to allow a selector to register
    somewhere that it exists and that it is willing to handle arbitrary
-   connections.

Services provide a way of allow components to share active
functionality:

-   As a server starts up, it can then check for the existance of a
    selector service. Since none exists, it creates a selector
    component. That selector component registers itself as a service
    with the CAT.
-   The next server that starts up can also check for the existance of a
    selector. This server finds a selector service. It can then send
    that service a message stating \"wake me up on this inbox if you
    find a this socket\". It does this, effectively, by sending a
    reference to the socket, itself and the inbox name to the selector.
    (This is why we talk about sending a service to a service)

It\'s worth noting that the only one of these two components needs to
know how to create a selector component. It is possible that as time
progresses that this aspect of services may expand.

[Component Creation Howto]{style="font-size:17pt;font-weight:600"}

In this section we shall describe how to create a basic component that
deals with one of the most common network formats, and translates this
from textual form to a python dictionary.

MIME/RFC2822 type objects are common in network protocols, used in
email, web, usenet systems and several others.

Essentially this forms a collection of serialised key/value pairs. In
python the closest natural structure that is key/value based is the
\"dict\" type. This leads us to the idea that if we had a MIME Dict
component we could place this between network connections handling
components and other components.

This \"MIME Dict\" component should:

-   Accept dict like objects, but translates them to MIME-like messages
-   Accept MIME-like messages and converts them to dicts.

[MimeDictComponent]{style="font-weight:600"}

The MimeDictComponent is a real component in Kamaelia, and we\'re largly
going to discuss how it was written, rather than laboriously go through
code (The code is always available in CVS and releases).

The basic approach was as follows. The core functionality was written
first. That is we first created a component that subclassed dict. The
\_\_str\_\_ method was replaced with a custom implementation that
returned an RFC2822/MIME style message. After that was written, a
staticmethod \"fromString\" was added to the MimeDict class that could
accept an RFC2822/MIME style message.

A further key point is that all this code was written entirely test
first, with no special considerations.

Only after the basic class was able to perform the desired
transformation did we consider the specific interface that the component
may need. It\'s worth noting that should this interface have required
changes to the MimeDict class these would have been added as tests to
the test suite for MimeDict first and implemented independently of the
component system.

When designing the MimeDictComponent we needed to decide what interface
we desired from the system. Specifically this relate to the inboxes and
outboxes on the component, and what data we expect to send/receive
to/from the component. We decided upon the following interface:

-   [control]{style="font-weight:600"} - on which we may recieve a
    shutdown message
-   [signal]{style="font-weight:600"} - one which we will send shutdown
    messages
-   [demarshall]{style="font-weight:600"} - an inbox to which you send
    strings for turning into dicts
-   [demarshalled]{style="font-weight:600"} - an outbox which spits out
    parsed strings as dicts
-   [marshall]{style="font-weight:600"} - an inbox to which you send
    objects for turning into strings
-   [marshalled]{style="font-weight:600"} - an outbox which spits out
    translated dicts as strings

The irony here though is that it turned out to be simpler to create a
generic marshalling component instead. During creation we pass over a
reference to the MimeDict. Then the generic marshalling code would use
the facilities of the MimeDict class to perform the actual
transformations detailed above.

For example, the main loop of the component ended up looking like this:

<div>

while 1:

</div>

<div>

self.pause()

</div>

<div>

if self.dataReady(\"control\"):

</div>

<div>

data = self.recv(\"control\")

</div>

<div>

if isinstance(data, Axon.Ipc.producerFinished):

</div>

<div>

if self.dataReady(\"marshall\"):

</div>

<div>

if self.dataReady(\"demarshall\"):

</div>

<div>

yield 1

</div>

For the specific marshaller that we wanted we could then take a
traditional subclassing style of approch:

<div>

class MimeDictMarshaller(MarshallComponent):

</div>

<div>

def \_\_init\_\_(self, \*argv, \*\*argd):

</div>

Or we could choose a class decoration approach:

<div>

def MarshallerFactory(klass):

</div>

<div>

class newclass(MarshalComponent):

</div>

<div>

def \_\_init\_\_(self, \*argv, \*\*argd):

</div>

<div>

return newclass

</div>

<div>

</div>

<div>

MimeDictMarshaller = MarshallerFactory(MimeDict)

</div>

It is interesting to note that this approach encouraged naturally the
creation of a generic component that allows for greater use of
non-component based code in the component framework.

[Summary: New Components]{style="font-weight:600"}

This has been a relatively high level brief overview of how to go about
designing and implementing a component. There is a longer tutorial on
the Kamaelia website revolving around creating a multicast transceiver.
Again, that code was designed and written using much the same approach:

-   Don\'t worry about concurrency, write single threaded
-   When the code works, then convert to components
-   Change control methods into inboxes/outboxes

[Ease of use Hypothesis]{style="font-size:17pt;font-weight:600"}

As noted we have hypothesised that using simple components communicating
to/from local inboxes/outboxes composed into systems may be simpler to
work with when building concurrent systems than traditional approaches.

We were recently able to test this hypothesis on a pre-university
trainee, who was happy to let me describe him as a novice programmer.
We\'ll call him \"C\" for the rest of this document. Prior to joining
our group \"C\" had done A-Level computer studies. This involved a small
amount of Visual Basic programming and creating a small Access database.

This trainee had a 3 month placement within our group which involved the
following:

Started off learning python & axon (2 weeks)

Created a \"learning system\" based around parsing a Shakespeare play:

-   Performs filtering, character identification, demultiplexing, etc
-   Used pygame for display, stopped short of using pyTTS\...

As well as working on his main project

The project we set \"C\" was something you would not normally give to a
novice programmer with \"C\"\'s background.

We asked him to created a simplistic low bandwidth video streamer, based
on a scalable architecture. The server would have an MPEG video, and
take a frame as JPEG every n seconds. This is sent to the client over a
framing protocol Ciaran designed and implemented. The client then
displays the images as they arrive. The client systems \"C\" would be
required to implement would be both PC based for testing, with the
primary target platform being series 60 mobiles.

The idea is this simulates previewing PVR content on a mobile.

The project was successful, \"C\" achieved the goals, and wrote
components satisfying every part of that of the description. For network
handling \"C\" was able to use the \"SimpleServer\" and simple
\"TCPclient\" components. It is also interesting to note that rather
than finding this a frustrating experience (given his background) that
he found the experience fun.

It would be interesting to retry this experiment, both with
Axon/Kamaelia and other frameworks for clients and servers.

[CSP vs State Machines]{style="font-weight:600"}

From a performance perspective the question arises: is a CSP based
approach - such as that taken by Axon - better or worse than a state
machine style system? At present we would suggest that neither is better
or worse than the other - at least theoretically.

After all, state machine systems often have intermediate buffers (even
single variables) for handoff between states and state machines. In many
respects this is akin to outboxes and inboxes. If they are collapsed
into one, as planned, this is probably as efficient as traditional
frameworks.

We have now performed some preliminary tests using a simpified version
of the component system and it does tend to imply that collapsing
outbox/inbox pairs into one is effectively as efficient as the
non-componentised system. The difference of course is that the
componentised system is easy to reuse.

[Integration with other systems]{style="font-weight:600"}

Kamaelia does not exist in a void. Having the ability to assimilate code
and functionality from other systems easily and quickly is something
needed by Kamaelia. Given that python generators do not exist in other
languages we need a default mechanism for interacting with traditional
procedural languages.

By providing this we provide a mechanism for components to be written in
languages other than python providing an incremental optimisation step
where needed.

The mechanism we provide is a default main generator which unless
overridden by a subclass calls 3 default callback:

-   initialiseComponent()
-   mainBody()
-   closeDownComponent()

The reason for just these 3 callbacks is because every program that
exists essentially matches the following underlying structure:

<div>

perform some initialisation

</div>

<div>

loop until some condition is true:

</div>

<div>

perform shutdown code

</div>

Sometimes different parts of this template program may be empty. For
example crash based systems are designed never to shutdown - only to
recover from crashes, and the simple \"hello world\" program generally
has an empty loop and no shutdown. Nevertheless many programs can be
brought down to these 3 phases of a program.

This logic, is mananged by the default [main
]{style="font-family:Courier"}generator, which looks like this:

def main(self):

<div>

result = self.initialiseComponent()

</div>

<div>

if not result: result = 1

</div>

<div>

yield result

</div>

<div>

while(result):

</div>

<div>

result = self.mainBody()

</div>

<div>

if result:

</div>

<div>

yield self.closeDownComponent()

</div>

You\'ll note that any returned value from a callback is yielded back to
the scheduler allowing components using the callback form to start new
components as required.

The secondary advantage of also having this callback mechanism in
addition to the generator approach is that some programmers simply find
a callback approach easier to work with. As a result having this call
back approach as well as the generator approach is extremely useful.

[Futures]{style="font-size:17pt;font-weight:600"}

Currently the version number of Kamaelia, whilst stable and useful
stands at 0.1.2. We there see a lot of enhancements to come to both Axon
and Kamaelia before we reach a 1.0 release which we consider feature
stable and sufficiently complete. This section details a few of the
areas which we may extend Kamaelia and Axon into given sufficient
interest and resources.

[Axon for C++]{style="font-weight:600"}

We do not wish the approach and benefits we have found in Axon/Kamaelia
to simply limited to those using the python language. As a result, when
adding features we have often considered \"how could this be implemented
in other languages\". With regard to python\'s generators, one can use
Duff\'s device to implement generator like functionality in C++.

As a proof of concept, we have produced a simple and naive translation
of a \"mini-axon\" system into C++. This is complete using generators. A
simple producer component using this C++ version of mini-axon looks like
this:

One interesting target system for a C++ based system using Axon would be
IBM\'s CELL processor, which is most notably known for powering Sony\'s
PS3. We currently hypothsis that Axon\'s dataflow architecture would be
a very good match for the dataflow architecture inside the CELL CPU.

[Axon Optimisations, Updates]{style="font-weight:600"}

Axon as it currently stands focusses on correctness and safety over
speed. One example of this is that linkages are currently registered
with a Postman who then manages deliveries from outboxes to inboxes.
This process involves copying of data from outboxes to inboxes.

One optimisation that can be made here for example is to collapse
inboxes into outboxes. Some initial tests with a model implementation of
a subset of Axon suggest that this does indeed bring performance
benefits, and is a worthwhile optimisation. When the issues in
collapsing inboxes into outboxes are sufficiently well understoof they
will be merged into Axon.

Similarly, at present some parts of Axon\'s API, and creation of
pipelines can be clunky, and so we are examining how to make this
clearer and easier to read.

[Automated Component Distribution over
Clusters]{style="font-weight:600"}

Since components in Axon only communicate with other components over
local interfaces, they have no way of knowing whether the component
they\'re communicating with is on the same machine or not. Indeed this
very fact makes the creation and testing of protocols fairly simple -
you simply test the client protocol handler and server protocol handlers
by joining their in/out-boxes together. When that works you simply place
the client & server protocol handlers in generic client and server code
on different machines.

This opens up the possibility of running entire axon systems over
clusters of machines transparently - Axon is designed of course to work
well with a single CPU system, but could be used to scale over clusters.
One method that would be needed here is opaque component creation, and
one method that may be of use here is to extend the services model of
the co-ordinating assistant tracker.

Automated component distribution over clusters would also assist in
naturally taking advantage of systems like the CELL CPU.

[Kamaelia Component Repository]{style="font-weight:600"}

A component system is only as useful as the components available in that
system. As a result the main focus of Kamaelia at present is on creating
new components useful in specific real world systems that BBC R&D needs.
However a standard repository (but perhaps not centralised) for
components such that people can find new components quickly and easily
to solve their task would magnify the value of Kamaelia/Axon
significantly.

At present the Kamaelia project itself is a component repository, but we
would be extremely interested in proposals that encourage sharing and
reuses between groups.

[More Concurrency Tools]{style="font-weight:600"}

The current releases of Kamaelia only include support for components
written as either generators or using the callback mechanism. In CVS we
have support for components written to use threading instead of
generators, and these are focussed around dealing with objects that can
only be used in a blocking manner. (The impetus for this was due to the
socket module in the Nokia Series 60 implementation of python not
supporting non-blocking sockets)

Other concurrency tools we\'d be interested in seeing back components
for would be:

-   Operating system level processes
-   Greenlets - essentially an implementation of coroutines for python
-   Twisted objects. (We see no reason why Axon/Kamaelia should compete
    with alternative frameworks and favour collaboration/co-operation)

[Extensions to Kamaelia: More protocols, experimental
servers]{style="font-weight:600"}

Since we\'re working on scaling delivery of BBC content, and believe
there to be issues with some of the existing open protocols for
streaming the best way to demonstrate this is to implement these
protocols and show what happens.

Initially we are implementing RTSP/RTP for streaming Ogg Vorbis, and
after that will work on other protocols. As well as this we need to
build support for experimentation with different protocols for peer to
peer and collaborative client hub systems.

[Finally, Collaboration]{style="font-weight:600"}

If you\'re interested in working with us, please do: join the mailing
list, download, the code, play with it and if you wnat to write docs,
code, components, or constructive feedback, please do. If you want to
explore some of the more \"future\" oriented ideas rather than work on
the stablising the code base, you\'re more than welcome.

If you find the code looks vaguely interesting, please use and give us
feedback. We\'re very open to exploring changes to the system and
willing to give people CVS commit access in order to try their ideas,
within some fair and free bounds.

Anyone working with alternative frameworks for single threaded
concurrency is [very]{style="font-style:italic"} welcome to come and
criticise and suggested new ideas. If you would like to integrate our
system with yours that would be extremely interesting.

Contacts, project blog:

-   michaels\@rd.bbc.co.uk, kamaelia-list\@lists.sourceforge.net
-   http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi
