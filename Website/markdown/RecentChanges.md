---
pagename: Recent Changes
last-modified-date: 2024/02/11
page-template: default
page-type: text/markdown
page-status: current
---
# Recent Changes

**Current status:** This site is currently undergoing a number of updates
and upgrades.  After this the plan is to bring the Kamaelia codebase up to
date relative to changes in the python eco system since the project was put
on indefinite hold.

**Why?** This was a relative safe thing to do when the project was
targetting python 2.7 since python 2.7 was an extraordinarily long lived
supported version.  Then the pandemic hit, and frankly, there were more
important things to worry about.  The pandemic is still with us, but
circumstances have changed, making updates at the moment practical and
realistic to achieve, so this has been done.


## Upcoming changes

In no particular order:

* Replacement of developer section - which was targetted at community
  engagement with a better user-developer targetted section.  This would
  build on the existing docs around tutorials, cookbooks and API reference
  etc
* Template fixes
* Content fixes, content refresh
* Code updates, guild tests
* Rebuild of auto-doc system
* Re-enable the quiz form of the mini-axon tutorial

## Future

* Actor-Flow.


## 2024/02/11

(This page created today, adding some entries and dates below for an
indication of activity)

Over the past 2 months, on and off, work has been done on the following
areas to start bringing this site back up to speed:

* Auto-API documentation generation has been rebooted. The [new tools][NEWDOCTOOLS] have
  been added to the [github repo][GITHUBREPO] ([2023/12/24][GITHUBPR11])

* In order to do this, there needed to be a whole load of python 3 related
  fixes ([2023/12/16][GITHUBPR8]).  There still need to be a bunch of fixes
  related to changes in the python ecosystem.  This especially included the
  removal of wildcard imports within the repo ([2023/12/21][GITHUBPR9]), along
  with other minor fixes ([2023/12/24][GITHUBPR10])

* The PDF of these docs are linked from the [Home page](/Home.html) - This
  is essentially a complete book level reference text which can accompany
  the tutorial written previously. ([2023/12/24][GITHUBPR12])

* [SSL/TLS has been enabled][ISSUESSL] on the Kamaelia website

* The ancient wiki engine which was used to manage this site, and never
  quite made the jump between server hosts, was temporarily resurrected
  offline, and used to create an unstyled, \"no furniture\" version of the
  site. This is all part of the [site revamp][GITHUBPR_REVAMP]

* Slideshare embeds fixed for presentations and tutorials

* This has allowed the site to be switched to being (almost entirely)
  generated from markdown files [2024/2/4][GITHUBPR_REVAMP], making it easier
  to edit.  (This still in part a WIP)
  * This uses pandoc to generate the HTML, and then that is styled using
    new CSS. This allows better/nicer autostyling of source code where
    enabled.
  * Some initial metadata has also been added, some for pandoc, but
    primarily to allow improved site management (rather than manglement)
  * Added some links back to the RD Website


