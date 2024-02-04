---
pagename: Kamaelia-0.2.0-ReleaseNotes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Release Notes]{style="font-size:24pt;font-weight:400"}

[Kamaelia 0.2.0 ]{style="font-size:18pt"}

[SUMMARY]{style="font-size:18pt;font-weight:600"}

[New Examples]{style="font-size:14pt"}

4 new examples showing of various new subsystem:

[Example 5]{style="font-weight:600"} : An introspecting version of
Examples 2/3. This creates a simple streaming system, and looks inside
to see what components are running/active, and passes the resulting
information over a network connection to an Axon Visualisation server.

[Example 6]{style="font-weight:600"} : This is a simple/generic topology
visualisation server. The server listens on port 1500, and accepts the
following commands:

::: {dir="ltr"}
As this stands this is pretty useful, but that\'s pretty much everything
it does like this.
:::

[Example 7]{style="font-weight:600"} : This shows how the visualisation
subsystem can be extended to work in different ways. What this does by
default when run is randomly create new nodes and new linkages quite
quickly, allowing you to see how the system works.

[Example 8]{style="font-weight:600"} : Sample slideshow/presentation
tool. Unlike traditional slideshow/presentation tools, you can modify
this to run arbitrary components. An example of how this can work is
provided - allowing stepping through some graph visualisations along
with the presentation.

[New Tools]{style="font-size:14pt"}

[Axon Shell]{style="font-weight:600"}. Implements a simple command line
shell which allows experimentation with Axon systems - the shell runs a
scheduler in the background. For a tutorial of use, see:

-   <http://kamaelia.sourceforge.net/AxonShell.html>

[Axon Visualiser. ]{style="font-weight:600"}Implements a simple tool for
looking inside (quite literally) running Axon/Kamaelia systems. This
allows a very different style of debugging and can be extremely useful.
Tutorial on its way!

[Graphlines and Pipelines]{style="font-size:14pt"}

These are probably the most useful additions to Kamaelia since 0.1.2.
They are essentially syntactic sugar for building and working with
systems of components, but make building interesting systems rapidly out
of pre-existing components fun and easy. The pipelines follow the same
sort of model as the Unix pipeline. Graphlines are something new, and
like pipelines and all linkages may take
[any]{style="font-style:italic"} data along them.

They\'re also probably best explained by example, so since these are
release notes, I\'ll just present a couple of examples here.

A graphline representing a simple presentation tool:

<div>

