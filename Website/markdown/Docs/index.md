---
pagename: Docs/index
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
```{=html}
<!-- -->
```
-   Find out [about Kamaelia](/Introduction.html)
-   [Setting up your environment](/GettingStarted.html) for development
-   Start with the examples in the [cookbook](/Cookbook.html)
-   Find out [how to make your own
    components](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1113495151)
-   Reference the full set of [components](/Components.html)
-   Learn the [fundamentals](/MiniAxon/)
-   Understand the full system

::: {.boxright}
[Please note: ]{style="font-weight:600"}The documentation here is
lagging, quite badly at the moment, behind the bulk of Kamaelia, which
is where all the interesting effort is going right now. Whilst
everything you see here should largely still be valid, be aware that
this really needs updating. We hope to rectify this ASAP. Good
documenters very welcome!
:::

Kamaelia\'s modules divide into 2 main sections:

[A core subsystem of modules](Axon.html) which provide the main
concurrency support

-   The core subsystem is suitable for use independently of Kamaelia
    itself, and is available as a separate download.

Modules for Kamaelia itself.

This document is the starting point for Kamaelia itself.

This file provides an overview of the current Kamaelia files, what they
are and where appropriate, how they work. This is designed to be a
living document, but not designed as raw API documentation. (There are
better ways of building API documentation) Essentially the purpose of
this documentis to act as \"the next layer up\" the documentation layers
- stating how and why the different parts are joined together.

-   [Base Modules](BaseModules.html)
-   [Internet Adaption Modules](InternetAdaptionModules.html)
-   [Network Protocol Modules](NetworkProtocolModules.html)
-   [UDP Components](UDPComponents.html)
-   [Utility Modules](UtilityModules.html)

