---
pagename: Cookbook
last-modified-date: 2009-03-08
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Cookbook]{style="font-size: 24pt; font-weight: 600;"}

[How can I\...?]{style="font-size: 18pt;"}

This section contains a number of examples in a number of different
application areas. These are all included in the Kamaelia distribution,
but are provided here for convenience. See also the
[documentation](/Docs/) in the older structure.

### Linking components together

-   [PipelinesAndGraphlines](/Cookbook/PipelinesAndGraphlines.html)
-   [Pipelines](/Cookbook/Pipelines.html)
-   [Graphlines](/Cookbook/Graphlines.html)
-   [Carousels](/Cookbook/Carousels.html)
-   [Backplanes](/Cookbook/Backplanes.html)\

### Build TCP Based Clients and Servers[]{style="font-weight: 600;"}

-   []{style="font-weight: 600;"}[FortuneCookieProtocol](/Examples/FortuneCookieProtocolClientServer.html)
-   [OggVorbisTCPClientServer](/Examples/OggVorbisTCPClientServer.html)\
-   [OggVorbisTCPScripts](/Examples/OggVorbisTCPScripts.html)\

### Build Multicast Based Clients and Servers[]{style="font-weight: 600;"}

-   []{style="font-weight: 600;"}[MulticastOggVorbisServer](/Examples/MulticastOggVorbisServer.html)
-   [MulticastOggVorbisClientServerScripts](/Examples/MulticastOggVorbisClientServerScripts.html)
-   [SimpleReliableMulticastExample](/Examples/SimpleReliableMulticastExample.html)\

### Create UDP Based Systems[]{style="font-weight: 600;"}

-   []{style="font-weight: 600;"}[UDPSimplePeerExample](/Examples/UDPSimplePeerExample.html)\

### Build tools for System Visualisation and Introspection

-   [TheAxonVisualiser](/AxonVisualiser.html)
-   [IntrospectingASimpleStreamingSystem](/Examples/IntrospectingASimpleStreamingSystem.html)
-   [NetworkControllableGraphViewer](/Examples/NetworkControllableGraphViewer.html)

### Build Multimedia Applications[]{style="font-weight: 600;"}

-   []{style="font-weight: 600;"}[SimplestPresentationTool](/Examples/SimplestPresentationTool.html)
-   [TopologySlideshowComponent](/Examples/TopologySlideshowComponent.html)
-   [TopologyAndSlidesPresentationTool](/Examples/TopologyAndSlidesPresentationTool.html)
-   [SimpleTextTickerDemonstration](/Examples/SimpleTextTickerDemonstration.html)\

### Working with Open GL

*Coming soon! ([open GL examples already in github here](https://github.com/sparkslabs/kamaelia/tree/master/Code/Python/Kamaelia/Examples/OpenGL) )*

### Write Games[]{style="font-weight: 600;"}

-   []{style="font-weight: 600;"}[SimpleBouncingCatsGame](Examples/SimpleBouncingCatsGame.html)

### Work with Audio and Video[]{style="font-weight: 600;"}

-   [SimplestPossibleDiracVideoPlayer](/Examples/SimplestPossibleDiracVideoPlayer.html)
-   [DiracVideoEncodeAndDecodeChain](/Examples/DiracVideoEncodeAndDecodeChain.html)
-   [SimpleStreamerWithPlaylistCapability](/Examples/SimpleStreamerWithPlaylistCapability.html)
-   [SimpleClientForSavingContentsOfTCPStream](/Examples/SimpleClientForSavingContentsOfTCPStream.html)[]{style="font-weight: 600;"}

### Working with HTTP

-   [HTTPServer](/Cookbook/HTTPServer.html) - How can I integrate a **web
    server** into my system? This is a relatively low level component,
    but does form a base for doing lots of interesting things.
-   [HTTPClient](/Cookbook/HTTPClient.html) - How can I integrate a **web
    client** into my system? **How can I deal with RSS feeds?**\

### Working with BitTorrent

-   [SimpleBitTorrentExample](Cookbook/SimpleBitTorrentExample.html)

### Working with AIM

-   [Simple AIM client with Pygame](Cookbook/AIM.html)

### Working with IRC 

-   [IRCClient](/Cookbook/IRCClient.html)

### Other ways of using Kamaelia

-   [Using Kamaelia concurrently in other systems](../../../Cookbook/LikeFile.html)



::: {.boxright}
See also [Kamaelia Macro](../../../KamaeliaMacro.html)
:::
Cookbook: Working with DVB 
--------------------------


-   [TransportStreamCapture](../../../Cookbook/DVB/TransportStreamCapture.html) -
    how can I capture an entire transport stream? (a DVB multiplex puts
    multiple channels inside a transport stream)\
-   [TransportStreamDemuxer](../../../Cookbook/DVB/TransportStreamDemuxer.html) -
    how can I work with **multiple channels** from a transport stream?
    (yes, you can deal with more than one at a time easily :)\
-   [SingleChannelTransportStreamCapture](../../../Cookbook/DVB/SingleChannelTransportStreamCapture.html) -
    How can I work with a **single channel** from a transport stream?\
-   [RecordNamedChannel](../../../Cookbook/DVB/RecordNamedChannel.html) -
    Numbers numbers numbers! I want to record BBC ONE! How can I use
    **named channels** ?\
-   [PersonalVideoRecorder](../../../Cookbook/DVB/PersonalVideoRecorder.html) -
    How can I record **named programmes** from a specific channel?
    (without even specifying the time ? :-)\

The [DVB Component documentation](/Components/pydoc/Kamaelia.Device.DVB.html)
also contains extensive examples\
\
\

------------------------------------------------------------------------