[Graphline(]{style="font-family:Courier"}

</div>

<div>

[CHOOSER = Chooser(items = files),\
IMAGE = Image(size=(800,600), position=(8,48)),\
NEXT = Button(caption=\"Next\", msg=\"NEXT\", position=(72,8)),\
PREVIOUS = Button(caption=\"Previous\", msg=\"PREV\",position=(8,8)),\
FIRST = Button(caption=\"First\", msg=\"FIRST\",position=(256,8)),\
LAST = Button(caption=\"Last\", msg=\"LAST\",position=(320,8)),\
linkages = {]{style="font-family:Courier"}

</div>

<div>

[}]{style="font-family:Courier"}

</div>

[ ).run()]{style="font-family:Courier"}

A pipeline representing a trivial multicast streaming server

<div>

[pipeline(]{style="font-family:Courier"}

</div>

::: {dir="ltr"}
[).activate()]{style="font-family:Courier"}
:::

A pipeline representing a trivial multicast streaming client:

<div>

[pipeline(]{style="font-family:Courier"}

</div>

::: {dir="ltr"}
[).run()]{style="font-family:Courier"}
:::

[New Packages & Subsystems]{style="font-size:14pt"}

These names should provide you with a flavour of the new subsystems that
have been added:

[New Components]{style="font-size:14pt"}

This section gives an overview of what\'s new in terms of actual new
files.

Examples/ \-- example5, example6, example7, example8

Kamaelia/Data/ \-- MimeDict.py

Kamaelia/Internet/ \-- ThreadedTCPClient.py

Kamaelia/ \-- SingleServer.py

Kamaelia/Physics/ \-- \_\_init\_\_.py

-   Kamaelia/Physics/Simple/ \-- \_\_init\_\_.py, MultipleLaws.py,
    Particle.py, ParticleSystem.py, SimpleLaws.py, SpatialIndexer.py

Kamaelia/UI/ \-- \_\_init\_\_.py, PygameDisplay.py

-   Kamaelia/UI/Pygame/ \-- Ticker.py, Multiclick.py, Image.py,
    Button.py
-   Kamaelia/UI/MH/ \-- \_\_init\_\_.py, PyGameApp.py, DragHandler.py

Kamaelia/Util/ \-- Chooser.py, Comparator.py, Graphline.py,
Introspector.py, LossyConnector.py, MarshallComponent.py,
NullSinkComponent.py, passThrough.py, PipelineComponent.py, Splitter.py,
TestResultComponent.py

Kamaelia/Visualisation/ \-- \_\_init\_\_.py

-   Kamaelia/Visualisation/Axon/ \-- \_\_init\_\_.py, AxonLaws.py,
    AxonVisualiserServer.py, ExtraWindowFurniture.py, PComponent.py,
    PPostbox.py
-   Kamaelia/Visualisation/PhysicsGraph/ \-- \_\_init\_\_.py,
    chunks\_to\_lines.py, lines\_to\_tokenlists.py, GridRenderer.py,
    ParticleDragger.py, RenderingParticle.py,
    TopologyViewerComponent.py, TopologyViewerServer.py

[Changed & Updated]{style="font-size:14pt"}

All updated siles & classes at a glance:

-   Examples/ \-- example1, example2, example3, example4
-   Kamaelia/Util/ \-- ConsoleEcho.py, Chargen.py
-   Kamaelia/Protocol/ \-- AudioCookieProtocol.py,
    EchoProtocolComponent.py, FortuneCookieProtocol.py, HTTPServer.py
-   Kamaelia-0.2.0/Kamaelia/ \-- ReadFileAdaptor.py,
    SampleTemplateComponent.py, MimeRequestComponent.py,
    SimpleServerComponent.py, test/SynchronousLinks\_SystemTest.py
-   Kamaelia/Internet/ \-- ConnectedSocketAdapter.py,
    Multicast\_receiver.py, Multicast\_sender.py,
    Multicast\_transceiver.py, Selector.py, TCPClient.py, TCPServer.py,
    test/test\_BasicMulticastSystem.py
-   Docs/index.html

[Large scale common changes]{style="font-weight:600"}

-   All classes changed from using self.\_\_super to using super(klass,
    self) \... on the advice of Michele Simionato

[Detailed Release Notes]{style="font-size:18pt;font-weight:600"}

[Kamaelia-0.2.0/AUTHORS]{style="font-weight:600"}

Modified

-   Joseph Lord (Moved on from BBC R&D)

Added

-   Matt Hammond, BBC R&D
-   Ciaran Eaton (Pre-University Trainee @ BBC R&D)
-   Tom Gibson (Vacation Trainee @ BBC R&D)
-   Gintautas Miliauskas, Programmers of Vilnius- first external
    contributor (Debian Packaging!)

[Kamaelia-0.2.0/CHANGELOG]{style="font-weight:600"}

-   Overview of some of the key changes

[NEW STUFF!]{style="font-size:18pt;font-weight:600"}

[Kamaelia-0.2.0/Examples/example5/]{style="font-weight:600"}

This is a new example, it is an introspecting version of the
SimpleStreamingSystem.py examples. This allows you to see inside a
running streamer server and client system and see what\'s actually
happening inside.

It is essentially very similar to the old version of Example2, but with
the addition of introspection components

New files:

-   IntrospectingSimpleStreamingSystem.py
-   README

[Kamaelia-0.2.0/Examples/example6/]{style="font-weight:600"}

This is a new example - a topology visualiser. This takes textual
commands from a single socket and renders the resulting graph.

Example

-   ADD NODE id1 label1 auto -
-   ADD NODE id2 label2 auto -
-   ADD LINK id1 id2

This draw and lays out and simple system linking 2 nodes, using a simple
physics type engine for layout

New files:

-   TopologyVisualiser.py

[Kamaelia-0.2.0/Examples/example7/]{style="font-weight:600"}

This is a more complex (new) example of using the topology/graph viewing
code. It extends the system to add in some new node types/behaviour via
the code in the BasicGraphVisualisation directory.

New files:

-   BasicGraphVisualisation.py
-   BasicGraphVisualisation/\_\_init\_\_.py
-   BasicGraphVisualisation/ParticleDragger.py
-   BasicGraphVisualisation/PhysApp1.py
-   BasicGraphVisualisation/VisibleParticle.py

[Kamaelia-0.2.0/Examples/example8/]{style="font-weight:600"}

Another new example - this one showing how to bolt together existing
Pygame based components using the simplistic \"window\" manager (more
surface manage really) to place mutiple buttons, image viewers etc into
a single display, and link them together tio form a simple slideshow
tool, which can be used for presentations. Includes a small number of
slides from the Europython talk about Kamaelia.

