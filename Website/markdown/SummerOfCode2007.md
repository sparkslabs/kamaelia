---
pagename: SummerOfCode2007
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Google Summer Of Code 2007
==========================

::: {.boxright}
**Project ideas are later down the page but include:**\

-   A file handle like interface to backgrounded Kamaelia components
-   Extend & make more user friendly the Kamaelia Web Server
-   A Testing Framework for Kamaelia Systems
-   High Level Kamaelia 3D Modelling Components
-   Visual Editor for Creation & Composition of Shard Components
-   Kamaelia Exemplar! What can you make that\'s cool?\
-   **Your Idea** (please see [the component list](/Components.html) for
    inspiration of appropriate areas)
:::

Kamaelia has been accepted into Google\'s Summer of Code 2007, so we\'re
very pleased to hear what projects you would like to do. The project
list is at the bottom of the page, however please also read these
guidelines first.\

### What is Kamaelia?

Well, let\'s answer this 4 ways.\

-   We have an [introduction](/Introduction.html)
-   There was [an article in Linux
    Format](/t/TN-LinuxFormat-Kamaelia.pdf) that covered the
    Whiteboarding application
-   There was [an article in Linux Magazin](/t/TN-LightTechnicalIntroToKamaelia.pdf) (germany)
    which discussed the key concepts in Kamaelia and a tour of key
    component types. This is probably most relevant to GSOC\

Finally, a short intro:\
\

> Kamaelia\'s aim is to make highly concurrent systems natural to create
> and simple to maintain. (given a choice  of forces the we choose the
> latter) We seem to be having some success in this and have a number of
> systems we\'ve built using Kamaelia.\
> \
> Kamaelia is primarily focussed around building networked, multimedia
> systems, tools and applications, however Kamaelia is a generic
> component framework & toolset. The current implementation is in
> python, but the approach and concepts are portable with a proof of
> concept in python.\

### What Sort of Person We Looking For?

We\'re looking for enthusiastic people to work on specific projects,
which are listed on our projects pages (to appear shortly) You don\'t
necessarily need lots of experience, indeed we\'ve found a naivete can
actually help since you have less preconceptions about how code should
be written (And often more open to the component approach).\
What we do expect from you though is a very clear interest in the
project your doing as part of Kamaelia, and it *must* fit in with
Kamaelia, or some other open source BBC Research project where there is
a suitable mentor.\

### We Want Code We Can Use

In practical terms this means that we want to be able to put your code
into the distribution for people to be able to use. This means printing
out and signing a contributor agreement. Our contributor agreement is
based on Python\'s, since our project is largely python based. What does
this mean?\

-   We ask you to grant the BBC a BSD license on your code
-   This then allows the BBC to remain the sole originator of the
    MPL/GPL/LGPL main release. (This is useful in case the license is
    breached - having on licensor simplifies things greatly)\

If you\'re curious as to the specific wording, you can see a [sample
contributor agreement](/Developers/SampleContributorAgreement.html).\

### What we will expect of you

We will expect you to have done the MiniAxon tutorial ***ideally before
submitting your application***. This teaches you how Kamaelia
essentially works under the hood (barring optimisations), and as a
result we feel is vitally important.

We will expect you to, where practical, discuss your application with us
on IRC or email ***sooner rather than later.***\

We will expect you to attend our normal weekly IRC meeting, unless
timezones simply don\'t work

We will expect you to attend a weekly guaranteed mentor time session.
This is an hour long session but it\'s specifically there to allow you
to have some guaranteed time with your mentor, rather than anything
else.

We will expect you to have some plan for maintenance of your code after
summer of code is finished. This can come in several forms. One option
is to plan to be around after summer of code because you\'re doing a
project you think is personally fascinating/useful. Another option is to
aim to write your code with the intent of having it maintainable.

We will expect you to also track your work in two ways:

-   To keep a development blog (can use your usual one if you like),
    which you update at least twice a week
-   To start a project task page for your work, and keep that up to
    date - creating subtask pages as and where needed.

If you use code from other sources (eg the python cookbook, reference
implementations) we expect you to quote your sources.

