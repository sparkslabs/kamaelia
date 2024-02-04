---
pagename: Developers/Projects
last-modified-date: 2008-10-13
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
\

Projects
========

This page details a bunch of projects, either in process, or which could
be done, or have been done.

Google Summer of Code 2008 Projects (don\'t follow the PTP format at
present)\

-   [**Kamaelia Paint**](/Developers/Projects/KamaeliaPaint.html)
-   [**Kamaelia Jam**](/Developers/Projects/KamaeliaJam.html)
-   [**Kamaelia Publish**](/Developers/Projects/KamaeliaPublish.html)
-   [**Testing Framework**](/Developers/Projects/TestingFramework.html) -
    this is a speculative project that may become \"the\" testing
    framework. It does not have that status yet.
-   [**3D Topology Visualiser**](/Developers/Projects/3DTopologyVisualiser.html)

Project Task Pages 
------------------

::: {.boxright}
[**Template PTP/Guide**](/Developers/Projects/ProjectTaskPageTemplate.html)\
Unfortunately, this page is not as up to date as it could be, and will
be replaced with something relatively lightweight when practical. In the
meantime it is useful to give a flavour of projects Kamaelia has been
useful and used for!
:::

**Existing PTPS**\

-   [**Kamaelia Macro**](/Developers/Projects/KamaeliaMacro.html)
-   [**DVB Tools**](/Developers/Projects/DVBTools.html)
-   [**Mobile Reframer**](/Developers/Projects/MobileReframer.html)
-   [**Multicast RTP MPEG TS remultiplexer**](/Developers/Projects/MulticastRtpMpegRemultiplexer.html)
-   [**Multicast Island Joining**](/Developers/Projects/MulticastProxyTools.html)
-   [**Whiteboard**](/Developers/Projects/Whiteboard.html)
-   [**Compose**](/Developers/Projects/Compose.html)
-   [**Video Cut Detector**](/Developers/Projects/VideoCutDetector.html)
-   [**Web Client**](/Developers/Projects/WebClient.html)
-   [**Axon box delivery optimisations**](/Developers/Projects/AxonBoxDeliveryOptimisations.html)
-   [**Axon ThreadedComponent API change**](/Developers/Projects/AxonThreadedComponentAPIChange.html)
-   [**Axon Quiescence optimisation**](/Developers/Projects/AxonQuiescenceOptimisation.html)
-   [**Axon Waking Producers Bug-fix**](/Developers/Projects/AxonWakingProducersBugfix.html)
-   [**Documentation**](/Developers/Projects/Documentation.html)
-   [**Reference Doc Generation Tools**](/Developers/Projects/ReferenceDocumentationGeneration.html)
-   [**Bugfix to BasicSprite component**](/Developers/Projects/BasicSpriteBugfix.html)
-   [**PyMedia Audio, Pygame and misc bugfixes**](/Developers/Projects/AudioPygameAndMiscBugfixes.html)
-   [**Fixing references to deprecated components in Examples and Tools**](/Developers/Projects/DeprecationFixes.html)
-   [**Dirac 0.6.0 bindings**](/Developers/Projects/Dirac0.6.0Bindings.html)
-   [**Mobile Reframer And RTP New Components**](/Developers/Projects/MobileReframerAndRTPNewComponents.html)
-   [**Detecting one-to-many linkage creation**](/Developers/Projects/AxonOneToManyDetection.html)
-   [**Threaded component termination bugfix**](/Developers/Projects/AxonThreadedComponentTerminationBugfix.html)
-   [**Unbuffered CSA Support**](/Developers/Projects/UnbufferedCSASupport.html)

\
**PTPs to be written:**\

-   [Web Server](/Developers/Projects/WebServer.html)
-   [TCP Subsystem](/Developers/Projects/TCPSubsystem.html)
-   [TCP Client Shutdown Bugfix](/Developers/Projects/TCPClient.html)
-   [Database Tools](/Developers/Projects/DatabaseTools.html)
-   [BitTorrent Integration](/Developers/Projects/BitTorrent.html)
-   [BitTorrent Standalone Tester/Diagnostic](/Developers/Projects/BitTorrentStandaloneTester.html)