This is also probably the nicest example (and the first example) of how
a Graphline can be of real use to make a system more declarative and
clearer.

New files:

-   slideshow.py - \"Just\" a slideshow/presentation tool
-   topology.py - \"Just\" a slideshow/presentation tool for showing
    structural diagrams clearly, and maniupulable
-   topology\_slideshow.py - comination showing how one tool can be
    overlaid on top of another forming a more useful, more general tool
    for doing presentations.
-   README
-   Slides/KamaeliaEuropython2005.001.gif
-   Slides/KamaeliaEuropython2005.016.gif
-   Slides/KamaeliaEuropython2005.021.gif
-   Slides/KamaeliaEuropython2005.030.gif
-   Slides/KamaeliaEuropython2005.036.gif
-   Slides/KamaeliaEuropython2005.039.gif

[Kamaelia-0.2.0/Examples/README]{style="font-weight:600"}

Updated to document the 4 new examples. Copied here for convenience.

[Example 5]{style="font-weight:600"} : An introspecting version of
Examples 2/3. This creates a simple streaming system, and looks inside
to see what components are running/active, and passes the resulting
information over a network connection to an Axon Visualisation server.

[Example 6]{style="font-weight:600"} : This is a simple/generic topology
visualisation server. The server listens on port 1500, and accepts the
following commands:

::: {dir="ltr"}
As this stands this is pretty useful, but that\'s pretty much everything
it does like this.
:::

[Example 7]{style="font-weight:600"} : This shows how the visualisation
subsystem can be extended to work in different ways. What this does by
default when run is randomly create new nodes and new linkages quite
quickly, allowing you to see how the system works.

[Example 8]{style="font-weight:600"} : Sample slideshow/presentation
tool. Unlike traditional slideshow/presentation tools, you can modify
this to run arbitrary components. An example of how this can work is
provided - allowing stepping through some graph visualisations along
with the presentation.

[Kamaelia-0.2.0/Kamaelia/Data/MimeDict.py]{style="font-weight:600"}

-   New data type for representing dictionaries as mime-like objects.
    Allows for simple transformation of a dict to a mime-like object
    (via [str()]{style="font-family:Courier;font-weight:600"} ), and
    from a suitable string. This is designed to support implementing
    (via specialisation) HTTP, SMTP, and NNTP objects.

[Kamaelia-0.2.0/Kamaelia/Internet/ThreadedTCPClient.py]{style="font-weight:600"}

New component

-   This allows you to have a TCP Client running, but in a different
    thread. This allows for blocking actions.
-   This is also probably the first/only usage to date of the threaded
    component class in Axon.
-   There may therefore be minor issues with this class.

Provides the same interface from a component user perspective to the
TCPClient.py class

Originally written because at the time Nokia Series 60 mobiles only
supported blocking sockets.

[Kamaelia-0.2.0/Kamaelia/Physics/\_\_init\_\_.py]{style="font-weight:600"}

-   New subsystem
-   Introduction of a simple physics system for use with the topology
    viewer code. This may be in the wrong location, but it\'s an initial
    starting point

[Kamaelia-0.2.0/Kamaelia/Physics/Simple/\_\_init\_\_.py]{style="font-weight:600"}

-   New subsystem
-   Just the \"Simple\", basic set of laws for now.

[Kamaelia-0.2.0/Kamaelia/Physics/Simple/MultipleLaws.py]{style="font-weight:600"}

New subsystem

Physics code for forces between particles. Unbonded force acts between
all non bonded particles. Bonded force acts between bonded particles.
Contains the following classes:

-   MultipleLaws(typesToLaws, defaultLaw = None):\
    Laws framework for systems containing multiple particle types\
    \
    typesToLaws = dictionary mapping particle type name pairs (type1,
    type2) to laws if you supply a pairing (t1, t2) it will also be
    applied to the case (t2,t1) without you needing to explicitly
    specify it. If you do, then your choice takes precedence.\
    \
    If you do not provide enough mappings to build a complete mapping
    from all types to all types, then the gaps will be automatically
    filled with mappings to defaultLaw.

[Kamaelia-0.2.0/Kamaelia/Physics/Simple/Particle.py]{style="font-weight:600"}

New subsystem

