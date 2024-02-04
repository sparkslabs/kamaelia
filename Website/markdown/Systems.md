---
pagename: Systems
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Systems]{style="font-size:21pt;font-weight:600"}

[Applications using Kamaelia]{style="font-size:16pt"}

This section describes some systems that have been created using
Kamaelia. Some of these are available for download, or as part of the
main Kamaelia distribution. If you\'d like to add a description of a
system you\'ve built (large or small), [please let us
know](/Contact.html)!

[Providing Tools to Provide the BBC the OPTION to put the Archive
online]{style="font-size:12pt;font-weight:600"}

This is a complex area in itself, so we discuss this in the
[Challenges](/Challenges/) section of the Kamaelia website. This is the
core motivation for Kamaelia from BBC R&D\'s perspective. Kamaelia is
however a general toolset, and can be used to prototype new mechanisms
for delivery of content to new platforms in new ways. These prototypes
can then evolve into useful tools and systems. As they do, they will be
described on here. The main tool developed so far, as part of the above
aim, is Kamaelia itself.

([NB]{style="font-weight:600"} when we say \"the archive online\", we
mean as much as is reasonable, practical, and as much as the license fee
payer, BBC, & industry deem appropriate within the context that much of
the archive has many rights issues. Kamaelia aims to knock down the
technical challenges)

[\"As Broadcast\" Radio Monitoring System - BBC Radio &
Music]{style="font-size:12pt;font-weight:600"}

[Availability:]{style="font-weight:600"} Internal to BBC Radio & Music
only

Similar in concept to a \"PVR for radio\". Kamaelia has been used by BBC
Radio & Music to produce a record of transmission (for 8 BBC channels
24x7). This is a development box for internally monitoring what is
actually broadcast vs what the EPG data says. This enables prototyping
of new services (subject to all sorts of restrictions). Examples include
podcasts of all of BBC radio, particular tastes or genres. That then
allows people to decide if they want these things and decide how to move
forward with the industry.

Kamaelia\'s role was to be used to build a proof of concept prototype.
It did prove the concept, so they worked on a traditional style,
production quality replacement. We\'re now working with them to work
towards a second generation architecture.

[\"Kamaelia Present\" - Presentation
Tool]{style="font-size:12pt;font-weight:600"}

[Availability:]{style="font-weight:600"} Tools directory of Kamaelia
distribution

This presentation tool has been used now for all presentations on
Kamaelia since Europython 2005. If you\'ve seen some cool stuff using
it, then this is the tool used. If you thought it sucked, it\'s
constantly evolving to include new features and stability :-) .

It features the following:

-   The ability to take 2 sets of slides, and overlay them on top of
    each other. Both can be advanced independently, and use alpha
    blending to fade out either set of slides as a toggle
-   Can take a set of \"graph slides\" for presenting more complex
    information easily - such as the structure of component systesm,
    choices through a system, or could potentially be used to show the
    structure of chemicals. Essentially anything that has blobs & lines
    joining them can use it. The layout of the blobs and lines uses the
    Topology Viewer Component , which uses a simple physics model to
    layout the components, which results in a dynamic pleasing layout,
    which can be moved around during a presentation.\
    \
    Like the slides, the graph slides can be advanced independently of
    the other slides. People who\'ve seen me using this will know this
    is useful for making several points regarding a particular idea
    hinted on a background. Like the normal slides, the graph slides can
    also be faded out using alpha blending.
-   Ability to incorporate a ticker into the presentation tool as well.
    This is nice for saying \"and we\'re also looking at these things\",
    without having to go through. The ticker is limited to the same sort
    of maximum rate for TV subtitles, so most people should be able to
    keep up, meaning that you don\'t really need to talk through the
    options (Indeed doing so would be laborious for an audience)

Limitations:

-   Slides are collections of images. You currently need to create the
    slides in another tool and export as PNGs or GIFs
-   The graphslides, whilst stored in an XML file, do not allow you to
    go \*backwards\* through a presentation. This may well change
    shortly, but is worth knowing about.
