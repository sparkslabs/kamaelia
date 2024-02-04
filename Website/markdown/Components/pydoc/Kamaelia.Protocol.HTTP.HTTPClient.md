---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}
=============================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SimpleHTTPClient.html){.reference}**
-   **component
    [SingleShotHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SingleShotHTTPClient.html){.reference}**
:::

-   [Single-Shot HTTP Client](#597){.reference}
    -   [Example Usage](#598){.reference}
    -   [How does it work?](#599){.reference}
-   [Simple HTTP Client](#600){.reference}
    -   [Example Usage](#601){.reference}
    -   [How does it work?](#602){.reference}
:::

::: {.section}
::: {.section}
[Single-Shot HTTP Client]{#single-shot-http-client} {#597}
---------------------------------------------------

This component is for downloading a single file from an HTTP server.
Pick up data received from the server on its \"outbox\" outbox.

Generally you should use SimpleHTTPClient in preference to this.

::: {.section}
### [Example Usage]{#example-usage} {#598}

How to use it:

``` {.literal-block}
Pipeline(
    SingleShotHTTPClient("http://www.google.co.uk/"),
    SomeComponentThatUnderstandsThoseMessageTypes()
).run()
```

If you want to use it directly, note that it doesn\'t output strings but
ParsedHTTPHeader, ParsedHTTPBodyChunk and ParsedHTTPEnd like HTTPParser.
This makes has the advantage of not buffering huge files in memory but
outputting them as a stream of chunks. (with plain strings you would not
know the contents of the headers or at what point that response had
ended!)
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#599}

SingleShotHTTPClient accepts a URL parameter at its creation (to
\_\_init\_\_). When activated it creates an HTTPParser instance and then
connects to the webserver specified in the URL using a TCPClient
component. It sends an HTTP request and then any response from the
server is received by the HTTPParser.

HTTPParser processes the response and outputs it in parts as:

``` {.literal-block}
ParsedHTTPHeader,
ParsedHTTPBodyChunk,
ParsedHTTPBodyChunk,
...
ParsedHTTPBodyChunk,
ParsedHTTPEnd
```

If SingleShotHTTPClient detects that the requested URL is a redirect
page (using the Location header) then it begins this cycle anew with the
URL of the new page, otherwise the parts of the page output by
HTTPParser are sent on to \"outbox\".
:::
:::

::: {.section}
[Simple HTTP Client]{#simple-http-client} {#600}
-----------------------------------------

This component downloads the pages corresponding to HTTP URLs received
on \"inbox\" and outputs their contents (file data) as a message, one
per URL, to \"outbox\" in the order they were received.

::: {.section}
### [Example Usage]{#id1} {#601}

Type URLs, and they will be downloaded and placed, back to back in
\"downloadedfile.txt\":

``` {.literal-block}
Pipeline(
    ConsoleReader(">>> ", ""),
    SimpleHTTPClient(),
    SimpleFileWriter("downloadedfile.txt"),
).run()
```
:::

::: {.section}
### [How does it work?]{#id2} {#602}

SimpleHTTPClient uses the Carousel component to create a new
SingleShotHTTPClient component for every URL requested. As URLs are
handled sequentially, it has only one SSHC child at anyone time.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}.[SimpleHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SimpleHTTPClient.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SimpleHTTPClient([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleHTTPClient}
--------------------------------------------------------------------------------------------------------

::: {.section}
### [Inboxes]{#symbol-SimpleHTTPClient.Inboxes}

-   **control** : Shut me down
-   **\_carouselready** : Receive NEXT when carousel has completed a
    request
-   **inbox** : URLs to download - a dict {\'url\':\'x\',
    \'postbody\':\'y\'} or a just the URL as a string
-   **\_carouselinbox** : Data from SingleShotHTTPClient via Carousel
:::

::: {.section}
### [Outboxes]{#symbol-SimpleHTTPClient.Outboxes}

-   **debug** : Information to aid debugging
-   **outbox** : Requested file\'s data string
-   **signal** : Signal I have shutdown
-   **\_carouselnext** : Create a new SingleShotHTTPClient
-   **\_carouselsignal** : Shutdown the carousel
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
#### [\_\_init\_\_(self)]{#symbol-SimpleHTTPClient.__init__}

Create and link to a carousel object
:::

::: {.section}
#### [cleanup(self)]{#symbol-SimpleHTTPClient.cleanup}

Destroy child components and send producerFinished when we quit.
:::

::: {.section}
#### [debug(self, msg)]{#symbol-SimpleHTTPClient.debug}
:::

::: {.section}
#### [main(self)]{#symbol-SimpleHTTPClient.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}.[SingleShotHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SingleShotHTTPClient.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class SingleShotHTTPClient([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SingleShotHTTPClient}
------------------------------------------------------------------------------------------------------------

SingleShotHTTPClient() -\> component that can download a file using HTTP
by URL

Arguments: - starturl \-- the URL of the file to download - \[postbody\]
\-- data to POST to that URL - if set to None becomes an empty body in
to a POST (of PUT) request - \[connectionclass\] \-- specify a class
other than TCPClient to connect with - \[method\] \-- the HTTP method
for the request (default to GET normally or POST if postbody != \"\"

::: {.section}
### [Inboxes]{#symbol-SingleShotHTTPClient.Inboxes}

-   **control** : UNUSED
-   **\_parserinbox** : Data from HTTP parser
-   **\_parsercontrol** : Signals from HTTP parser
-   **\_tcpcontrol** : Signals from TCP client
-   **inbox** : UNUSED
:::

::: {.section}
### [Outboxes]{#symbol-SingleShotHTTPClient.Outboxes}

-   **signal** : UNUSED
-   **\_parsersignal** : Signals for HTTP parser
-   **\_tcpoutbox** : Send over TCP connection
-   **debug** : Output to aid debugging
-   **outbox** : Requested file
-   **\_tcpsignal** : Signals shutdown of TCP connection
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
#### [\_\_init\_\_(self, starturl\[, postbody\]\[, connectionclass\]\[, extraheaders\]\[, method\])]{#symbol-SingleShotHTTPClient.__init__}
:::

::: {.section}
#### [formRequest(self, url)]{#symbol-SingleShotHTTPClient.formRequest}

Craft a HTTP request string for the supplied url
:::

::: {.section}
#### [handleRedirect(self, header)]{#symbol-SingleShotHTTPClient.handleRedirect}

Check for a redirect response and queue the fetching the page it points
to if it is such a response. Returns true if it was a redirect page and
false otherwise.
:::

::: {.section}
#### [main(self)]{#symbol-SingleShotHTTPClient.main}

Main loop.
:::

::: {.section}
#### [mainBody(self)]{#symbol-SingleShotHTTPClient.mainBody}

Called repeatedly by main loop. Checks inboxes and processes messages
received. Start the fetching of the new page if the current one is a
redirect and has been completely fetched.
:::

::: {.section}
#### [makeRequest(self, request)]{#symbol-SingleShotHTTPClient.makeRequest}

Connect to the remote HTTP server and send request
:::

::: {.section}
#### [shutdownKids(self)]{#symbol-SingleShotHTTPClient.shutdownKids}

Close TCP connection and HTTP parser
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
