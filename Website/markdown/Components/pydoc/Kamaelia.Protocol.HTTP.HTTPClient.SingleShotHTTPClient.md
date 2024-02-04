---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SingleShotHTTPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}.[SingleShotHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SingleShotHTTPClient.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}

------------------------------------------------------------------------

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
