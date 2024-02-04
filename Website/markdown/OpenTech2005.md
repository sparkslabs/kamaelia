---
pagename: OpenTech2005
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Kamaelia @ OpenTech 2005]{style="font-size:20pt;font-weight:600"}

Open Tech 2005\* is a follow on from previous years\' NotCon events
which are community driven low cost events by geeks & developers for
geeks & developers. (Much like Pycon & Europython but much more general
in nature)

-   Website: <http://www.ukuug.org/events/opentech2005/>
-   Where/When: Hammersmith, London, UK, July 23rd

The reason I\'m posting about it is because I\'m going to be talking
about Kamaelia there. Unlike Python UK & Europython this is going to be
a 15 minute talk, so I\'ll be focussing on what we\'ve been doing with
Kamaelia, what you can do with Kamaelia, and so on rather than going
through internals.

In addition since my talk on Kamaelia is before lunch, I\'d really like
to help people get started using Kamaelia (this really the point of
giving talks!), so I\'m going to be running a small ad-hoc/mini sprint
that afternoon.

There\'s a variety of possible sprintable things ranging from [how to
put together simple Kamaelia
systems](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=viewpost&postid=1113495151)
through to using [Kamaelia on Nokia Series 60
mobiles](http://cvs.sourceforge.net/viewcvs.py/kamaelia/Code/Python/Axon/Platforms/Series60/)
through to using [Kamaelia for writing
games](http://cvs.sourceforge.net/viewcvs.py/kamaelia/Sketches/OptimisationTest/)
(since we have some nice [Pygame based
components](http://cvs.sourceforge.net/viewcvs.py/kamaelia/Code/Python/Kamaelia/Kamaelia/UI/)
now).

I\'ll probably be sprinting on converting a proof of concept P2P
swarming algorithm into a protocol for creating TCP server swarms. This
is for joining together multicast islands to make it so that internet
broadcasting, rather than narrowcasting, can become a reality for the
BBC - which has clear benefits for everyone! (Even though the internet
is not TV :)

Kamaelia is designed to be able to picked up relatively quickly/easily,
but having a working knowledge of python is probably a necessity.

If you\'re interested, please let [me](mailto:michaels@rd.bbc.co.uk)
know! (Either before, or at Open Tech :)

[Original Proposal to Open Tech Organisers]{style="font-weight:600"}

[Kamaelia - Taking back the pipeline]{style="font-weight:400"}

Kamaelia is a project from BBC R&D that is aimed at building next
generation systems, software and protocols for next generation hardware.
That means high levels concurrency, and we need it to be easy. Whilst
Kamaelia is supporting the goal of putting as much BBC content online as
possible, its core technology holds promise to make concurrency simple
FUN and natural to work with, by giving Unix pipelines a 2,3/n-D twist
and weaving a new web with them. Tools exist for making TCP/Multicast
servers, clients, visual games, physics simulations, audio playback and
more. This talk will focus on the general ideas and use as a taster, and
we would also like to hold a sprint afterwards for anyone interested in
learning more.

[15 minutes (though longer - up to 45 minutes would be well
used)]{style="font-style:italic"}

Michael, July 2005
