---
pagename: Cookbook/PipelinesAndGraphlinesDiscuss
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Cookbook/PipelinesAndGraphlinesDiscuss
======================================

I\'ve been wanted to write something like this for ages, so it\'s cool
to see this :-)\

I have some concerns about this page, which revolve around this idea
from the [Kamaelia Principles Page](../../../Developers/Principles):\

-   Descriptions of things optimised for the 80% of programmers are
    preferable to those with only the top 20% will understand. If this
    seems \"dumbing down\", consider that it is often harder to describe
    something complex simply, than to describe something simple in a
    complex fashion.\

As a result, in the spirit of improving this page, some hopefully
constructive criticism:\

This page is really 2 pages (perhaps even part of a sequence/progression
like MiniAxon!) - one about pipelines and one about graphlines - it\'s
trying to do too much. Creating 2 pages base on this (and linked from
this ala the MiniAxon tutorial) would be really cool :-)

Repace PureTransformer with something real or simply drop it ( *lambda*
in a tutorial? :-)

-   Replaced with multicast example\

If all inboxes & outboxes are linked, in *initial* diagrams on the page,
perhaps use the sort of diagram the Visual Pipe Builder used to show (ie
single line :-) )\

Consider building the diagrams with **Compose** and snapshotting those
instead :-)

-   Alternatively - if a box isn\'t linked, do you need to show it on
    the diagram?
-   If all the boxes are linked in the same way, can\'t you just show
    one arrow?

I prefer the approach taken with the Graphlines example over that of the
pipeline - ie taking a real example which is in the Examples directory
and using that to talk about. More specifically, the Graphline example
is an example that has general usefulness, whereas I\'m unconvinced of
the *general* usefulness of the Pipeline example. (Sure **I\'d** find it
useful, maybe, but\... :-)

Final point: don\'t start off saying \"these are chassis\". It\'s very
useful to finish on that point, but starting on it confuses things.
Consider:

-   This is how you could link together some components
-   But this is how you can do it with a Pipeline

And:

-   This is how you can link together lots of components
-   But isn\'t this Graphline easier?\

Followed by:

And hey, actually, this is a general principle - you can have components
you give components to and they get wired up

Hey that\'s just like a chassis with a car isn\'t that cool?

But hey look, you do that with SimpleServer - a tutorial for another
time

And look, that\'s what the Carousel is - and that\'s another tutorial
for another time

-   I still find Carousel breaks my head\...

Let me see if that Kathy Sierra page is around still\... [It is it\'s
here](http://headrush.typepad.com/creating_passionate_users/2005/01/keeping_users_e.html)
- the part I\'m thinking of is where she starts talking about
superpowers. (The miniaxon tutorial kinda does this without thinking\...
and then stops\...)

Oh, and consider also:

-   Fun descriptions, ideas and code tend to win arguments :-)
-   ;-)\

All that said, ***something*** is *(almost :)* always more useful than
nothing, so many thanks who-ever wrote the first draft - rewriting
(docs) almost always easier than writing :-) (The (hopefully
constructive) criticism above is **certainly** easier to write than the
first draft)\
\
Oh, and as I say above, I\'ve been wanted to write something like this
for ages, but it\'s cool to see this :-)\
\
\-- Michael Sparks, 17 December 2006\

------------------------------------------------------------------------

Thanks for the feedback.\
\

-   Pages separated as suggested.
-   \"These are chassis\" wording dropped for the moment
-   Pipeline example switched for a \'real\' one (multicast sender)\

Things I\'ve not done (yet):\

-   My concern with a compose/visualiser style diagram would be that it
    would not show the encapsulation. I\'m thinking that it may be as
    helpful to show what the graphline or pipeline isn\'t doing as well
    as what it is - if pipeline/graphline is wiring up some boxes but
    not others, then perhaps its important to show that?
-   I\'m thinking of perhaps doing a simpler initial diagram for both
    pipeline and graphline to give a rough idea of the flow, then
    following it with the existing diagrams to be more explicit.\
-   Carousel page - in the pipeline (sic) \... though its a concern if
    you find it hard to get your head round them. If I\'m the only
    person really able to make use of them, then perhaps they need a
    rethink.\

\
I\'ll do some more editing tomorrow :)\
\
\-- Matt Hammond, 17 Dec 2006\
\
The comment about a page for Carousel was a bit of a side joke - I
don\'t have a problem with balancing power vs complexity - it\'s just
that the latter is a lot harder to explain. I think it really comes
under the concept of a higher order component (as chassises/ chasses?
(sp?)) are, and hence that\'s probably why it\'s more awkward. (I really
think you\'d need to have some sort of animation to make it clear to be
honest!)\
\
Regarding the encapsulation, true - that can be handled by some light
editting after perhaps. If not, I can always put a [santa hat on it
too](/Home) :).\
Something worth bearing in mind - perhaps:\

-   Initially pipelines are a nice shortcut for, well, building
    pipelines.
-   Initially graphlines are a nice shortcut for the other useful
    shapes.
-   It\'s only later that it becomes clear that pipelines are useful
    abstractions in and of themselves (cf how you use them like crazy in
    the Whiteboard)
-   Similarly for graphlines.

Each of these aspects are all independent topics - at least in my mind.
Each step gives you an extra level of power. For example, consider the
following plan for developing Compose (which I accidentally wiped a
while back):\

-   Introspect a system
-   Create a pipeline
-   Create a graphline
-   Be able to edit set up code before a pipeline/graphline
-   Be able to take the setup code & pipeline/graphline body and add
    that as a component to the repository.
-   Be able to edit the body of the component instead of use a
    pipeline/graphline & insert that into the repository.

By their very nature, a description of Pipeline/Graphline ***could***
follow a similar path (doesn\'t have to), but it does allude to the
\"just a container\" vs \"not just a container\" nature.\
\
As for the final comment on piplelines, bear in mind that just because
they\'re (at present) only really ***used*** by you (as far as I can
tell), that doesn\'t mean that they need a rethink :). (I can use it
BTW, it\'s just that I often find a different method instead, at
present).\
\
Also, there\'s no rush :)\
\
\-- Michael Sparks, 17 December 2006\
\

------------------------------------------------------------------------

I\'ve stuck with the current diagram style for the moment, but added
extra, simplified, diagrams hopefully better demonstrate the pipeline
concept.\
\
I\'ve also fleshed out the explanations a little starting more from the
perspective of simply wanting to chain the components together. The
greater detail level around using a pipeline as a container, and the
detail of how the wiring is done as been separated a little by grouping
it under more distinct headings - hopefully giving a natural break point
for those who aren\'t interested in reading that far.\
\
Your \"final comment\" was wrt. Carousels? :-)\
\
\-- Matt Hammond, 18 December 2006\
\