-   Currently the ticker is a one shot affair - you can show one ticker,
    once, and what it shows is hardcoded.

However this is sufficiently useful, interesting to build on a move
forward.

[\"Kamaelia Paint\" - Image
Creation]{style="font-size:12pt;font-weight:600"}

[Availability:]{style="font-weight:600"} Kamaelia CVS, in Sketches

Many moons ago there were [paint]{style="font-style:italic"} programs on
systems like the Amiga. Things like Deluxe Paint, Photon Paint, and so
on. They differ from tools like \"the gimp\" and \"photoshop\", in that
they\'re not primarily aimed (or originally) at modifying an existing
images ([Photo]{style="font-style:italic;font-weight:600"}shop, Gnu
[image manipulation
]{style="font-style:italic;font-weight:600"}program), but rather with
providing tools an an interface aimed at creating images, using pixels,
from scratch. Deluxe paint also had very nice tools for [painting
animations]{style="font-style:italic"}.

As a result Kamaelia Paint serves the following purposes:

-   To show how to create a paint program using Kamaelia
-   To aim towards making available once again this sort of incredibly
    useful tool.
-   To have fun - this isn\'t a sponsored project by anyone, this is
    purely done in the personal time of [Michael](Michael.html).

Currently (29/10/2005) this tool is incredibly primitive, but in
conjunction with a (low cost :) graphics tablet is quite nice. An
interesting difference from a traditional paint program is that it
allows a command console as well (due to being written using Kamaelia).

[Networked Audio Mixer Matrix]{style="font-size:12pt;font-weight:600"}

[Availability:]{style="font-weight:600"} Kamaelia CVS, in Sketches

Detail TBH

[Collaborative Whiteboarding]{style="font-size:12pt;font-weight:600"}

[Availability:]{style="font-weight:600"} KamaeliaCVS, in
Sketches/MH/Sketcher

An experimental sketch drawing program, where multiple users can connect
together and all see and draw on the same sketch. You can also load and
save the whiteboard. The fun bit is that instances can act as both
client and server, meaning users can connect together in an ad-hoc peer
to peer fashion. It is implemented using our pygame and networking
components, and a few new ones.

Run [sketcher.py]{style="font-family:courier new"} with neither, either,
or both of these command line arguments:

-   [\--serveport=\<port\>]{style="font-family:courier new"}\
    Tell sketcher to allow other instances to connect on the specified
    port.

```{=html}
<!-- -->
```
-   [\--connectto=\<host\>:\<port\>]{style="font-family:courier new"}\
    Tell sketcher to connect to another instance listening on the
    specified port.

Draw using the mouse (or stylus if you\'ve got a tablet). At the top is
a drawing colour palette and eraser tool. Click on them to select them.
Click with the right mouse button to toggle in and out of a fullscreen
mode.

Whilst it is running, you also get a command prompt. This injects
commands directly to the drawing Canvas component. Primarily it is there
for you to load and save sketches (in bmp format, ensure you include the
extension) and to clear the whiteboard:

[\>\>\> load \"filename.bmp\"\
\>\>\> save \"filename.bmp\"\
\>\>\> clear]{style="font-family:courier new"}

The design centres on a Backplane component that acts as a bus. This
connects together:

-   The local \'sketcher\' (Canvas and paint tools)
-   Any clients that have connected (if you allowed serving)
-   A connection to a server

Whenever something sends to the backplane, everything else receives. So,
if two or more backplanes are coupled (by, for example, network
connections) then they effectively behave like a single distributed
backplane.

This has started out as a pet, personal time project by
[Matt](Matt.html).

[General Stuff]{style="font-size:12pt;font-weight:600"}

[Availability:]{style="font-weight:600"} Many of these are in
Kamaelia\'s CVS, in Sketches

At R&D we\'ve used it for sending subtitles to mobiles, building a
networked audio mixer matrix, previewing PVR content on mobiles, joining
multicast islands together using application layer tunneling and also a
game for small children :-)