Physics code for forces between particles. Unbonded force acts between
all non bonded particles. Bonded force acts between bonded particles.
Contains the following classes:

-   Particle - Particle within a physics system with an arbitrary number
    of dimensions.\
    \
    Represents a particle that interacts with other particles. One set
    of forces are applied for those particles that are unbonded.
    Interactions between bonded particles are controlled by another set
    of forces.\
    \
    Bonds are bi-directional. Establishing a bond from A to B, will also
    establish it back from B to A. Similarly, breaking the bond will do
    so in both directions too.

[Kamaelia-0.2.0/Kamaelia/Physics/Simple/ParticleSystem.py]{style="font-weight:600"}

New subsystem

Contains class:

-   ParticleSystem(laws, initialParticles = \[\], initialTick = 0)\
    System of particles.\
    Maintains the set of particles and runs the physics simulation over
    them the specified laws.

[Kamaelia-0.2.0/Kamaelia/Physics/Simple/SimpleLaws.py]{style="font-weight:600"}

New subsystem

Contains class:

-   SimpleLaws(object):\
    Implements a simple set of physics laws for the particle system.\
    Repulsion force : force proportional to 1/distance\_squared\
    bonds : force proportional to extension (Hook\'s law)\
    \
    All force strengths etc. are set up to vaguely sensible values on
    the basis of the specified bond length.

[Kamaelia-0.2.0/Kamaelia/Physics/Simple/SpatialIndexer.py]{style="font-weight:600"}

New subsystem

Probably the most generally useful addition to the core of Kamaelia from
the Physics subsytem. Provides a Spatial Indexer class that:

-   Allows fast spatial lookups of entities - quickly find all entities
    within a given radius of a set of coordinates.\
    Optimised by specifying the most commonly used proximity distance.
    This affects the speed of lookups and the size of the internal data
    structure.\
    Entities must provide a getLoc() method that returns the coordinates
    as a tuple.\
    To first register entities or if they change coordinates, something
    must call updateLoc(\<entities\>). If entities are removed,
    something must call remove(\<entities\>)

[Kamaelia-0.2.0/Kamaelia/SingleServer.py]{style="font-weight:600"}

-   New component. This essentially can be used in the same manner as
    the server mode to \"netcat\"/\"nc\". That is it can be used in a
    pipeline, anything received from the
    [first]{style="font-style:italic;font-weight:600"} connection is
    forwarded to the outbox, anything received on the inbox is forwarded
    to that connection. It only handles one connection - hence the name
    \"[Single]{style="font-weight:600"}Server\"
-   Includes a simple example

[Kamaelia-0.2.0/Kamaelia/UI/\_\_init\_\_.py]{style="font-weight:600"}

-   New subsystem for user interfaces. (Normally graphical user
    interfaces)

[Kamaelia-0.2.0/Kamaelia/UI/MH/\_\_init\_\_.py]{style="font-weight:600"}

-   An experimental pygame based application subsystem

[Kamaelia-0.2.0/Kamaelia/UI/MH/DragHandler.py]{style="font-weight:600"}

-   Part of an experimental pygame based application handler subsystem
-   Examples 6,7 uses this class indirectly

[Kamaelia-0.2.0/Kamaelia/UI/MH/PyGameApp.py]{style="font-weight:600"}

-   Base class for Pygame Applications. This component is expected to be
    inherited by components.
-   Uses the new PygameDisplay service.
-   Thus any component using a PyGameApp can be composed onto a shared
    display and not worry about how it\'s sharing the display, and not
    worry about whether it\'s connected to another display component or
    a sink, or a socket, etc.
-   Used by example 5-8, and many components

[Kamaelia-0.2.0/Kamaelia/UI/Pygame/Button.py]{style="font-weight:600"}

-   Part of the new Pygame subsystem
-   Sits happily inside the PygameDisplay service
-   Implements a simple button. When clicked, sends a message to it\'s
    outbox \"outbox\"
-   Example 8 uses this component

[Kamaelia-0.2.0/Kamaelia/UI/Pygame/Image.py]{style="font-weight:600"}

Part of the new Pygame subsystem

Sits happily inside the PygameDisplay service

Implements a image display component.

-   When it receives a message on its inbox \"inbox\", it assumes it\'s
    a new filename, loads the image associated with the filename and
    updates it\'s display surface.

Example 8 uses this component

[Kamaelia-0.2.0/Kamaelia/UI/Pygame/Multiclick.py]{style="font-weight:600"}

-   Like button, but has different behaviours associated with different
    mouse buttons. Clicking a different button causes different messages
    to be sent. Can also be transparent to overlay other surfaces (this
    allows apparently global click handling)
-   This is used by a number of example presentation tools

[Kamaelia-0.2.0/Kamaelia/UI/Pygame/Ticker.py]{style="font-weight:600"}

-   Simple component that implements a simple \"ticking\" display - this
    can be used for display of text for presentations, subtitling (since
    the display can be transparent\...) and autocue/teleprompter
    behaviour.

[Kamaelia-0.2.0/Kamaelia/UI/PygameDisplay.py]{style="font-weight:600"}

Simple window/surface manager component.

Registers a service called \"pygamedisplay\", where components may
request a display from.

These displays are then blitted to the display once every tick of the
PygameDisplay component

Currently all events are global, but the pygame display could change
that.

Handles the farming out of pygame events to components as well.

-   Events are sent as bundles to try and manage mousemoveevents
    sensibly. (Work still needed there though)

Simple tests of bouncing surfaces (tickers, images) round the screeen
whilst the other components are running shows that this can happen
without confusing the components using those displays. (Largely due to
single writer semantics always being preserved)

Conceptually very similar to a TCP Server / primary listen socket vs
connected socket adaptor issue.

[Kamaelia-0.2.0/Kamaelia/Util/Chooser.py]{style="font-weight:600"}

-   New component
-   Chooses items out of a set, as directed by commands sent to its
    inbox\
    Emits the first item at initialisation, then whenever a command is
    received it emits another item (unless you\'re asking it to step
    beyond the start or end of the set)

[Kamaelia-0.2.0/Kamaelia/Util/Comparator.py]{style="font-weight:600"}

New component

This class was originally written to assist in testing by making it easy
to compare an expected data stream with that from the tested system.
This is the current equality test between the two inputs. It\'s been
realised however that this can be generalised by making an overidable
compare function to do the real work. This is therefore a general system
for combining two inputs into a single output!

-   You override the \"combine\" method (the default compares a==b, and
    returns a boolean, but could be anything - for example summation,
    etc)

