---
pagename: Components/pydoc/Kamaelia.XML.SimpleXMLParser.SimpleXMLParser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[XML](/Components/pydoc/Kamaelia.XML.html){.reference}.[SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.html){.reference}.[SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.SimpleXMLParser.html){.reference}
====================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.html){.reference}

------------------------------------------------------------------------

::: {.section}
class SimpleXMLParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}, xml.sax.handler.ContentHandler) {#symbol-SimpleXMLParser}
---------------------------------------------------------------------------------------------------------------------------------------

SimpleXMLParser() -\> new SimpleXMLParser component.

Send XML data to the \"inbox\" inbox, and events describing documents,
elements and blocks of characters (as parsed by SAX) will be sent out of
the \"outbox\" outbox.

::: {.section}
### [Inboxes]{#symbol-SimpleXMLParser.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Incoming XML
:::

::: {.section}
### [Outboxes]{#symbol-SimpleXMLParser.Outboxes}

-   **outbox** : XML events
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self)]{#symbol-SimpleXMLParser.__init__}
:::

::: {.section}
#### [characters(self, chars)]{#symbol-SimpleXMLParser.characters}
:::

::: {.section}
#### [checkShutdown(self)]{#symbol-SimpleXMLParser.checkShutdown}

Collects any new shutdown messages arriving at the \"control\" inbox,
and returns \"NOW\" if immediate shutdown is required, or \"WHENEVER\"
if the component can shutdown when it has finished processing pending
data.
:::

::: {.section}
#### [endDocument(self)]{#symbol-SimpleXMLParser.endDocument}
:::

::: {.section}
#### [endElement(self, name)]{#symbol-SimpleXMLParser.endElement}
:::

::: {.section}
#### [main(self)]{#symbol-SimpleXMLParser.main}
:::

::: {.section}
#### [safesend(self, data, boxname)]{#symbol-SimpleXMLParser.safesend}

Generator.

Sends data out of the named outbox. If the destination is full
(noSpaceInBox exception) then it waits until there is space and retries
until it succeeds.

If a shutdownMicroprocess message is received, returns early.
:::

::: {.section}
#### [startDocument(self)]{#symbol-SimpleXMLParser.startDocument}
:::

::: {.section}
#### [startElement(self, name, attrs)]{#symbol-SimpleXMLParser.startElement}
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
