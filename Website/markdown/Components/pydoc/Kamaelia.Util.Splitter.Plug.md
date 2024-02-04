---
pagename: Components/pydoc/Kamaelia.Util.Splitter.Plug
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}.[Plug](/Components/pydoc/Kamaelia.Util.Splitter.Plug.html){.reference}
=============================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Plug([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Plug}
--------------------------------------------------------------------------------------------

Plug(splitter,component) -\> new Plug component.

A component that \'plugs\' the specified component into the specified
splitter as a destination for data.

Keyword arguments:

-   splitter \-- splitter component to plug into (any component that
    accepts addsink(\...) and removesink(\...) messages on a
    \'configuration\' inbox
-   component \-- component to receive data from the splitter

::: {.section}
### [Inboxes]{#symbol-Plug.Inboxes}

-   **control** : Incoming control data for child component, and
    shutdown signalling
-   **inbox** : Incoming data for child component
:::

::: {.section}
### [Outboxes]{#symbol-Plug.Outboxes}

-   **outbox** : Outgoing data from child component
-   **signal** : Outgoing control data from child component, and
    shutdown signalling
-   **splitter\_config** : Used to communicate with the target splitter
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
#### [\_\_init\_\_(self, splitter, component)]{#symbol-Plug.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Plug.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Plug.main}

Main loop.
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
