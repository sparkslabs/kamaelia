---
pagename: Components/pydoc/Kamaelia.Util.Backplane
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}
========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Backplane](/Components/pydoc/Kamaelia.Util.Backplane.Backplane.html){.reference}**
-   **component
    [PublishTo](/Components/pydoc/Kamaelia.Util.Backplane.PublishTo.html){.reference}**
-   **component
    [SubscribeTo](/Components/pydoc/Kamaelia.Util.Backplane.SubscribeTo.html){.reference}**
:::

-   [Publishing and Subscribing with Backplanes](#177){.reference}
    -   [Example usage](#178){.reference}
    -   [More detail](#179){.reference}
    -   [Implementation details](#180){.reference}
:::

::: {.section}
Publishing and Subscribing with Backplanes {#177}
==========================================

Backplanes provide a way to \'publish\' data under a name, enabling
other parts of the system to \'subscribe\' to it on the fly, without
having to know about the actual component(s) the data is coming from.

It is a quick and easy way to distribute or share data. Think of them
like backplane circuit boards - where other circuit boards can plug in
to send or receive any signals they need.

::: {.section}
[Example usage]{#example-usage} {#178}
-------------------------------

A system where several producers publish data, for consumers to pick up:

``` {.literal-block}
Pipeline( Producer1(),
          PublishTo("DATA")
        ).activate()

Pipeline( Producer2(),
          PublishTo("DATA")
        ).activate()

Pipeline( SubscribeTo("DATA"),
          Consumer1(),
        ).activate()

Pipeline( SubscribeTo("DATA"),
          Consumer2(),
        ).activate()

Backplane("DATA").run()
```

A server where multiple clients can connect and they all get sent the
same data at the same time:

``` {.literal-block}
Pipeline( Producer(),
          PublishTo("DATA")
        ).activate()

SimpleServer(protocol=SubscribeTo("DATA"), port=1500).activate()

Backplane("DATA").run()
```
:::

::: {.section}
[More detail]{#more-detail} {#179}
---------------------------

The Backplane component collects data from publishers and sends it out
to subscribers.

You can have as many backplanes as you like in a running system -
provided they all register under different names.

A backplane can have multiple subscribers and multiple publishers.
Publishers and subscribers can be created and destroyed on the fly.

To shut down a PublishTo() component, send a producerFinished() or
shutdownMicroprocess() message to its \"control\" inbox. This does *not*
propagate and therefore does *not* cause the Backplane or any
subscribers to terminate.

To shut down a SubscribeTo() component, send a producerFinished() or
shutdownMicroprocess() message to its \"control\" inbox. It will then
immediately forward the mesage on out of its \"signal\" outbox and
terminate.

To shut down the Backplane itself, send a producerFinished() or
shutdownMicroprocess() message to its \"control\" inbox. It will then
immediately terminate and also propagate this message onto any
subscribers (SubscribeTo components), causing them to also terminate.
:::

::: {.section}
[Implementation details]{#implementation-details} {#180}
-------------------------------------------------

Backplane is actually based on a
[Kamaelia.Util.Splitter.PlugSplitter](/Components/pydoc/Kamaelia.Util.Splitter.PlugSplitter.html){.reference}
component, and the SubscribeTo component is a wrapper around a
[Kamaelia.Util.Splitter.Plug](/Components/pydoc/Kamaelia.Util.Splitter.Plug.html){.reference}.

The Backplane registers itself with the coordinating assistant tracker.

-   Its \"inbox\" inbox is registered under the name
    \"Backplane\_I\_\<name\>\"
-   Its \"configuration\" inbox is registered under the name
    \"Backplane\_O\_\<name\>\"

PublishTo components look up the \"Backplane\_I\_\<name\>\" service and
simply forward data sent to their \"inbox\" inboxes direct to the
\"inbox\" inbox of the PlugSplitter - causing it to be distributed to
all subscribers.

SubscribeTo components look up the \"Backplane\_O\_\<name\>\" service
and request to have their \"inbox\" and \"control\" inboxes connected to
the PlugSplitter. SubscribeTo then forwards on any messages it receives
out of its \"outbox\" and \"signal\" outboxes respectively.

The PlugSplitter component\'s \"control\" inbox and \"signal\" outbox
are not advertised as services. To shut down a Backplane you must
therefore send a shutdownMicroprocess() or producerFinished() message
directly to its \"control\" inbox. When this happens, the shutdown
message will be forwarded on to all subscribers - causing SubscribeTo
components to also shut down.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.Backplane.html){.reference}
==========================================================================================================================================================================================================================================================================

::: {.section}
class Backplane([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Backplane}
-------------------------------------------------------------------------------------------------

Backplane(name) -\> new Backplane component.

A named backplane to which data can be published for subscribers to pick
up.

-   Use PublishTo components to publish data to a Backplane.
-   Use SubscribeTo components to receive data published to a Backplane.

Keyword arguments:

-   name \-- The name for the backplane. publishers and subscribers
    connect to this by using the same name.

::: {.section}
### [Inboxes]{#symbol-Backplane.Inboxes}

-   **control** : Shutdown signalling (shuts down the backplane and all
    subscribers
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-Backplane.Outboxes}

-   **outbox** : NOT USED
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
#### [\_\_init\_\_(self, name)]{#symbol-Backplane.__init__}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-Backplane.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-Backplane.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}.[PublishTo](/Components/pydoc/Kamaelia.Util.Backplane.PublishTo.html){.reference}
==========================================================================================================================================================================================================================================================================

::: {.section}
class PublishTo([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PublishTo}
-------------------------------------------------------------------------------------------------

PublishTo(destination) -\> new PublishTo component

Publishes data to a named Backplane. Any data sent to the \"inbox\"
inbox is sent to all (any) subscribers to the same named Backplane.

Keyword arguments:

-   destination \-- the name of the Backplane to publish data to

::: {.section}
### [Inboxes]{#symbol-PublishTo.Inboxes}

-   **control** : Shutdown signalling (doesn\'t shutdown the Backplane)
-   **inbox** : Send to here data to be published to the backplane
:::

::: {.section}
### [Outboxes]{#symbol-PublishTo.Outboxes}

-   **outbox** : NOT USED
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
#### [\_\_init\_\_(self, destination)]{#symbol-PublishTo.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-PublishTo.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Backplane](/Components/pydoc/Kamaelia.Util.Backplane.html){.reference}.[SubscribeTo](/Components/pydoc/Kamaelia.Util.Backplane.SubscribeTo.html){.reference}
==============================================================================================================================================================================================================================================================================

::: {.section}
class SubscribeTo([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SubscribeTo}
---------------------------------------------------------------------------------------------------

SubscribeTo(source) -\> new SubscribeTo component

Subscribes to a named Backplane. Receives any data published to that
backplane and sends it on out of its \"outbox\" outbox.

Keyword arguments:

-   source \-- the name of the Backplane to subscribe to for data

::: {.section}
### [Inboxes]{#symbol-SubscribeTo.Inboxes}

-   **control** : Shutdown signalling (doesn\'t shutdown the Backplane)
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-SubscribeTo.Outboxes}

-   **outbox** : Data received from the backplane (that was published to
    it)
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
#### [\_\_init\_\_(self, source)]{#symbol-SubscribeTo.__init__}
:::

::: {.section}
#### [childrenDone(self)]{#symbol-SubscribeTo.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-SubscribeTo.main}

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