**Background on Project Task Pages**\
\
Project Task Pages (PTPs) take a standard format, and recognise that
feature dev, bug fix, and any other task have commonalities. PTP\'s aim
to capture this information to make it easier to see what\'s going on,
and assign priorities. PTP\'s as a result have a [template format](/Developers/Projects/ProjectTaskPageTemplate.html),
which is based on the way Kamaelia itself is designed.\
\
A project task page may cover a project as small as a single feature of
a single component of a single module, or something as large as an
entire application comprisig of several systems. The key aspect here is
that each of those subsystems would also have project task pages, as and
when they become necessary.\
\
As a result Kamaelia development and management of components should
naturally reflect the component system itself.\
\
**PTPs to be fleshed out**\
\
Each project here will gain its own page as soon as practical - this is
a capture of current state. (This does mean also that there SHOULD be a
PTP for ch of the tools listed above)\

[**Kamaelia Macro**](/Developers/Projects/KamaeliaMacro.html) - Timeshifting
tools\

-   [DVB Tools](/Developers/Projects/DVBTools.html) - Tools for timeshifting
    in a storage efficient, automated manner

```{=html}
<!-- -->
```
-   Database Tools for working with databases in Kamaelia (at present,
    very unclear what\'s *sensible*)\

[**Mobile Reframer**](/Developers/Projects/MobileReframer.html)

[**Multicast RTP MPEG TS remultiplexer**](/Developers/Projects/MulticastRtpMpegRemultiplexer.html)

[**Video Cut Detector**](/Developers/Projects/VideoCutDetector.html)

**Component Integration Tasks** - Small ad hoc tasks of documenting,
reviewing and merging components into the mainline codebase\

/Sketches/MH/pixFormatConversion/VideoSurface

-   pixel format conversion (yuv\<-\>rgb)
-   Pygame surface based video display\

/Sketches/MH/dirac/\*

-   new dirac bindings

/Sketches/MH/Video/VideoSurface.py

-   yuv4mpeg file parsing and generation
-   Cropping and scaling of video frames\

/Sketches/MH/audio/WAV.py

/Sketches/MH/audio/ToWAV.py

-   wav file parsing and generation

/Sketches/MH/MobileReframer/\...\

-   rewritten UnixProcess component (possibly needs a rename?)
-   Pipeline and Graphline that allows size limits to be set on inboxes\

```{=html}
<!-- -->
```
-   SAX stream based parser
-   Sequencer for running components in sequence
-   File reader that rate limits by the destination inbox becoming full

/Code/Python/Kamaelia/Tools/Whiteboard/Whiteboard/\...

-   Some components are potential candidates for the mainline codebase

/Sketches/MH/RTP/

-   Selector (made more responsive to requests)
-   Multicast\_transceiver (reduced CPU usage by using the Selector)\
-   ConnectedSocketAdaptor (minor mod to support multicast transceiver)
-   RTPFramer and RTPDeframer

Challenges Related - It\'s worth noting that as Kamaelia matures in
scope, it\'s capabilities are beginning to branch out well beyond these
challenges\

Lunch - The fact the world is becoming massively parallel and we need
better tools to deal with this.

-   [**Axon**](Axon.html) - Our toolset for making concurrency easier to work
    with\

Deliver - Tools and mechanisms for distributing and synchronising
effectively a huge database of content\

-   [**Macro**](/KamaeliaMacro.html) - tools for timeshifting, but also
    *tools for delivering content via the broadcast chain*.\

Share - Creation of tools for sharing that people can trust

-   Tools to allow the audience to trust the content they recieve

```{=html}
<!-- -->
```
-   Tools to allow content creators to trust that their ability exploit
    their copyright will be kept intact

P2P & Multicast joining\

-   Peer To Peer Events Backplane (A project based on extraction from
    the whiteboard)\
-   Peer To Peer Mesh Creation
-   Tools for Handling DHTs
-   [**Multicast Island
    Joining**](/Developers/Projects/MulticastProxyTools.html)
-   See also: [Peer-to-Peer streaming architecture using
    Kamaelia](/Projects/Soc2006/PeerToPeerStreaming.html)

Thins that aren\'t appropriate as project task pages here:\

-   Moore\'s Law Growing both sides of an equation doesn\'t help - [The
    Dirac project](http://dirac.sourceforge.net/) is largely aimed at
    dealing with these, and is outside the scope of Kamaelia

```{=html}
<!-- -->
```
-   Open - This relates to the fact that open systems need to be able to
    scale. This is inherently Kamaelia\'s core goal regarding online
    delivery.\

###  

Projects are to be labelled with tags to help classify and organise
them. We\'ve chosen this over having a predefined url based hierarchical
structure as it gives greater flexibility and acknowledges the fact that
projects will change in status and scope over time.

Possible tags to us include:

-   *Experimental* (for stuff in /Sketches)\
-   *Tool* (typically the kind of thing that ends up in
    /Kamaelia/Tools)\
-   *Example* (pieces of code that exist to demonstrate functionality)*\
    *
-   Mainline (work affecting the main /Code codebase)\

Tools
-----

These are relatively substantial systems in their own right. Their
development, and components driving their development are ongoing.\

-   [**Compose**](/Compose/) - a tool for composing (creating) Kamaelia
    systems *graphically*\
-   [**Whiteboard**](/Whiteboard/) - a tool for collaboration\
-   [**Macro**](/KamaeliaMacro.html) - tools for timeshifting
-   [**Mobile Reframer**](/MobileReframer.html) - tool for applying edit
    decision lists to video for use with mobiles.
-   [**Multicast RTP MPEG TS
    remultiplexer**](/MulticastRtpMpegRemultiplexer.html) - tools for
    remultiplexing and rebroadcasting mpeg transport streams over
    multicast

### **Summer of Code 2006 Project Ideas**

Each of the ideas here have been fleshed out to some degree to or
another and are considered useful to differing degrees. If you\'re
looking for a project worth doing, these are worth looking at for ideas.
Aside from anything else if we\'ve added them here there\'s a good
chance that they\'ve had some serious thought behind them already,
bootstrapping your idea!\
\
The following list contains the aggregated projects grouped under like
for like ideas. *The order of projects here has no significance*

-   [AV Codec Support](/Projects/Soc2006/AVCodecs.html)
-   [Generalised Events Backplane](/Projects/Soc2006/GeneralisedEventsBackplane.html)\
-   [XML Pygame Interface definition and CSS based styling](/Projects/Soc2006/XML2DInterfaces.html)\
-   [Open GL](/Projects/Soc2006/OpenGLWidgets.html)
-   [Integrated Bit Torrent Reimplementation](/Projects/Soc2006/BitTorrent.html)\
-   [Primitives - Components for codeless composition](/Projects/Soc2006/CodelessComposition.html)
-   [Peer-to-Peer streaming architecture using Kamaelia](/Projects/Soc2006/PeerToPeerStreaming.html)
-   [Distributed physics](/Projects/Soc2006/DistributedPhysics.html)
-   [Kamaelia Visual Editor, Graphical  IDE](/Projects/Soc2006/VisualEditor.html) - This is similar, but more ambitious in scope than Compose\
-   [OH-Kamaelia (***O***DMRP based Ad ***H***oc extensions to *Kamaelia*)](/Projects/Soc2006/OHKamaelia.html)\

One of the most interesting aspects of this list of projects is that
many of them were proposed by undergraduate students, and all thought
they could achieve these projects over a 3 month coding period, most of
them after having done the [MiniAxon](/MiniAxon/) tutorial.\

### **Completed Summer of Code 2006 Projects**

In some cases these were exploratory, some were concrete, some were half
way. All were useful for different reasons.\
\
\
\
