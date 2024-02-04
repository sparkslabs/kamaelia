---
pagename: Developers/Projects/KamaeliaJam
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia Jam
------------

### What is it?

Kamaelia Jam is a music sequencer designed to be used simultaneously by
more than one user over a network. It will also act as a toolkit for
quickly prototyping networked music applications.

### Where do I get and install it?

\
Barely tested pre-alpha packages (marking the end of GSoC \'08) can be
downloaded below:\
\
[Linux](http://www.box.net/shared/mle3bl31on) - See INSALL instructions
in the Docs folder\
\
[Windows](http://www.box.net/shared/mpov64vgx0) - Run through the
installer\
\

The latest version of jam is available from a branch in svn.
Instructions for installing the dependencies are available
[here](http://kamaelia.svn.sourceforge.net/viewvc/kamaelia/trunk/Sketches/JT/INSTALL?revision=3916&view=markup).\

**SVN\
**

-   `svn checkout http://kamaelia.googlecode.com/svn/`branches/private\_JT\_JamDev
    jam\

-   cd jam/Apps/Kamaelia-Jam/DistBuild

-   ./Jam.build.sh\

-   cd ../

-   python setup.py install (as root)\

### Documentation for developers

[High-level diagram of the major pipe and graphlines within
Jam](KamaeliaJam/GraphlineDiagram)\
\

### Planned Schedule

`< 6 Jun - Rearrange directory structure, start to look at packaging, sit`\
`exams`\
`Functionality:`\
`Become the proud owner of a degree :)`\
\
`6 ``Jun`` -Improve and test timing code.  Begin to work out details of`\
`extenally controlling components.  Get Matt's modified CSA working with`\
`UDP.`\
`Functionality:`\
`* Basically this week will be mainly setting the groundwork.  The timing`\
`code will let me write components which talk nicely and accurately`\
`(<1ms) in music timing (beats, bars, bpm etc).`\
`* Externally controlling components = getting data from an inbox (the`\
`network eventually) to control UI elements.  I think this will take a`\
`couple of goes to get right, so start to look at it here.`\
`* Modified CSA with UDP.  This will let me receive data over a UDP port`\
`without using 100% CPU.`\
\
`16`` ``Jun`` - Write basic networking code, allowing two users to communicate.`\
`Test out network communication, and make strange twiddly noises with`\
`someone :)`\
`Functionality:`\
`* At the end of the week there should be two people at different`\
`computers controlling XY pads on each others computers.  As you say this`\
`is probably a bit pessimistic timing-wise, but I'm not very hot on`\
`networking, so have given a bit of leeway here for me to get up to`\
`speed.`

\
============================================================

\
`9 ``Jun`` - Various bits of documentation.  Package everything up and test it out.`\
`Functionality:`\
`* Packaging everything - in the week before I should have got to the`\
`point where I have a (albeit unexciting) working networked music app.`\
`Seems like a good point to test out packaging - so I should have a`\
`working distribution of it for the big three, which can be easily`\
`tested.`\
\
`16 ``Jun`` - Get multiple client networking code working - sort out how having`\
`lots of users will work practically.`\
`Functionality:`\
`* Again, maybe a bit pessimistic.  By the end of the week have a system`\
`where multiple users can join in a session and control XY pads.  Again I`\
`think this may take a couple of goes to get right practically.`\
\
`23 Jun - Write the step sequencer`\
`Functionality:`\
`* Working step sequencer which can be used by as many users as you like.`\
\
30 Jun` - Write the piano roll (add/delete functionality)`\
`Functionality:`\
`* Working piano roll, where users can add and delete notes.`\
\
`7 Jul`` - Extend the piano roll (move/resize functionality)`\
`Functionality:`\
`* Users will be able to move and resize notes at will - basically a`\
`complete network enabled step sequencer`

14 Jul - Add in various filters to make Jam work with midi out, and make
sure midi component is up to scratch and working.

Functionality:\
\* A version of Jam which can switch between MIDI and OSC output for
local control\

\
21
`Jul`` - Write "glue" code and fix up details (peer select widget, any`\
`extra UI niceness, port/socket configuration etc.)`\
`Functionality:`\
`* Deliver the above - program should be basically "complete" and ready`\
`for packaging here.`\
\
28
`Jul - Finish off detail, have a look at "extra" components (hopefully)`\
`Functionality:`\
`* Detail = package it up, make sure everything is well tested, prepare`\
`things which need to be merged but haven't, any other stuff which needs`\
`doing and I've overlooked :)`

4 Aug - End - Any overrun fits here. Also work on extra components
(Arduino, Multitouch etc)\

===============================================================\
`11`` Aug`` - Code cleanup, write documentation and test cases`\
`Functionality:`\
`* I'll do this as I go along - put this in because Google recommend it`\
`as your "pens down" date.  I guess this week can work as a bit of a`\
`buffer for overrun, or to sort out any of my extras stuff a bit more.`

\
