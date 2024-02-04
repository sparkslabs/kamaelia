---
pagename: KamaeliaStatus
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Status]{style="font-size: 20pt; font-weight: 600;"}

The bulk of Kamaelia is a collection of components that use Axon. These
range from components for building network servers and clients using TCP
and Multicast, through to music playback, audio codec decode through to
components suitable for viewing network topologies and interactive
systems - such as networked personal autocues.

[[Axon]{style="font-weight: 600;"}](http://kamaelia.sourceforge.net/Docs/Axon.html)[
- ]{style="font-weight: 600;"}Kamaelia core concurrency framework

Axon is available from Kamaelia\'s main [sourceforge project
page](http://sourceforge.net/projects/kamaelia/).

The current status of the project is that Axon itself has been deemed
feature stable, and currently stands at version 1.5.1. Axon runs on
Windows, Mac OS X, Linux and Series 60 mobile phones. This is
sufficiently stable in terms of API and coverage in terms of testcases
to be used as is. It should work with python 2.2 onwards. [If it
doesn\'t, please let us know!](Contact.html)

[Documentation, Stability, Completeness]{style="font-style: italic;"}

We believe Axon to be largely feature complete given that it\'s
functionality has been driven by application spikes whilst writing
Kamaelia. Documentation for Axon is in the process of collation into
this website, with the [main starting page here](Docs/Axon.html).

Examples included with Axon\'s release:

-   A simple producer/consumer example - this shows how to build
    components, and build pipelines manually. (Syntactic sugar for
    pipelines exists inside Kamaelia\'s Util tree)
-   A more complex, but still simple producer/consumer example.

[Kamaelia]{style="font-weight: 600;"}

The Kamaelia portion is the larger of the two parts to the project since
it is a collection of components that use Axon. These range from
components for building network servers and clients through to music
playback, audio codec decode through to components suitable for viewing
network topologies and interactive systems.

We feel we\'re about half way towards reaching a 1.0 release. As a
result the current version number reflects this and currently stands at
0.5.0. That said, like Axon, it runs on Windows, Mac OS X, Linux and
Series 60 mobile phones. Though it is considered an alpha release,
don\'t be put off. It is already very functional and generally very
stable.\

Examples included with Kamaelia\'s 0.1.2 release:

-   [Example 1: ]{style="font-weight: 600;"}A simple \"FortuneCookie\"
    protocol system. Includes server and client as part of a single
    system.
-   [Example 2: ]{style="font-weight: 600;"}This has much the same
    structure, but rather than serve and display fortune cookies, serves
    (ogg vorbis) audio over a TCP connection to a client which decodes
    and plays back the audio.
-   [Example 3: ]{style="font-weight: 600;"}Splits the structure in
    example 2 into a specific server application and a client
    application. On a single CPU system with Axon versions 1.1.0 or
    lower, this causes problems because Axon doesn\'t hint to the system
    it\'s busy waiting and interruptable. Above that Axon does. (Hence
    why the latest version of Axon is generally recommended)
-   [Example 4: ]{style="font-weight: 600;"} Simple multicast based ogg
    vorbis streaming system.

Examples to be included in Kamaelia\'s 0.2 release (see
[Downloads](Download.html)):

-   [Example 5: ]{style="font-weight: 600;"} An introspecting version of
    Examples 2/3. This creates a simple streaming system, and looks
    inside to see what components are running/active, and passes the
    resulting information over a network connection to an Axon
    Visualisation server.
-   [Example 6: ]{style="font-weight: 600;"} This is a simple/generic
    topology visualisation server. The server listens on port 1500, and
    accepts the following commands:\
    ADD NODE id label auto -\
    ADD LINK id id\
    DEL NODE id\
    DEL ALL
-   [Example 7: ]{style="font-weight: 600;"} This shows how the
    visualisation subsystem can be extended to work in different ways.
    What this does by default when run is randomly create new nodes and
    new linkages quite quickly, allowing you to see how the system
    works.
-   [Example 8: ]{style="font-weight: 600;"} Sample
    slideshow/presentation tool. Unlike traditional
    slideshow/presentation tools, you can modify this to run arbitrary
    components. An example of how this can work is provided - allowing
    stepping through some graph visualisations along with the
    presentation.
-   [Example 9]{style="font-weight: 600;"}: Simple component based game
    using pygame. Not quite fully integrated with the other pygame code
    (will be), but fully reusable & reconfigurable code and it\'s a
    useful start for people wanting to see how to write things varying
    from games through other interactive systems.

Other Kamaelia Modules & comments:
