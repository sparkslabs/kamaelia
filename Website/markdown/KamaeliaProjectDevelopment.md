---
pagename: KamaeliaProjectDevelopment
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Kamaelia Project
Development]{style="font-size: 21pt; font-weight: 600;"}

[How do you work, how can I join in?]{style="font-size: 16pt;"}

::: {.boxright}
See also, [how to contribute to Kamaelia](/Developers/Contributing.html)
:::

[NOTE: Needs updating to deal with creation of Kamaelia.Community.
Consider turning into a tabbed document
instead.]{style="font-weight: 600;"}

Since Kamaelia is exploring a new way of building software in many
respects, much of our development work goes into experimenting with
ideas, as well as the core codebase. We\'ve established a simple process
to help us do this. More detail below, but here are the headlines:

[Version control]{style="font-weight: 600;"} using SVN, courtesy of
sourceforge

[Experiment]{style="font-weight: 600;"} in[
/trunk/Sketches/]{style="font-family: courier;"}[YOUR\_INITIALS]{style="font-family: courier; font-style: italic;"}

[Main code base]{style="font-weight: 600;"} in
[/trunk/Code]{style="font-family: courier;"}

[Use Branches]{style="font-weight: 600;"} used for substantial changes

[Merges]{style="font-weight: 600;"} should be done by someone else
(unless the project admins give you permission)

-   \... so also be prepared to merge other people\'s branches!

This page is largely about [doing stuff,]{style="font-style: italic;"}
so we have a separate page about [meetings, and stuff like
that](ProjectAdmin.html).

Why all this? We want to be able to explore ideas in a shared
collaborative environment without imposing too many risks (bad builds,
bad code, bad design decisions, etc). Hopefully you\'ll think this a
sensible way to get things done ([please tell us](/Contact.html) if you
disagree) and you\'ll do something similar. If it works for you, please
do consider [asking](Contact.html) for access to use the the
[/Sketches]{style="font-family: courier;"} space. In practice this
should all be quite light touch - despite the length of this document!

[Version control]{style="font-size: 16pt; font-weight: 600;"}

All development for Kamaelia is done under version control using the
sourceforge SVN service. See our info on [how to access the
repository](Repository.html).

All file paths below are relative to the
[trunk]{style="font-style: italic;"} which is where the bulk of
development happens.

For reference, the [trunk]{style="font-style: italic;"} currently
contains the following top level entries:

[/Sketches]{style="font-family: Courier; font-weight: 600;"} (dir)

-   This is where [development of an exploratory
    nature]{style="font-weight: 600;"} occurs. ie \"we don\'t know what
    this code should look like yet\".

[/Code]{style="font-family: Courier; font-weight: 600;"} (dir)

-   This is the [main codebase]{style="font-weight: 600;"} from which
    releases are periodically built.

[/Tests]{style="font-family: Courier; font-weight: 600;"} (dir)

-   Becomes relavant after a 1.0 release and/or code maturity.

[/AUTHORS]{style="font-family: Courier; font-weight: 600;"},
[/COPYING]{style="font-family: Courier; font-weight: 600;"},
[/CVSROOT]{style="font-family: Courier; font-weight: 600;"} (dir),
[/Other]{style="font-family: Courier; font-weight: 600;"} (dir),
[/Website]{style="font-family: Courier; font-weight: 600;"} (dir)

Any re-development of code in
[/Code]{style="font-family: Courier; font-weight: 600;"} (such as large
scale refactoring) should be done on a branch (see below). To make life
simple for everyone, the branch should be of the entire development
tree.

[What do I do then?!]{style="font-size: 14pt; font-weight: 600;"}

So what do you do?

Experiment in
[/trunk]{style="font-family: Courier;"}[/Sketches/INITIALS]{style="font-family: Courier; font-weight: 600;"}

Move working things into
[/trunk/Code]{style="font-family: Courier; font-weight: 600;"}

Solidify into something we can trust

Add test suites

<div>

Preferably re-implement [test
first](http://www.agiledata.org/essays/tdd.html)

</div>

Make large swathe changes in branches called
[private\_INITIALS\_AnythingYouWant]{style="font-family: Courier; font-weight: 600;"}

Be prepared to merge other people\'s branches

-   Remember you are not allowed to merge your own branch into the trunk
    without the permission of the project admins - to encourage peer
    review, knowledge sharing and collaboration.

If all else fails, become an agent of
[CHAOS]{style="font-family: Courier; font-weight: 600;"} :-)

-   And yes, if this happens we\'ll with release scripts.
-   Obviously this is a place to edit things and just have fun if the
    above process isn\'t your thing :-)

Read on\...

[Exploratory Development in
]{style="font-size: 12pt; font-weight: 600;"}[/Sketches]{style="font-family: Courier; font-size: 12pt; font-weight: 600;"}

[Why sketches?]{style="font-weight: 600;"}

Development can be an engineering discipline - if you know your
requirements you can start with a spec and work forwards. This applies
to both \"Big design up front\" and to a lesser extent many agile
development processes. Alternatively, development can be like writing or
painting, where the artist will create many sketches before taking the
best and integrating them into a single coherant whole. Long term
developers will often experiment, writing small throwaway stubs of code
to see how something might work - especially if there are no clear
requirements to start off with. You can then often understand the
requirements better and then work on an engineered approach.

Kamaelia\'s development process is designed to support the creative \"we
don\'t know what we want, so let\'s sketch out a few ideas\" development
through to the fully engineered test-driven development approach. The
[/Sketches]{style="font-family: courier;"} area is a place to do this
experimentation and prototyping.

Both viewpoints have merit, and one group may term itself hackers (not
to be confused with crackers) or even artists, the other may term
themselves engineers or even computer scientists. In reality of
development is often a mixture of both. We therefore hope to support
both approaches in a reasonable fashion.

[Creating working space in
]{style="font-weight: 600;"}[/Sketches]{style="font-family: Courier; font-weight: 600;"}

Suppose your name is Mr Warren W. King and you want to create QT based
components. You probably need to experiment first, after all you don\'t
know exactly what you want, and you may need to change other existing
components, or maybe even Axon.

First, create yourslef some working space. You have the right to create
a subdirectory named your initials:
[/Sketches/WWK/]{style="font-family: Courier; font-weight: 600;"} . So
do that:

-   [cd Sketches]{style="font-family: Courier; font-weight: 600;"}
-   [mkdir WWK]{style="font-family: Courier; font-weight: 600;"}
-   [svn add WWK]{style="font-family: Courier; font-weight: 600;"}

This directory is yours to do with as you please, without clashing with
other people. If WWK is gone (say Wendy Wescot-Krinchbottom took it
already) just use your full name instead or something else
differentiating!

In this particular case, it would make sense to create the following
directories for development at that stage:

-   [/Sketches/WWK/QT/]{style="font-family: Courier; font-weight: 600;"}
-   [/Sketches/WWK/QT/test]{style="font-family: Courier; font-weight: 600;"}

You can then experiement with various implementations. You might do one
implementation, or you might do a variety. They may, or may not, become
full Kamaelia components or systems. The point is though, you can
develop any way you like. The advantage of doing this in the shared
repository is that if you abandon your work, someone else can always
pick it up later on. They\'ll know it might not perfect or complete, and
might not have been meant seriously - because it\'s in sketches. But by
having a shared sketch book you may save someone else time later on.
Obviously you also benefit from the shared code sketch book.

Suppose you\'re now happy that your code works and is useful, and now
you want to see how it might work in the repository.

[Migrating from
]{style="font-size: 12pt; font-weight: 600;"}[/Sketches]{style="font-family: Courier; font-size: 12pt; font-weight: 600;"}[
into
]{style="font-size: 12pt; font-weight: 600;"}[/Code]{style="font-family: Courier; font-size: 12pt; font-weight: 600;"}

This is the beginning of changing from an experimental mode to a mode
where we can say \"this is something we find useful\". As a result we
take some care in thinking about where code should go and the naming of
component before they enter the repository. The guidelines are really as
follows:

-   As far as possible, the name of the object should as obviously as
    possible reflect what the thing does. For example, a component that
    takes other components and bolts them together/plugs them into
    itself is termed a chassis. This name was not the first such name
    that was discussed, and there were a

Please note: you might do a sketch, and put it forward to going into
[/Code]{style="font-family: Courier; font-weight: 600;"}, or equally
someone else may do so. Don\'t be offended if the latter happens!

[What\'s the structure of
]{style="font-size: 12pt; font-weight: 600;"}[/Code
]{style="font-family: courier; font-size: 12pt; font-weight: 600;"}[?]{style="font-size: 12pt; font-weight: 600;"}

In order to understand the where something might fit, and what it might
be named it\'s useful to know the current structure. This discussion
will focus on the Python code tree.

Currently [/Code]{style="font-family: Courier; font-weight: 600;"} is
subdivided by language, then major projects & bindings as follows:

-   [/Code/CPP]{style="font-family: Courier; font-weight: 600;"} - This
    is reserved largely for work developing a C++ version of
    Kamaelia/Axon.
-   [/Code/Java]{style="font-family: Courier; font-weight: 600;"} - This
    is reserved largely for work developing a Java version of
    Kamaelia/Axon.
-   [/Code/Ruby]{style="font-family: Courier; font-weight: 600;"} - this
    does not exist as yet, but if someone were to port the ideas in
    Kamaelia/Axon to Ruby, their implementation would be welcome here.
-   [/Code/Python]{style="font-family: Courier; font-weight: 600;"} -
    the current focus of work.

[/Code/Python]{style="font-family: Courier; font-weight: 600;"} is
subdivided into the following key directories:

-   [/Code/Python/Axon]{style="font-family: Courier; font-weight: 600;"} -
    this contains the full distribution/development tree of the kernel
    of the component system
-   [/Code/Python/Kamaelia]{style="font-family: Courier; font-weight: 600;"} -
    this contains the full distribution/development tree of the bulk of
    the component system - the component system user.
-   [/Code/Python/Bindings]{style="font-family: Courier; font-weight: 600;"} -
    this contains a number of python bindings for C & C++ libraries that
    are used by a number of components. They are here because they\'ve
    been developed as part of the project.
-   [/Code/Python/Releases/]{style="font-family: Courier; font-weight: 600;"}
-   There\'s also a handful of scripts in this directory which are
    designed to simplify the process of building releases.

In the general case, most of the time the result of work on actual
components will end up in
[/Code/Python/Kamaelia]{style="font-family: Courier; font-weight: 600;"}.
For example
[Kamaelia.Internet.UDP.SimplePeer]{style="font-family: Courier; font-weight: 600;"}
resides inside the file
[/Code/Python/Kamaelia/Kamaelia/Internet/UDP.py]{style="font-family: Courier; font-weight: 600;"}
(at present).

Before making changes to
[/Code]{style="font-family: Courier; font-weight: 600;"} (on a shared
branch - such as a default checkout), please discuss them first on
either [\#kamaelia]{style="font-family: Courier; font-weight: 600;"} on
freenode\'s IRC or on the kamaelia mailing list. You will find we are
generally accommodating towards requests, but ask you to have some
patience, since we might have nefarious plans you\'re not aware of :-)

[Criterion for something going in
]{style="font-size: 12pt; font-weight: 600;"}[/Code]{style="font-family: Courier; font-size: 12pt; font-weight: 600;"}

Code that goes into
[/Code]{style="font-family: Courier; font-weight: 600;"} is expected to
be a candidate for adding to the
[RELEASE]{style="font-family: Courier; font-weight: 600;"} branch at
some point, but is not automatically added. Due to this expected next
step, it is expected that people committing to the SVN
[trunk]{style="font-style: italic;"} in
[/Code/Python/Kamaelia]{style="font-family: Courier; font-weight: 600;"}
will discuss what they\'re doing either [on IRC](/IRC.html) or [on the
mailing list](/mailinglists.html), or similar. Should a process be
needed, it will be invented as it becomes apparent :-) It will probably
take a form similar to that used on python-dev. Project admins act as
arbiters if there\'s a loggerhead.

The basic criterion for something going into
[/Code]{style="font-family: Courier; font-weight: 600;"} is simply
\"this is something we\'ve found useful for
[]{style="font-family: Courier; font-weight: 600;"}, and would now like
to try using it in other things and seeing how it fits\".

However, recently we added a simple rule for things that go in
[/Code]{style="font-family: Courier; font-weight: 600;"} :

must [have a ]{style="font-weight: 600;"}[simple
]{style="font-style: italic; font-weight: 600;"}[working
example]{style="font-weight: 600;"} to accompany it:

-   You\'ll probably already have this, since you will have been using
    it in /Sketches
-   It forms a simple acceptance test
-   Helps explain how to use your code to others

should have [some docstring documentation:]{style="font-weight: 600;"}

-   see our [guidelines](DocumentationGuidelines.html)

should declare a [global tuple referencing all classes in the
file]{style="font-weight: 600;"}:

<div>

[\_\_kamaelia\_components\_\_ = ( BasicPeer, SimplePeer, TargettedPeer,
PostboxPeer, )]{style="font-family: Courier; font-weight: 600;"}

</div>

-   Allows documentation to be automagically picked up and added to the
    documeation tree.
-   Makes your component available to graphical pipeline editors and
    other tools.
-   This declaraction should (obviously?) be a top level statement and
    come BEFORE any [if \_\_name\_\_ == \"\_\_main\_\_\":
    \...]{style="font-family: Courier; font-weight: 600;"}

[Note:]{style="font-weight: 600;"} Not all components in
[/Code]{style="font-family: Courier; font-weight: 600;"} currently have
an example. This is due to the development process evolving over time,
and becoming more concrete about what\'s useful. Also, depending on how
useful we percieve your component to be, we may waive this requirement
in favour of seeing what can be done.

If you do NOT feel you have time to hang around and wait for us (perhaps
only a few hours), please see discussion of the
[CHAOS]{style="font-family: Courier; font-weight: 600;"} branch below.

[Use of SVN Branches in
Kamaelia]{style="font-size: 16pt; font-weight: 600;"}

The bulk of day to day development with a view to release occurs on the
SVN [trunk]{style="font-style: italic;"}. It is the natural working
point that new developers - especially those new to version control -
start from. We prefer to have a situation where you can just get on with
development.

If you want to make experimental sweeping changes to the main
[/Code]{style="font-family: courier;"} codebase you need to use a branch
- either personal one, or the
[CHAOS]{style="font-family: Courier; font-weight: 600;"} branch.

[RELEASE]{style="font-family: Courier; font-style: italic; font-size: 12pt; font-weight: 600;"}[
branch]{style="font-size: 12pt; font-weight: 600;"}

[No editting ]{style="font-style: italic; font-weight: 600;"}[at
all]{style="font-style: italic; font-weight: 600; text-decoration: underline;"}[
happens on the release branch.
]{style="font-style: italic; font-weight: 600;"} This tracks the actual
releases. It\'s function is to simplify the automated release build.
Files are manually added to the release branch, but automatically
mirrored and updated from [trunk]{style="font-style: italic;"} at
release point.

Criterion (as of April 2006) for adding to the release branch:

-   Shown to be stable
-   Has an example in
    [/Code/Python/Kamaelia/Examples]{style="font-family: Courier; font-weight: 600;"}
