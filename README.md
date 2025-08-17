Kamaelia
========

For future (maintenance mode) Kamaelia development

Note:

* Kamaelia is stable, and useful.
* Kamaelia is not  under active development at present.
* Kamaelia IS maintained. Pull requests WILL be considered. Fixes are
  welcome
* There are approximately 1-2 releases per year at the moment as of August
  2025

The website still exists here, and still largely correct: http://kamaelia.org/


Guild
=====

There's a note in the description of guild - which is the effective successor
to Kamaelia. (Starting with replacing Axon first with something more pythonic)

The short description of guild is:

* Guild is a basic pipelineable Actor system, currently based around threads
  and a developer friendly syntax. In particular it introduces 2 notions to
  an actor system - the idea of late binding, and of having common names (or
  aliases) for the purposes of enabling pipelining.

  It's inspired by Kamaelia, but with all the ugly parts removed.

The focus of guild is primarily *usability* and *correctness* first, speed later.
The latebinding is directly equivalent (and inspired by) the outbox model in
Kamaelia and common names/aliases again relates "inbox/control/outbox/signal"
and to Kamaelia's idea of backplanes and similar.

Links for Guild:

* https://github.com/sparkslabs/guild - main repo
* http://www.sparkslabs.com/guild/ - placeholder website (generated from the repo)
* http://www.sparkslabs.com/michael/blog/category/guild - blog posts

Compatibility
-------------
Guild is NOT directly compatible with Kamaelia. It's a ground up rewrite, using 
everything learnt in Kamaelia in how to make concurrent systems conceptually
easy to work with.

That said, no one likes to throw away work, so there is some work on a compatibility
layer occasionally being worked on. 

So, what is that compatibility layer?

Kamaelia is a collection of components though as well as concurrency approach, and
Guild includes a handful of useful components (including video capture, pygame, STM,
backplanes, pipelines, audio capture, QT etc), but as you'd expect these are written
as and when needed.

To avoid reinventing useful wheels I started work on a compatibility layer here:

* https://github.com/sparkslabs/guild-kamaelia - This is a repo for reimplementing
  components for Guild of the same name and behaviour as their Kamaelia counterparts.
  (The idea to allow drop in replacements to simplify porting)

There is a todo/done/WIP list:

* https://github.com/sparkslabs/guild-kamaelia/blob/master/TODO.md

What might actually happen though is for their to become created some form of
decorator to allowing wrapping a kamaelia component as a guild actor. The reason
for this - in case it's not obvious - is because there are lots of useful kamaelia
components that exist and reimplementing them all seems a little silly :-)

That's not been done yet though.

Michael, October 2015

Update  - This repo is in maintenance mode, and is currently updated at
least once per year. There had been a delay due problems with the vorbis
library.


Michael, August 2025