[Multimedia
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:11pt;font-weight:600"}

These three files are all related to the same purpose - playback of
audio, and also decoding ogg vorbis. There are some restrictions on some
of these, and there is a recommendation on which ones to use. Each of
these requires a set of libraries - these are covered below.

[AOPlayer.py]{style="font-family:Courier 10 Pitch"} is deprecated, the
actual component has moved location, and you really ought not to use
this at the moment. This may change at some point in time.

-   Requires [libao]{style="font-family:Courier 10 Pitch"}, and the
    [pyao]{style="font-family:Courier 10 Pitch"} python bindings.

[oggFilePlayComponent.py ]{style="font-family:Courier 10 Pitch"}is the
oldest piece of code that can be used for decode and playback. It uses
the official xiph python bindings to decode ogg vorbis. On the surface
this is useful and if all you want to do is decode audio from a file,
this does work.

-   There is a key restriction - it MUST come from a file object that
    you have opened. It can\'t be something that looks like a file, it
    must be a file. The reason for this is internally the xiph bindings
    dive into the file object supplied, pull out the C filehandle and
    pass that over to
    [libvorbisfile]{style="font-family:Courier 10 Pitch"}.
-   Requires the following libraries:
    [libao]{style="font-family:Courier 10 Pitch"},
    [libogg]{style="font-family:Courier 10 Pitch"},
    [libvorbis]{style="font-family:Courier 10 Pitch"},
    [libvorbisfile]{style="font-family:Courier 10 Pitch"}
-   Requires the following python bindings:
    [pyogg]{style="font-family:Courier 10 Pitch"},
    [pyvorbis]{style="font-family:Courier 10 Pitch"},
    [pyao]{style="font-family:Courier 10 Pitch"}

This file contains the following components:

[oggPlayer]{style="font-family:Courier 10 Pitch"} - legacy component -
you used to be able to choose between AOPlayer and

[PlayerComponent]{style="font-family:Courier 10 Pitch"} - This is an
abstract class that provides the main functionality of a player. Is is
overridden by client subclasses. Subclasses are only expect to override
the [write]{style="font-family:Courier 10 Pitch"} method. The key method
in the payer component is a [play]{style="font-family:Courier 10 Pitch"}
generator. Nastily, this generator calls
[VorbisFile]{style="font-family:Courier 10 Pitch"} to enable file
reading, unpacking of ogg and decode.

<div>

Current concrete subclasses:

</div>

-   [AOPlayer]{style="font-family:Courier 10 Pitch"} - This simply
    provides a [write]{style="font-family:Courier 10 Pitch"} method to
    send audio to a [libao]{style="font-family:Courier 10 Pitch"} audio
    device.

It\'s worth noting that the execution here is pretty ugly, and it was
the motivation for writing the next file. However, if all you want is to
use [libvorbisfile]{style="font-family:Courier 10 Pitch"},
[oggFilePlayComponent.py]{style="font-family:Courier 10 Pitch"} can be
useful.

[vorbisDecodeComponent.py]{style="font-family:Courier 10 Pitch"} was
written to overcome the limitations metioned above. Specifically this
provides 2 components - one that will accept ogg vorbis data on an inbox
and provide back raw decoded audio on its outbox, and another that takes
audio on its inbox and plays the audio. This provides much cleaner
separation. The testing spike included shows how to use a file reading
component in conjuction with these two components to provide a file
reading/decode chain.

The two components provided are:

-   [VorbisDecode]{style="font-family:Courier 10 Pitch"} - takes ogg
    vorbis encoded audio from its inbox and provides raw decoded audio
    on its outbox.\
    Important note: This is currently ogg vorbis - as you would read
    from a file, NOT just vorbis encoded data.
-   [AOAudioPlaybackAdaptor]{style="font-family:Courier 10 Pitch"} -
    takes raw audio recieved on its inbox and sends it to the audio
    device. Currently this may well be a blocking operation. How to do
    this in a non-blocking manner is under investigation. If it recieves
    a [producerFinished]{style="font-family:Courier 10 Pitch"} message
    on its control inbox, this component exits.

These components rely on the following libraries being installed:

-   [libogg]{style="font-family:Courier 10 Pitch"}[,
    ]{style="font-family:Cursor"}[libao]{style="font-family:Courier 10 Pitch"}[,
    ]{style="font-family:Cursor"}[libvorbis]{style="font-family:Courier 10 Pitch"}[,
    ]{style="font-family:Cursor"}[libvorbissimple]{style="font-family:Courier 10 Pitch"}

The python bindings required are:

-   The python bindings supplied with[
    ]{style="font-family:Cursor"}[libvorbissimple]{style="font-family:Courier 10 Pitch"}
-   Pyrex is therefore also required.

[RTP Related
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:11pt;font-weight:600"}

\...\...

[bitfieldrec.py - ]{style="font-family:Courier 10 Pitch"}Module
containing utility functions to allow structures with arbitrary
structures for bitstreams/bitfields. Currently only supports packing.
Does not support unpacking (yet).Bit Field Record Support. Usage:\
1. subclass bfrec\
2. Define a class var \"fields\"\
3. The value for this field should be a list of \"field\"s, created by
calling the static method field.mkList. This takes a list of tuples, one
tuple per field. (fieldname, bitwidth, None or list)

class field(str)

-   staticmethod mkList(fieldDefs)
-   fieldDefs = seq of (name, size,extra)

class bfrec(AxonObject)

\_\_init\_\_(self, \*\*args):

structureSize(self)

pack(self)

serialiseable(convert,aField) - Returns an iterable collection of
values. (eg list) Either an existing one, or puts scalar/singleton
values into a list. Doing this removes a special case.

Algorithm:

-   This actually does need documenting properly. The algorithm was
    designed using test first approaches, and so is pretty solid, but
    documenting it would be a good idea. If only because it\'s actually
    quite nice :)

[NullPayloadPreFramer.py]{style="font-family:Courier 10 Pitch"} - \....

-   This Null payload also assumes constant bit rate load.

Subcomponents functionality:

FileControl: - Only if RFA internal - isn\'t

-   FileReader - only if internal - isn\'t
-   FileSelector - only if internal - isn\'t

Format Decoding

DataFramaing

Command Interpreter (Likely to be component core code)

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

-   [NullPayloadRTP.py ]{style="font-family:Courier 10 Pitch"}\...\...
-   [RTCPHeader.py ]{style="font-family:Courier 10 Pitch"}\...\...
-   [RTPHeader.py ]{style="font-family:Courier 10 Pitch"}\...\...
-   [RtpPacker.py ]{style="font-family:Courier 10 Pitch"}\...\...

[MIME & Disk Related
modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:11pt;font-weight:600"}

\...\...

[Testing
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:11pt;font-weight:600"}

\...\...

[Experimentation
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:11pt;font-weight:600"}

\...\...

[Support
Files]{style="font-family:Century Schoolbook L;font-style:italic;font-size:11pt;font-weight:600"}

\...\...
