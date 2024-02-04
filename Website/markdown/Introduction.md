---
pagename: Introduction
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[OK, What *is* Kamaelia?]{style="font-size: 23pt; font-weight: 600;"}

[An Introduction]{style="font-size: 15pt;"}

::: {.boxright}
[A key aim of Kamaelia is to enable even novice programmers to create
scalable and safe concurrent systems, quickly and
easily]{style="font-style: italic; font-weight: 600;"}
:::

Lego/K\'nex for programmers. For people. For building things. It\'s
about making concurrency on systems easier to use, so easy you forget
that you\'re using it. It\'s been done once before, spectacularly well,
so well many people forget it\'s there, a key example - unix pipelines.
However it\'s been done in hardware since day 1, since that\'s how
hardware works.

One day, I sat back and realised that network systems looked almost
identical in nature to the asynchronous hardware systems, conceptually,
with one major exception. In hardware, you don\'t know who your buffers
are connected to via wires. You have a protocol for getting that
information over (be it a clock, or handshake circuits) but no other
knowledge.

Kamaelia was borne, technology wise, from the idea \"what if we
developed software like hardware\" - each component with no direct
knowledge of any other. Similar to programs in a unix pipeline. This is
proving to be a very useful approach.

Kamaelia is the result. Kamaelia is divided into 2 sections:

-   [Axon]{style="font-weight: 600;"} - this is a framework, developed
    by application spikes, for wrapping active objects. Specifically
    these are generators (mainly) and threads. The resulting library at
    it\'s core is pretty simple - a novice programmer can learn python
    one week and implement [their own version](/MiniAxon/) in about a
    week.\
-   [Kamaelia]{style="font-weight: 600;"} - this is the toy box - a
    library of components you can take and bolt together, and customise.
    This includes components for TCP/multicast clients and servers,
    backplanes, chassis, Dirac video encoding & decoding, Vorbis
    decoding, pygame & Tk based user interfaces and Tk, visualisation
    tools, presentation tools, games tools\...

The reason for concurrency here isn\'t because we\'re after performance,
but due to the problems we\'re facing are
[naturally]{style="font-style: italic;"} concurrent - millions of people
watching content. Therefore, the aim is to make dealing with this
concurrency simple/easy, or natural/fun. Hence the lego/K\'nex analogy.

[What\'s the underlying metaphor we
use?]{style="font-size: 15pt; font-weight: 600;"}

In hardware you have pins which the hardware \"talks\" to. In unix
shells, you have stdin and stdout. For Kamaelia we decided to use
something a little more concrete.

Take a person sitting at a desk in a world pre-desktop-computing. She
could have a bunch of inboxes & outboxes on her desk. Suppose that the
inboxes are labelled \"timesheets\", \"newhires\", \"fires\", and that
the outtrays are \"accounts\", \"security\", \"HR\".

She can work on messages she gets on inboxes, and generate messages on
outboxes. A postman then performs deliveries between the people - the
active objects. The postman knows where things are going, and therefore
if you need to add ing (say) auditing you can do that without modifying
the way the person/active object works.

This is precisely how Kamaelia works. It models itself on a real world
system to encourage behaviours that simplify concurrency.

[Example]{style="font-size: 15pt; font-weight: 600;"}

Suppose I want to create a simple presentation tool - where I type some
text, it goes to a server. People connect to that server and can
\"listen\" to what I\'m typing in a nice display, the three main
sections of that system could look like this:

You write new components in the same way as writing a small script.
Start off reading/writing from stdin/stdout, until you\'re happy with
it. You then replace inputs/outputs with inboxes/outboxes. That
component can then be used with any other as long as they accept that
form of python object. For example, consider exchanging ConsoleReader()
& Ticker() with AlsaReader() and AlsaPlayer() to create a simple radio
style system.

That\'s the idea in a nutshell. (did I mention all the components above
run in parallel?)

[Things people have done with
it]{style="font-size: 15pt; font-weight: 600;"}

At R&D we\'ve used it for sending subtitles to mobiles, building a
networked audio mixer matrix, previewing PVR content on mobiles, joining
multicast islands together using application layer tunneling and also a
game for small children :-)

I also use Kamaelia for all my presentations these days.

Kamaelia has been used by BBC Radio & Music to produce a record of
transmission (for 8 BBC channels 24x7). This is a development box for
internally monitoring what is actually broadcast vs what the EPG data
says. This enables prototyping of new services (subject to all sorts of
restrictions). Examples include podcasts of all of BBC radio, particular
tastes or genres. That then allows people to decide if they want these
things and decide how to move forward with the industry.

Kamaelia\'s role was to be used to build a proof of concept prototype.
It did prove the concept, so they worked on a traditional style,
production quality replacement. We\'re now working with them to work
towards a second generation architecture.

[Getting Started]{style="font-size: 15pt; font-weight: 600;"}

[We\'ve got a page on this](/GettingStarted.html, but the short instructions
are:

-   Grab a Kamaelia Bundle ([with lib(ogg,
    vorbis,ao)](http://prdownloads.sourceforge.net/kamaelia/KamaeliaMegaBundle-1.0.1.tar.gz?download),
    [without](http://prdownloads.sourceforge.net/kamaelia/KamaeliaBundle-1.0.1.tar.gz?download))
-   Install the files (all installed in the standard ways)
-   Start working through the examples in the [cookbook](/Cookbook.html
-   Look through [the components](/Components.html for more information
-   [Find out how axon works](/MiniAxon/) in detail!

[Summary ]{style="font-size: 15pt; font-weight: 600;"}

And that is Kamaelia. A framework for components, a library of
components, and a way of making systems quickly and easily.

So, the reason I\'m talking about it at Euro OSCON, is because we\'re
Kamaelia itself to be useful & fun, and also it\'s seems to make
concurrency easy to work with. Hopefully this should come over in my
talk!

More information:

-   Project Website: <http://kamaelia.sourceforge.net/>
-   Axon Tutorial: <http://kamaelia.sourceforge.net/MiniAxon/>
-   Motivations (non-technical):
    <http://kamaelia.sourceforge.net/Challenges/>
-   White paper (technical) :
    <http://www.bbc.co.uk/rd/pubs/whp/whp113.shtml>
-   Euro OSCON, Python Track, Wednesday 19th October 2005
