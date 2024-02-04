---
pagename: Components/pydoc/Kamaelia.Internet.Multicast_receiver
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver.html){.reference}
=======================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver.Multicast_receiver.html){.reference}**
:::

-   [Simple multicast receiver](#101){.reference}
    -   [Example Usage](#102){.reference}
    -   [More detail](#103){.reference}
:::

::: {.section}
Simple multicast receiver {#101}
=========================

A simple component for receiving packets in the specified multicast
group.

Remember that multicast is an unreliable connection - packets may be
lost, duplicated or reordered.

::: {.section}
[Example Usage]{#example-usage} {#102}
-------------------------------

Receiving multicast packets from group address 1.2.3.4 port 1000 and
displaying them on the console:

``` {.literal-block}
Pipeline( Multicast_receiver("1.2.3.4", 1000),
          ConsoleEchoer()
        ).activate()
```

The data emitted by Multicast\_receiver (and displayed by ConsoleEchoer)
is of the form (source\_address, data).
:::

::: {.section}
[More detail]{#more-detail} {#103}
---------------------------

Data received from the multicast group is emitted as a tuple:
(source\_addr, data) where data is a string of the received data.

This component ignores anything received on its \"control\" inbox. It is
not yet possible to ask it to shut down. It does not terminate.

Multicast groups do not \'shut down\', so this component never emits any
signals on its \"signal\" outbox.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Internet](/Components/pydoc/Kamaelia.Internet.html){.reference}.[Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver.html){.reference}.[Multicast\_receiver](/Components/pydoc/Kamaelia.Internet.Multicast_receiver.Multicast_receiver.html){.reference}
=========================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Multicast\_receiver([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Multicast_receiver}
-----------------------------------------------------------------------------------------------------------

Multicast\_receiver(address, port) -\> component that receives multicast
traffic.

Creates a component that receives multicast packets in the given
multicast group and sends it out of its \"outbox\" outbox.

Keyword arguments:

-   address \-- address of multicast group (string)
-   port \-- port number

::: {.section}
### [Inboxes]{#symbol-Multicast_receiver.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-Multicast_receiver.Outboxes}

-   **outbox** : Emits (src\_addr, data\_received)
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
#### [\_\_init\_\_(self, address, port)]{#symbol-Multicast_receiver.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Multicast_receiver.main}

Main loop
:::
:::

::: {.section}
:::
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
