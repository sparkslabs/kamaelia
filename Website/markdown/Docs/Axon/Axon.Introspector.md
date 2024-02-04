---
pagename: Docs/Axon/Axon.Introspector
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Introspector](/Docs/Axon/Axon.Introspector.html){.reference}
------------------------------------------------------------------------------------------------------
:::
:::

::: {.section}
Detecting the topology of a running Axon system
===============================================

::: {.container}
-   **component
    [Introspector](/Docs/Axon/Axon.Introspector.Introspector.html){.reference}**
:::

-   [Example Usage](#85){.reference}
-   [More detail](#86){.reference}
-   [How does it work?](#87){.reference}
:::

::: {.section}
The Introspector is a component that introspects the current local
topology of an Axon system - that is what components there are and how
they are wired up.

It continually outputs any changes that occur to the topology.

::: {.section}
[Example Usage]{#example-usage} {#85}
-------------------------------

Introspect and display whats going on inside the system:

``` {.literal-block}
MyComplexSystem().activate()

pipeline( Introspector(),
          AxonVisualiserServer(noServer=True),
        )
```
:::

::: {.section}
[More detail]{#more-detail} {#86}
---------------------------

Once activated, this component introspects the current local topology of
an Axon system.

Local? This component examines its scheduler to find components and
postmen. It then examines them to determine their inboxes and outboxes
and the linkages between them. In effect, it determines the current
topology of the system.

If this component is not active, then it will see no scheduler and will
report nothing.

What is output is how the topology changes. Immediately after
activation, the topology is assumed to be empty, so the first set of
changes describes adding nodes and linkages to the topology to build up
the current state of it.

Subsequent output just describes the changes - adding or deleting
linkages and nodes as appropriate.

Nodes in the topology represent components and postboxes. A linkage
between a component node and a postbox node expresses the fact that that
postbox belongs to that component. A linkage between two postboxes
represents a linkage in the Axon system, from one component to another.

This topology change data is output as string containing one or more
lines. It is output through the \"outbox\" outbox. Each line may be one
of the following:

-   \"DEL ALL\"
    -   the first thing sent immediately after activation - to ensure
        that the receiver of this data understand that we are starting
        from nothing
-   \"ADD NODE \<id\> \<name\> randompos component\"
-   \"ADD NODE \<id\> \<name\> randompos inbox\"
-   \"ADD NODE \<id\> \<name\> randompos outbox\"
    -   an instruction to add a node to the topology, representing a
        component, inbox or outbox. \<id\> is a unique identifier.
        \<name\> is a \'friendly\' textual label for the node.
-   \"DEL NODE \<id\>\"
    -   an instruction to delete a node, specified by its unique id
-   \"ADD LINK \<id1\> \<id2\>\"
    -   an instruction to add a link between the two identified nodes.
        The link is deemed to be directional, from \<id1\> to \<id2\>
-   \"DEL LINK \<id1\> \<id2\>\"
    -   an instruction to delete any link between the two identified
        nodes. Again, the directionality is from \<id1\> to \<id2\>.

the \<id\> and \<name\> fields may be encapsulated in double quote marks
(\"). This will definitely be so if they contain space characters.

If there are no topology changes then nothing is output.

This component ignores anything arriving at its \"inbox\" inbox.

If a shutdownMicroprocess message is received on the \"control\" inbox,
it is sent on to the \"signal\" outbox and the component will terminate.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#87}
--------------------------------------

Every execution timeslice, Introspector queries its scheduler to obtain
a list of all components. It then queries the postoffice in each
component to build a picture of all linkages between components. It also
builds a list of all inboxes and outboxes on each component.

This is mapped to a list of nodes and linkages. Nodes being components
and postboxes; and linkages being what postboxes belong to what
components, and what postboxes are linked to what postboxes.

This is compared against the nodes and linkages from the previous cycle
of processing to determine what has changed. The changes are then output
as a sequence of \"ADD NODE\", \"DEL NODE\", \"ADD LINK\" and \"DEL
LINK\" commands.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[Introspector](/Docs/Axon/Axon.Introspector.html){.reference}.[Introspector](/Docs/Axon/Axon.Introspector.Introspector.html){.reference}
=================================================================================================================================================================================

::: {.section}
class Introspector([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Introspector}
----------------------------------------------------------------------------------------------------

Introspector() -\> new Introspector component.

Outputs topology (change) data describing what components there are, and
how they are wired inside the running Axon system.

::: {.section}
### [Inboxes]{#symbol-Introspector.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-Introspector.Outboxes}

-   **outbox** : Topology (change) data describing the Axon system
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
#### [introspect(self)]{#symbol-Introspector.introspect}

introspect() -\> components, postboxes, linkages

Returns the current set of components, postboxes and interpostbox
linkages.

-   components \-- a dictionary, containing components as keys
-   postboxes \-- a list of (component.id, type, \"boxname\") tuples,
    where type=\"i\" (inbox) or \"o\" (outbox)
-   linkages \-- a dictionary containing (postbox,postbox) tuples as
    keys, where postbox is a tuple from the postboxes list
:::

::: {.section}
#### [main(self)]{#symbol-Introspector.main}

Main loop.
:::
:::

::: {.section}
::: {.section}
#### Methods inherited from [Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference} :

-   [mainBody](/Docs/Axon/Axon.Component.html#symbol-component.mainBody){.reference}(self)
-   [\_\_str\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__str__){.reference}(self)
-   [childComponents](/Docs/Axon/Axon.Component.html#symbol-component.childComponents){.reference}(self)
-   [\_\_init\_\_](/Docs/Axon/Axon.Component.html#symbol-component.__init__){.reference}(self,
    \*args, \*\*argd)
-   [setInboxSize](/Docs/Axon/Axon.Component.html#symbol-component.setInboxSize){.reference}(self,
    boxname, size)
-   [send](/Docs/Axon/Axon.Component.html#symbol-component.send){.reference}(self,
    message\[, boxname\])
-   [dataReady](/Docs/Axon/Axon.Component.html#symbol-component.dataReady){.reference}(self\[,
    boxname\])
-   [initialiseComponent](/Docs/Axon/Axon.Component.html#symbol-component.initialiseComponent){.reference}(self)
-   [anyReady](/Docs/Axon/Axon.Component.html#symbol-component.anyReady){.reference}(self)
-   [\_\_addChild](/Docs/Axon/Axon.Component.html#symbol-component.__addChild){.reference}(self,
    child)
-   [closeDownComponent](/Docs/Axon/Axon.Component.html#symbol-component.closeDownComponent){.reference}(self)
-   [\_closeDownMicroprocess](/Docs/Axon/Axon.Component.html#symbol-component._closeDownMicroprocess){.reference}(self)
-   [link](/Docs/Axon/Axon.Component.html#symbol-component.link){.reference}(self,
    source, sink, \*optionalargs, \*\*kwoptionalargs)
-   [unlink](/Docs/Axon/Axon.Component.html#symbol-component.unlink){.reference}(self\[,
    thecomponent\]\[, thelinkage\])
-   [recv](/Docs/Axon/Axon.Component.html#symbol-component.recv){.reference}(self\[,
    boxname\])
-   [\_deliver](/Docs/Axon/Axon.Component.html#symbol-component._deliver){.reference}(self,
    message\[, boxname\])
-   [removeChild](/Docs/Axon/Axon.Component.html#symbol-component.removeChild){.reference}(self,
    child)
-   [Inbox](/Docs/Axon/Axon.Component.html#symbol-component.Inbox){.reference}(self\[,
    boxname\])
-   [addChildren](/Docs/Axon/Axon.Component.html#symbol-component.addChildren){.reference}(self,
    \*children)
:::

::: {.section}
#### Methods inherited from [Axon.Microprocess.microprocess](/Docs/Axon/Axon.Microprocess.microprocess.html){.reference} :

-   [pause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.pause){.reference}(self)
-   [\_unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._unpause){.reference}(self)
-   [\_microprocessGenerator](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._microprocessGenerator){.reference}(self,
    someobject\[, mainmethod\])
-   [\_isStopped](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isStopped){.reference}(self)
-   [stop](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.stop){.reference}(self)
-   [next](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.next){.reference}(self)
-   [activate](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.activate){.reference}(self\[,
    Scheduler\]\[, Tracker\]\[, mainmethod\])
-   [unpause](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.unpause){.reference}(self)
-   [run](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess.run){.reference}(self)
-   [\_isRunnable](/Docs/Axon/Axon.Microprocess.html#symbol-microprocess._isRunnable){.reference}(self)
:::
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
