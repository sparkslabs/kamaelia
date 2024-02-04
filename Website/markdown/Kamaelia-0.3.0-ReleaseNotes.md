---
pagename: Kamaelia-0.3.0-ReleaseNotes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Release Notes]{style="font-size:24pt;font-weight:600"}

[0.3.0]{style="font-size:18pt"}

[Summary]{style="font-size:18pt;font-weight:600"}

[New Examples]{style="font-size:14pt"}

7 new examples including:

-   Simple reliable multicast based streamer using Ogg Vorbis.
-   Dirac Player
-   Dirac encode & playback.
-   Simple bouncing images game. Designed for very small children who
    are amused by things take beep and react when you press left/right
    mouse buttons.
-   Simple example showing how to use the ticker (First developed for
    showing subtitles).
-   Demonstration system showing how to use the new software chassis
    facility in the context of multiple chassis.

[New Tools, Notable Additions]{style="font-size:14pt"}

-   Visual tool for building Kamaelia pipelines
-   Tk Support
-   Video encode, decode and playback.

[New Packages & Subsystems]{style="font-size:14pt"}

These names should provide you with a flavour of the new subsystems that
have been added:

-   Kamaelia.Codec
-   Kamaelia.Chassis
-   Kamaelia.File
-   Kamaelia.UI.Tk
-   Kamaelia.Internet.Simulate

[Other Highlights]{style="font-size:14pt"}

Software chassis

Tk integration. (The pipeline builder is a nice example of a tool this
enables)

Dirac encoded video decoders and encoders

Support for video playback. (dirac & YUV)

Variety of pygame based components, including

-   Tools for greater control over the pygame surface managed
    environment
-   Tools for building simple games. (controlling sprite behaviour for
    example)

Much richer tools for file reading and writing

-   Includes re-usable file readers.

More utilities for message filters and splitting of messages

Basic tools for simuluating error conditions and failure rates for
delivery of messages (Sufficient for simulating an unstable underlying
internet infrastructure).

The test suite has been further extended in this release.

[Detailed Changelog]{style="font-size:18pt;font-weight:600"}

[Added Files:]{style="font-size:14pt"}

Examples/example10/SimpleDiracEncodeDecode.py

-   Simple dirac base encode/decode chain.

Examples/example10/SimpleDiracPlayer.py

-   Simple dirac player. Shows how to play a specific file.

Examples/example11/Ticker.py

-   Simple example showing how to use the ticker. First developed for
    showing subtitles.

Examples/example12/SimpleMultiFileStreamer.py

-   Simple streamer that repeatedly streams (3 times) the same audio
    file.
-   This is a mainly a demonstration of how to use the
    JoinChooserToCarousel Chassis, and the
    FixedRateControlledReusableFileReader
-   What really happens is a \"chooser\" takes a playlist of things to
    serve, and the filereader asks the chooser what file it should be
    reading next when it finishes reading a file.

Examples/example12/ClientStreamToFile.py

-   Simple client for the above streamer

Examples/example4/MulticastStreamingSystem\_SRM.py

-   This is a modification to the multicast streaming system that uses
    the SimpleReliableMulticast protocol, to add a thin skein of
    reliability over multicast. Passes basic lab tests, but needs real
    world testing to be certain.

Examples/example9/Simplegame.py

-   Simple bouncing images game. Designed for very small children who
    are amused by things take beep and react when you press left/right
    mouse buttons.
-   Forms a demonstration of the new BasicSprite and SpriteScheduler
    components, along with the associated EventHandler code, which is a
    substantial subsystem. Shutdown of active bouncing sprites and their
    associated components controlling them is controlled by a fanout
    component. Also contains a nice demonstration of the flexibility of
    Graphline

Kamaelia/Chassis/Carousel.py

-   A carousel chassis gets it\'s name from broadcast carousels. A
    broadcast carousel is where a programme or set of programmes, is
    broadcast one after another after another, often on a loop. (The
    canonical UK example here is ceefax/teletext) Movie channels which
    show the same film over and over are another form of carousel.\
    \
    If this makes no sense, consider a file reader. It reads a file and
    then it\'s done. Logically we can create a component that receives a
    set of filenames (and perhaps other arguments) and then creates a
    file reader for each on, one after another. The output from the file
    reader is then made the output for that component. If a carousel is
    provided with a filereader component, this is precisely the
    functionality you get. You gain reusability from things that are not
    directly reusable and normally come to a halt.

Kamaelia/Chassis/ConnectedServer.py

