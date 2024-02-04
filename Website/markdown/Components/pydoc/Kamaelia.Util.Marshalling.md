---
pagename: Components/pydoc/Kamaelia.Util.Marshalling
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling.html){.reference}
============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [DeMarshaller](/Components/pydoc/Kamaelia.Util.Marshalling.DeMarshaller.html){.reference}**
-   **component
    [Marshaller](/Components/pydoc/Kamaelia.Util.Marshalling.Marshaller.html){.reference}**
:::

-   [Simple Marshalling/demarshalling framework](#225){.reference}
    -   [Example usage](#226){.reference}
    -   [How does it work?](#227){.reference}
    -   [Post script](#228){.reference}
:::

::: {.section}
Simple Marshalling/demarshalling framework {#225}
==========================================

A pair of components for marshalling and demarshalling data
respectively. You supply a class containing methods to marshall and
demarshall the data in the way you want.

The idea is that you would place this between your logic and a network
socket to transform the data to and from a form suitable for transport.

::: {.section}
[Example usage]{#example-usage} {#226}
-------------------------------

Marshalling and demarshalling a stream of integers:

``` {.literal-block}
class SerialiseInt:

    def marshall(int):
        return str(int)
    marshall = staticmethod(marshall)

    def demarshall(string):
        return int(string)
    demarshall = staticmethod(demarshall)

Pipeline( producer(...),
          Marshaller(SerialiseInt),
          sender(...)
        ).activate()

Pipeline( receiver(...),
          DeMarshaller(SerialiseInt),
          consumer(...)
        ).activate()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#227}
--------------------------------------

When instantiating the Marshaller or DeMarshaller components, you
provide an object (eg. class) containing these static methods:

-   marshall(item) - returns the item serialised for transmission
-   demarshall(item) - returns the original item, deserialised

Marshaller requires only the marshall(\...) static method, and
DeMarshaller requires only demarshall(\...).

Why static methods? Because marshalling/demarshalling is a stateless
activity. This distinguishes marshalling activity from other protocols
and other processes that can be implemented with a similar style of
framework.

For simplicity this component expects to be given an entire object to
marshall or demarshall. This requires the user to deal with the framing
and deframing of objects separately.

Any data sent to the Marshaller or DeMarshaller components\' \"inbox\"
inbox is passed to the marshall(\...) or demarshall(\...) method
respectively of the class you supplied. The result is immediately sent
on out of the components\' \"outbox\" outbox.

If a producerFinished or shutdownMicroprocess message is received on the
components\' \"control\" inbox, it is sent on out of the \"signal\"
outbox. The component will then immediately terminate.
:::

::: {.section}
[Post script]{#post-script} {#228}
---------------------------

The initial data format this is designed to work with is the MimeDict
object.

It is expected that there will be a more complex marshaller that
supports receiving that is capable of receiving objects segmented over
multiple messages.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling.html){.reference}.[DeMarshaller](/Components/pydoc/Kamaelia.Util.Marshalling.DeMarshaller.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class DeMarshaller([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-DeMarshaller}
----------------------------------------------------------------------------------------------------

DeMarshaller(klass) -\> new DeMarshaller component.

A component for demarshalling data (deserialising it from a string).

Keyword arguments: - klass \-- a class with static method:
demarshall(data) that returns the data, demarshalled.

::: {.section}
### [Inboxes]{#symbol-DeMarshaller.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : data to be demarshalled
:::

::: {.section}
### [Outboxes]{#symbol-DeMarshaller.Outboxes}

-   **outbox** : demarshalled data
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self, klass)]{#symbol-DeMarshaller.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-DeMarshaller.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling.html){.reference}.[Marshaller](/Components/pydoc/Kamaelia.Util.Marshalling.Marshaller.html){.reference}
==================================================================================================================================================================================================================================================================================

::: {.section}
class Marshaller([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Marshaller}
--------------------------------------------------------------------------------------------------

Marshaller(klass) -\> new Marshaller component.

A component for marshalling data (serialising it to a string).

Keyword arguments:

-   klass \-- a class with static method: marshall(data) that returns
    the data, marshalled.

::: {.section}
### [Inboxes]{#symbol-Marshaller.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : data to be marshalled
:::

::: {.section}
### [Outboxes]{#symbol-Marshaller.Outboxes}

-   **outbox** : marshalled data
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self, klass)]{#symbol-Marshaller.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Marshaller.main}

Main loop.
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
