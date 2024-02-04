---
pagename: AnsweredQuestions
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Asked and Answered Questions ]{style="font-size:22pt;font-weight:600"}

[Draft]{style="font-size:16pt"}

(Names regarding questions removed, more generalisation/summarisation to
come)

\> - (how) does kamaelia help me in defining my protocol state machines?

Kamaelia doesn\'t \_directly\_ simplify the process of building a
protocol using

a state machine, but can help people avoid having to implement the
protocol

as a state machine.

Take a simple TCP Client for example. One of the most direct ways to
write a

TCP client might be as follows (handling some basic error cases):

def runClient(self,sock=None):

try: sock = socket.socket(socket.AF\_INET, socket.SOCK\_STREAM)

try:

sock.setblocking(0);

try: sock.connect(sock,(self.host, self.port)

while working:

\# Do work with the connection.

finally:

result = sock.shutdown(2)

finally:

sock.close()

finally:

sock.close()

This is relatively clear, and in a threaded environment you could quite

happily use this. However in a single threaded environment you\'d
normally

need to change that to being a state machine.

However, using Kamaelia, since we use generators we can choose to use
this in

a single threaded environment quite happily by yielding at various
points in

time.

Since the ability to do try:\... finally:\... in

generators is only just appearing in 2.5, we use the

following to force the same behaviour:

try:

\... some work that requires shutdown

raise Finality \# (subclasses Exception)

except Exception, e

\# do shutdown

raise e

Furthermore, since TCP connecting can fail at any point in time, we can
use

the yields during testing to force failures and check that the correct

behaviours ensue by checking execution traces:

def runClient(self,sock=None):

\# The various numbers yielded here indicate progress through the

\# function, and nothing else specific.

try:

sock = socket.socket(socket.AF\_INET, socket.SOCK\_STREAM); yield 0.3

try:

sock.setblocking(0); yield 0.6

try:

while not self.safeConnect(sock,(self.host, self.port)):

yield 1

yield newComponent(\*self.setupCSA(sock))

while self.waitCSAClose():

self.pause()

yield 2

raise Finality

except Exception, x:

result = sock.shutdown(2) ; yield 3

raise x \# XXXX If X is not finality, an error

\# The logical place to send the error is to the signal outbox

except Exception, x:

sock.close() ; yield 4,x \# XXXX If x is not finality, an error

raise x

except Finality: \# Not an error

yield 5

except socket.error, e:

\# Pass on the socket error to the next in the chain to let them know

\# of failure.

\#

self.send(e, \"signal\")

This still clearly follows the same basic structure, and in Python 2.5
will

be able to be shorter and clearer (due to supporting try\...finally in

generators).

Obviously you could turn the above into a state machine - essentially
take

the code chunks between yields, turn each into a state and then use a
state

variable to control which state you\'re in.

The ability to have the structure of the code follow the basic logic of
the

protocol in hand (TCP setup/shutdown clearly being a simple case - but
easy

to get wrong) makes it easier for a maintainer to look at later on.

That\'s relatively low level. If you\'re writing a protocol that sits on
top of

TCP or multicast then at present you can write a protocol using the
following

basic pattern:

class myProtocol(component):

def main(self):

\# Local protocol setup

while 1:

yield 1

if self.dataReady(\"inbox\"):

\# Data has been recieved on the socket and passed to our inbox

data = self.recv(\"inbox\") take the data

\< do whatever you\'d normally do for your protocol \>

self.send(response, \"outbox\")

\# send data to the connection via our outbox.

OK, on the surface it doesn\'t look like you\'ve gained much, but what
it does

allow is the automated testing of a protocol handler without involving
the

network at all. This allows you for example to do the following:

pipeline(

ReadFileAdaptor(\"destruction\_data\"),

myProtocol(),

ResultsChecker(\"expected\_data\"),

consoleEchoer()

).run()

Furthermore, if you have a protocol that has stages (such as read
header,

read body), this can be expressed very directly:

class stagedProtocol(component):

def main(self):

\# Local protocol setup

try:

readingHeader = True

while readingHeader:

yield 1

if self.dataReady(\"inbox\"):

\# Assume data from socket has been collated as a line

\# (lines starting with whitespace appended onto preceding

\# lines

data = self.recv(\"inbox\") take the data

try:

header, value = self.parseHeaderLine(data)

try:

self.requestHeader\[header\].append(value)

except KeyError:

self.request\[header\] = \[ value \]

except BadHeader:

readingHeader = False

readingBody = True

while readingBody:

yield 1

if self.dataReady(\"inbox\"):

\# Data has been recieved on the socket and passed to our inbox data =
self.recv(\"inbox\") take the data

\< do whatever you\'d normally do for your protocol \>

self.send(response, \"outbox\")

\# send data to the connection via our outbox.

self.send(self.generateResponse(), \"outbox\")

OK, in pratice you might want to split this into probably 3 methods -
one for

handling the reading header loop, one for the reading body loop, but you

can clearly see the logic - as could any new programmer coming along (in

what, a screenfull of code?).

Obviously this doesn\'t preclude using a traditional state machine
approach,

but it does provide an alternative (hopefully interesting/compelling).

For an example on composing a protocol is here:

\* http://kamaelia.sourceforge.net/SimpleReliableMulticast.html

The source files relating to this are here:

\* Actual logic of protocol: http://tinyurl.com/9ls9v

\* Framing and chunking: http://tinyurl.com/9rarp

\> - are timers supported?

At present not directly. However a component can do this:

self.pause()

yield 1

That will tell the scheduler not to give the component any CPU time.
Whilst

there isn\'t a component for this at present, we do have the concept of

services. A timer service could be constructed fairly easily such that a

timer service could be used as follows:

class myComponent(component):

Outboxes = { \"outbox\": \"default data outbox\",

\"signal\": \"default data outbox\",

\"timerbox\": \"default data outbox\",

}

\...

timerservice = Timer.getTimerService()

self.link((self, \"timerbox\"), timerservice)

sleep\_seconds = 5 \# number of seconds to sleep

self.send( (sleep\_seconds, (self,\"control\") ) , \"timerbox)

self.pause(); yield 1

\...

This would not be a hard realtime event of course, rather a soft
realtime

event. (We\'ve deliberately shied away from a specific events model so
far,

though it will be added at some point)

\> - do you have any experience with load/stress testing? (e.g. can I

\> use kamaelia to set a server under heavy load for testing?)

If you haven\'t seen it I\'ve written a white paper about Kamaelia which
is

essentially a translation of \"slides+what I said\" into text
(presentations

given at Europython & ACCU/Python UK). This can be found here:

\* http://www.bbc.co.uk/rd/pubs/whp/whp113.shtml

(PDF only, if you want a different format for whatever reason, let me

know - it will be on the website in HTML form at some point.)

\> Quoting Michael Sparks \<michaels\@rd.bbc.co.uk\>:

\> \> data = self.recv(\"inbox\") take the data

\> \> \< do whatever you\'d normally do for your protocol \>

\> \> self.send(response, \"outbox\")

\>

\> Can I assume, that I can have multiple in- and outboxes?

Sure - think pins on a chip - you have multiple in-pins and out-pins.
Each

expecting specific sorts of information carrying either signalling or
data

information.

The default set is as follows - this declaration simply overwrites the

defaults with the defaults:

class someComponent(component):

Inboxes = \[ \"inbox\", \"control\" \]

Outboxes = \[ \"outbox\", \"signal\" \]

A more complex example in CVS which is currently being documented is a

sprite component (originally part of an optimisation test). Since the
actual

inbox/outbox datastructures are created during initialisation by simply

interating through the lists of names of components, you can use this to

help document the purpose of the inboxes/outboxes as well. For example

the sprite component:

class BasicSprite(component):

Inboxes= {

\"rotator\" : \"Recieves a value between 0 and 360 to set the current
rotation\",

\"translation\" : \"Set the current position - translation - from the
origin - expects a tuple for the pixel position\",

\"scaler\" : \"Expects a floating value greater that 0, normally \<=1.0
- scales the current image by this preserving aspect\",

\"imaging\" : \"Expects a pygame surface that contains an image,
replaces the image the sprite surface is showing with this\",

\"inbox\" : \"default, unused\",

\"control\" : \"default, used to tell the BasicSprite to shutdown\",

}

\# Take default outboxes

\> \> \* Actual logic of protocol: http://tinyurl.com/9ls9v

\> \> \* Framing and chunking: http://tinyurl.com/9rarp

\>

\> I could not access these pages. Could you please send the

\> complete link? Thanks.

Sorry - simply used it for brevity - the links are here:

Logic:

-   http://cvs.sourceforge.net/viewcvs.py/kamaelia/Code/Python/Kamaelia/Kamaelia/Protocol/SimpleReliableMulticast.py?rev=1.2&view=markup

Framing/Chunking:

-   http://cvs.sourceforge.net/viewcvs.py/kamaelia/Code/Python/Kamaelia/Kamaelia/Protocol/Framing.py?rev=1.2&view=auto

\> \> This would not be a hard realtime event of course, rather a soft
realtime

\> \> event. (We\'ve deliberately shied away from a specific events
model so

\> \> far, though it will be added at some point)

\>

\> Some communication protocols have some demands on timer accuracy\...

Indeed - currently we\'re building up the building blocks slowly -
rather than

jumping straight in with ones that do require timer accuracy. (Think

automated creation of tunnels between multicast islands, and bit-rate

limited serving of pre-encoded content on a content agnostic channel)

\> What do you mean by events model? The structure/encoding of

\> events?

One common approach to concurrency - is to have an events wheel - much

like the approach taken by simulation systems. However it can encourage
a

certain kind of architecture, and we\'re really experimenting to find a

method of building these sorts of systems easily. (Hence modelling the

system on an approach where building blocks seems to work)

\> Btw. do you know SimPy (= Simulation in Python)? See

\> http://simpy.sourceforge.net/ and the Debian packages at

\> http://packages.debian.org/stable/python/python-simpy

I do indeed. I haven\'\'t had a look at how they\'re doing recently, but
at some

point we\'ll need to revisit things because their events model is pretty
good.

(But then being based on Simula\'s approach it would be!)

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\> Kamaelia seems it might be an interesting project. However, I don\'t

\> think the project is well served by this announcement \-- which I

\> find vague and hard to understand. Which is a shame, because it

\> means that other people probably don\'t understand it very well

\> either, which means less people will use it.

It is a shame, and thanks for mentioning this.

OK, here\'s a better go. (It\'s always difficult to think where to pitch

this sort of thing)

\-\--START\-\--

The project aims to make it simple to build networked multimedia

systems (eg audio, video, interactive systems), which are naturally

componentised and naturally concurrent allowing quick and fast reuse in

the same way as Unix pipelines do.

It is designed as a practical toolkit, such that you can build systems

such as:

\* Ogg Vorbis streaming server/client systems (via vorbissimple)

\* Simple network aware games (via pygame)

\* Quickly build TCP based network servers and clients

\* Quickly build Multicast based network servers and clients

It runs on Linux, Window, Mac OS X with a subset running on Series 60

phones.

The basic underlying metaphor of a component us like an office worker

with inboxes and outboxes, with deliveries occuring between desks,

offices, and depts. The component can thus do work anyway it likes but

only communicates with these inboxes and outboxes. Like office workers,

components run in parallel, and to achieve this are generally

implemented using python generators, but can also used threads.

The rationale behind the project is to provide a toolkit enabling the

development of new protocols, including streaming, for large scale

media delivery. The license essentially allows use in proprietary

systems without change, but all changes to the system itself must be

shared.

\-\--END\-\--

Is that clearer ?

A short summary of all that could be:

\"\"\"Kamaelia is a networking/communications infrastructure for
innovative

multimedia systems. Kamaelia uses a component architecture designed to

simplify creation and testing of new protocols and large scale media

delivery systems.\"\"\"

Hopefully that\'s clearer than:

\>\>Kamaelia is a collection of Axon components designed for network

\>\>protocol experimentation in a single threaded, select based

\>\>environment. Axon components are python generators are augmented by

\>\>inbox and outbox queues (lists) for communication in a communicating

\>\>sequential processes (CSP) like fashion.

\[ which you noted \"I really have very little idea what this means.\"
\]

\> The information I can guess out of this is: \"Kamaelia is a library

\> for creating network protocols that sit on top of tcp and/or udp\".

\> Given that it\'s a BBC project, I imagine we\'re talking about

\> protocols for transferring large amount of data, e.g. sound or

\> motion pictures.

Indeed. However, if you\'re having to guess I\'m not doing the best job

(despite trying!) at explaining this.

\> BTW, the html is broken in that it\'s very poorly written,

It\'s written using a PyQT based WYSIWYG editor (written on my time,

not the BBC\'s) that has the limitation that preformatted text gets

squished (since the editor doesn\'t support the pre tag - or indeed

a lot of other tags). At some point I\'ll fix the editor to handle

pre-formatted text, but it\'s not a priority right now. (Should it be?)

The HTML isn\'t really \*that\* bad as far as generated code is
concerned

IMHO, and is directly what the PyQT QTextEdit widget creates. (It\'s not

that great either - you may notice it doesn\'t have proper headings

either)

\> doesn\'t use CSS,

This isn\'t a problem IMHO, YMMV. The site\'s been tested on a variety
of

browsers/platforms and looks pretty much the same on all.

\> I guess the main question that needs to be answered is \"Why would I,

\> as a programmer, use Kamaelia?\"

Probably the most interesting response I\'ve had back from people
who\'ve

picked it up is that it\'s FUN. You can write small sketches (throwaway

code fragments), rewrite their inputs/outputs to take data from inboxes

& outboxes, and then it\'s usable in a much wider system. It encourages

reuse of code, and assimilating existing systems can be relatively

trivial.

For example, trivial sketches:

\* A program to display an image using pygame

\* A program that can understand when an area of space has been

clicked. (call it a button)

\* A program that can print a list of filenames, pausing waiting for a

user to press return. (call it a chooser)

Trivial changes:

\* Take the filename of the image from an inbox

\* Rather than print the filenames to send the filename to an outbox.

\* Rather than wait for a user to press a key, wait for a message on

an inbox.

A useful composition linking some of these together:

Graphline(

CHOOSER = Chooser(items = files),

IMAGE = Image(size=(800,600), position=(8,48)),

NEXT = Button(caption=\"Next\", msg=\"NEXT\", position=(72,8)),

PREVIOUS = Button(caption=\"Previous\", msg=\"PREV\",position=(8,8)),

linkages = {

(\"NEXT\",\"outbox\") : (\"CHOOSER\",\"inbox\"),

(\"PREVIOUS\",\"outbox\") : (\"CHOOSER\",\"inbox\"),

(\"CHOOSER\",\"outbox\") : (\"IMAGE\",\"inbox\"),

}

).run()

And you have a simple presentation tool !

Another example. The visualisation framework was originally a stand

alone piece of code and was essentially just a piece of eye candy. I

threw in a few yields into certain locations. File reading & static

graph construction was replaced with recieving data from inboxes, and

then it was available for use (and networked after creating trivial

protocol components).

A piece of eye candy is now a useful tool. It\'s likely to gain the

ability to send to an outbox a message saying \"this blob is clicked\"

meaning we can have \'WYSIWYG\' GUI based construction of pipelines

easily.

It\'s designed literally as a tool for making it simple to bolt things

together with minimal change. (Which means you choose what you

use, not the framework.)

The system also lends itself to test driven and network independent

development, something not that simple normally with network

protocols.

Why wouldn\'t you use it? When Twisted is appropriate (Twisted is a more

mature framework).

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\>\>\> Is the audience programmers or

\>\>\> less technical people? A project that allows non-technical people

\>\>\> to build complex network applications is an ambitious one, but
not

\...

\>\>It\'s a little ambitious at this stage, yes.

\> But it couldbe there eventually?

Could? Yes. Will? Can\'t say. I can agree it would be nice, and given

time/resources (or someone sufficiently interested externally) then it

may happen. (IMO there\'s no real reason that it couldn\'t happen aside

from time/effort/resources)

\>\>\> What sort of servers and clients?

\>\>Whatever you feel like. If you want a server to split and serve
audio,

\>\>you could do that.

\> This is streaming audio, right? For non-streaming I can just use an

\> ftp or http server.

There\'s more to network servers and clients than just audio & video, or

unidirectional download.

For example the visualisation/introspection tool is an example of a

client server system. The server is the visualisation tool. It listens
on a

specified port waiting for a connection. The client connects and sends

data to it about the internal structure, and the server displays this.

\>\>\>\> \* Quickly build Multicast based network servers and clients

\>\>\> Serving what? Could I use it, for example, to build an n-player

\>\>\> encrypted VoIP server to allow people to do conference calls over

\>\>\> the Internet?

\>\>

\>\>You could do that probably. (Though we don\'t have a component

\>\>for audio capture (though a read file adaptor reading from
/dev/audio

\>\>might work depending on your platform I suppose) and audio

\>\>encoding at the moment, so those would probably be the core

\>\>components to integrate.

\>

\> That\'s a slightly worrying answer for me, worrying because it seems

\> I\'ve misunderstood the nature of the project. I assumed that

\> components for audio capture, and related activities, would be at

\> the heart of the project.

\*Our\* main interest, at the moment, is in /delivery/ of content.

Dealing with capture would be largely re-inventing wheels before we know

whether the framework is a suitable framework. We are looking at making
it

possible to use pymedia for dealing with capture/encoding/decoding.

There\'s a number of things along the way we need to deal with this, but

we\'re not starting from the perspective of capture.

(After all for capture we can generally look at using dedicated encoder

hardware that will often spit out it\'s encoded information in the form
of a

network connection. As a result capture and encoding hasn\'t been a
priority

as yet. Sometimes looking into a project from the outside I can
appreciate

that certain decisions might look strange, but consider that you don\'t
need

to worry about capture in order

\>\>\> (I mean proper encryption here, the sort GCHQ or the NSA can\'t
break)

\>\>

\>\>I\'d be impressed if that could be written, using anything really.
(Can\'t

\>\>implies never)

\>

\> What \-- good encryption? That\'s pretty much a well-known technique

\> these days (unless the NSA has some \*very\* advanced hardware in

\> their basement, which I strongly suspect they don\'t).

You said \*can\'t\*. That says to me cannot ever be broken. If you have
a large

number of listeners, as your statement implied, that implies decryptable
by

many listeners - you then just need one compromised listener
(essentially

you\'re asking for the equivalent of implementing a DRM system that the
NSA

couldn\'t break\...).

If you can provide me with a library that you can guarantee that it will

satisfy the following properties:

encoded = F(data)

and a piece of client code that can do this:

decoded = G(encoded)

Then yes, that can be wrapped. That\'s trivial in fact:

\-\--(start)\-\--

from magic import unbreakable\_encryption

class encoder(component):

def \_\_init\_\_(self, \*\*args):

self.encoder = unbreakable\_encryption.encoder(\*\*args)

def main(self):

while 1:

if self.dataReady(\"inbox\"):

data = self.recv(\"inbox\")

encoded = self.encoder.encode(data)

self.send(encoded, \"outbox\")

yield 1

class decoder(component):

def \_\_init\_\_(self, \*\*args):

self.decoder = unbreakable\_encryption.decoder(\*\*args)

def main(self):

while 1:

if self.dataReady(\"inbox\"):

data = self.recv(\"inbox\")

decoded = self.decoder.decode(data)

self.send(decoded, \"outbox\")

yield 1

\-\--(end)\-\--

If you believe you can implement F&G for general use such that F&G

can //never// be decrypted by anyone other than authorised recipients, I

suggest you cease this conversation - you have some highly marketable

technology.

\>\>\>\>The basic underlying metaphor of a component us like an office
worker

\>\>\>\>with inboxes and outboxes, with deliveries occuring between
desks,

\>\>

\>\>\> That metaphor brings up an image (at least to me) that the sorts
of

\>\>\> data that can be communicated are things like documents,

\>\>\> spreadsheets, business graphs, memos.

\>\>

\>\>They could indeed. The underlying framework doesn\'t differentiate

\>\>between data nor have any realtime aspect embedded in the system

\>\>at present. Just because we\'re focussing on systems that have a
realtime

\>\>element and are multimedia based, this does not mean the system is

\>\>limited to that.

\>

\> Again, this makes me think I\'ve misunderstood the project.

Realtime systems are a subset of all systems that are interesting in
terms

of network delivery & multimedia systems. Realtime scheduling is a well

known area and if/when this becomes an issue, we\'ll look at adding it
into

the mix. The real problem is dealing with concurrency and making it
simple

to work with. Making realtime concurrent systems easy to work with
strikes

me as running before you can walk.

(Network systems are naturally concurrent, so if you\'re aiming to make

network systems easy to build you\'re really talking about making
concurrent

systems easy to build.)

\>\>\> OK, I get the straming part of it. But what asbout non-streaming

\>\>\> stuff? What other protocols are necessary?

\>\>

\>\>One example is peer to peer mesh setup. People normally

\>\>think of P2P as a distribution mechanism. However, the underlying

\>\>approach also very good at setting up communications meshes.

\>

\> When you say a mesh, what do you mean?

I mean a mesh. (see below)

\>\>This could be of use in many areas, such as GRID based systems

\>\>for distributed rendering, application layer multicast, and network

\>\>multicast island joining.

\> Unpack, please.

They\'re all big systems, all of which utilise networks of collaborating

systems for different purposes.

Grid starting point:

\* http://en.wikipedia.org/wiki/Grid\_computing

\*short\* introduction to application level multicast (has many names,

including overlay multicast):

\* http://www.mnlab.cs.depaul.edu/seminar/fall2002/Overcast.pdf

\* Also puts the term \"mesh\" in context.

Multicast island joining is a special case and is exactly what it says -

joining multicast islands together.

\>\>Due to the illegal /uses/ of P2P, much work in this area is
difficult to

\>\>reuse due to defensive coding.

\>

\> Oh. Could you give an example?

How many RFCs have you seen documenting the protocols used by (say)

Napster, Bit Torrent, Gnutella, Limewire, Freenet? The legitimate uses
of

Bit Torrent for example tend to get ignored by certain large companies

when trying to shut down systems.

\>\>We also have to be able to demonstrate system to other people

\>\>inside the BBC in a way non-technical people understand. That means

\>\>showing structures in a friendly dynamic way, showing pictures,

\>\>playing sounds (hence visualisation - looking inside running
systems).

\>

\> Visualisation, if done properly, ought to be useful to technical

\> people too.

It is (as mention on the page describing the visualisation tool).

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\>\>Which aside from other things means you can\'t build (say) a video

\>\>& SMIL playback system trivially, yet.

\>

\> Isn\'t SMIL something that\'s goinhg to go into web browsers? In
which

\> case, you\'d presumably not want to build one yourself, I imagine?

SMIL was used as an example to be illustrative of a class of networked

applications that require visual support. A more direct example

would be MHEG (not mpeg) decoding and display systems, which

have similarities to SMIL systems in terms of capabilities required.

\>\>It\'s designed to make bolting things together to make these sorts
of

\>\>system simpler and easier.

\>

\> What you say \"bolting things together\" do you mean writing Python

\> code?

Yes.

\> Or will there be some other way?

A clicky pointy approach would be nice. (There\'s two sorts of interface
in

the world IMO - \"tappity tappity\" and \"clicky pointy\" - if being
equally

playfully disdainful :) Unix shell systems are very \"tappity tappity\",
and whilst I

can do \"tappity tappity\", and have been doing \"tappity tappity\" for
my

entiring working life, I do prefer \"clicky pointy\" systems.)

Though building systems using AR Toolkit type systems would be the
ideal.

( http://www.hitl.washington.edu/people/poup/research/ar.htm\#artoolkit
)

That\'s probably a couple of years off though (at least).

\> What I have in mind is something like a project I worked on some

\> time ago, where a program could be written by drawing boxes on a GUI

\> application, and drawing lines (representing data flow) to connect

\> the boxes. So one half of a VoIP application might look like:

\>

\> +\-\-\-\-\-\-\-\-\--+ +\-\-\-\-\-\-\-\-\-\-\--+
+\-\-\-\-\-\-\-\-\-\--+

\> \| listen \| \| convert to \| \| volume \|

\> \| on udp \|====\>\| audio \|====\>\| control + \|

\> \| port 600 \| \| stream \| \| output \|

\> +\-\-\-\-\-\-\-\-\--+ +\-\-\-\-\-\-\-\-\-\-\--+
+\-\-\-\-\-\-\-\-\-\--+

From example 4:

pipeline(

Multicast\_transceiver(\"0.0.0.0\", 1600, \"224.168.2.9\", 0),

detuple(1),

SRM\_Receiver(),

detuple(1),

VorbisDecode(),

AOAudioPlaybackAdaptor(),

).run()

Join multicast group \"224.168.2.9\", listen for packets on port 1600,
throw

away information relating to who sent it, pass it through a simple
reliable

multicast reordering subsystem, throw away the annotation, decode the

vorbis, and playback.

The visual representation of that isn\'t dissimilar to your diagram
above.

\> With something like this novel multimedia apps could be prototyped

\> quickly (though making them into useful apps would take extra work

\> \-- in the case of a VoIP application you\'d want a phonebook, for

\> example).

Agreed.

\>\>At the same time it\'s designed to encourage

\>\>writing code in a way that makes it simpler.

\>

\> Examples would be useful here. Both of what it can do now, and what

\> it will be able to do eventually.

Examples of what can be done now are here:

\* http://kamaelia.sourceforge.net/KamaeliaStatus.html

I\'ll think about the latter part of that. (I personally loath
technologies

that promise much and deliver little. Hence why I like to focus on what

we /can/ do)

\>\>The natural side effect of

\>\>this is the system might make it easier to take advantage of
multiple

\>\>CPU systems as they come online, since it makes a system naturally

\>\>concurrent. As the original announcement said \"Kamaelia is designed
as

\>\>a testbed\". And by testbed I mean testbed as it testing out new
ideas,

\>\>see if they work and see if they pan out. (Not as in a testing
suite)

\>

\> So what it will eventually do is not cast in stone?

The high level goals are to solve the problems in the Challenges
document.

We\'re not particularly wedded to any one particular approach, and
Kamaelia

can/should be moulded to solve those problems, not the other way round.

By definition along the way a variety of components will be generated,
which

can obviously be put together in an arbitrary fashion, assuming type

adaptors as necessary, to form new interesting systems.

This ability to explore new/interesting systems quickly is something

generally of value to an R&D dept, so there\'s some people at BBC R&D

interested in using Kamaelia for all sorts of interesting projects.
(which I

can\'t discuss here)

\>\>Components are object instances of python classes. The data passed

\>\>between components are object instances.

\>

\> What sort of objects?

Python objects. Numbers, strings, chunks of audio in a string, chunks of

audio in a binary object wrapped by a python class, etc. Precisely as I

said.

\> For example, if an application is audio

\> straming, what sort of objects will be passed?

That depends on the level to which you dive inside the audio being

streamed. If you\'re trying to be a content agnostic streamer then you

don\'t care what\'s inside the byte stream (from, say, a file) just what
the

bit rate is you\'re supposed to send at. (for that you can just chop up
the

file and send it chunks at a time)

If however you\'re dealing with variable bit rate data you may wish to
look

inside the wrapper to figure out the where data blocks are for a given
time

period in order to send those. This (for example in the case of sending
MPEG

over RTP) can mean that you need to parse the data stream in order to
send

the data. At that point it makes sense to send over a structured object

representing each chunk/block/frame (depending on codec/transport).

\> Will there be onre

\> object passed for each 10 ms or so of sound, or will there be a

\> continuously-set-up object that passes the data throught it a byte

\> at a time?

Small messages turn out to be inefficient for what it\'s worth. (It\'s
more

efficient to send bundles of small message or larger messages)

\> And if it\'s written in Python, will it run fast enough?

I\'ve seen overlay mesh networks implemented in TCL shipping 60Mbit/s

(sustained) in the past, which if we\'re implementing an overlay joining

multicast islands together would mean multicasting the equivalent of
\~200

channels through each node. Scaling is not always about throughput of

course - Bit Torrent\'s initial implementation was also in python, and
scales

very well.

If it doesn\'t scale sufficiently we can always optimise specific
subsystems

when we need to rather than prematurely optimise. Also we have done a

naive (deliberately naive) translation of the ideas into C++, including

generators, so if things don\'t pan out we have a natural migration path
else

where. (After knowing whether the overall approach is workable or not)

\> cdef class test(Axon.Component.component):

\> def mainBody(self):

\> if self.dataReady(\"inbox\"):

\> data = self.recv(\"inbox\")

\> self.send(data, \"outbox\")

\> return 1

\>

\> My first impressions are that it seems obvious to me what this does:

A line of code is more often read than written, so if it\'s obvious,
that\'s

good.

\> it merely passes its input throught to its output

Correct.

\> (no doubt there are places where such a null component is useful).

An echo protocol is one example - a server you connect to that simply
echoes

back to you whatever you send it. (an echo server can be useful for all

sorts of network testing in practice)

\> Hopefully all code written with Kamaelia will be so clear.

See here for a longer example - which should show that generally
speaking

things do tend to remain clear: http://tinyurl.com/dp8n7 (also shows how

you can incrementally develop new components).

\> Now I have some questions.

\>

\> 1. mainBody() is evidently being called at intervals. At what

\> frequency are these intervals? For example, if the data stram is

\> video data, will mainBody() get called once for each frame?

The scheduler is currently a dumb scheduler with essentially the
following

logic:

for thread in microthreads:

thread.next()

As a result the time between calls is not guaranteed (nor can it be with

this sort of scheduler). The system does however allow for multiple

schedulers, so you could potentially have a realtime scheduler if it

was found to be necessary, at which point information about how a

component wished to be scheduled would become important.

\> 2. what data type is (data) in the code? Or can it be any type?

Any data type python handles. (as indicated above)

In case you\'re wondering \"why doesn\'t it do everything yet\", I\'ll

just simply reiterate that we\'re at version 0.2, and we\'re getting

to the crawling/walking stage first before the walking/talking/running

stage :-)

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\> It seems as though all components basically have to do busy waiting
now.

You are right - components are, for the most part, busy-waiting. Which

is not a good thing!

\* However the scheduler does periodic POSIX sched\_yield calls

\> So do you plan on including a kind of scheduler-aware blocking

\> communication (like the \`channels\` of the \`tasklets\` in
stackless)?

\>

\> (as you have a postman already - not a bad idea i think if you
compare

\> with multi-agent-systems theory (see jade) - it could be responsible
for

\> alerting the scheduler of box.has\_data)

There is basic support for components to block, by calling the

self.pause() method. From the next yield, this blocks further execution

until data arrives on any inbox.

The un-pausing action is actually performed by code within the component

itself, though this is in effect, as you suggested it might be,
instigated by

the postman microprocess.

A simple example would be an improved \'consoleEcho\' component:

class consoleEchoer(Axon.Component.component):

\....

def main(self):

while 1:

yield 1

while self.dataReady(\"inbox\"):

print self.recv(\"inbox\")

self.pause()

That said, if you look at the code, you\'ll see that probably the

majority of components do not make good use of this yet!

There are quite probably better mechanisms around - hence the

distinction, in the code, between microprocesses and components.

We\'d be very interested if yourself or other people want to play with

alternative communication & blocking mechanisms.

I\'d hope that even if the components and postboxes model doesn\'t

work out in the long run, the underlying generator based

microprocesses code could still be of some value to others!

\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\> At what stage of completion is it?

This is something we deliberately try to reflect in the version number.

Yes, you can build network servers and new protocols relatively simply

at the moment. Yes, you can integrate with pygame in a limited useful

fashion at present. Yes we have audio playback.

However we don\'t have yet\... (some examples)

\* Decent GUI integration yet.

\* /Full/ pygame integration.

\* Nice integration with pymedia

\* Direct support for Dirac.

Which aside from other things means you can\'t build (say) a video

& SMIL playback system trivially, yet.

As a result that\'s why the version number is 0.2 - whilst you /can/ do
a

lot, there\'s a lot more to do. Clearly that also naturally implies that

we don\'t expect any end user to be looking at the site. (The low

version number will normally scare them away)

\>\>The project aims to make it simple to build networked multimedia

\>\>systems (eg audio, video, interactive systems),

\>

\> There\'s plenty of software that facilitates networking, for example

\> Python already has software for tcp and http clients/servers, and

\> for xmlrpc remote procedure calls.

There is indeed.

\> So what does Kamaelia do that\'s extra? I imagine it\'s to to with

\> streaming large amounts of data. For example, a streaming video or

\> audio player. Or VoIP, perhaps.

It\'s designed to make bolting things together to make these sorts of

system simpler and easier. At the same time it\'s designed to encourage

writing code in a way that makes it simpler. The natural side effect of

this is the system might make it easier to take advantage of multiple

CPU systems as they come online, since it makes a system naturally

concurrent. As the original announcement said \"Kamaelia is designed as

a testbed\". And by testbed I mean testbed as it testing out new ideas,

see if they work and see if they pan out. (Not as in a testing suite)

Probably the best way of describing the difference is this\... After my

talk about Kamaelia at Europython, I had an long chat with Tommi

Virtinan about integration between Kamaelia and Twisted. I haven\'t had

a chance to follow up with him yet regarding how this would work, though

I have set a line in the sand aiming to have easy integration between

Kamaelia and Twisted before Kamaelia hits version 1.0.0. The impression

I got from Tommi was that he was most interested in the communications

aspect - the fact we can bolt together systems in a manner directly

akin to Unix pipelines, though I suspect he found the graphines aspect

more interesting.

Or as someone asking a similar question at Open Tech exclaimed after

I finally managed to explain it better to them \"Ooooh - you\'re trying

to make concurrency EASY!\".

\> OK, so what do the components in the pipelines do? What sort of data

\> do they hold? Unix pipelines act on ascii files; I assume you are

\> do this on audio and visual data. What langauage will the ele,ments

\> in thne pipelines be written it? I assume some will be in C/C++ for

\> speed.

Components are object instances of python classes. The data passed

between components are object instances. Clearly these python classes

can be written in python, C, C++, pyrex etc. Currently all of
Kamaelia\'s

components are python based. Some existing components make calls

into some related C libraries via python bindings.. An example of

writing a component using Pyrex can be found here:

\* http://kamaelia.sourceforge.net/PyrexComponents.html

\>\>It is designed as a practical toolkit, such that you can build
systems

\>\>such as:

\> When you say \"you\" who do you mean?

Generally I expect the readership of c.l.p/python-l\...\@python.org to
be

programmers. Python is generally easy to pick up and having asked

someone who\'s not done much programming beforehand (beyond

a small amount of VB and Access), and is pre-university to use the

system to build a simple streaming system prototyping visualising PVR

content on a mobile (and watching them succeed), they seem

relatively reasonable examples.

At some point, the ability to allow non-programmers to bolt together

Kamaelia systems would be desirable, but a first step is making it

simpler for programmers to bolt together systems. We currently have an

interactive visualisation tool(\*), and the logical extension of that is

a tool that allows systems to be bolted together without knowing any

code.

(\*) http://kamaelia.sourceforge.net/AxonVisualiser.html

It\'d be an interesting side project for someone to take forward, and

might be low hanging fruit in terms of projects. (Especially if viewed

initially as a tool for assisting development, rather than replacing

development)

\> Is the audience programmers or

\> less technical people? A project that allows non-technical people

\> to build complex network applications is an ambitious one, but not

\> impossible (I\'d find it very impressive and very exciting,

\> particularly if it runs on devices such as mobile phones).

It\'s a little ambitious at this stage, yes.

\>\> \* Ogg Vorbis streaming server/client systems (via vorbissimple)

\>\> \* Simple network aware games (via pygame)

\>\> \* Quickly build TCP based network servers and clients

\>

\> What sort of servers and clients?

Whatever you feel like. If you want a server to split and serve audio,

you could do that. if you want a server to spit out fortune cookies,

you can do that. (Useful only really as an alternative to a chargen

test protocol IMO)

\>\> \* Quickly build Multicast based network servers and clients

\> Serving what? Could I use it, for example, to build an n-player

\> encrypted VoIP server to allow people to do conference calls over

\> the Internet?

You could do that probably. (Though we don\'t have a component

for audio capture (though a read file adaptor reading from /dev/audio

might work depending on your platform I suppose) and audio

encoding at the moment, so those would probably be the core

components to integrate. If you want to use multicast over the wide

area internet you\'d also have to convince all the people using the

system to use ISPs that support multicast\...\...)

\> (I mean proper encryption here, the sort GCHQ or the NSA can\'t
break)

I\'d be impressed if that could be written, using anything really.
(Can\'t

implies never)

\>\>The basic underlying metaphor of a component us like an office
worker

\>\>with inboxes and outboxes, with deliveries occuring between desks,

\> That metaphor brings up an image (at least to me) that the sorts of

\> data that can be communicated are things like documents,

\> spreadsheets, business graphs, memos.

They could indeed. The underlying framework doesn\'t differentiate

between data nor have any realtime aspect embedded in the system

at present. Just because we\'re focussing on systems that have a
realtime

element and are multimedia based, this does not mean the system is

limited to that.

\> May I suggest a different metaphor? \[hifi\]

I\'ll think about it. It\'s closer to the model that pysonic seems

to take, and it implies a functional transform - ie /just/ dataflow

\- rather than connected processing units that /might/ take time

to do processing.

\> OK, I get the straming part of it. But what asbout non-streaming

\> stuff? What other protocols are necessary?

One example is peer to peer mesh setup. People normally

think of P2P as a distribution mechanism. However, the underlying

approach also very good at setting up communications meshes.

This could be of use in many areas, such as GRID based systems

for distributed rendering, application layer multicast, and network

multicast island joining.

Due to the illegal /uses/ of P2P, much work in this area is difficult to

reuse due to defensive coding. Decoupling development of protocols

from use of those protocols is generally a wide idea IMO.

\>\>Is that clearer ?

\>\>

\>\>A short summary of all that could be:

\[ new descscription followed by useful comments, we\'ll take

them on board, I think I\'ve answered most points inline \]

\> \"innovative\". This actually has two meanings. One is \"is new /

\> allows new things to be built\".

Bingo. It could be argued the other is misuse as buzzword.

\> That\'s certainly less lines of code than it would take in Tkinter.

\> And easier to follow.

We\'re looking at tkinter as well. (Some tests at tkinter integration

are in CVS)

\>\>And you have a simple presentation tool !

\> Now I\'m confused. Is Kamaelia a GUI builder?

Multimedia systems have many aspects. They include taking in

audio/video and spitting out audio/video/pictures/text/\... Take

a look a SMIL if you\'re curious - it\'s a system that Kamaelia would be

incomplete if it made decoding/display/interpretation of SMIL

difficult.

We also have to be able to demonstrate system to other people

inside the BBC in a way non-technical people understand. That means

showing structures in a friendly dynamic way, showing pictures,

playing sounds (hence visualisation - looking inside running systems).

That means we need ways of integrating with systems like pygame &

other toolkits. If however I\'m talking outside the BBC I\'ll try to
give

examples which people might find interesting - such as building a

presentation tool. The blocks are very much like Lego & K\'Nex and

adding in a new block enables all sorts of new applications.

For example, we could take the text ticker, combine that with a text

feed and have a personal autocue/teleprompter. Alternatively someone

could use it to have subtitles (say) at the opera displayed on a Nokia

770 (maemo) based device.

\> Ah, so now I\'m guessing it allows me to write networked PyGame

\> applications, where with just a few lines of code I can have

\> networked streaming video on my pyGame screen\... am I right?

As yet, no. When we hit version 1.0, yes. Why? Because we haven\'t

built components for video decode & display (and that\'s the only

reason). That\'s why I don\'t mention video normally - I prefer to focus

on where we are when announcing things, rather than where we\'re

going (leaving that to more appropriate forums).
