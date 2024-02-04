---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}
===================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastClient.html){.reference}**
-   **component
    [IcecastDemux](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastDemux.html){.reference}**
-   **prefab
    [IcecastStreamRemoveMetadata](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastStreamRemoveMetadata.html){.reference}**
-   **component
    [IcecastStreamWriter](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastStreamWriter.html){.reference}**
:::

-   [Icecast/SHOUTcast MP3 streaming client](#575){.reference}
    -   [Example Usage](#576){.reference}
    -   [How does it work?](#577){.reference}
:::

::: {.section}
Icecast/SHOUTcast MP3 streaming client {#575}
======================================

This component uses HTTP to stream MP3 audio from a SHOUTcast/Icecast
server.

IcecastClient fetches the combined audio and metadata stream from the
HTTP server hosting the stream. IcecastDemux separates the audio data
from the metadata in stream and IcecastStreamWriter writes the audio
data to disk (discarding metadata).

::: {.section}
[Example Usage]{#example-usage} {#576}
-------------------------------

Receive an Icecast/SHOUTcast stream, demultiplex it, and write it to a
file:

``` {.literal-block}
pipeline(
    IcecastClient("http://64.236.34.97:80/stream/1049"),
    IcecastDemux(),
    IcecastStreamWriter("stream.mp3"),
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#577}
--------------------------------------

The SHOUTcast/Icecast protocol is virtually identical to HTTP. As such,
IcecastClient subclasses SingleShotHTTPClient modifying the request
slightly to ask for stream metadata(e.g. track name) to be included (by
adding the icy-metadata header). It is otherwise identical to its parent
class.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastClient.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class IcecastClient(SingleShotHTTPClient) {#symbol-IcecastClient}
-----------------------------------------

IcecastClient(starturl) -\> Icecast/SHOUTcast MP3 streaming component

Arguments: - starturl \-- the URL of the stream

::: {.section}
### [Inboxes]{#symbol-IcecastClient.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-IcecastClient.Outboxes}
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
#### [formRequest(self, url)]{#symbol-IcecastClient.formRequest}

Overrides the standard HTTP request with an Icecast/SHOUTcast variant
which includes the icy-metadata header required to get metadata with the
stream
:::

::: {.section}
#### [main(self)]{#symbol-IcecastClient.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}.[IcecastDemux](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastDemux.html){.reference}
========================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class IcecastDemux([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-IcecastDemux}
----------------------------------------------------------------------------------------------------

Splits a raw Icecast stream into A/V data and metadata

::: {.section}
### [Inboxes]{#symbol-IcecastDemux.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-IcecastDemux.Outboxes}
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
#### [dictizeMetadata(self, metadata)]{#symbol-IcecastDemux.dictizeMetadata}

Convert metadata that was embedded in the stream into a dictionary.
:::

::: {.section}
#### [main(self)]{#symbol-IcecastDemux.main}
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}.[IcecastStreamRemoveMetadata](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastStreamRemoveMetadata.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: IcecastStreamRemoveMetadata {#symbol-IcecastStreamRemoveMetadata}
-----------------------------------
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}.[IcecastStreamWriter](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastStreamWriter.html){.reference}
======================================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class IcecastStreamWriter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-IcecastStreamWriter}
-----------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-IcecastStreamWriter.Inboxes}

-   **control** : UNUSED
-   **inbox** : Icecast stream
:::

::: {.section}
### [Outboxes]{#symbol-IcecastStreamWriter.Outboxes}

-   **outbox** : UNUSED
-   **signal** : UNUSED
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
#### [\_\_init\_\_(self, filename)]{#symbol-IcecastStreamWriter.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-IcecastStreamWriter.main}
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
