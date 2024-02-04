---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPParser](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser.html){.reference}
=============================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [HTTPParser](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser.HTTPParser.html){.reference}**
:::

-   [HTTP Parser](#588){.reference}
    -   [Example Usage](#589){.reference}
:::

::: {.section}
HTTP Parser {#588}
===========

This component is for transforming HTTP requests or responses into
multiple easy-to-use dictionary objects.

Unless you are implementing a new HTTP component you should not use this
component directly. Either SimpleHTTPClient, HTTPServer (in conjuncton
with SimpleServer) or SingleShotHTTPClient will likely serve your needs.

If you want to use it directly, note that it doesn\'t output strings but
ParsedHTTPHeader, ParsedHTTPBodyChunk and ParsedHTTPEnd objects.

::: {.section}
[Example Usage]{#example-usage} {#589}
-------------------------------

If you want to play around with parsing HTTP responses: (like a client):

``` {.literal-block}
pipeline(
    ConsoleReader(),
    HTTPParser(mode="response"),
    ConsoleEchoer()
).run()
```

If you want to play around with parsing HTTP requests: (like a server):

``` {.literal-block}
pipeline(
    ConsoleReader(),
    HTTPParser(mode="response"),
    ConsoleEchoer()
).run()
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPParser](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser.html){.reference}.[HTTPParser](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPParser.HTTPParser.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class HTTPParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-HTTPParser}
--------------------------------------------------------------------------------------------------

Component that transforms HTTP requests or responses from a single TCP
connection into multiple easy-to-use dictionary objects.

::: {.section}
### [Inboxes]{#symbol-HTTPParser.Inboxes}

-   **control** : UNUSED
-   **inbox** : Raw HTTP requests/responses
:::

::: {.section}
### [Outboxes]{#symbol-HTTPParser.Outboxes}

-   **debug** : Debugging information
-   **outbox** : HTTP request object
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
#### [\_\_init\_\_(self, mode, \*\*argd)]{#symbol-HTTPParser.__init__}
:::

::: {.section}
#### [closeConnection(self)]{#symbol-HTTPParser.closeConnection}
:::

::: {.section}
#### [dataFetch(self)]{#symbol-HTTPParser.dataFetch}

Read once from inbox (generally a TCP connection) and add what is
received to the readbuffer. This is somewhat inefficient for long lines
maybe O(n\^2)
:::

::: {.section}
#### [debug(self, msg)]{#symbol-HTTPParser.debug}
:::

::: {.section}
#### [getBody(self, requestobject)]{#symbol-HTTPParser.getBody}
:::

::: {.section}
#### [getBodyDependingOnHalfClose(self)]{#symbol-HTTPParser.getBodyDependingOnHalfClose}
:::

::: {.section}
#### [getBody\_ChunkTransferEncoding(self, requestobject)]{#symbol-HTTPParser.getBody_ChunkTransferEncoding}
:::

::: {.section}
#### [getBody\_KnownContentLength(self, requestobject)]{#symbol-HTTPParser.getBody_KnownContentLength}
:::

::: {.section}
#### [getHeaders(self, requestobject)]{#symbol-HTTPParser.getHeaders}
:::

::: {.section}
#### [getInitialLine(self)]{#symbol-HTTPParser.getInitialLine}
:::

::: {.section}
#### [handleInitialLine(self, requestobject)]{#symbol-HTTPParser.handleInitialLine}
:::

::: {.section}
#### [handle\_requestline(self, splitline, requestobject)]{#symbol-HTTPParser.handle_requestline}
:::

::: {.section}
#### [initialiseRequestObject(self)]{#symbol-HTTPParser.initialiseRequestObject}
:::

::: {.section}
#### [main(self)]{#symbol-HTTPParser.main}
:::

::: {.section}
#### [nextLine(self)]{#symbol-HTTPParser.nextLine}

Fetch the next complete line in the readbuffer, if there is one
:::

::: {.section}
#### [setConnectionMode(self, requestobject)]{#symbol-HTTPParser.setConnectionMode}
:::

::: {.section}
#### [setServer(self, requestobject)]{#symbol-HTTPParser.setServer}
:::

::: {.section}
#### [shouldShutdown(self)]{#symbol-HTTPParser.shouldShutdown}
:::

::: {.section}
#### [splitProtocolVersion(self, protvers, requestobject)]{#symbol-HTTPParser.splitProtocolVersion}
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
