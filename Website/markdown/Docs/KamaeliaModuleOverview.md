---
pagename: Docs/KamaeliaModuleOverview
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Modules Overview]{style="font-size:24pt;font-weight:600"}

This file provides an overview of the current Kamaelia files, what they
are and where appropriate, how they work. This is designed to be a
living document, but not designed as raw API documentation. (There are
better ways of building API documentation) Essentially the purpose of
this documentis to act as \"the next layer up\" the documentation layers
- stating how and why the different parts are joined together.

-   Base Modules
-   Internet Adaption Modules
-   Network Protocol Modules
-   UDP Components
-   Utility Modules

[Base
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

The purpose of [\_\_init\_\_.py]{style="font-family:Courier 10 Pitch"}
is as usual to allow the kamaelia modules to be imported in the
traditional manner. It is empty however, so explicit naming of
submodules is needed after import.

[KamaeliaExceptions.py]{style="font-family:Courier 10 Pitch"} contains a
number of exceptions covering different potential failure points in the
modules. These exceptions generally inherit from
[AxonException]{style="font-family:Courier 10 Pitch"}.

[KamaeliaIPC.py]{style="font-family:Courier 10 Pitch"} however defines
some specific payloads for intercomponent communication. These are
generally control messages used by various Internet Adaption components
for signalling various events - normally relating to new or closed
socket events. The IPC messages inherit from
[Axon.IPC]{style="font-family:Courier 10 Pitch"}, and are mainly notify
events. Currently the only [producerFinished
]{style="font-family:Courier 10 Pitch"}class is [socketShutdown
]{style="font-family:Courier 10 Pitch"}- issued by Internet Abstraction
Modules.

[Internet Adaption
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

These modules provide the basic primitives relating to network handling.
Essentially the

purpose of each file defines a basic primitive in a normal network
system.

As with the base Kamaelia package,
[\_\_init\_\_.py]{style="font-family:Courier 10 Pitch"} is empty and
simply exists to allow package import as follows:

Clearly [socketConstants.py]{style="font-family:Courier 10 Pitch"}
contains a bunch of common constants - these aren\'t provided by the
socket module and largely cover error conditions, and are defined to
increase code readability.

The internet abstraction primitives can divided thus:

Connection Factories

-   [TCPServer.py]{style="font-family:Courier 10 Pitch"} acts as a
    factory spawning new connections which are handled by their own
    components and will often have a protocol handler associated with
    this.
-   [TCPClient.py]{style="font-family:Courier 10 Pitch"} also acts as a
    factory, but only spawns one connected socket. It acts as a data
    passthrough proxy for the subcomponent.

<div>

</div>

<div>

Neither connection factory [directly ]{style="font-style:italic"}handles
any data to/from a connected socket.

</div>

<div>

</div>

Specific Socket Handling:

[ConnectedSocketAdapter.py]{style="font-family:Courier 10 Pitch"}
manages any connected socket.

-   Any data recieved on its
    [DataSend]{style="font-family:Courier 10 Pitch"} inbox is sent to
    the socket in a non-blocking fashion, and any data recieved from the
    socket in a non-blocking fashion, is sent to the component outbox
    [outbox]{style="font-family:Courier 10 Pitch"}.
-   It only attempts to get data from the socket when it recieves an
    appropriate message on its
    [dataReady]{style="font-family:Courier 10 Pitch"} inbox.
-   When it recieves a
    [producerFinished]{style="font-family:Courier 10 Pitch"} message on
    its control port after having sent all outstanding
    [dataSend]{style="font-family:Courier 10 Pitch"} messages, it goes
    into a shutdown mode. This results in shutdown messages being sent
    to the [FactoryFeedback]{style="font-family:Courier 10 Pitch"} and
    [signal]{style="font-family:Courier 10 Pitch"} outboxes. This is due
    to the [ownership ]{style="font-style:italic"}of the connected
    sockets being elsewhere.

<div>

This simplicity allows the to be used
[ConnectedSocketAdapter]{style="font-family:Courier 10 Pitch"} by both
the connection factories.

</div>

Multiple socket handling.

-   [Selector.py]{style="font-family:Courier 10 Pitch"} is designed for
    dealing with checking to see if any network connections are active,
    and which
    [ConnectedSocketAdapter]{style="font-family:Courier 10 Pitch"}s need
    to be told they can/should attempt to recieve data. When it detects
    a server socket has a connection ready to be accepted it simply
    sends a message to a dynamically allocated outbox to send the
    appropriate [TCPServer]{style="font-family:Courier 10 Pitch"}
    factory a message to tell it to accept the connection.

Other code:

[InternetConnection.py]{style="font-family:Courier 10 Pitch"} is legacy
code and due to be ditched

[InternetHandlingTests.py]{style="font-family:Courier 10 Pitch"} is the
current test code being used to drive integration between
client/server/selector service. This is a relatively complex example:

-   It creates a SimpleServer running and EchoProtocol, and a client
    running an EchoCheckerProtocolComponent, and a TCPClient. The
    EchoCheckerProtocolComponent is wired in to handle the application
    communications. The client connects to the server making a complete
    loop.

[Network Protocol
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

This directory contains a collection of modules, each implementing a
simple of not so simple network protocol. Some of this are designed as
toy protocols and were used during the design of the system to flesh out
key areas. As before,
[\_\_init\_\_.py]{style="font-family:Courier 10 Pitch"} is simply an
empty file.

The only protocol here with a potential to be non-trivial is the
[HTTPServer.py]{style="font-family:Courier 10 Pitch"} protocol. The
implementation inside that component at this point in time is
deliberately very simplistic, and only implements a very simple very
small subset of HTTP/1.0. When run standalone it runs a simple webserver
on port 8082, sending random files to the client. The server code isn\'t
actually complete. Also note that this is an [extremely
]{style="font-style:italic;font-weight:600"}[insecure
]{style="font-style:italic"}web server as a result of these two facts.

[EchoProtocolComponent.py]{style="font-family:Courier 10 Pitch"} is the
simplest protocol implemented, and was unsurprisingly the first one to
be implemented - since it forms a simple loopback protocol useful for
integration testing. In practice this component is really a [data pass
through ]{style="font-style:italic"}component since all data recieved on
its inbox is passed on directly to its outbox. As a result this
component\'s implementation may actually migrate out to
[Kamaelia.Util]{style="font-family:Courier 10 Pitch"} as a simple buffer
component and allow this actual protocol component to simply inherit
from [Kamaelia.Util]{style="font-family:Courier 10 Pitch"}.

[FortuneCookieProtocol.py]{style="font-family:Courier 10 Pitch"} is one
step above
[EchoProtocolComponent.py]{style="font-family:Courier 10 Pitch"}. It
runs the fortune program on the server and sends the result to its
outbox. In a networked environment what this means is the server will
simply blat the fortune cookie to a client that connects to the server.

[AudioCookieProtocol.py]{style="font-family:Courier 10 Pitch"} is a
logical extension to
[FortuneCookieProtocol.py]{style="font-family:Courier 10 Pitch"}.
Similar to
[FortuneCookieProtocol.py]{style="font-family:Courier 10 Pitch"} it too
runs an external program and sends the result to its outbox. In this
case however rather than a short piece of text, it is a short snippet of
audio.

[SimpleVideoCookieServer.py]{style="font-family:Courier 10 Pitch"} does
essentially the same as
[FortuneCookieProtocol.py]{style="font-family:Courier 10 Pitch"} and
[AudioCookieProtocol.py]{style="font-family:Courier 10 Pitch"}, but this
time with a short piece of video.

[Utility
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

This is a small collection of utility components. They\'re designed as
simple filters for various uses - some perform simple, but useful
transformations that convert data into a format suitable for other
components, others are designed to be dropped in the middle of existing
linkages to allow debugging and/or output.

[\_\_init\_\_.py]{style="font-family:Courier 10 Pitch"} is as usual an
empty file for the usual reasons.

[ConsoleEcho.py]{style="font-family:Courier 10 Pitch"} is designed to
allow the system to take any data given on its inbox and send it to
stdout. It can also optionally forward the data recieved to it\'s outbox
meaning that it can be dropped in the middle of a linkage to enable
precise debugging when you wish to know what communications is taking
place.

[ToStringComponent.py ]{style="font-family:Courier 10 Pitch"}is a simple
filter component - it takes every object supplied via its inbox, calls
[str()]{style="font-family:Courier 10 Pitch"} on the object, and
forwards the result to its outbox. This allows, for example, a user to
take the output of any component, convert it to a string suitable for
output to a console. This doesn\'t require the console component to do
the conversion (since someone may wish to send the objects to a console
as an easy way to check types), and doesn\'t require components to
provide special behaviour.

[Multimedia
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

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
separation. The[ testing spike included shows how to use a file reading
component in conjuction with these two components to provide a file
reading/decode chain. ]{style="font-family:Cursor"}

[The two components provided are:]{style="font-family:Cursor"}

-   [VorbisDecode]{style="font-family:Courier 10 Pitch"}[ - takes ogg
    vorbis encoded audio from its inbox and provides raw decoded audio
    on its outbox.\
    Important note: This is currently ogg vorbis - as you would read
    from a file, NOT just vorbis encoded
    data.]{style="font-family:Cursor"}
-   [AOAudioPlaybackAdaptor]{style="font-family:Courier 10 Pitch"}[ -
    takes raw audio recieved on its inbox and sends it to the audio
    device. Currently this may well be a blocking operation. How to do
    this in a non-blocking manner is under investigation. If it recieves
    a
    ]{style="font-family:Cursor"}[producerFinished]{style="font-family:Courier 10 Pitch"}[
    message on its control inbox, this component
    exits.]{style="font-family:Cursor"}

[These components rely on the following libraries being
installed:]{style="font-family:Cursor"}

-   [libogg]{style="font-family:Courier 10 Pitch"}[,
    ]{style="font-family:Cursor"}[libao]{style="font-family:Courier 10 Pitch"}[,
    ]{style="font-family:Cursor"}[libvorbis]{style="font-family:Courier 10 Pitch"}[,
    ]{style="font-family:Cursor"}[libvorbissimple]{style="font-family:Courier 10 Pitch"}

[The python bindings required are:]{style="font-family:Cursor"}

-   [The python bindings supplied with
    ]{style="font-family:Cursor"}[libvorbissimple]{style="font-family:Courier 10 Pitch"}
-   [Pyrex is therefore also required.]{style="font-family:Cursor"}

[RTP Related
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

Bla bLa bla

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

[NullPayloadPreFramer.py]{style="font-family:Courier 10 Pitch"} - Not
written yet

Null Payload RTP Classes

Null Payload Pre-Framer

Null Payload RTP Packet Stuffer - Same thing.

This Null payload also assumes constant bit rate load.

Subcomponents functionality:

FileControl: - Only if RFA internal - isn\'t

FileReader - only if internal - isn\'t

FileSelector - only if internal - isn\'t

Format Decoding

DataFramaing

Command Interpreter (Likely to be component core code)

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

a [NullPayloadRTP.py]{style="font-family:Courier 10 Pitch"}sdsd

a [RTCPHeader.py]{style="font-family:Courier 10 Pitch"}adf

a [RTPHeader.py]{style="font-family:Courier 10 Pitch"}sdsd

a[ RtpPacker.py]{style="font-family:Courier 10 Pitch"} adf

[MIME & Disk Related
modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

adf

[Testing
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

adf

[Experimentation
Modules]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}

d

[Support
Files]{style="font-family:Century Schoolbook L;font-style:italic;font-size:13pt;font-weight:600"}
