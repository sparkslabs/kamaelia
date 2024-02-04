---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPRequestHandler.HTTPRequestHandler
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPRequestHandler](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPRequestHandler.html){.reference}.[HTTPRequestHandler](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPRequestHandler.HTTPRequestHandler.html){.reference}
===================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPRequestHandler.html){.reference}

------------------------------------------------------------------------

::: {.section}
class HTTPRequestHandler([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-HTTPRequestHandler}
----------------------------------------------------------------------------------------------------------

HTTPRequestHandler() -\> new HTTPRequestHandler component capable of
fulfilling the requests received over a single connection after they
have been parsed by HTTPParser

::: {.section}
### [Inboxes]{#symbol-HTTPRequestHandler.Inboxes}

-   **control** : Signal component termination
-   **\_handlercontrol** : Signals from the request handler
-   **inbox** : Raw HTTP requests
-   **\_handlerinbox** : Output from the request handler
:::

::: {.section}
### [Outboxes]{#symbol-HTTPRequestHandler.Outboxes}

-   **debug** : Information to aid debugging
-   **outbox** : HTTP responses
-   **signal** : Signal connection to close
-   **\_handleroutbox** : POST data etc. for the request handler
-   **\_handlersignal** : Signals for the request handler
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
#### [\_\_init\_\_(self, requestHandlerFactory)]{#symbol-HTTPRequestHandler.__init__}
:::

::: {.section}
#### [\_sendChunkChunked(self, resource)]{#symbol-HTTPRequestHandler._sendChunkChunked}

Send some more of the resource\'s data, for a response that uses chunked
transfer-encoding
:::

::: {.section}
#### [\_sendChunkExplicit(self, resource)]{#symbol-HTTPRequestHandler._sendChunkExplicit}

Send some more of the resource\'s data, having already sent a
content-length header
:::

::: {.section}
#### [\_sendEndChunked(self)]{#symbol-HTTPRequestHandler._sendEndChunked}

Called when a chunk-encoded response ends
:::

::: {.section}
#### [\_sendEndClose(self)]{#symbol-HTTPRequestHandler._sendEndClose}

Called when a connection: close terminated response ends
:::

::: {.section}
#### [\_sendEndExplicit(self)]{#symbol-HTTPRequestHandler._sendEndExplicit}

Called when a response that had a content-length header ends
:::

::: {.section}
#### [checkRequestValidity(self, request)]{#symbol-HTTPRequestHandler.checkRequestValidity}
:::

::: {.section}
#### [connectResourceHandler(self)]{#symbol-HTTPRequestHandler.connectResourceHandler}

Link to the resource handler we\'ve created so we can receive its output
:::

::: {.section}
#### [createHandler(self, request)]{#symbol-HTTPRequestHandler.createHandler}
:::

::: {.section}
#### [debug(self, msg)]{#symbol-HTTPRequestHandler.debug}
:::

::: {.section}
#### [determineConnectionType(self, request)]{#symbol-HTTPRequestHandler.determineConnectionType}
:::

::: {.section}
#### [disconnectResourceHandler(self)]{#symbol-HTTPRequestHandler.disconnectResourceHandler}

Disconnect the now finished resource handler
:::

::: {.section}
#### [formResponseHeader(self, resource, protocolversion\[, lengthMethod\])]{#symbol-HTTPRequestHandler.formResponseHeader}
:::

::: {.section}
#### [forwardBodyChunks(self)]{#symbol-HTTPRequestHandler.forwardBodyChunks}
:::

::: {.section}
#### [handleRequest(self, request)]{#symbol-HTTPRequestHandler.handleRequest}
:::

::: {.section}
#### [isValidRequest(self, request)]{#symbol-HTTPRequestHandler.isValidRequest}
:::

::: {.section}
#### [main(self)]{#symbol-HTTPRequestHandler.main}
:::

::: {.section}
#### [resourceUTF8Encode(self, resource)]{#symbol-HTTPRequestHandler.resourceUTF8Encode}

Encode a resource\'s unicode data as utf-8 octets
:::

::: {.section}
#### [sendMessageChunks(self, msg)]{#symbol-HTTPRequestHandler.sendMessageChunks}
:::

::: {.section}
#### [setChunkingModeMethod(self, msg, request)]{#symbol-HTTPRequestHandler.setChunkingModeMethod}
:::

::: {.section}
#### [setUpRequestHandler(self, request)]{#symbol-HTTPRequestHandler.setUpRequestHandler}
:::

::: {.section}
#### [shutdownRequestHandler(self, lengthMethod)]{#symbol-HTTPRequestHandler.shutdownRequestHandler}
:::

::: {.section}
#### [updateShouldShutdown(self)]{#symbol-HTTPRequestHandler.updateShouldShutdown}
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
