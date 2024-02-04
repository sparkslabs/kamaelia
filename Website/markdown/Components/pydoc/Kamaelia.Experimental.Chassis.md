---
pagename: Components/pydoc/Kamaelia.Experimental.Chassis
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}
============================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [Carousel](/Components/pydoc/Kamaelia.Experimental.Chassis.Carousel.html){.reference}**
-   **prefab
    [Graphline](/Components/pydoc/Kamaelia.Experimental.Chassis.Graphline.html){.reference}**
-   **prefab
    [InboxControlledCarousel](/Components/pydoc/Kamaelia.Experimental.Chassis.InboxControlledCarousel.html){.reference}**
-   **prefab
    [Pipeline](/Components/pydoc/Kamaelia.Experimental.Chassis.Pipeline.html){.reference}**
:::

-   [Inbox size limiting Pipelines, Graphlines and
    Carousels](#563){.reference}
    -   [Example Usages](#564){.reference}
    -   [More details](#565){.reference}
:::

::: {.section}
Inbox size limiting Pipelines, Graphlines and Carousels {#563}
=======================================================

Extended versions of
[Kamaelia.Chassis.Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference},
[Kamaelia.Chassis.Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}
and
[Kamaelia.Chassis.Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}
that add the ability to specify size limits for inboxes of components.

::: {.section}
[Example Usages]{#example-usages} {#564}
---------------------------------

A pipeline with inbox size limits on 3 of the components\' \"inbox\"
inboxes:

``` {.literal-block}
Pipeline( 5,  MyComponent(),      # 'inbox' inbox limited to 5 items
          2,  MyComponent(),      # 'inbox' inbox limited to 2 items
              MyComponent(),      # 'inbox' inbox unlimited
          28, MyComponent()       # 'inbox' inbox limited to 28 items
        )
```

A graphline where component \'A\' has a size limit of 5 on its \"inbox\"
inbox; and component \'C\' has a size limit of 17 on its \"control\"
inbox:

``` {.literal-block}
Graphline( A = MyComponent(),
           B = MyComponent(),
           C = MyComponent(),
           linkages = { ... },
           boxsizes = {
               ("A","inbox") : 5,
               ("C","control") : 17
           }
         )
```

A Carousel, where the child component will have a size limit of 5 on its
\"inbox\" inbox:

``` {.literal-block}
Carousel( MyComponent(), boxsize=5 )
```

Decoding a Dirac video file and saving each frame in a separate file:

``` {.literal-block}
Pipeline(
    RateControlledFileReader("video.dirac", ... ),
    DiracDecoder(),
    TagWithSequenceNumber(),
    InboxControlledCarousel(
        lambda (seqnum, frame) :
            Pipeline( OneShot(frame),
                      FrameToYUV4MPEG(),
                      SimpleFileWriter("%08d.yuv4mpeg" % seqnum),
                    )
        ),
    )
```
:::

::: {.section}
[More details]{#more-details} {#565}
-----------------------------

The behaviour of these three components/prefabs is identical to their
original counterparts
([Kamaelia.Chassis.Pipeline](/Components/pydoc/Kamaelia.Chassis.Pipeline.html){.reference},
[Kamaelia.Chassis.Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.html){.reference}
and
[Kamaelia.Chassis.Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}).

*For Pipelines*, if you want to size limit the \"inbox\" inbox of a
particular component in the pipeline, then put the size limit as an
integer before it. Any component without an integer before it is left
with the default of an unlimited \"inbox\" inbox.

The behaviour therefore reduces back to be identical to that of the
normal Pipeline component.

*For Graphlines*, if you want to size limit particular inboxes, supply
the \"boxsizes\" argument with a dictionary that maps (componentName,
boxName) keys to the size limit for that box.

Again, if you don\'t specify a \"boxsizes\" argument, then behaviour is
identical to that of the normal Graphline component.

*For Carousels*, if you want a size limit on the \"inbox\" inbox of the
child component (created by the factory function), then specify it using
the \"boxsizes\" argument.

Again, if you don\'t specify a \"boxsizes\" argument, then behaviour is
identical to that of the normal Carousel component.

*InboxControlledCarousel* behaves identically to Carousel.

The \"inbox\" inbox is equivalent to the \"next\" inbox of Carousel. The
\"data\_inbox\" inbox is equivalent to the \"inbox\" inbox of Carousel.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Experimental.Chassis.Carousel.html){.reference}
==================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: Carousel {#symbol-Carousel}
----------------

Carousel(componentFactory\[,make1stRequest\]\[,boxSize\]) -\> new
Carousel component

Create a Carousel component that makes child components one at a time
(in carousel fashion) using the supplied factory function.

Keyword arguments:

-   componentFactory \-- function that takes a single argument and
    returns a component
-   make1stRequest \-- if True, Carousel will send an initial \"NEXT\"
    request. (default=False)
-   boxsize \-- size limit for \"inbox\" inbox of the created child
    component
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[Graphline](/Components/pydoc/Kamaelia.Experimental.Chassis.Graphline.html){.reference}
====================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: Graphline {#symbol-Graphline}
-----------------

Graphline(\[linkages\]\[,boxsizes\],\*\*components) -\> new Graphline
component

Encapsulates the specified set of components and wires them up with the
specified linkages.

Keyword arguments:

-   linkages \-- dictionary mapping (\"componentname\",\"boxname\") to
    (\"componentname\",\"boxname\")
-   boxsizes \-- dictionary mapping (\"componentname\",\"boxname\") to
    size limit for inbox
-   components \-- dictionary mapping names to component instances
    (default is nothing)
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[InboxControlledCarousel](/Components/pydoc/Kamaelia.Experimental.Chassis.InboxControlledCarousel.html){.reference}
================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: InboxControlledCarousel {#symbol-InboxControlledCarousel}
-------------------------------

InboxControlledCarousel(componentFactory\[,make1stRequest\]\[,boxSize\])
-\> new Carousel component

Create an InboxControlledCarousel component that makes child components
one at a time (in carousel fashion) using the supplied factory function.

Keyword arguments:

-   componentFactory \-- function that takes a single argument and
    returns a component
-   make1stRequest \-- if True, Carousel will send an initial \"NEXT\"
    request. (default=False)
-   boxsize \-- size limit for \"inbox\" inbox of the created child
    component
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Experimental](/Components/pydoc/Kamaelia.Experimental.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Experimental.Chassis.html){.reference}.[Pipeline](/Components/pydoc/Kamaelia.Experimental.Chassis.Pipeline.html){.reference}
==================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: Pipeline {#symbol-Pipeline}
----------------

Pipeline(\*components) -\> new Pipeline component.

Encapsulates the specified set of components and wires them up in a
chain (a Pipeline) in the order you provided them.

Keyword arguments:

-   components \-- the components you want, in the order you want them
    wired up. Any Integers set the \"inbox\" inbox size limit for the
    component that follows them.
:::
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