-   A chassis is a component that can have other components attached or
    plugin to it. The existing SimpleServer is just that - it takes a
    protocol handler class such that when a connection is made an
    instance of the protocol handler is created to handle the
    connection. This menas it has components attached to it. We also
    note that the SimpleServer is a special case of a connected server,
    as a result the old Kamaelia.SimpleServer.SimpleServer class now
    resides in Kamaelia.Chassis.ConnectedServer.SimpleServer

Kamaelia/Chassis/Prefab.py

-   This will be a collection of functions that act as prefabs. That is
    they take a collection of arguments that will be linked up in a
    standardised way. This makes them a specialised form of chassis
-   JoinChooserToCarousel Automated \"What are arguments should I use
    next time for my reusable component?\" prefab.\
    \
    Takes a carousel that will repeatedly create components of
    particular type. It asks the chooser what the arguments should be
    for the next item.\
    \
    Purpose of carousel : Repeatedly creates a component. It creates the
    component with a set of arguments. The magic is that it can recieve
    those arguments on \"next\" inbox. Further magic: it can ask
    something else to give it it\'s \"next\" set of argument. Purpose of
    chooser : To step through a list of things given to it. When asked
    \"what next\" it provides the next in the list.\
    \
    Combination, for example, allows you to wire up a playlist to
    something reusable that reads files at a given rate.

Kamaelia/Codec/Dirac.py

-   Provides dirac encoding & decoding components. The output of the
    dirac decoder matches that of the RawYUV framer

Kamaelia/Codec/RawYUVFramer.py

-   Takes raw YUV data as read from a file and forms frames suitable for
    passing to (for example) a pygame video overlay.

Kamaelia/Data/Escape.py

-   Contains data escaping functions used by the components that form
    the SimpleReliableMulticast protocol.

Kamaelia/Data/Rationals.py

-   Data types & conversion functions used by the Dirac encoder/decoder

Kamaelia/File/Reading.py

-   Provide a variety of new tools for handling different file reading
    issues. These have not (yet) entirely replaced the original
    ReadFileAdaptor.

Kamaeli/File/Writing.py

-   Initial tools for writing to files

Kamaelia/Internet/Simulate/BrokenNetwork.py

-   Components created during testing of the simple reliable multicast.
    They force out of order lossy delivery with duplicates added.

Kamaelia/Protocol/Framing.py

-   Deals with identifcation and verification that data frames are a
    certain size. (Assists detection of packetloss/duplication)
-   Also provides chunking facilities for identifying start & end points
    in a chunk

Kamaelia/Protocol/SimpleReliableMulticast.py

-   Implements a simple protocol for introducing a level of reliability
    into multicast. Includes full coverage testing.

Kamaelia/UI/Pygame/BasicSprite.py

Currently lower level than PygameDisplay related components

Initial implementation of a sprite component which has a number of
controls:

-   Inboxes=\[\"rotator\", \-- current rotation (in degrees)\
    \"translation\", \-- Control sprite\'s current position\
    \"scaler\", \-- Control how large the sprite\'s inmage is scaled\
    \"imaging\", \-- Control which image is currently displayed.\
    \"inbox\",\
    \"control\"\]

Kamaelia/UI/Pygame/EventHandler.py

-   Currently lower level than PygameDisplay related components
-   Simple tool for handling events

Kamaelia/UI/Pygame/KeyEvent.py

-   Pygame display level component for ndependently handling key
    strokes. You may add a list of outboxes, and have a message sent to
    a given outbox when the key is pressed. This can be used for games,
    slideshows, and other things that are key activated.

Kamaelia/UI/Pygame/SpriteScheduler.py

-   This is a specialised scheduler that provides sprites\' logic with a
    timeslice by calling the sprite\'s update method. (Thereby also
    visually updating the sprite)

Kamaelia/UI/Pygame/VideoOverlay.py

-   Provides a useful video playback tool. Video overlays can accept YUV
    data (as comes from many codecs) and display it without
    transformation.

Kamaelia/UI/Tk/TkWindow.py

-   Provides the base level of integration required for TK based
    widgets. This allows for Tk based guis to be implemented and
    integrated trivially into Kamaelia with callbacks mapped to events.
    This was a simple first pass and has proved remarkably resilient.

Kamaelia/Util/Fanout.py

-   Another simple splitter. The reason for allowing a variety of
    splitters is to see which approach/metaphor works best before
    limiting implementations. The usecases of each will need to be
    supportable by any resulting system.

Kamaelia/Util/FilterComponent.py

-   Implements a generic filter system.

Kamaelia/Util/Marshalling.py

-   The Marshalling/DeMarshalling Component is given a simple class. It
    then expects to be passed objects of that class, and then performs
    the following actions: \_\_str\_\_ on an object and fromString on an
    object. The idea is that you would place this between your logic and
    a network socket, which simply serialises and deserialises objects
    for transmission over the wire. The initial data format this is
    designed to work with is the MimeDict object.

