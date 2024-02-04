---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SimpleHTTPClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[HTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}.[SimpleHTTPClient](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.SimpleHTTPClient.html){.reference}
=======================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.HTTP.HTTPClient.html){.reference}

------------------------------------------------------------------------

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