-   Has pydoc style documentation of the code

Desirable when adding to the release branch:

-   Full coverage test suite. Note, this is desirable. Anything added
    without full coverage testing is considered either alpha or beta
    quality. This would be expected to reside initially in a
    subdirectory called test. As time matures, this will move out to
    /Tests/Python/Kamaelia - in the same way as /Tests/Python/Axon
    today. Tests should NOT move into /Tests/Python/Kamaelia until they
    are older than 1 year, and not expected to change. The reason for
    this delay is to find out whether they\'re a mistake or not! (As a
    result 1 year is meant to signify \"a significant time period\",
    rather than be prescriptive)

Expected development regarding code on the
[RELEASE]{style="font-family: Courier; font-weight: 600;"} branch:

-   Code added without full coverage testing is expected to gain a full
    coverage test suite over time. This may lead to reimplementation of
    the modue based on experience of using the module. Experience has
    shown that modules reimplemented test first after this process have
    a level of use & maturity which is extremely useful.

Adding something to the release branch should only be done with the
knowledge of a project admin. (Hey, that\'s part ofthe idea of project
[admin]{style="font-style: italic; font-weight: 600;"} after all. Whilst
this may seem restrictive, it\'s simply to ensure a level of
consistency, and in practice will often be a very short discussion.

[Personal Branches]{style="font-size: 12pt; font-weight: 600;"}

Much like having a personal namespace in
[/Sketches]{style="font-family: Courier; font-weight: 600;"} is useful,
having the ability to change anything and everything in the entire code
tree is extremely useful. It\'s also often by far the best way of
demonstrating why your point is right - why your way is better than the
current method or a proposed method. It\'s not always the best way, but
sufficiently often to be worth supporting.

As was hinted above in \"Version Control\", if you do make a branch it
should be across the whole code tree, and we have a naming mechanism to
simplify things. Suppose once again your name is Warren W King. Suppose
also you were the first person with those initials to start developing
things in Kamaelia, so your subdirectory name in
[/Sketches]{style="font-family: Courier; font-weight: 600;"} is
[/Sketches/WWK/]{style="font-family: Courier; font-weight: 600;"} . ie
your personal \"tag\" is
[WWK]{style="font-style: italic;"}[.]{style="font-style: italic; font-weight: 600;"}

For sake of argument, lets say you\'re doing integrations that require a
variety of changes in the code tree in various locations, based on some
changes in perspective the implementation of the QT module we described
above. You might consider calling that
[INTEGRATION\_BOOSTS]{style="font-family: Courier; font-weight: 600;"} .
However this precludes someone else using the same name.

As a result the suggested approach is to name your personal branches as:

-   [private\_]{style="font-family: Courier; font-weight: 600;"}[YOURTAG]{style="font-family: Courier; font-style: italic; font-weight: 600;"}[\_]{style="font-family: Courier; font-weight: 600;"}[Anything\_You\_Like]{style="font-family: Courier; font-style: italic; font-weight: 600;"}

So in this case, the branch name would be:

-   [private\_WWK\_INTEGRATION\_BOOSTS]{style="font-family: Courier; font-weight: 600;"}

Again, personally I\'d suggested something more descriptive/precise like
[private\_WWK\_QT\_INTEGRATION\_BOOSTS]{style="font-family: Courier; font-weight: 600;"},
but any branch with a name starting
[private\_]{style="font-family: Courier; font-weight: 600;"}[YOURTAG]{style="font-family: Courier; font-style: italic; font-weight: 600;"}
is yours to do as you will. This allows others to see what\'s happening
and share ideas, and see your ideas as they develop.

[There is a special rule here though: you are NOT allowed to merge a
branch you create (unless all project admins
agree)]{style="font-weight: 600;"}. The reason for this is this means
someone else has to merge it. This automatically gains 2 things - peer
review of code, and also it means that at least 2 people understand the
changes embodied in the code. Where possible, [please
]{style="font-style: italic;"}include documentation since it\'s a pain
to add later on!

If you don\'t know how to create branches, please just say it\'s
relatively simple, but remember the rule - the branch must be across the
entire tree.

[Agent of
]{style="font-size: 12pt; font-weight: 600;"}[CHAOS]{style="font-family: Courier; font-size: 12pt; font-weight: 600;"}[
branch]{style="font-size: 12pt; font-weight: 600;"}

If you feel the need to try out radical new ideas, AND also want to have
shared development of them, please use the
[CHAOS]{style="font-family: Courier; font-weight: 600;"} branch.
Co-ordinate amongst yourselves what you want to do and what the ground
rules are. If you\'re making someone upset here, you\'re doing something
wrong.

If the main CVS head ends up having too much control, the
[CHAOS]{style="font-family: Courier; font-weight: 600;"} branch is
design to allow you to bypass that control and produce your own version
that potentially has different goals from the project admin. If this
idea sounds familiar, it\'s because it\'s the approach that governs the
development of content on wikis, and we\'d like to run the
[CHAOS]{style="font-family: Courier; font-weight: 600;"} branch in that
way - you get to add things and work on things your way. If you break
things, your code may get reverted by someone else, or changed by
someone else.

In theory this sounds like complete anarchy and like it wouldn\'t work.
Experience with another project has shown that if it\'s taken on board
in the manner as described above (never ask permission on
[CHAOS]{style="font-family: Courier; font-weight: 600;"}) then you can
get great creative drives and experience from trying out a variety of
ideas quickly and effectively.

[Note: ]{style="font-weight: 600;"}This branch does not exist at time of
writing, but this document allows for its existance. If you feel the
need to use the [CHAOS]{style="font-family: Courier; font-weight: 600;"}
branch, please just create and use it.

[Finally \... Some General Guiding
Principles!]{style="font-size: 12pt; font-weight: 600;"}

Descriptions of things optimised for the 80% of programmers are
preferable to those with only the top 20% will understand. If this seems
\"dumbing down\", consider that it is often harder to describe something
complex simply, than to describe something simple in a complex fashion.
Remember that a key aim is to make life easier for the bulk of
programmers, with a recognition that its worth optimising for
maintenance.\

Fun descriptions, ideas and code tend to win arguments :-)\

