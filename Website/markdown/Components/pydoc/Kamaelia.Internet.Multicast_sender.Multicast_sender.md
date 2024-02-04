---
pagename: Components/pydoc/Kamaelia.Internet.Multicast_sender.Multicast_sender
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Multicast\_sender](/Components/pydoc/Kamaelia.Internet.Multicast_sender.html){.reference}.[Multicast\_sender](/Components/pydoc/Kamaelia.Internet.Multicast_sender.Multicast_sender.html){.reference}
===============================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Internet.Multicast_sender.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Multicast\_sender([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Multicast_sender}
---------------------------------------------------------------------------------------------------------

Multicast\_sender(local\_addr, local\_port, remote\_addr, remote\_port)
-\> component that sends to a multicast group.

Creates a component that sends data received on its \"inbox\" inbox to
the specified multicast group.

Keyword arguments:

-   local\_addr \-- local address (interface) to send from (string)
-   local\_port \-- local port number
-   remote\_addr \-- address of multicast group to send to (string)
-   remote\_port \-- port number

::: {.section}
### [Inboxes]{#symbol-Multicast_sender.Inboxes}

-   **control** : NOT USED
-   **inbox** : Data to be sent to the multicast group
:::

::: {.section}
### [Outboxes]{#symbol-Multicast_sender.Outboxes}

-   **outbox** : NOT USED
-   **signal** : NOT USED
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
#### [\_\_init\_\_(self, local\_addr, local\_port, remote\_addr, remote\_port)]{#symbol-Multicast_sender.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Multicast_sender.main}

Main loop
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
