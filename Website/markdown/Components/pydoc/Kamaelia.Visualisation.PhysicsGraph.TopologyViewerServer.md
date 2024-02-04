---
pagename: Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.html){.reference}
=============================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [TextControlledTopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.TextControlledTopologyViewer.html){.reference}**
-   **prefab
    [TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.TopologyViewerServer.html){.reference}**
:::

-   [Generic Topology Viewer Server](#438){.reference}
    -   [Example Usage](#439){.reference}
    -   [How does it work?](#440){.reference}
:::

::: {.section}
Generic Topology Viewer Server {#438}
==============================

A generic topology viewer that one client can connect to at a time over
a TCP socket and send topology change data for visualisation.

::: {.section}
[Example Usage]{#example-usage} {#439}
-------------------------------

Visualiser that listens on port 1500 for a TCP connection through which
it receives topology change data to render:

``` {.literal-block}
TopologyViewerServer( serverPort = 1500 ).run()
```

A simple client to drive the visualiser:

``` {.literal-block}
Pipeline( ConsoleReader(),
          TCPClient( server=<address>, port=1500 ),
        ).run()
```

Run the server, then run the client:

``` {.literal-block}
>>> DEL ALL
>>> ADD NODE 1 "1st node" randompos -
>>> ADD NODE 2 "2nd node" randompos -
>>> ADD NODE 3 "3rd node" randompos -
>>> ADD LINK 1 2
>>> ADD LINK 3 2
>>> DEL LINK 1 2
>>> DEL NODE 1
```

See also
[Kamaelia.Visualisation.Axon.AxonVisualiserServer](/Components/pydoc/Kamaelia.Visualisation.Axon.AxonVisualiserServer.html){.reference}
- which is a specialisation of this component.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#440}
--------------------------------------

TopologyViewerServer is a Pipeline of the following components:

-   [Kamaelia.Internet.SingleServer](/Components/pydoc/Kamaelia.Internet.SingleServer.html){.reference}
-   chunks\_to\_lines
-   lines\_to\_tokenlists
-   TopologyViewer
-   ConsoleEchoer

This Pipeline serves to listen on the specified port (defaults to 1500)
for clients. One client is allowed to connect at a time.

That client can then send topology change commands formatted as lines of
text. The lines are parsed and tokenised for the TopologyViewer.

Any output from the TopologyViewer is sent to the console.

If the noServer option is used at initialisation, then the Pipeline is
built without the SingleServer component. It then becomes a
TopologyViewer capable of processing non-tokenised input and with
diagnostic console output.

See TopologyViewer for more detail on topology change data and its
behaviour.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.html){.reference}.[TextControlledTopologyViewer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.TextControlledTopologyViewer.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: TextControlledTopologyViewer {#symbol-TextControlledTopologyViewer}
------------------------------------
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Visualisation](/Components/pydoc/Kamaelia.Visualisation.html){.reference}.[PhysicsGraph](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.html){.reference}.[TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.html){.reference}.[TopologyViewerServer](/Components/pydoc/Kamaelia.Visualisation.PhysicsGraph.TopologyViewerServer.TopologyViewerServer.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: TopologyViewerServer {#symbol-TopologyViewerServer}
----------------------------

TopologyViewerServer(\[noServer\]\[,serverPort\],\*\*args) -\> new
TopologyViewerServer component.

Multiple-clients-at-a-time TCP socket Topology viewer server. Connect on
the specified port and send topology change data for display by a
TopologyViewer.

Keyword arguments:

-   serverPort \-- None, or port number to listen on (default=1500)
-   args \-- all remaining keyword arguments passed onto TopologyViewer
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