You\'re going to get it wrong. Whether you like it or not, something you
do will go wrong and be very wrong. We\'d like to aim for a very high
hit rate of \"good\" decisions, but often the only way to find out what
the \"right\" answer is to actually try something and find out. Please
don\'t be afraid of pointing out the emperor has new clothes. We might
be embarrassed (possibly even upset) for a while, but we\'d rather be
told and know when we\'ve got something wrong. We\'re human too after
all :-) For a good discourse on why it\'s worth taking this risk, read
Paul Arden\'s excellent (and brief!) read \"Whatever you think, think
opposite\".\

-   A corrollary of this is that it might make sense occasionally to do
    sketches and branches of ideas that you think are really bad ideas
    and see how they pan out!\

Implementations change, but interfaces stay the same. If the interfaces
change, you\'ve written something new. ie you may add new inboxes and
outboxes to components, but if you change behaviours of existing
in-/out-boxes you should consider whether you\'re actually writing
something new. If in doubt, talk to the team.\

Quick, simple, clear, justified decisions (But not hasty).\

All rules have exceptions.\

[import this]{style="font-family: Courier; font-weight: 600;"} :-)\

Oh, and if it\'s not blatantly obvious, yes we\'d like to allow you to
check in. We have
[cvs\_acl]{style="font-family: Courier; font-weight: 600;"}s we could
use to protect our code if we think you\'re acting badly, so we\'re not
afraid to share our workspace, we\'d love for you to find Kamaelia as
useful as we do.
