---
pagename: Components/pydoc/Kamaelia.Chassis.Prefab
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Prefab](/Components/pydoc/Kamaelia.Chassis.Prefab.html){.reference}
===========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [JoinChooserToCarousel](/Components/pydoc/Kamaelia.Chassis.Prefab.JoinChooserToCarousel.html){.reference}**
:::

-   [Pre-fabrication function chassis](#259){.reference}
    -   [JoinChooserToCarousel](#260){.reference}
        -   [Example Usage](#261){.reference}
        -   [More detail](#262){.reference}
        -   [To do](#263){.reference}
:::

::: {.section}
Pre-fabrication function chassis {#259}
================================

This is a collection of functions that link up components standardised
ways.

They take a collection of components as arguments, and then wire them up
in a particular fashion. These components are children inside the
prefab.

::: {.section}
[JoinChooserToCarousel]{#joinchoosertocarousel} {#260}
-----------------------------------------------

Automated \"what arguments should I use for my next reusable
component?\"

Take a Carousel that makes components on request from a set of
arguments. Take a Chooser that responds to request for the \'next\' set
of arguments.

This pre-fab is a component that wires them together. When the Carousel
requests the arguments for the next component, the Chooser can respond
with them.

For example, you could wire up a playlist to something reusable that
reads files at a given rate. Alternatively, it could be a list of videos
or pictures passed to a reusable media viewer. It could even be a list
of shell commands passed to a reusable shell/system caller.

::: {.section}
### [Example Usage]{#example-usage} {#261}

Reading from a playlist of files:

``` {.literal-block}
def makeFileReader(filename):
    return ReadFileAdapter(filename = filename, ...other args... )

reusableFileReader = Carousel componentFactory = makeFileReader)
playlist = Chooser(["file1","file2" ... ])

playlistreader = JoinChooserToCarousel(playlist, reusableFileReader)
playlistreader.activate()
```
:::

::: {.section}
### [More detail]{#more-detail} {#262}

Any component can be used that has the expected inboxes and outboxes,
and which behaves in a relevant manner.

Chooser must have inboxes \"inbox\" and \"control\" and outboxes
\"outbox\" and \"signal\".

Carousel must have inboxes \"inbox\", \"control\" and \"next\" and
outboxes \"outbox\", \"signal\" and \"requestNext\".

The Chooser and Carousel are encapsulated within this prefab component
as children.

\"inbox\", \"outbox\" and \"signal\" of the Carousel are \"inbox\",
\"outbox\" and \"signal\" of this prefab.

Messages sent to this prefab\'s \"control\" inbox go to the Chooser,
which should then pass it onto the Carousel, allowing shutdown.
:::

::: {.section}
### [To do]{#to-do} {#263}

This prefab needs a better name - it currently describes its design, not
what its for.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Prefab](/Components/pydoc/Kamaelia.Chassis.Prefab.html){.reference}.[JoinChooserToCarousel](/Components/pydoc/Kamaelia.Chassis.Prefab.JoinChooserToCarousel.html){.reference}
=====================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: JoinChooserToCarousel {#symbol-JoinChooserToCarousel}
-----------------------------

JoinChooserToCarousel(chooser, carousel) -\> component containing both
wired up

Wires up a Chooser and a Carousel, so when the carousel requests the
next item, the Chooser supplies it.

Keyword arguments:

-   chooser \-- A Chooser component, or one with similar interfaces
-   carousel \-- A Carousel component, or one with similar interfaces
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
