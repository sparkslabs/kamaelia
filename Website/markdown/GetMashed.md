---
pagename: GetMashed
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
BBC Mashed: Getting Started With Kamaelia
=========================================

::: {.boxright}
[**Want a single page rapid overview of
everything?**](../../../NewIntroduction.html) **[Click this link :-)](../../../NewIntroduction.html)**
:::

\

::: {.boxright}
**MASHED HACKS:**\
**[Speak And Learn](../../../SpeakAndLearn.html)** - A tool based on
gesture/stroke recognition and speech synthesis to be a toy assisting a
child to learn to read and write**\
[IRCSpeakerBot](../../../IRCSpeakerBot.html)** - A tool for connecting to IRC
sessions you want to keep abreast of, but don\'t want to read. This
connections to groups and using speech synth ***literally*** allows you
to listen into chatter on an IRC channel.
:::

\

Step 1 - Get Kamaelia & Install it
----------------------------------

Get the latest version from here:\

> [http://www.kamaelia.org/release/](../../../release/)

Install:\

>     ~/> tar zxf Kamaelia-0.6.0-rc7.tar.gz
>     ~/> cd Kamaelia-0.6.0-rc7/
>     ~/Kamaelia-0.6.0-rc7> sudo python setup.py install

Step 2 - Run & Tweak the Examples
---------------------------------

Many of these require pygame or similar libraries. We\'re putting
together dependencies as we speak. You\'ll find the examples in the
examples directory.\
You will also find a large number of examples in the [**Kamaelia Cookbook**](/Cookbook.html)\
\

Step 3 - Start writing your own components
------------------------------------------

For the moment, see [this tutorial on how to go from non-component code to component code](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1113495151)\
\

Step 4 - Wire up your component to a new system
-----------------------------------------------

The best way to get started here is to look at the examples in the
already [**Kamaelia Cookbook**](../../../Cookbook.html) mentioned.\
\
You\'ll be looking at using a number of the [**components from the
reference area**](/Components.html)**.**\

Step 5 - Build something new
----------------------------

All sorts of possible ideas exist here - as inspiration please look
here:\

-   [Projects](../../../Developers/Projects.html)
-   [SpeculativeNewIdeas](../../../Developers/SpeculativeNewIdeas.html)
-   [HelpWanted](../../../Developers/HelpWanted.html)
-   [Tasks](../../../Developers/Tasks.html)

Our pages for our involvement with [**Google Summer of
Code**](../../../SummerOfCode.html) have lots of ideas.\

-   **[Summer of Code 2008](../../../SummerOfCode2008.html)** **(This page
    also has a presentation/overview there)\
    **
-   [Summer of Code 2007](../../../SummerOfCode2007.html)
-   [Summer of Code 2006](../../../SummerOfCode2006.html)
-   Introductions: [Overview](../../../Introduction.html), 
    [Whiteboard Article](../../../t/TN-LinuxFormat-Kamaelia.pdf),
    [Light Technical Intro](../../../t/TN-LightTechnicalIntroToKamaelia.pdf),
    [Presentations](http://www.slideshare.net/kamaelian/slideshows)

What\'s in the Release Candidate?
---------------------------------

Well, the usual slew of extra components and bug fixes, a variety of new
tools - from video shot change detection, through to SMTP greylisting,
but also perhaps the biggest extra: **Multiprocess & hence multicore
support** (experimental at this stage, but so far so good :) )\
\
And a large number of extra components - this is actually a lot more
than originally expected/anticipated. However they\'re divided into two
halves - new components and components from applications merged into the
repository. (the latter means that you can take parts of random Kamaelia
applications and embed them in other random Kamaelia applications. As a
result\...\
\
New Components:\

Kamaelia.

-   Chassis

```{=html}
<!-- -->
```
-   Seq

Codec

-   WAV, YUV4MPEG

Device

DVB

SoftDemux

Parse

-   ParseEventInformationTable, ParseNetworkInformationTable,
    ParseProgramAssociationTable, ParseProgramMapTable,
    ParseServiceDescriptionTable, ParseTimeAndDateTable,
    ParseTimeOffsetTable, PrettifyTables, ReassemblePSITables

Experimental

-   Chassis, ERParsing

File

-   MaxSpeedFileReader, UnixProcess2

Internet

-   TimeOutCSA

Protocol

MimeRequestComponent, RecoverOrder, SDP\

AIM

-   AIMHarness, ChatManager, LoginHandler, OSCARClient

HTTP

-   Handlers

```{=html}
<!-- -->
```
-   Minimal, Handlers/SessionExample, UploadTorrents

IRC

-   IRCClient

RTP

-   NullPayloadPreFramer, NullPayloadRTP, RTCPHeader, RTPHeader,
    RtpPacker, RTP

Util

Tokenisation

-   Simple

Collate, FirstOnly, Max, OneShot, PromptedTurnstile, RangeFilter,
RateChunker, SequentialTransformer, Sync, TagWithSequenceNumber,
TwoWaySplitter

UI

Pygame

-   Text, VideoSurface

Video

-   CropAndScale, DetectShotChanges, PixFormatConversion

Visualisation

ER

-   ERLaws, ERVisualiserServer, ExtraWindowFurniture, PAttribute,
    PEntity, PISA, PRelation

XML

-   SimpleXMLParser\

Components merged in from Apps:\

Kamaelia

Apps

Compose\

-   BuildViewer, CodeGen, PipeBuild, PipelineWriter, GUI

GUI

-   ArgumentsPanel, BuilderControlsGUI, TextOutputGUI

IRCLogger

-   Support

Show

-   GraphSlides

Whiteboard

-   Audio, Canvas, CheckpointSequencer, CommandConsole, Entuple,
    Options, Painter, Palette, Router, Routers, SingleShot,
    TagFiltering, Tokenisation, TwoWaySplitter, UI\

All of this also totally ignores the new examples & new Kamaelia based
apps.\
Also a new website is coming soon, but time ran out :-)\
\
\
\
