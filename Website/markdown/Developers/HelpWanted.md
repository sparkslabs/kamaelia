---
pagename: Developers/HelpWanted
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
\

Help Needed/Wanted
==================

**Stuff that would be useful**\

-   Update the [Getting Started](../../../GettingStarted) page
-   [Optimisation bug with WaitComplete implementation\
    ](http://sourceforge.net/mailarchive/forum.php?thread_id=30966325&forum_id=43377)
-   [Axon Change Proposal Summary: Inheritance of Inboxes/Outboxes
    making default in/out-boxes
    mandatory](http://sourceforge.net/mailarchive/forum.php?thread_id=30706615&forum_id=43377)
    (unresolved)
-   [Proposal: Change default component
    behaviour](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1155124531)
-   [Destroying inboxes and
    outboxes](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1143036671)
-   [Race Hazard in Visual Ordering of
    Widgets](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1141992386)
-   [Kamaelia.Util.Splitter.PlugSplitter needs
    simplifying](http://koala.ilog.fr/twikiirc/bin/irclogger_log/kamaelia?date=2006-09-15,Fri&sel=600#l596)
-   Decide what to do with Kamaelia.Experimental.Services
-   Upgrade existing components to handle \'noSpaceInBox\' exceptions
    (pending merge of private\_MH\_axon\_outboxwakeups)
-   [Fix Graphline and other components to not modify klass.Inboxes and
    klass.Outboxes](http://sourceforge.net/mailarchive/message.php?msg_id=37273092)\

next part included from [Developers/Tasks](/Developers/Tasks)\

Project Tasks 
=============

Specific things that would be useful. If you want to work on these,
please start a /Developers/Projects/ProjectTaskPage with a basic outline
of what, why, how, when, who, where, etc. The key things out of those
really are the who, what, where.\

### TCP Server improvements 

Shutdown:\

~~\* Calling stop on the scheduler causes it to call stop on all the
scheduled microprocesses~~

-   DONE - now sitting on Michael\'s branch. Needs merge.\

~~\* The stop on TCP Server & CSA causes respective sockets to be
shutdown cleanly~~

-   INITIAL PASS DONE - Needs testing. Likely to need to catch situation
    where sockets are closed multiple times. (Since the internet
    subsystem is going to prefer to attempt to close too many times
    rather than not enough times!!)
-   Need to write test examples showing usage.
-   Needs to also catch keyboardInterrupt and allow that to be a general
    case which can kill the system via a .stop()\

\
Throttling\

~~\* CSA needs to respect the fact that when it forwards data it make
get a NoSpaceInbox~~

-   DONE - now sitting on Michael\'s branch. Needs merge.

Interesting thought:

-   A later version of the CSA & TCPServer could have an option to make
    it such that when a client (or protocol) tries to \_send\_ data to a
    socket that it fails if there\'s no capacity As a configurable
    option. (Most protocol handlers won\'t be expecting it) That should
    be doable by setting the max inbox size to zero

### Platform compatibility (Windows, Mac):

Windows\

-   Check windows, find out what works, what doesn\'t
-   Windows specific megabundle
-   Package up whiteboard for windows users
-   Something similar to the selector for files for windows, preferably
    transparent so the developer doesn\'t have to choose different
    components for different platforms
-   Get speex working for windows users

Mac\

-   Package up whiteboard for mac users
-   Audio capture component for macs
-   Get speex working for macs
-   Resolve (likely) arising endian issues.

General\

-   Test on Python 2.5

### Axon core:

Improve box destruction to handle when a box is still linked to another

-   linkages are not properly broken at the moment

Fix WaitComplete microprocess closures so the substitute microprocess
self.pause() actually pauses\

Make CAT fully threadsafe\

### Tidying-up and Quick wins: 

-   Tidy and simplify the Plug & PlugSplitter components
-   Have SimpleServer tell the source IP, source port, dest IP, dest
    port

### Topology visualiser & Introspection:

Change topology visualiser to support \"on demand\" screen update rather
than continuous

Support \"no render\" layout update (has to an extent already).

Change topology visualiser to support hierarchical display/etc

Rewrite topology viewer to abstract from rendering mechanism (so
rendering components could be plugged in for opengl, pygame etc)

Rewrite topology physics in pyrex for serious speed boost :-) (thereby
making it practical for visualising \'real\' systems, eg. whiteboard,
which contains 61 components when running stand alone)

-   Ryan expressed doubt that the slowness was all due to python and
    offered to investigate how it could be rewritten to be faster. Matt
    gratefully accepted

\

### Whiteboard ideas: 

-   Try whiteboard in 3D
-   Try an automated \"scatter onto a concave hemisphere with me the me
    middle layout for auto layout of pictures. Allow links to be drawn
    between said pictures positioned in 3D, potentially integrate with
    topology visualiser subsystem (simply different rule set?).
-   Ability to edit the different pages of the same \"shared pad\" in
    whiteboard session, rather than forced to be on the same page
-   A whiteboard in 3d with multiple sheets etc.
-   \

### Protocols, codecs, integration: 

User authentication modules

Clean integration with twisted for reuse of twisted.protocols

DNS client (would be useful in several places)

Gstreamer integration

A better way to do his (Ryan\'s) HTML parser in Kamaelia:

-   \"I ended up doing my HTML parser as a state machine and a stack -
    if I did it as a standard unix program (like a filter) it would have
    been much simpler using function calls and blocking.\"

```{=html}
<!-- -->
```
-   Michael commented that he had some ideas on this issue

### AIM Support

-   Remove from x import \* statements from Protocol/AIM/ChatManager.
-   Provide a set of pre-defined SNAC constants (or possibly even
    classes) such that it is possible to write
    self.sendSnac(MESSAGE\_TO\_USER, data) instead of self.sendSnac(04,
    07, data).
-   Remove the block of code at the end of AIMHarness\'s main method
    that keeps it running.  After that code is run, AIMHarness serves
    only to pass messages between ChatManager and OSCARClient.  It could
    probably be refactored such that those two components link directly
    to each other rather than keeping the AIMHarness around.
-   The LoginHandler code can be a tad confusing with several different
    levels of WaitCompletes.  It could probably be refactored to
    simplify things.\

### Graphics framework support (pygame, OpenGL, etc): 

Integrate PGU (Phil\'s pyGame Utils)

Use integrated PGU for buttons drop down lists, etc

-   in Whiteboard

```{=html}
<!-- -->
```
-   Inside Compose, (simplifying use on Macs)

Simple window manager support components -

-   Add policies to display locations and management for xxDisplays
    (providing layering, z positioning, reposition for pygame & opengl
    surfaces, opengl code has this to an extent),

Styleable HTML layout engine for the window manager

Flesh out pygame related tools (perhaps independently of PGU)

Resolve MH.PygameApp issues,

Create joined spaces (2D and 3D) using Pygame & OpenGL code

Adding visual ordering of components to pygame: eg. a component
specifies a \"layer number\" to appear on

Adding better event routing for pygame & opengl - eg. only top-most
component receives a click event

### Random project ideas 

Write 3D game using Kamaelia

Automate release process.

A major python web framework, (eg turbogears or django) with a kamaelia
based web server and sample bi-directional \"ajax\" chat application

-   Michael mentioned that Simon Willison of Django queried the
    possibility of integrating Kamaelia at Euro OSCON

RTP client and server implementation - potential internal bbc
requirement

-   Matt has developed nascent RTP packeting/depacketing components\

### DVB, PVRs timeshifting, etc: 

-   Write a graphical EPG for DVB
-   Build a more complete PVR application
-   An interactive introspector/visualiser that only displays
    \'neighbourhood\' of a component (eg. those connected to a
    particular component) \... allowing you to explore by moving through
    a system
-   Implementation of ssh protocol

### Relevant to HTTP, SMTP systems:

-   Half-close support in TCP client and server components (e.g. by
    sending messages via the signal outbox, or accepting a half-close
    command via the control inbox)
-   Better flow control (i.e. pausing components when what they\'ve
    already processed is setting in a big backlog of the next component,
    or that the component way down the chain has limited bandwidth)
-   DNS client component

\
\
\
