---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer.html){.reference}
=============================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer.HTTPServer.html){.reference}**
:::

-   [HTTP Server](#578){.reference}
    -   [Example Usage](#579){.reference}
    -   [How does it work?](#580){.reference}
-   [HTTP Request Handler](#581){.reference}
    -   [How does it work?](#582){.reference}
    -   [What does it support?](#583){.reference}
:::

::: {.section}
::: {.section}
[HTTP Server]{#http-server} {#578}
---------------------------

The fundamental parts of a webserver - an HTTP request parser and a
request handler/response generator. One instance of this component can
handle one TCP connection. Use a SimpleServer or similar component to
allow several concurrent HTTP connections to the server.

::: {.section}
### [Example Usage]{#example-usage} {#579}

> def createhttpserver():
> :   return HTTPServer(HTTPResourceGlue.createRequestHandler)
>
> SimpleServer(protocol=createhttpserver, port=80).run()

This defines a function which creates a HTTPServer instance with
HTTPResourceGlue.createRequestHandler as the request handler component
creator function. This function is then called by SimpleServer for every
new TCP connection.
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#580}

HTTPServer creates and links to a HTTPParser and HTTPRequestHandler
component. Data received over TCP is forwarded to the HTTPParser and the
output of HTTPRequestHandler forwarded to the TCP component\'s inbox for
sending.

See HTTPParser (in HTTPParser.py) and HTTPRequestHandler (below) for
details of how these components work.

HTTPServer accepts a single parameter - a request handler function which
is passed onto and used by HTTPRequestHandler to generate request
handler components. This allows different HTTP server setups to run on
different ports serving completely different content.
:::
:::

::: {.section}
[HTTP Request Handler]{#http-request-handler} {#581}
---------------------------------------------

HTTPRequestHandler accepts parsed HTTP requests (from HTTPParser) and
outputs appropriate responses to those requests.

::: {.section}
### [How does it work?]{#id1} {#582}

HTTPServer creates 2 subcomponents - HTTPParser and HTTPRequestHandler
which handle the processing of requests and the creation of responses
respectively.

Both requests and responses are handled in a stepwise manner (as opposed
to processing a whole request or response in one go) to reduce latency
and cope well with bottlenecks.

One request handler (self.handler) component is used per request - the
particular component instance (including parameters, component state) is
picked by a function called createRequestHandler - a function specified
by the user. A suitable definition of this function is available in
HTTPResourceGlue.py.

Generally you will have a handler spawned for each new request,
terminating after completing the sending of the response. However, it is
also possible to use a \'persistent\' component if you do the required
jiggery-pokery to make sure that at any one time this component is not
servicing more than one request simultaenously (\'cause it wouldn\'t
work).
:::

::: {.section}
### [What does it support?]{#what-does-it-support} {#583}

Components as request handlers (hurrah!).

3 different ways in which the response data (body) can be terminated:

::: {.section}
#### [Chunked transfer encoding]{#chunked-transfer-encoding}

This is the most complex of the 3 ways and was introduced in HTTP/1.1.
Its performance is slightly worse that the other 2 as multiple
length-lines have to be added to the data stream. It is recommended for
responses whose size is not known in advance as it allows keep-alive
connections (more than one HTTP request per TCP connection).
:::

::: {.section}
#### [Explicit length]{#explicit-length}

This is the easiest of the 3 ways but requires the length of the
response to be known before it is sent. It uses a header
\'Content-Length\' to indicate this value. This method is prefered for
any response whose length is known in advance.
:::

::: {.section}
#### [Connection: close]{#connection-close}

This method closes (or half-closes) the TCP connection when the response
is complete. This is highly inefficient when the client wishes to
download several resources as a new TCP connection must be created and
destroyed for each resource. This method is retained for HTTP/1.0
compatibility. It is however preferred for responses that do not have a
true end, e.g. a continuous stream over HTTP as the alternative, chunked
transfer encoding, has poorer performance.

The choice of these three methods is determined at runtime by the
characteristics of the first response part produced by the request
handler and the version of HTTP that the client supports (chunked
requires 1.1 or higher).

::: {.section}
##### [What may need work?]{#what-may-need-work}

-   HTTP standards-compliance (e.g. handling of version numbers for a
    start)

-   

    Requests for byte ranges, cache control (though these may be better implemented

    :   in each request handler)

-   Performance tuning (also in HTTPParser)

-   

    Prevent many MBs of data being queued up because TCPClient finds it has a slow

    :   upload to the remote host
:::
:::
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer.html){.reference}.[HTTPServer](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPServer.HTTPServer.html){.reference}
===========================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: HTTPServer {#symbol-HTTPServer}
------------------

HTTPServer() -\> new HTTPServer component capable of handling a single
connection

Arguments:

:   

    \-- createRequestHandler - a function required by HTTPRequestHandler that
    :   creates the appropriate request-handler component for each
        request, see HTTPResourceGlue
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
