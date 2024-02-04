---
pagename: Components/pydoc/Kamaelia.Util.Introspector
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Introspector](/Components/pydoc/Kamaelia.Util.Introspector.html){.reference}
==============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Introspector](/Components/pydoc/Kamaelia.Util.Introspector.Introspector.html){.reference}**
:::

-   [Detecting the topology of a running Kamaelia
    system](#253){.reference}
    -   [Example Usage](#254){.reference}
    -   [How does it work?](#255){.reference}
:::

::: {.section}
Detecting the topology of a running Kamaelia system {#253}
===================================================

The Introspector component introspects the current local topology of a
Kamaelia system - that is what components there are and how they are
wired up.

It continually outputs any changes that occur to the topology.

::: {.section}
[Example Usage]{#example-usage} {#254}
-------------------------------

Introspect and display whats going on inside the system:

``` {.literal-block}
MyComplexSystem().activate()

Pipeline( Introspector(),
          text_to_token_lists()
          AxonVisualiser(),
        )
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#255}
--------------------------------------

Once activated, this component introspects the current local topology of
a Kamaelia system.

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
represents a linkage in the [Axon](/Docs/Axon/Axon.html){.reference}
system, from one component to another.

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
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Introspector](/Components/pydoc/Kamaelia.Util.Introspector.html){.reference}.[Introspector](/Components/pydoc/Kamaelia.Util.Introspector.Introspector.html){.reference}
=========================================================================================================================================================================================================================================================================================

::: {.section}
class Introspector([Axon.Introspector.Introspector](/Docs/Axon/Axon.Introspector.Introspector.html){.reference}) {#symbol-Introspector}
----------------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-Introspector.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Introspector.Outboxes}
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
