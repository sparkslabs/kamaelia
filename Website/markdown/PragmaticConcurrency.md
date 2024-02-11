
::: { #pagebanner }

Kamaelia: Pragmatic Concurrency, A tutorial 
===========================================

This was a tutorial held at Europython \'09 in Birmingham on the morning
of Sunday 28 June 2009
:::

Concurrency is viewed as an advanced topic by many developers, meaning how
to handle concurrency pragmatically is often overlooked.  However, many real
world systems, including transportation, companies, electronics and Unix
systems are highly concurrent and accessible by the majority of people.  So,
one motivation can be \"many hands make light work\".

With software this maxim often appears to be false - in no small part due to
the tools we use to create concurrent systems.  Despite this, the need for
concurrency often creeps into many systems - even something as basic as
\"attaching a debugger\".

Kamaelia is a toolset and mindset aimed at assisting in structuring your
code such that you can focus on the problem you want to solve, but in a
way that results in naturally reusable code that happens to be
concurrent.

This tutorial aims to introduce this, and the core aspects of Kamaelia
systems. ([Accompanying notes](https://www.kamaelia.org/Europython09/A4KamaeliaEuroPython09.FINAL.pdf))

---

<iframe src="https://www.slideshare.net/slideshow/embed_code/key/7Y3geLqCM40kGb?startSlide=1"
        width="597"  height="486" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"
        style="margin: auto; display: block; border:1px solid #CCC; border-width:1px; margin-bottom:5px;max-width: 100%;" allowfullscreen></iframe>
<div style="margin-bottom:5px"><strong><a href="https://www.slideshare.net/kamaelian/kamaelia-europython-tutorial" title="Kamaelia Europython Tutorial" target="_blank">Kamaelia Europython Tutorial</a></strong> from <strong><a href="https://www.slideshare.net/kamaelian" target="_blank">kamaelian</a></strong></div>

---


These core aspects are: 

> **Axon**\
>
> > All Kamaelia systems are dependent on this core library - it
> > provides you with tools for making systems which are naturally
> > concurrent. Its primary metaphor is components with inboxes and
> > outboxes, which get linked by parent components.\
>
> **Kamaelia Components**\
>
> > The bulk of Kamaelia is actually a large collection of components.
> > By themselves each component is useful, but their real power comes
> > from being linked to each other, like programs in /usr/bin get
> > linked together, forming pipelines.\
>
> **Applications**\
>
> > This is the point of Kamaelia - to build useful systems. Kamaelia
> > was originally designed for naturally concurrent problems, so there
> > was a desire to make this simple(r) to work with. Using Axon based
> > components means applications generate more reusable components, and
> > also have a naturally concurrent structure. This can simplify many
> > applications, allowing their reuse in unexpected ways.\
>
> **Testing & Debugging**\
>
> > Testing & debugging concurrent systems is considered hard, we\'ll
> > cover some approaches we can use in Kamaelia for debugging systems.
> > Some of these are surprisingly familiar. Indeed, some can be used in
> > non-Kamaelia based systems.\

Kamaelia was designed originally to make maintenance of highly
concurrent network systems simpler, but has general application in a
wider variety of problem domains, including desktop applications, web
backend systems (eg video transcode & SMS services), through to tools
for teaching a child to read and write.\

More Information
----------------

The rest of this website obviously contains more information, and based
on lots of feedback, it does need work, but please [do tell
us](http://groups.google.com/group/kamaelia) how you think it needs
work.\
\
Also, a number of presentations have been made in the past. You can find
these [Kamaelia presentations on
slideshare](http://www.slideshare.net/kamaelian/presentations).\

**Notes**
---------

The notes are available in 3 forms:

One is [PDF suitable for printing on A4
paper](http://www.kamaelia.org/Europython09/A4KamaeliaEuroPython09.FINAL.pdf).

The other 2 ways are via lulu.com, which is a paid for print on demand
service.\

-   One is as [a PDF download from
    lulu.com](http://www.lulu.com/content/paperback-book/kamaelia-pragmatic-concurrency/7302222http://www.lulu.com/content/paperback-book/kamaelia-pragmatic-concurrency/7302222) -
    this is set to a cost of zero, but **isn\'t** A4 paper. If you
    prefer screen reading rather than printing, this is probably the
    nicest one for that.\

The other is as [a printed book from
lulu.com](http://www.lulu.com/content/paperback-book/kamaelia-pragmatic-concurrency/7302222http://www.lulu.com/content/paperback-book/kamaelia-pragmatic-concurrency/7302222)
- this is basically at production cost (£1.89), meaning it\'s cheap, but
beware of two points:

-   Postage from lulu.com can sting - but they appear to charge a flat
    fee whether it\'s 1 copy or 50 copies. (hence why I used them\...)
-   Currently I\'m going through it for typoes!
-   I do also still have some spares of the paper copies\

The slides used in the tutorial are available on
[slideshare](http://www.slideshare.net/kamaelian/kamaelia-europython-tutorial).
As you might expect, different media have different benefits, and so
each way of explaining things covers the same things in slightly
different ways, but following a common theme.

Videos will go up on blip.tv, and are currently being transcoded.

Two relevant downloads are also available:

-   [Kamaelia
    0.9.8.0](http://www.kamaelia.org/release/MonthlyReleases/Kamaelia-0.9.8.0.tar.gz) -
    is the latest monthly release. These were started just before the
    conference, and we used 0.9.6.0 there. 0.9.8.0 also includes the
    changes/apps inside the Europython09 release. A number of minor
    issues with the 0.9.6.0 release have been resolved in this release,
    along with a fair number of merges of kamaelia based apps. (enable
    reuse of applications as well as components)\
    \
-   The [Europython
    \'09](http://www.kamaelia.org/release/Kamaelia-Europython09-1.0.0.tar.gz)
    specific release - this packages up all the example programs and
    scripts used in the tutorial.

\