[Kamaelia-0.2.0/Kamaelia/Util/Graphline.py]{style="font-weight:600"}

New component

Provides syntactic sugar for making pipeline type systems trivial, but
in the the form of arbitrary graphs, not just 1D pipes

Example 8 provides the nice example:

<div>

[Graphline(]{style="font-family:Courier"}

</div>

<div>

[CHOOSER = Chooser(items = files),\
IMAGE = Image(size=(800,600), position=(8,48)),\
NEXT = Button(caption=\"Next\", msg=\"NEXT\", position=(72,8)),\
PREVIOUS = Button(caption=\"Previous\", msg=\"PREV\",position=(8,8)),\
FIRST = Button(caption=\"First\", msg=\"FIRST\",position=(256,8)),\
LAST = Button(caption=\"Last\", msg=\"LAST\",position=(320,8)),\
linkages = {]{style="font-family:Courier"}

</div>

<div>

[}]{style="font-family:Courier"}

</div>

<div>

[).run()]{style="font-family:Courier"}

</div>

[Kamaelia-0.2.0/Kamaelia/Util/Introspector.py]{style="font-weight:600"}

-   New component. Much of the body of this will actually shift into
    Axon, but leave this component behind as a proxy.
-   \"This component introspects the current local topology of an axon
    system.\
    \
    Local? This component examines its scheduler to find components and
    postmen. It then examines them to determine their inboxes and
    outboxes and the linkages between them.\
    \
    If this component is not active, then it will see no scheduler and
    will report nothing.\
    \
    The output is a description of the a graph topology, where
    components and postboxes are the nodes, and their
    relationships/linkages form the links between them. As the shape of
    the graph changes, this component relays only the changes.\
    \
    The output format is a stream of strings, designed to be fed to an
    AxonVisualiserServer component.

[Kamaelia-0.2.0/Kamaelia/Util/LossyConnector.py]{style="font-weight:600"}

-   New component
-   This implements a \"lossy connector\". Currently much of Kamaelia
    works on the assumption that when you send to an outbox that there
    will always be space. However due to the existance of synchronised
    linkages, and maximum pipewidths, this may not actually be the case.
-   This component can be used as an intemediary that may drop messages
    if there is not space. One example usage of this might be to limit
    the amount of data that may be allowed into your inbox, then place
    the lossy connector before your input. This might mean that messages
    are lost, but in some circumstances this may not be an issue. (eg
    faking realtime encoding using a slow encoder)
-   If the recipient can receive the data fast enough this component
    essentially acts as a pass through.

[Kamaelia-0.2.0/Kamaelia/Util/MarshallComponent.py]{style="font-weight:600"}

New component

Basic Marshalling Component\
The Basic Marshalling Component is given a simple class. It then expects
to be passed objects of that class, and then performs the following
actions:

-   \_\_str\_\_ on an object
-   fromString on an object

<div>

</div>

<div>

The idea is that you would place this between your logic and a network
socket, which simply serialises and deserialises objects for
transmission over the wire. The initial data format this is designed to
work with is the MimeDict object.\
\
For simplicity, this component expects to be given an entire object to
marshall/demarshall. This requires the user to deal with framing of
objects. It is expected that there will be a more complex marshaller
that is capable of taking (say) a generator or component as an argument
for the fromString static method.\
\
Since this is a bidirectional component we have the following boxes:

</div>

-   control - on which we may receive a shutdown message
-   signal - one which we will send shutdown messages
-   demarshall - an inbox to which you send strings for demarshalling
-   marshall - an inbox to which you send objects for marshalling
-   demarshalled - an outbox which spits out demarshalled objects
-   marshalled = an outbox which spits out marshalled strings

[Kamaelia-0.2.0/Kamaelia/Util/NullSinkComponent.py]{style="font-weight:600"}

-   New component
-   Conceptually this provides the same device as the NULL device under
    windows, and /dev/null under Unix type systems
-   Any data received is thrown away - EXCEPT shutdownMicroprocess and
    producerFinished messages. If either of these are received on the
    \"control\" inbox, then the component shuts down

[Kamaelia-0.2.0/Kamaelia/Util/passThrough.py]{style="font-weight:600"}

-   New component
-   Simple passthrough component - a more generic version of the echoer
    component
-   Used during the small test suite for Kamaelia.Util.Pipeline

[Kamaelia-0.2.0/Kamaelia/Util/PipelineComponent.py]{style="font-weight:600"}

New component

Provides syntactic sugar for making pipeline type systems trivial.

A nice example is from example 4, where 2 pipelines are put together to
build a simplistic multicast streaming system as follows:

Server:

<div>

[pipeline(]{style="font-family:Courier"}

</div>

::: {dir="ltr"}
[).activate()]{style="font-family:Courier"}
:::

Client

<div>

[pipeline(]{style="font-family:Courier"}

</div>

::: {dir="ltr"}
[).run()]{style="font-family:Courier"}
:::

[Kamaelia-0.2.0/Kamaelia/Util/Splitter.py]{style="font-weight:600"}

-   New component
-   This component is likely to be replaced by another component with a
    similar, but possibly different interface.
-   This component allows the data from a single outbox to be sent to
    many inboxes. Tis version blocks all data if any of the outboxes
    have no space in them (in theory). Other versions could take other
    approaches such as dropping messages to those outboxes which are
    full.

[Kamaelia-0.2.0/Kamaelia/Util/TestResultComponent.py]{style="font-weight:600"}

New component

DO NOT USE IN LIVE SYSTEMS. This class is largely intended for use is
system testing and particularly unit testing of other components. In the
case of error or request it is intended to throw an exception stop the
Axon system and jump back to the unit test.

-   If this receives a FALSE value on it\'s inbox, this raises an
    [AssertionError]{style="font-family:Courier"} - it only expects true
    values.
-   If it receives a StopSystem exception on its inbox, it raises a
    StopSystemException.

[Kamaelia-0.2.0/Kamaelia/Visualisation/\_\_init\_\_.py]{style="font-weight:600"}

-   Base directory of the new visualisation/graphics subsystems

[Kamaelia-0.2.0/Kamaelia/Visualisation/Axon/\_\_init\_\_.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems

[Kamaelia-0.2.0/Kamaelia/Visualisation/Axon/AxonLaws.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Selection of simple physics laws to help modelling how to lay out
    different visual elements in when visualising an Axon system using
    the physics code. (eg inboxes, outboxes, etc)

[Kamaelia-0.2.0/Kamaelia/Visualisation/Axon/AxonVisualiserServer.py]{style="font-weight:600"}

-   New component
-   Subclasses TopologyViewerServer
-   Essentially runs a TopologyViewerServer with a collection of default
    rules some specialised particle types and specialised laws for
    dealing with laying out those particle types

[Kamaelia-0.2.0/Kamaelia/Visualisation/Axon/ExtraWindowFurniture.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Draws some extra window furniture (logos, lines as appropriate) for
    the display.

[Kamaelia-0.2.0/Kamaelia/Visualisation/Axon/PComponent.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Particle that represents a component in the Axon visualisation
    subsystem

[Kamaelia-0.2.0/Kamaelia/Visualisation/Axon/PPostbox.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Particle that represents an inbox/oubox (POSTBOX) in the Axon
    visualisation subsystem

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/\_\_init\_\_.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/chunks\_to\_lines.py]{style="font-weight:600"}

-   New Component, related to providing a convenient interface to the
    topology subsystem
-   Expects to receive non-line aligned data in chunks on its inbox
    \"inbox\" and spits out whole lines on its outbox \"outbox\".

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/lines\_to\_tokenlists.py]{style="font-weight:600"}

New component - related to provide a convenient interface to the
topology subststem.

Takes in lines and outputs a list of tokens on each line.\
\
Tokens are separated by white space.\
\
Tokens can be encapsulated with single or double quote marks, allowing
you to include white space. If you do this, backslashs should be used to
escape a quote mark that you want to include within the token. Represent
backslash with a double backslash.\
\
Example:

<div>

Becomes:

</div>

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/GridRenderer.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Simple grid drawing class facility. (used by the topology viewer)

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/ParticleDragger.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Implements dragging of particles.

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/RenderingParticle.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Version of Physics.Particle with added rendering functions. (Used to
    make a system visible, not just simulated)

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/TopologyViewerComponent.py]{style="font-weight:600"}

-   Part of the new visualisation/graphics subsystems
-   Generic Topology Viewer Component\
    \
    Displays a topology in a pygame application. It can be interacted
    with by dragging nodes with the mouse.\
    Receives command tuples on its inbox. See handleCommunication() for
    command syntax.\
    Outputs diagnostic and error messages on its outbox\
    See keyDownHandler() for keyboard controls.

[Kamaelia-0.2.0/Kamaelia/Visualisation/PhysicsGraph/TopologyViewerServer.py]{style="font-weight:600"}

-   New component, Part of the new visualisation/graphics subsystems
-   Builds a simple pipeline allowing the TopologyViewerComponent to
    take commands from a network connection and then update the display
    accordingly. This can be customised with new laws, particles etc,
    but can be used in it\'s basic form as a simple self laying out
    graph visualistaion tool.

[Kamaelia-0.2.0/Kamaelia/vorbisDecodeComponent.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/PKG-INFO]{style="font-weight:600"}

-   Automagically bumped by change to setup.py

[Kamaelia-0.2.0/setup.py]{style="font-weight:600"}

Added packages:

-   Kamaelia.Internet.Simulate
-   Kamaelia.UI
-   Kamaelia.UI.MH
-   Kamaelia.UI.Pygame
-   Kamaelia.Physics
-   Kamaelia.Physics.Simple
-   Kamaelia.Visualisation
-   Kamaelia.Visualisation.Axon
-   Kamaelia.Visualisation.PhysicsGraph

[Kamaelia-0.2.0/Tools/axonshell.py]{style="font-weight:600"}

New tool. Implements a simple command line shell which allows
experimentation with Axon systems - the shell runs a scheduler in the
background. For a tutorial of use, see:

-   <http://kamaelia.sourceforge.net/AxonShell.html>

[Kamaelia-0.2.0/Tools/AxonVisualiser.py]{style="font-weight:600"}

-   New Tool. Implements a simple tool for looking inside (quite
    literally) running Axon/Kamaelia systems. This allows a very
    different style of debugging and can be extremely useful. Tutorial
    on its way!

[UPDATED AND CHANGED]{style="font-size:18pt;font-weight:600"}

[Kamaelia-0.2.0/Kamaelia/Util/ToStringComponent.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/Util/ConsoleEcho.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   Change to the way objects can be sent to the console. Specifically
    the change is to allow the use of the \_\_repr\_\_ method of objects
    instead of the \_\_str\_\_ method - by calling repr() and str()
    respectively

[Kamaelia-0.2.0/Kamaelia/Util/Chargen.py]{style="font-weight:600"}

-   Copyright notice added (ie grants permissions not otherwise
    available)

[Kamaelia-0.2.0/Kamaelia/test/SynchronousLinks\_SystemTest.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/SimpleServerComponent.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   Variety of small changes relating to shutdown messages

[Kamaelia-0.2.0/Kamaelia/Protocol/AudioCookieProtocol.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/Protocol/EchoProtocolComponent.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/Protocol/FortuneCookieProtocol.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   Additional comments

[Kamaelia-0.2.0/Kamaelia/Protocol/HTTPServer.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   NB: this is incomplete and a work in progress (may change
    completely)

[Kamaelia-0.2.0/Kamaelia/ReadFileAdaptor.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/SampleTemplateComponent.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/MimeRequestComponent.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/Internet/test/test\_BasicMulticastSystem.py]{style="font-weight:600"}

-   Minor change wrt use of the scheduler

[Kamaelia-0.2.0/Kamaelia/\_\_init\_\_.py]{style="font-weight:600"}

-   Whitespace change

[Kamaelia-0.2.0/Kamaelia/Internet/ConnectedSocketAdapter.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   When the connection dies, for any reason, send a
    [shutdownCSA]{style="font-family:Courier;font-weight:600"} message
    to the signal outbox, rather than a
    [socketShutdown]{style="font-family:Courier;font-weight:600"}
    message

[Kamaelia-0.2.0/Kamaelia/Internet/Multicast\_receiver.py]{style="font-weight:600"}

Change from using self.\_\_super to using super(klass, self) \... on the
advice of Michele Simionato

-   This class will probably change in the next release to being a
    factory rather than a class, providing Multicast\_transceiver with
    some default arguments.

[Kamaelia-0.2.0/Kamaelia/Internet/Multicast\_sender.py]{style="font-weight:600"}

Change from using self.\_\_super to using super(klass, self) \... on the
advice of Michele Simionato

-   This class will probably change in the next release to being a
    factory rather than a class, providing Multicast\_transceiver with
    some default arguments.

[Kamaelia-0.2.0/Kamaelia/Internet/Multicast\_transceiver.py]{style="font-weight:600"}

Change from using self.\_\_super to using super(klass, self) \... on the
advice of Michele Simionato

Better handling when our sending fails first time round.

-   Code is written on the assumption of send failure, not on the
    assumption of success

[Kamaelia-0.2.0/Kamaelia/Internet/Selector.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   wireOutComponent rewritten. This removes any lookup table entries,
    unwires the component, and deletes any special in/outboxes created.
-   Small bugfix related to wiring in components using the service

[Kamaelia-0.2.0/Kamaelia/Internet/TCPClient.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Kamaelia/Internet/TCPServer.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   When shutting down, tell the selector that we\'re shutting down
-   When shutting down, any protocol handlers that we\'re shutting down
-   Linkage changes - signal has been split into \_selectorSignal and
    protocolHandlerSignal

[Kamaelia-0.2.0/Examples/example4/README]{style="font-weight:600"}

-   A note, essentially recommending installing ctypes on systems
    running Linux.

[Kamaelia-0.2.0/Examples/example1/FortuneCookie\_ServerClient.py]{style="font-weight:600"}

-   Changed to use the new pipeline syntactic sugar

[Kamaelia-0.2.0/Examples/example1/README]{style="font-weight:600"}

-   Whitespace change

[Kamaelia-0.2.0/Examples/example2/README]{style="font-weight:600"}

-   Whitespace change

[Kamaelia-0.2.0/Examples/example2/SimpleStreamingSystem.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   Change from using a wrapper component for testing to using
    standalone components and the new pipeline syntactic sugar

[Kamaelia-0.2.0/Examples/example3/README]{style="font-weight:600"}

-   Updated comment regarding the recommendation to using Axon 1.1.1,
    this makes the system much more self friendly - since the scheduler
    provides hints to the OS essentially saying \"you can interrupt now
    if you like\"

[Kamaelia-0.2.0/Examples/example3/SimpleStreamer.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   Change from using a wrapper component for testing to using simple
    standalone components

[Kamaelia-0.2.0/Examples/example3/SimpleStreamingClient.py]{style="font-weight:600"}

-   Change from using a wrapper component for testing to using
    standalone components and the new pipeline syntactic sugar

[Kamaelia-0.2.0/Examples/example4/MulticastStreamingClient.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato

[Kamaelia-0.2.0/Examples/example4/MulticastStreamingSystem.py]{style="font-weight:600"}

-   Change from using self.\_\_super to using super(klass, self) \... on
    the advice of Michele Simionato
-   Change from using a wrapper component for testing to using multiple
    simple pipelines (syntactic sugar)

[Kamaelia-0.2.0/Docs/index.html]{style="font-weight:600"}

-   Minor changes caused by changes to packaging