* Significant chunks of [breakage on the website have been fixed][WEBSITEBREAKAGE].
  (Started 23/12/15, issue closed on 2024/02/03)
  This includes:
  * Removal of old site infrastructure that no longer makes sense.
     * For example, the [site map][SITEMAP] has been removed from page
       links. The reason for this:
        * While the links have been fixed on that page, not all the links
          should be there
        * Lots of the content linked to is stale, and removing the link from
          general pages gives a chance to update and rename it
        * It has links to old wiki infrastructure that no longer exist.
     * Same goes for the site infrastructure links to the ancient wiki. 
     * Removal of the old automated \"Recent Changes\" page because it made it
       look like it was automated, but the wiki engine used to do that went
       away a long time ago
  * Fixes to lots of links - like in the cookbook
  * The CSS is now a lot leaner, simpler and cleaner. (It could be better
    and more responsive, but that\'ll wait for an overall redesign)
  * Links to pages that said \"this will be written shortly\" removed as have
    been many placeholders.

* A number of key things that need updating have been captured in a github
  project.

## Before 2023/12/15

The project was on hold in a \"the things we\'re using aren\'t broken so
this isn\'t being updated\" state.  Kamaelia had been used in a number of
small projects internally while the project was in this state, but there
were few public updates.

There were minor fixes to the DVB subsystems (2016).


## 2014-2022 - Guild

Most effort in this space has actually gone into Kamaelia\'s follow on
project [Guild][GUILD] which focussed on a \"syntactic sugar\" first
approach.  Guild was not heavility advertised, but was used internally in a
number of projects.  For example it was used in the micro:bit prototype to
implement the [batch compiler][GUILDBATCHCOMPILER] in the python to
arduino-C++ [toolchain][MICROBITCOMPILER]. To give an idea of timeframe of
activity there:

* 2014 - Guild first released as a public project (after use with internal
  project)
* 2014/2015 - Guild used in production system to manage compilation of user
  programs in the micro:bit prototype
* 2015 - basic STM added, support for actor functions, actor exceptions,
  alongside actor methods, various examples
* 2017 - Python 3 related updates, usability tweaks based on use in systems.
* 2019 - Experiments around pygame actors
* 2021 - Usability tweaks, based on use in an internal system.
* 2022
   - Internal tweaks and cleanups (again based on internal usage), removed
     python 2 support
   - Examples improved (esp using pygame as a core example)
   - Initial version of a promises API (which allows concurrent
     actor_function calls and handling as they return) - including job
     cancellation
   - Added [Mini-Guild][MINIGUILD_INITIAL] - based on [Mini-Axon][MINIAXON] in
     Kamaelia, which was then fleshed out to a more complete
     [miniguild][MINIGUILD_CURRENT]
   - Initial C++ Guild tests

Future work on Kamaelia will probably relate to bringing the best ideas from
Guild into Kamaelia and allowing the use of Kamaelia components in guild
systems.


## Why mention Guild and resurrect Kamaelia?

*This section needs editting down, or perhaps shifting off to a blog*

**Why mention Guild here?** While this is the Kamaelia site, not the guild
one, guild was very much intended as a follow on from Kamaelia.  It\'s
intention was very much \"OK, we\'ve proven that can work, can we make it work
with a nice syntax?\".  As a result, Guild started from a \"syntactic sugar
first\" approach, but the aim was always to unify the two projects.  This
never actually happened, but probably will at some point.

To cut a long story short, I figured out a way of doing a guild type
syntax in C++.  From a kamaelia perspective a C++ version has always been
possible.  This was first demonstrated in a [C++ MiniAxon][CPPMINIAXON]
from as long ago as Feb 2005.  I recently benchmarked the
generators that used relative to C++20 coroutines, and found that
[ancient code was remarkably good][CPP03_CPP20_GENERATORS].

Also, since starting Guild, I\'ve become increasingly aware that actually
formally publishing this stuff would be useful.  For example, this approach
of having **outboxes** - which was first in Kamaelia, and then reused in
Guild actually seems pretty unique, especially from the perspective of
seeking to simplify development for novice users. This was noted by Ted
Leung in an [O\'Reilly keynote in back in 2009][TED_LEUNG_CONCURRENCY_SLIDESHARE]. 

The point being though, Kamaelia isn\'t really a CSP system (which to an
extent inspired Kamaelia though async hardware & network systems were the
core).  This point was raised at an early Pycon UK and the person noting it
said \"you\'re doing actor systems\".  At the time I didn\'t know an awful lot
about actor systems, so I went away, and thought \"maybe I can use that idea
for syntactic sugar\"

So that inspired Guild.  Kamaelia was put on hold for various reasons, but
primarily because I noted that while begineers could start, get up to speed
with kamaelia and do interesting things, there was a reticence from
experienced developers.  I figured then that syntactic sugar was the way
forward.  Then life got busy and we all got allocated to different projects.

Kamaelia pretty much sought to ask the question \"can you build systems like
this?\" Guild pretty much sought to ask the question \"Can you make this
readable and friendlier to experienced developers?\" My current question is
\"can I generalise this across different languages and gain significant
performance gains, and later down the line interoperability?\".

Then I realised that I could implement Guild like sugar in modern C++ and I
got re-interested.  This time I did a literature search (ACM, Springer, etc)
to see if anyone had done this. To my surprise, no.

* Actor systems were/are very much stuck with the `address ->  process+mailbox`
  model. There\'s literally hundreds of variants on this model, but they all
  boil down to this. This means the late binding you get with outboxes (even
  as a metaphor) simple doesn\'t exist as a systemic thing.
* Flow based systems - which are very Kamaelia like - also don\'t tend to
  look at things in this way.
* The thing that people didn\'t like about Kamaelia - the matching for
  messages - which tends to map to an if or switch statement - is the
  default in the actor world.
* There was a *language* - Thal - written as part of a thesis that had
  Guild\'s concept of actor methods, but not really actor methods or
  exceptions, and no concept of late binding.
* Most systems try to be \"pure\" actor models, and avoid secondary forms of
  concurrency, even though this sort of thing is necessary to avoid
  convoluated code in real world code. (Such as STM - which underlies the
  CAT in Kamaelia, and is a core piece of functionality in Guild.)
* Nesting and pipelining ala Kamaelia and guild seems rare.

Please note though, there are some really awesome things in the actor world
at the moment, and the two that spring to mind are Pony and Akka.  If you're
interested in looking at actors more, those are great starting points. 
There are also a number of high performance actor systems in languages like
C++, but I personally feel that readability and ease of use are vital.  (And
those two \"soft\" aspects don\'t tend to apply to languages like C++ :-) -
and I use C++ daily as well as python these days\.\.\.)

**Why resurrect Kamaelia?**  The upshot from this, is that I thought \"this
all needs formally publishing and talking about\", primarily because I\'ve now
got code over 20 years old that is still useful today *because* of
Kamaelia\'s separation of concerns.

Yes, Kamaelia could do with a root and branch update.  Many subsystems could
do with Guild style rewrites, but the code and systems tend to just *work*. 
The core version of [Kamaelia Grey][KAMAELIA_GREY] - the greylisting server
that handled my email *for over a decade* (until I abandoned running my home
sever) was *written in an afternoon,* and tweaked over a few days following.

The point is this combination of flow and actors hasn\'t really been talked
about in the literature, as far as I can tell.  Not in the way used in
Kamaelia and Guild and not really from the perspective of ease of use, and
clarity of systems. So publishing struck me as a good idea.

That led me to revisiting fixing the Kamaelia site, and leads me to
rethinking interoperability between the two - especially given the changes
in the python language since Kamaelia started.

\-\- Michael, 12/2/2024 (needs editting down)


[KAMAELIA_GREY]: /KamaeliaGrey.html
[TED_LEUNG_CONCURRENCY_SLIDESHARE]: https://www.slideshare.net/twleung/a-survey-of-concurrency-constructs
[CPP03_CPP20_GENERATORS]: http://www.sparkslabs.com/blog/posts/coroutines-5-benchmarking-cpp03-cpp20-python-generators.html
[MINIGUILD_INITIAL]: https://github.com/sparkslabs/guild/commit/04d7d03f0551bf81179baa08e3155f330172df06
[MINIGUILD_CURRENT]: https://github.com/sparkslabs/guild/tree/master/examples/blog/miniguild
[SITEMAP]: /Sitemap.html
[NEWDOCTOOLS]: https://github.com/sparkslabs/kamaelia/tree/master/Code/Python/Kamaelia/Tools/NewDocGen
[GITHUBREPO]: https://github.com/sparkslabs/kamaelia
[ISSUESSL]: https://github.com/sparkslabs/kamaelia/issues/14
[GITHUBPR8]: https://github.com/sparkslabs/kamaelia/pull/8/files
[GITHUBPR9]: https://github.com/sparkslabs/kamaelia/pull/9/files
[GITHUBPR10]: https://github.com/sparkslabs/kamaelia/pull/10/files
[GITHUBPR11]: https://github.com/sparkslabs/kamaelia/pull/11/files
[GITHUBPR12]: https://github.com/sparkslabs/kamaelia/pull/12/files
[GITHUBPR_REVAMP]: https://github.com/sparkslabs/kamaelia/pull/16
[WEBSITEBREAKAGE]: https://github.com/sparkslabs/kamaelia/issues/7
[GUILD]: https://github.com/sparkslabs/guild
[GUILDBATCHCOMPILER]: https://github.com/sparkslabs/microbit-prototype/blob/master/compiler/batch_compiler.py
[MICROBITCOMPILER]: https://github.com/sparkslabs/microbit-prototype/tree/master/compiler
[MINIAXON]: /MiniAxon.html
[CPPMINIAXON]: https://github.com/sparkslabs/kamaelia/blob/master/Code/CPP/Scratch/miniaxon.readme
