---
pagename: Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastClient
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Protocol](/Components/pydoc/Kamaelia.Protocol.html){.reference}.[HTTP](/Components/pydoc/Kamaelia.Protocol.HTTP.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}.[IcecastClient](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.IcecastClient.html){.reference}
==========================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Protocol.HTTP.IcecastClient.html){.reference}

------------------------------------------------------------------------

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
