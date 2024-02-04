---
pagename: Components/pydoc/Kamaelia.Chassis.Carousel.Carousel
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}.[Carousel](/Components/pydoc/Kamaelia.Chassis.Carousel.Carousel.html){.reference}
=================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Chassis.Carousel.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Carousel([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Carousel}
------------------------------------------------------------------------------------------------

Carousel(componentFactory,\[make1stRequest\]) -\> new Carousel component

Create a Carousel component that makes child components one at a time
(in carousel fashion) using the supplied factory function.

Keyword arguments:

-   componentFactory \-- function that takes a single argument and
    returns a component
-   make1stRequest \-- if True, Carousel will send an initial \"NEXT\"
    request. (default=False)

::: {.section}
### [Inboxes]{#symbol-Carousel.Inboxes}

-   **control** :
-   **inbox** : child\'s inbox
-   **next** : requests to replace child
:::

::: {.section}
### [Outboxes]{#symbol-Carousel.Outboxes}

-   **outbox** : child\'s outbox
-   **signal** :
-   **\_signal** : internal use: for sending \'shutdownMicroprocess\' to
    child
-   **requestNext** : for requesting new child component
:::

::: {.section}
### Methods defined here

::: {.container}
::: {.boxright}
**Warning!**

You should be using the inbox/outbox interface, not these methods
(except construction). This documentation is designed as a roadmap as to
their functionalilty for maintainers and new component developers.
:::
:::

::: {.section}
#### [\_\_init\_\_(self, componentFactory\[, make1stRequest\])]{#symbol-Carousel.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkControl(self)]{#symbol-Carousel.checkControl}
:::

::: {.section}
#### [handleChildTerminations(self)]{#symbol-Carousel.handleChildTerminations}

Unplugs any children that have terminated
:::

::: {.section}
#### [instantiateNewChild(self, args)]{#symbol-Carousel.instantiateNewChild}
:::

::: {.section}
#### [main(self)]{#symbol-Carousel.main}
:::

::: {.section}
#### [requestNext(self)]{#symbol-Carousel.requestNext}

Sends \'next\' out the \'requestNext\' outbox
:::

::: {.section}
#### [shutdownChild(self, shutdownMsg)]{#symbol-Carousel.shutdownChild}
:::
:::

::: {.section}
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