To have fun :) (What\'s the point otherwise? :)\

### Feedback! 

This is a wiki page. It uses dojotoolkit so you can edit this page an
add your own ideas here, but please don\'t edit the text above!\

Ideas! 
------

*Fleshing out now:*\
\

### A file handle like interface to backgrounded Kamaelia components

::: {.boxright}
The key point of this project is to make it easier to embed the usage of
kamaelia facilities and systems in non-kamaelia based systems. It should
also naturally simplify kamaelia systems. You **must** be able to show
us that you have done the [MiniAxon](/MiniAxon/) tutorial to do this
project
:::

This would enable traditional, non-kamaelia-component oriented systems
to use the facilities of Kamaelia components in a manner similar to that
of a filehandle, crossed with a dictionary.\
\
A user would be able to do something like this:\

>     from kamaelia.background import background, likefile
>
>     background.start() # Start the scheduler in the background
>
>     page = []
>     P = likefile(HTTPClient("http://tinyurl.com/35fjbr"))
>     while P.get("signal", False) != "shutdown":
>        data = P.get("outbox")
>        page.append(data)
>
>     P.shutdown()
>     pagetext = "".join(page)

\
In terms of context, this is a wishlist item for syntactic sugar to
allow this sort of ability. The key thing is what\'s happening here.\

-   ***background.start()*** starts a scheduler in a background thread.
-   ***likefile*** takes a component, passes it to the scheduler and
    asks it to activate it - running it in the background, passing back
    an object as a handle.\
-   The user can then interact with the component in a functional
    manner, much like reading from a filehandle. However due to having
    inboxes&outboxes, you name which one you\'re acting on, like a
    dictionary.This would mean, for example, that you could start many
    many TCP connections\

for example, and have them all managed in a second background thread in
a scalable fashion. Similarly it might be a pygame display with many
many sprites, and so on.\
\
This takes inspiration from the fact that a traditional filehandle
actually abstracts away the fact that the operating system file handling
can be quite complex, and writing of data to finally disk (for example)
can happen after your programme has exitted. To you however, the
operation appears simple.\
\
The key benefit of this is that it will simplify embedding & using
kamaelia components in non-kamaelia based systems.\
\

------------------------------------------------------------------------

\
\

### Extend & make more user friendly the Kamaelia Web Server

::: {.boxright}
**Note:** The key aim of this project should be to support the full
range of HTTP methods in a fashion that is simple for a web developer to
extend and override.
:::

The key intent here behind this project is to take the [Kamaelia web
server](/Cookbook/HTTPServer.html), written as a by product of last year\'s
Google summer of Code, and make it more usable and useful. Specifically
this means extending support to all HTTP methods, making it simpler to
extend and override, and ideally supporting WSGI based applications, or
at minimum CGI applications.\
\
A relatively novice user should at the end of this project be able to
say something like:\
\

>     from Kamaelia.Systems.WebServer import WebServer
>
>     WebServer(docroot="/data/mydocs").run()

\
In order to start a basic webserver which serves static content.\
\
A more advanced user should be able to specify where CGI applications
exist:\

>     from Kamaelia.Systems.WebServer import WebServer
>
>     Extend & make more user friendly the Kamaelia Web Server
>     WebServer(docroot="/data/mydocs", cgiroot="/data/cgi").run()

\
An even more advanced user may wish to support WSGI based application.
No suggested syntax/API is given here since we would expect the student
to explore programmer friendly scenarios here. It\'s worth bearing in
mind that often web applications can care about HTTP method was used
(POST, GET, PUT, DELETE, etc) when making the request, so looking at how
to deal with this would be useful.\
\
CGI support should be relatively simple given the existence of the
UnixProcess component, though some adaptation to support standard CGI
environment variables is likely to be needed.\
\
A key benefit of this project is that this would enable Kamaelia to have
a native, single threaded, scalable, extensible webserver written in a
Kamaelia style. This not only simplifies maintenance but opens up
interesting opportunities in desktop applications since Kamaelia works
well in that environment too.\
\
There are some potentially very interesting applications possible as a
result of a client side, but scalable webserver that can integrate
easily with lots of other applications. If you\'re curious, chat to us
on IRC.\

------------------------------------------------------------------------

\

### A Testing Framework for Kamaelia Systems

\
This project would aim to produce something similar to unittest/jtest,
but in a context and manner which makes sense for individual Kamaelia
components and also for Kamaelia systems.\
\
Clearly this is a two part project, and two different main use cases:\

-   It should be possible at the end of this project to systematically
    and programmatically, in a lightweight, useful manner test a
    component against an API and verify the output/behaviour matches
    expected results. This should include both expected data sources and
    results and unexpected data sources and results. Test cases should
    have a mode whereby any docstrings can be output along with an
    indication of success/failure to assist with documentation
    creation.\
    \
-   The other main use case is testing systems. For example, it should
    be possible to take a Kamaelia system that is designed to do a two
    phase commit, and test both succesful and unsuccessful scenarios
    automatically.\
    \
    This could involve creating a customised scheduler to change timings
    and run orders, etc. Similarly there are opportunities to be had
    with block box system testing (treating a system like you would a
    component), facilities mocking for subsystems and facilities for
    mocking modules that subsystems use (eg mocking select & socket when
    testing TCP code is particularly useful).\
    \
    An example system that would benefit from this is testing that a
    peer to peer system which is designed to create a certain kind of
    mesh **does** indeed create the expected kind of mesh in the context
    of errors & timeouts, missed data delivery and damage. (A test
    harness for this is essentially a simulation, but one that operates
    on the actual components & system).\
    \
    Tracing of data along linkages, and suggestions for how to check
    that data going across linkages is correct would also be useful.

\
This is a project that is something we have wanted for some time, but is
now becoming clear that it would be extremely useful as Kamaelia usage
continues to grow. Informal test systems must give way to automated. It
is also expected that any student working on this will look at the
existing way systems are developed and tested.\
\
The key benefit of this approach is to push an extra layer of system
verification into software systems - specifically allowing the testing
and verification of concurrent systems. This is something hardware
systems have had for a long time now, but a practical toolkit and with a
practical verification suite for concurrent systems for software is
extremely attractive. The primary test cases for a framework are
expected to be existing Kamaelia systems, however where necessary small,
but focussed examples are likely to be needed as well.\

------------------------------------------------------------------------

\

### High Level Kamaelia 3D Modelling Components 

The purpose of this project is to produce higher level 3D primitives,
***which are still components*** such as walls, mannequins, water,
clouds & terrain for creating and interacting with 3D worlds, ideally in
a human friendly way.\
\
By doing so it will be easier to contstruct a variety of 3D models. The
core of this idea started from looking at an artist\'s mannequin - the
kind often made from wood and poseable. Having a basic starting
mannequin that\'s unskinned would be extremely useful, since it
bootstraps alot of basic 3D work. Furthermore, unlike a wooden mannequin
we can change things.\

-   You can change the size of all the ovoids - such that as well as
    obviously different person shapes, you can do more - you can also
    change from human to animal. (given that skeletal structure for many
    animals is 4 limbs, a torso, head, ears. The only optional addition
    would be a tail)
-   It would make sense to be able to skin the mannequin

Beyond this however, having some basic similar objects would make
sense:\

-   A box with an optional number of wheels along the sides, of variable
    radius
-   A surface/terrain object - grassy, roadlike, sandy, watery
-   A \"fluffy object\" - think clouds, shrubs, bushes
-   A malleable tree. (think deformable fluffy object with a pole)
-   A wall object - or a hollow cube shape with optional entrances cut
    in the sides. (this approach is probably easier to work with)\
-   Finally a slanted roof surface with 2 or more sides. (Two sides
    gives you a traditional house roof, 3 or 4 gives you a pyramid, etc)

Texturing should ideally take into account the existing texturing
options - that allow, for example, existing pygame components to be used
as textures.\
\
The practical outcome of this is that rather than using low level
primitives of surfaces, a user could work at a much higher level.\
\
The context of this project really revolves around the fact that last
summer the Open GL components created were a success, and this is aimed
at pushing usablility of these components up higher.\
\
The key benefit of this proect is that it would become simpler to use
Kamaelia for ad hoc 3D modelling. (Combined with the whiteboard\'s
backplace, this could be extremely useful) These are all \"for
examples\" - the mannequin & wall/floor parts however I view as pretty
core.\

------------------------------------------------------------------------

\

### Visual Editor for Creation & Composition of Shard Components

This boils down to creating an editor for making components out of
pieces of components - shards. These pieces are also by definition
components, but unlike normal Kamaelia components are more functional,
single shot than generator or thread based. Ie they don\'t really
control flow.\
\
The practical result of this is that it should mean that you would be
able to largely create/prototype new components for Kamaelia
graphically. A user would be able to use an editor to take pieces of
components (Shard Components, maybe) and join them together using some
connectors wrapping control flow.\
\
A [diagram showing a potential component structure can be found here](http://thwackety.com/FunctionalComponents.png).
In this diagram
you can see some parts of the diagram are reusable. Other parts can be
reused as a chassis, and some parts simply can\'t be reused. The
notation is based loosely on [JSP](http://en.wikipedia.org/wiki/Jackson_Structured_Programming), but
the reason isn\'t to copy JSP (we\'re using it as a component system
after all), but to use a metaphor that many developers are already
familiar with. It is also relatively simple and completely abstracts out
control flow - making components more likely to be reusable.\
\
The project sits in the context that we already have a graphical
composition tool ([Compose](/Developers/Projects/Compose.html)) for
standard Kamaelia component. However it is highly desirable to be able
to create new low level components graphically.\
\
Specific benefits of doing this project will be both the components
created for editting essentially structured diagrams, but also the work
done on developing the shards idea further. In the long term this offers
opportunity to drive usability of the system up into the realms of the
expert non-programmer user. Shards are a relatively new idea, so this
project is partly about exploration of the problem space and partly
about implementing the first pass at a useful tool.\
\
Longer discussion on this topic has happened on the mailing list.
([start of
thread](http://sourceforge.net/mailarchive/forum.php?thread_id=31878613&forum_id=43377),
[continuation](http://sourceforge.net/mailarchive/forum.php?thread_id=31881069&forum_id=43377))\

------------------------------------------------------------------------

\

### Kamaelia Exemplar

The aim of this project is for you to take something you\'ve always
wanted to do and create it using Kamaelia, with the aim of creating
something which is a cool/useful demo/tool. (preferably useful tool :-)\
\
The result of this should be something that you\'ve wanted to build for
sometime, that you think others will also gain from. From the
perspective of the Kamaelia project, this should ideally be an exemplar
of what can be achieved using kamaelia - be it\...\

-   Large scale audio distribution, a second life clone, 3D game, 2D
    game, video player, video annotator, image manipulation tool, chat
    system, integration of handwriting & shape recognition (and perhaps
    vector drawing) into the whiteboard application, etc

The entire system should be created out of new and existing Kamaelia
components.\
\
The list of existing Kamaelia Components (excluding experiemental in
/Sketches) can be found here:\

-   [/Components](/Components.html)

The key benefit of working on this project from Kamaelia\'s perspective
will be the creation of an exemplar project which has real benefits for
the user - be it entertainment or practical. (The BBC ***is*** about
entertainment among other things after all)\
If you \*do\* do this one, please follow the template given below in
\"Your Idea as a title\"\

------------------------------------------------------------------------

\

### *Your Idea as a title*

-   One sentance of what the task is designed to achieve/create.
-   A practical, clear result of what will be possible as a result of
    achieving this task. This is best described in the case of a user
    story.
-   The context in which this task sits. Has this task any history? Is
    it the result of any previous tasks - either within the project or
    outside.
-   What benefits will be gained by working on this task, and achieving
    its goals? Speculative as well as certained/realistically expected
    benefits are valid here.

------------------------------------------------------------------------

\
To be added over the next 24 hours. You can get ideas however by looking
at [last years page](/SummerOfCode2006.html).\
You can also add your own ideas here (hit the edit button).\
\
