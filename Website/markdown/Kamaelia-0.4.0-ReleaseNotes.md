---
pagename: Kamaelia-0.4.0-ReleaseNotes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Kamaelia Release Notes]{style="font-size:28pt;font-weight:600"}

[0.4.0]{style="font-size:21pt"}

[Summary]{style="font-size:21pt;font-weight:600"}

[Kamaelia 0.4.0 is a consolidation, documentation and optimisation
enhanced release. ]{style="font-weight:600"}Whilst there are a wide
variety of new components, existing functionality has been consolidated,
and is now in use in a handful of (beta) production systems.

[Kamaelia 0.4.0 requires the use of Axon 1.5 (released at the same time
as this release).]{style="font-style:italic;font-weight:600"}

Also, virtually all components now have highly detailed documentation
inside their sourcefiles. A (large) subset of this is available here:

-   <http://kamaelia.sourceforge.net/Components.html>

The examples have been duplicated onto the website, and are here:

-   <http://kamaelia.sourceforge.net/Cookbook.html>

Our tutorial for helping getting started is here:

-   <http://kamaelia.sourceforge.net/MiniAxon/>

This has now been battle tested by a good few dozen people, and we feel
is a good introduction to Kamaelia\'s approach, and others have also
stated they find it a good way of understanding generators too. (even if
they\'re not interested in Kamaelia)

[Notable New Components]{style="font-size:16pt"}

-   Tools for Timeshifting Digital TV (DVB-T handling to be precise)\
    [These tools are only intended for use as legal under UK law, you
    need to check locally if you can use
    them.]{style="font-style:italic;font-weight:600"}
-   A software data backplane
-   Tools for piping data easily/trivially through external processes
-   Tools for taking advantage of system optimisations allowing
    quiescent behaviour. (both in terms of pygame & network based
    systems)
-   Tools for using UDP

[New Examples]{style="font-size:16pt"}

-   Tools for using UDP & SingleServer

A collaborative whiteboard \"sketcher\" which is both a server to other
whiteboards and/or a client to other whiteboards. (Due to changes, when
not in use CPU usage for these is as close to zero as it can be for any
software) This is also a good example of usage of the backplane
component.\
\
This application is particularly nice to use in conjunction with a
tablet PC!\
\
An overview of the sketcher can be found on our systems page:

-   <http://kamaelia.sourceforge.net/Systems.html>\
    (see Collaborative Whiteboarding)

Examples for using the tools for timeshifting including:

Tuning into a TV channel on Freeview and recording it to disk

Dumping a DVB multiplex transport stream

Demultiplexing a prestored DVB multiplex

::: {dir="ltr"}
A system for grabbing a TV channel and it\'s now & next information,
such that this can allow the programmes to be captured and transcoding
as individual programmes for watching later.\
\
This is the core of the BBC Macro system (an internal prototype) that
can be seen here:
:::

-   <http://bbc.kamaelia.org/cgi-bin/blog/blog.cgi>

::: {dir="ltr"}
An overview of the architecture can be found here:
:::

-   <http://kamaelia.sourceforge.net/KamaeliaMacro.html>

<div>

Essentially, this allows you to build your own space efficient PVR.

</div>

[General overview of other large scale changes]{style="font-size:16pt"}

Massively improved documentation across the board (no file left
untouched). This is all largely in the form of pydoc based
documentation, a fair chunk of it is available at

-   <http://kamaelia.sourceforge.net/Components.html>

However the documentation in those files goes further than that,
including many, many more examples than are even at:

-   <http://kamaelia.sourceforge.net/Cookbook.html>

Large scale removal of cruft and change over to use pipelines and
graphlines where suitable. This is most noticable inside the examples.

Code quality of a number of pieces of code has been improved:

-   A small number of components have been rewritten from the 3 callback
    form into the generator form of component to simplify their
    implementation.

-   Shutdown handling is now more consistent.

-   Some core components have been rewritten, test first, now that their
    expected usage is clearer, making the system more dependable.

-   Throughput handling has also generally been improved. Many locations
    where the following was written:\

                 if self.dataReady("inbox"):
                    d = self.recv("inbox")
                    e = SomeTransform(d)
                    self.send(e, "outbox")

    \
    We\'ve discovered gain better throughput if you write:\

                 while self.dataReady("inbox"):
                    d = self.recv("inbox")
                    e = SomeTransform(d)
                    self.send(e, "outbox")

-   Improved handling of child components, specific examplars are
    pipeline & graphline components.

-   Increased use of .activate() and .run() methods rather than manually
    using the Axon.Ipc.newComponent message of manually starting the
    scheduler.

-   Peppered through the code is some hints to improve introspection and
    detection of components for both code generation and interactive
    graphical pipeline builder applications. Example lines added to
    files:\

            __kamaelia_components__  = ( Annotator, RecoverOrder, )
            __kamaelia_prefab__ = ( SRM_Sender, SRM_Receiver)

    \
    These can be extracted using Kamaelia.Data.Repository

[Pygame related changes]{style="font-size:16pt"}

-   Major changes to do with how components update the display.
    Specifically they MUST send redraw requests through. This is akin to
    doing a flip for the surfaces.
-   A private \_PygameEventSource has also been created.

These two changes combined allow the system to become quiescent, where
possible.

-   A number of components now understand what to do if sent an alpha
    value on an alphacontrol inbox.

[Detailed Overview of other changes]{style="font-size:16pt"}

Initial release, largely rewritten or includes new components:

-   Examples/example13/UDP\_demo.py
-   Examples/example15/Macro.py
-   Examples/example15/SingleChannelTransportStreamCapture.py
-   Examples/example15/TransportStreamCapture.py
-   Examples/example15/TransportStreamDemuxer.py
-   Kamaelia/Codec/\_\_init\_\_.py
-   Kamaelia/Community/\_\_init\_\_.py
-   Kamaelia/Data/Repository.py
-   Kamaelia/Data/tests/test\_MimeDict.py
-   Kamaelia/Device/\_\_init\_\_.py
-   Kamaelia/Device/DVB/Core.py
-   Kamaelia/Device/DVB/EIT.py
-   Kamaelia/Device/DVB/\_\_init\_\_.py
-   Kamaelia/File/UnixPipe.py
-   Kamaelia/Internet/UDP.py
-   Kamaelia/Util/Backplane.py
-   Kamaelia/Util/Console.py
-   Kamaelia/Support/Tk/Scrolling.py
-   Kamaelia/Internet/ConnectedSocketAdapter.py
-   Kamaelia/Internet/Selector.py
-   Kamaelia/KamaeliaIPC.py
-   Kamaelia/Util/RateFilter.py

Changed to take advantage of Axon changes allowing quiescent behaviour:

Kamaelia/Internet/ConnectedSocketAdapter.py

Kamaelia/Internet/Selector.py

Kamaelia/Chassis/ConnectedServer.py

Kamaelia/Internet/TCPClient.py

Kamaelia/Internet/TCPServer.py

Kamaelia/UI/PygameDisplay.py

Kamaelia/UI/Pygame/Button.py

Kamaelia/Util/Introspector.py

New/Changed functionality to existing components:

-   Kamaelia/Visualisation/PhysicsGraph/TopologyViewerComponent.py
-   Kamaelia/Visualisation/PhysicsGraph/chunks\_to\_lines.py
-   Kamaelia/UI/Pygame/Ticker.py
-   Kamaelia/UI/Pygame/KeyEvent.py
-   Tools/PipeBuilder/GUI.py
-   Tools/VisualPipeBuilder.py (no longer uses a hardcoded list of
    components)
-   Examples/example10/SimpleDiracPlayer.py

Namespace cleanup:

-   Kamaelia/Util/ConsoleEcho.py \--\> Kamaelia/Util/Console.py
-   Kamaelia/SimpleServer.py \--\> Kamaelia/Chassis/ConnectedServer.py
-   The marshalling code in util has had a similar change.

Michael, June 2006