Kamaelia/Util/RateFilter.py

-   Provides a variety of tools for time based message limitation.
    Either in terms of byte count, raw message rate and so on.
    MessageRateLimit, ByteRate\_RequestControl,
    VariableByteRate\_RequestControl

Tools/VisualPipeBuilder.py

-   Script that runs a pipebuilder. This is very much a version 0.1
    tool, and only handles pipelines. It is however pretty useful.

Tools/PipeBuilder/BuildViewer.py

-   Support file - builds a specialised topology viewer - for example
    using a crawling dashed line to indicate dataflow direction

Tools/PipeBuilder/GUI.py

-   Builds the Tk based interface for the pipe builder. This includes
    the source code display window/widget and the main component display
    widget.

Tools/PipeBuilder/PipeBuild.py

Tools/PipeBuilder/PipelineWriter.py

-   Based on the topology, writes out python code.

[Test suites Added:]{style="font-size:14pt"}

-   Kamaelia/Data/tests/test\_Escape.py
-   Kamaelia/Data/tests/test\_Rationals.py
-   Kamaelia/Protocol/test/test\_framing.py
-   Kamaelia/Util/test/test\_Chooser.py
-   Kamaelia/Util/test/test\_Comparator.py
-   Kamaelia/Util/test/test\_ForwardIteratingChooser.py
-   Kamaelia/Util/test/test\_LossyConnector.py
-   Kamaelia/Util/test/test\_Marshalling.py
-   Kamaelia/Util/test/test\_RateControl.py
-   Kamaelia/Util/test/test\_Splitter.py
-   Kamaelia/Util/test/test\_TestResultComponent.py
-   Kamaelia/Util/test/test\_VariableRateControl.py

[Changed files:]{style="font-size:14pt"}

setup.py

Added:

-   Kamaelia.Codec
-   Kamaelia.Chassis
-   Kamaelia.File
-   Kamaelia.UI.Tk

Examples/example8/slideshow.py

-   Now looks in the local \"Slides\" directory for slides to show.

Kamaelia/SimpleServerComponent.py

-   Changed to a stub file that for now has compatibility imports from
    the new location Kamaelia.Chassis.ConnectedServer

Kamaelia/SingleServer.py

-   In/outboxes now documented as to purposes

Kamaelia/UI/PygameDisplay.py

-   Support for overlays added
-   Overlays are displayed \*after\* the other surfaces are rendered
-   Display tries to be doublebuffered where possible

Kamaelia/UI/MH/DragHandler.py

-   Issues in dragging resolved.

Kamaelia/UI/Pygame/Image.py

-   Allows the user to add in extra arguments controlling the display
    for the image - if possible.
-   Allows for scaling relative to maximum aspect ratio.

Kamaelia/UI/Pygame/Ticker.py

-   Outline colour now defaults to the bac kground colour if not given
-   Starting of configurability for word playback
-   Abiility to provide a logical position for the ticker on an abstract
    surface.
-   Requests a display using the new \"Wait\" directive to the
    scheduler. This might actually have similarities to deferred
    generators in twisted. Need to look into.
-   Better modularisation
-   Allows for line oriented tickers - ie reach end of a line, start a
    new line style ticker (rather than subtitle style ticker)

Kamaelia/Util/Chooser.py

-   ForwardIteratingChooser added.

Kamaelia/Util/Graphline.py

-   Variety of changes to deal with shutdown of components within the
    graphline better.
-   Key change is the graphline has changed from passive to active. This
    might need revisiting once this API/approach has stablised.

Kamaelia/Util/PipelineComponent.py

-   Variety of changes to deal with shutdown of components within the
    pipeline better.
-   Key change is the pipeline has changed from passive to active. This
    might need revisiting once this API/approach has stablised.

Kamaelia/Util/Splitter.py

-   Merge of the test driven rewrite of splitter into here replacing the
    old implementation. Has the same API and passes the old tests, but
    also provdes a pluggable splitter system.

Kamaelia/Visualisation/Axon/PComponent.py

-   Nicer abbreviation of component names in the introspector

Kamaelia/Visualisation/PhysicsGraph/ParticleDragger.py

-   Allow overrideable information on selection of node/particle

Kamaelia/Visualisation/PhysicsGraph/RenderingParticle.py

-   Optional naming of particles.

Kamaelia/Visualisation/PhysicsGraph/TopologyViewerComponent.py

-   Added in facilitiy for querying the current topology the topology
    viewer is displaying.
-   Also sends out a message when a particle is selected.

Michael, October 2005
