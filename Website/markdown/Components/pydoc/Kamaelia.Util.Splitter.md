---
pagename: Components/pydoc/Kamaelia.Util.Splitter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}
======================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Plug](/Components/pydoc/Kamaelia.Util.Splitter.Plug.html){.reference}**
-   **component
    [PlugSplitter](/Components/pydoc/Kamaelia.Util.Splitter.PlugSplitter.html){.reference}**
-   **component
    [Splitter](/Components/pydoc/Kamaelia.Util.Splitter.Splitter.html){.reference}**
:::

-   [Simple Fanout of messages](#191){.reference}
    -   [Example Usage](#192){.reference}
    -   [How does it work?](#193){.reference}
-   [Pluggable Fanout of messages](#194){.reference}
    -   [Example Usage](#195){.reference}
    -   [How does it work?](#196){.reference}
-   [Plug for PlugSplitter](#197){.reference}
    -   [Example Usage](#198){.reference}
    -   [How does it work?](#199){.reference}
    -   [Thoughts](#200){.reference}
:::

::: {.section}
::: {.section}
[Simple Fanout of messages]{#simple-fanout-of-messages} {#191}
-------------------------------------------------------

A component that splits a data source, fanning it out to multiple
destinations.

::: {.section}
### [Example Usage]{#example-usage} {#192}

Component connecting to a Splitter:

``` {.literal-block}
class Consumer(Axon.Component.component):
    Outboxes = [ "outbox", "signal", "splitter_config" ]

    def main(self):
         self.send( addsink( self, "inbox", "control" ), "splitter_config")
         yield 1
         ... do stuff when data is received on "inbox" inbox

mysplitter = Splitter()
Pipeline( producer(), mysplitter ).activate()

myconsumer = Consumer().activate()
myconsumer.link( (myconsumer, "splitter_config"), ("mysplitter", "configuration") )
```
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#193}

Any data sent to the component\'s \"inbox\" inbox is sent out to
multiple destinations (but not to the \"outbox\" outbox).

Add a destination by sending an addsink(\...) message to the
\"configuration\" inbox of the component. Splitter will then wire up to
the \'sinkbox\' inbox specified in the message, and send it any data
sent to its \"inbox\" inbox.

NOTE: Splitter only does this for the \'sinkbox\' inbox, not for the
\'sinkcontrol\' inbox. If one is specified, it is ignored.

There is no limit on the number of \'sinks\' that can be connected to
the splitter. The same component can add itself as a sink multiple
times, provided different named inboxes are used each time.

NOTE: The data is not duplicated - the same item is sent to all
destinations. Care must therefore be taken if the data item is mutable.

If one or more destinations cause a noSpaceInBox exception, the data
item will be queued, and Splitter will attempt to resend it to the
destinations in question until successful. It will stop forwarding any
new incoming data until it has succeeded, thereby ensuring the order of
data is not altered.

Stop data being sent to a destination by sending a removesink(\...)
message to the \"configuration\" inbox of the Splitter component.
Splitter will then cease sending messages to the \'sinkbox\' inbox
specified in the message and will unwire from it.

Any messages sent to the \"control\" inbox are ignored. The \"outbox\"
and \"signal\" outboxes are not used.

This component does not terminate.
:::
:::

::: {.section}
[Pluggable Fanout of messages]{#pluggable-fanout-of-messages} {#194}
-------------------------------------------------------------

The PlugSplitter component splits a data source, fanning it out to
multiple destinations. The Plug component allows you to easily \'plug\'
a destination into the splitter.

::: {.section}
### [Example Usage]{#id1} {#195}

Two consumers receiving the same data from a single consumer. Producer
and consumers are encapsulated by PlugSplitter and Plug components
respectively:

``` {.literal-block}
mysplitter = PlugSplitter( producer() ).activate()

Plug(mysplitter, consumer() ).activate()
Plug(mysplitter, consumer() ).activate()
```

The same, but the producer and consumers are not encapsulated:

``` {.literal-block}
mysplitter = PlugSplitter()
Pipeline( producer, mysplitter ).activate()

Pipeline( Plug(mysplitter), consumer() ).activate()
Pipeline( Plug(mysplitter), consumer() ).activate()
```
:::

::: {.section}
### [How does it work?]{#id2} {#196}

Any data sent to the component\'s \"inbox\" and \"control\" inboxes is
sent out to multiple destinations. It is also sent onto the components
\"outbox\" and \"signal\" outboxes, respectively.

Alternatively, initialisation you can specify a \'source\' component. If
you do, then data to be sent out to multiple destinations is instead
received from that component\'s \"outbox\" and \"signal\" outboxes,
respectively. Any data sent to the \"inbox\" and \"control\" inboxes of
the PlugSplitter component will be forwarded to the \"inbox\" and
\"control\" inboxes of the \'source\' component, respectively.

This source component is encapsulated as a child within the PlugSplitter
component, and so must not be separately activated. Activating
PlugSplitter will also activate this child component.

Add a destination by making a Plug component, specifying the
PlugSplitter component to \'plug into\'. See documentation for the Plug
component for more information.

Alternatively, you can add and remove destinations manually:

-   Add a destination by sending an addsink(\...) message to the
    \"configuration\" inbox of the component.

    If a \'sinkbox\' inbox is specified in the message, then
    PlugSplitter will wire up to it and forward to it any
    \'inbox\'/\'outbox\' data. If a \'sinkcontrol\' inbox is specified,
    then Plugsplitter will wire up to it and forward to it any
    \'control\'/\'signal\' data.

-   Stop data being sent to a destination by sending a removesink(\...)
    message to the \"configuration\" inbox of the Splitter component.

    Splitter will then cease sending messages to the \'sinkbox\' inbox
    specified in the message and will unwire from it.

There is no limit on the number of \'sinks\' that can be connected to
the splitter. The same component can add itself as a sink multiple
times, provided different named inboxes are used each time.

NOTE: The data is not duplicated - the same item is sent to all
destinations. Care must therefore be taken if the data item is mutable.

If a shutdownMicroprocess or producerFinished message is received on the
\"control\" inbox and there is NO \'source\' child component, then the
message is forwarded onto all \'control\' destinations and the
\'signal\' outbox. The component then immediately terminates, unwiring
from all destinations.

If there is a child component then PlugSplitter will terminate when the
child component terminates, unwiring from all destinations.
:::
:::

::: {.section}
[Plug for PlugSplitter]{#plug-for-plugsplitter} {#197}
-----------------------------------------------

The Plug component \'plugs into\' a PlugSplitter as a destination to
which the source data is split.

::: {.section}
### [Example Usage]{#id3} {#198}

See PlugSplitter documentation.
:::

::: {.section}
### [How does it work?]{#id4} {#199}

Initialise the Plug component by specifying a PlugSplitter component to
connect to and the component that wants to receive the data from the
Plugsplitter.

The destination/sink component is encapsulated as a child component, and
is therefore activated by the Plug component when it is activated. Do
not activate it yourself.

The Plug component connects to the PlugSplitter component by wiring its
\"splitter\_config\" outbox to the \"configuration\" inbox of the
PlugSplitter component and sending it an addsink(\...) message. This
causes PlugSplitter to wire up to the Plug\'s \"inbox\" and \"control\"
inboxes.

The Plug\'s \"inbox\" and \"control\" inboxes are forwarded to the
\"inbox\" and \"control\" inboxes of the child component respectively.
The \"outbox\" and \"signal\" outboxes of the child component are
forwarded to the \"outbox\" and \"signal\" outboxes of the Plug
component respectively.

When the child component terminates, the Plug component sends a
removesink(\...) message to the PlugSplitter, causing PlugSplitter to
unwire from it. It then terminates.
:::

::: {.section}
### [Thoughts]{#thoughts} {#200}

PlugSplitter is probably more reliable than Splitter however it *feels*
too complex. However the actual \"Splitter\" class in this file is not
the preferable option.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}.[Plug](/Components/pydoc/Kamaelia.Util.Splitter.Plug.html){.reference}
=============================================================================================================================================================================================================================================================

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

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}.[PlugSplitter](/Components/pydoc/Kamaelia.Util.Splitter.PlugSplitter.html){.reference}
=============================================================================================================================================================================================================================================================================

::: {.section}
class PlugSplitter([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-PlugSplitter}
--------------------------------------------------------------------------------------------------------------------------------------------------------

PlugSplitter(\[sourceComponent\]) -\> new PlugSplitter component.

Splits incoming data out to multiple destinations. Send addsink(\...)
and removesink(\...) messages to the \'configuration\' inbox to add and
remove destinations.

Keyword arguments:

-   sourceComponent \-- None, or component to act as data source

::: {.section}
### [Inboxes]{#symbol-PlugSplitter.Inboxes}

-   **control** : Shutdown signalling, and signalling to be fanned out.
-   **\_control** : Internal inbox for receiving from the child source
    component (if it exists)
-   **configuration** : addsink(\...) and removesink(\...) request
    messages
-   **inbox** : Data items to be fanned out.
-   **\_inbox** : Internal inbox for receiving from the child source
    component (if it exists)
:::

::: {.section}
### [Outboxes]{#symbol-PlugSplitter.Outboxes}

-   **outbox** : Data items received on \'inbox\' inbox.
-   **signal** : Shutdown signalling, and data items received on
    \'control\' inbox.
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
#### [\_\_init\_\_(self\[, sourceComponent\])]{#symbol-PlugSplitter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [\_addSink(self, sink\[, sinkinbox\]\[, sinkcontrol\])]{#symbol-PlugSplitter._addSink}

Add a new destination for data.

Specify target component (sink), and target inbox (sinkinbox) and/or
target shutdown signalling inbox (sinkcontrol).
:::

::: {.section}
#### [\_delSink(self, sink\[, sinkinbox\]\[, sinkcontrol\])]{#symbol-PlugSplitter._delSink}

Remove a destination for data.

Specify target component (sink), and target inbox (sinkinbox) and/or
target shutdown signalling inbox (sinkcontrol).
:::

::: {.section}
#### [childrenDone(self)]{#symbol-PlugSplitter.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-PlugSplitter.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.html){.reference}.[Splitter](/Components/pydoc/Kamaelia.Util.Splitter.Splitter.html){.reference}
=====================================================================================================================================================================================================================================================================

::: {.section}
class Splitter([Axon.AdaptiveCommsComponent.AdaptiveCommsComponent](/Docs/Axon/Axon.AdaptiveCommsComponent.AdaptiveCommsComponent.html){.reference}) {#symbol-Splitter}
----------------------------------------------------------------------------------------------------------------------------------------------------

Splitter() -\> new Splitter component.

Splits incoming data out to multiple destinations. Send addsink(\...)
and removesink(\...) messages to the \'configuration\' inbox to add and
remove destinations.

::: {.section}
### [Inboxes]{#symbol-Splitter.Inboxes}

-   **control** : NOT USED
-   **configuration** : addsink(\...) and removesink(\...) request
    messages
-   **inbox** : Source of data items
:::

::: {.section}
### [Outboxes]{#symbol-Splitter.Outboxes}

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
#### [\_\_init\_\_(self)]{#symbol-Splitter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [createsink(self, sink\[, sinkbox\]\[, passthrough\])]{#symbol-Splitter.createsink}

Set up a new destination for data.

Creates an outbox, links it to the target (component,inbox) and records
it in self.outlist.
:::

::: {.section}
#### [deletesink(self, oldsink)]{#symbol-Splitter.deletesink}

Removes the specified (component, inbox) as a destination for data where
(component, inbox) = (oldsink.sink, oldsink.sinkbox).

Unlinks the target, destroys the corresponding outbox, and removes the
corresponding record from self.outlist.
:::

::: {.section}
#### [mainBody(self)]{#symbol-Splitter.mainBody}

Main loop body.
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
