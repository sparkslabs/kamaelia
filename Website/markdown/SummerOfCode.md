---
pagename: SummerOfCode
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Kamaelia & Google\'s Summer of
Code]{style="font-size: 21pt; font-weight: 600;"}

> ***Kamaelia\'s aim is to make it easier and more fun to make software,
> quickly and maintainably in a way that makes concurrency (eg
> multicore) easy and fun to work with. The more code that is multicore
> friendly, the easier we make it for everyone.***\

::: {.boxright}
**Don\'t know python?** [Read this!](http://www.greenteapress.com/thinkpython/) Want an overview of
how we handle mentoring? [Read this!](/SummerOfCodeMentoring.html)]
:::

::: {.boxright}
**IMPORTANT:** As a general point (whatever org you\'re interested in),
pick (or create) a project idea you\'re **passionate** about or think
will be **fun** *that fits with the mentor org*. You\'ll be doing this
all summer, and we all want you to have fun, as well as create something
cool. You might think \"oh that\'s low priority\", or \"they wouldn\'t
be interested in my idea for\", well, if you\'re **passionate** about an
idea and it \"fits\", then you being passionate becomes as important as
the project!
:::

**Our primary pages for each year are listed below:\
**

-   **[Summer of Code 2008](/SummerOfCode2008.html)** **(Yes, you
    really want to see this page - there\'s also a presentation/overview
    there)\
    **
-   [Summer of Code 2007](/SummerOfCode2007.html)
-   [Summer of Code 2006](/SummerOfCode2006.html)
-   Introductions: [Overview](/Introduction.html),
    [Whiteboard Article](/t/TN-LineuxFormat-Kamaelia.pdf),
    [Light Technical Intro](/t/TN-LightTechnicalIntroToKamaelia.pdf),
    [Presentations](http://www.slideshare.net/kamaelian/slideshows)

### Students we\'re looking for

Please don\'t prejudge yourself as \"I can\'t do that, I don\'t have the
right experience\". Some of the best projects we\'ve seen have come from
the most inexperienced of students. Some of the best insights have come
from the most naive. If you have a lot of experience, you don\'t
necessarily have the \"right\" experience, and so lull yourself into a
false sense of security. However, fundamentally, if you think the
project is interesting, the ideas are interesting or you\'re inspired by
the ideas, please get in touch. Let us make the judgement, rather than
prejudge youself out of a fun summer. Yes, we can\'t take everyone, but
that doesn\'t mean we always take people with lots of experience :-)
Your lack of experience can be a fantastic asset, OK? :-)\

### **Previous Years**

**Previous year students**\
In previous years we\'ve accepted students who have had a wide range of
experience. Some have been pre-university students who are starting
university following the summer, other ones we\'ve had have been in the
middle of the course. Still others have been graduating and even one
post grad student. Lack of knowledge of python isn\'t something we
consider a major hurdle, as long as you put the effort into learning
python and doing the mini axon tutorial. (We don\'t expect any prior
knowledge of Kamaelia)\

**Previous year projects**\

As an idea of how useful Summer of Code has been all round, a selection
of the great work students did last summer as a part of [Google Summer
Of Code 2006](http://code.google.com/soc) has:

-   Bittorrent client (created components for seeding and fetching from
    a swarm including means of chunking live data for \"live\"
    bittorrent based streaming)\
-   Modular HTTP Server\
-   OpenGL capabilities (including, for example, putting pygame
    components on opengl objects as textures - still able to recieve
    pixel perfect updates ([eg drawing on a 3D surface](/Components/pydoc/Kamaelia.UI.Pygame.MagnaDoodle.html))\
-   Key authentication infrastructures (proof of concept)\
-   Speex codec bindings
-   A file handle like interface to backgrounded Kamaelia components
-   Some work on extending & making more user friendly the Kamaelia Web
    Server (though more work here is welcome)
-   High Level Kamaelia 3D Modelling Components
-   Beginnings of a visual editor for creation & composition of shard
    components
-   Pygame based scribble pad & textual input and standardised textual
    output

### **This year**

**What we expect**\
\
**We expect you to only propose a project you\'re enthusiastic about** -
we can say alot more about this, but that is actually one of the most
important criterion. We all get more out of it that way!\
\
This can be either one off the list, or something you think fits with
the project. Kamaelia is a fairly wide ranging project (potentially) due
to the goal of making concurrency easy & fun to work with in all
contexts. As a result, if you\'ve ever wanted to write that multicore,
3D, P2P game, Kamaelia should be the technology that makes it possible,
and we\'d view it a valid test of Kamaelia. Then again, if you want to
write a program to assist children to learn to read and write (based on
the gesture code & speech synthesis) that would be equally cool and
useful. Then again, if you want to create systems for working with
databases or social software systems, that would be useful as well,
since it hits needs of the project. As we say, wide ranging.\
\
There are however expectations we have as a result.\

We will expect you to have done the MiniAxon tutorial ***ideally before
submitting your application***. This teaches you how Kamaelia
essentially works under the hood (barring optimisations), and as a
result we feel is vitally important.

We will expect you to, where practical, discuss your application with us
on IRC or email ***sooner rather than later.*** We work primarily over
IRC, we will expect you to do so too, so start as you mean to go on!\

Since you\'re being paid to do this, we expect you to treat it like a
full time job. Generally speaking that means 35-40 hours a week, though
cultures round the world vary. (the numbers are indicative, not
prescriptive based on european norms of what \"full time work\" means)\

Since its summer we won\'t be surprised if you say you\'re having a
holiday, so we expect to see how that is scheduled and planned for.

Yes, we know exams happen at different times of the year and we all have
to juggle. It is your responsibility to say how you will manage the
clash between your studies and your proposed work. (yes, we feel
academic work must come first, but if someone\'s paying you to do
something you\'re taking on a responsibility. It\'s your responsibility
to say how you manage your commitments)

We expect you to manage your time and checkin code at least 2-3 times
per week - [we give you a way of doing
this](http://www.slideshare.net/kamaelian/managing-creativity/) which is
safe to do so.

We will expect you to attend our normal weekly IRC meeting, unless
timezones simply don\'t work

We will expect you to attend a weekly guaranteed mentor time session.
This is an hour long session but it\'s specifically there to allow you
to have some guaranteed time with your mentor, rather than anything
else.\

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

We may ask you to write an introductory presentation to the project work
you have done, in a similar way to what you see on the [Kamaelia
Grey](/KamaeliaGrey.html) page. You want people to use your work, right? :-)\

To have fun :) (What\'s the point otherwise? :)

ie it\'s your project and your commitment - we expect you to act that
way ! :-)\
\
**What to expect from us**\
Given that freedom of ideas, what do we expect in return? We expect
you:\

-   Expect us to challenge you. Support you. We want you to achieve your
    goals, and retain the same enthusiasm for your project at the end as
    you\'ve got at the beginning.
-   You can expect guaranteed time specifically set aside to help you
    discuss your issues/successes
-   By checking in code often, we can and will give you honest feedback
    on it. This may be hard to take, but we\'ll try and be gentle :)
    Bear in mind this works both ways - if you criticise our code, even
    harshly, we\'ll thank you for it. (best way to get more feedback :-)
-   We will give you the freedom and support to develop your ideas, and
    to integrate them with the rest of the project.
-   Whilst we won\'t spoon feed you - we expect you to read docs for
    example - we will recognise that you\'re new to this and help you in
    finding docs (for example) and in showing you common shortcuts.

Essentially, we want you to achieve your goals, create something fun and
useful, we want you to learn how open source works, and we want to have
fun at the same time. So we\'ll do whatever we can to help you, so long
as you do whatever you can to help yourself. (which seems a fair deal
:)\

**Ideas for This Year** 
-----------------------

Our [ideas list](/SummerOfCode2008.html) for projects this year keeps on
growing, and reflects the broad scope of the project which you can see
from [the components list](/Components.html). This is divided into two groups
- exemplars (interesting useful applications which could be built and
would usefully extend Kamaelia at the same time) and core improvements.\

**Application Ideas**\

-   [Multiwindow pygame](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1196129474)
    based paint program
-   Extend the [ER modelling](http://yeoldeclue.com/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1195955570)
    tool to be a full database front end (includes a requirement for
    Components for working with SQL Databases)
-   Small children friendly version of Compose
-   Extend the [XMPP implementation](http://trac.defuze.org/wiki/headstock) code
-   3D Social Network Visualisation tool
-   A Testing Framework for Kamaelia Systems

**Core Improvements**\
Whilst these are core improvements, we would prefer these to be done in
the context of a usecase. (Since whilst it is \_possible\_ to develop
new and useful technology without a usecase, its not amazingly useful
since no one can see how to use it. As a result, even the Open GL
project for example in the past was required to have examples of usage.
Where examples of usage have been weak, the projects have often been
weaker. (Which shouldn\'t be a surprise :-)\

WSGI-ify the Kamaelia Web Server

Tools for working with SQL Databases.

Improved Multicore support (We can already do multicore, but it requires
merge into the core, and how does it affect things like backplanes and
all the various components.)\

Extensions to the [co-ordinating assistant tracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html) :

-   Modify the [co-ordinating assistant tracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html)
    to use the minimal [STM](/STM.html) code

```{=html}
<!-- -->
```
-   Make [co-ordinating assistant tracker](/Docs/Axon/Axon.CoordinatingAssistantTracker.html)
    environments inheritable

Change the [topology visualiser](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewer.html)
to work in full 3D\

Extend Kamaelia\'s [Dirac](http://dirac.sourceforge.net/) support to
include support for the optimsed version of
[Dirac](http://dirac.sourceforge.net/) called
[Schoedinger](http://schrodinger.sourceforge.net/ideas.php)

Platform specific improvements\

-   Improve Kamaelia\'s support on Windows (XP and Vista primarily),
    including how to package up Kamaelia Apps for it. (eg the ER
    Modelling tool)\

```{=html}
<!-- -->
```
-   Improve Kamaelia\'s support on Mac OS X

```{=html}
<!-- -->
```
-   See how much of Kamaelia can run on IronPython 2\

Explore how the [changes to the way components can be
defined](/cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1155124531)
can be handled and introspected by Compose.\

However, if you just want to write a game using Kamaelia, that would be
interesting, simply because it then becomes a nice demo of Kamaelia -
especially if its networked and you can explore the contents of worlds
on other people\'s runtimes (say flying round different people\'s
universes) :-)\

Many of last years ideas are discussed:

-   On the [project ideas](/cgi-bin/projects/blog.cgi) blog we set up
    last year, *but aren\'t really using this year*
-   And also on the [Projects](/Developers/Projects) page near the
    bottom.

If you\'re interested in those please [get in touch](/Contact.html)!

Please note [**please use our template**](/SummerOfCode2006Template.html)
**in your application, its there to give you an idea of how we\'re
evaluating apps!**\

-   [Historic: [Taking part in SoC 2006](SummerOfCode2006.html)]{style="font-weight: 600;"}
