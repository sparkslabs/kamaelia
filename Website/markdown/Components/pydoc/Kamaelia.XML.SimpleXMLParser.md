---
pagename: Components/pydoc/Kamaelia.XML.SimpleXMLParser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[XML](/Components/pydoc/Kamaelia.XML.html){.reference}.[SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.html){.reference}
=================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.SimpleXMLParser.html){.reference}**
:::

-   [Simple/Basic parsing of XML using SAX](#403){.reference}
    -   [Example Usage](#404){.reference}
    -   [What does it output?](#405){.reference}
    -   [Behaviour](#406){.reference}
:::

::: {.section}
Simple/Basic parsing of XML using SAX {#403}
=====================================

XMLParser parses XML data sent to its \"inbox\" inbox using SAX, and
sends out \"document\", \"element\" and \"character\" events out of its
\"outbox\" outbox.

::: {.section}
[Example Usage]{#example-usage} {#404}
-------------------------------

The following code:

``` {.literal-block}
Pipeline( RateControlledFileReader("Myfile.xml"),
          SimpleXMLParser(),
          ConsoleEchoer(),
        ).run()
```

If given the following file as input:

``` {.literal-block}
<EDL xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MobileReframe.xsd">>
    <FileID>File identifier</FileID>

    <Edit>
        <Start frame="0"  />
        <End   frame="24" />
        <Crop  x1="0" y1="0" x2="400" y2="100" />
    </Edit>
    <Edit>
        <Start frame="25" />
        <End   frame="49" />
        <Crop  x1="80" y1="40" x2="480" y2="140" />
    </Edit>
</EDL>
```

Will output the following (albeit without the newlines, added here for
clarity):

``` {.literal-block}
('document',)
('element', u'EDL', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaaca86e60>)
('chars', u'>')
('chars', u'\n')
('chars', u'    ')
('element', u'FileID', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028758>)
('chars', u'File identifier')
('/element', u'FileID')
('chars', u'\n')
('chars', u'    ')
('chars', u'\n')
('chars', u'    ')
('element', u'Edit', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028908>)
('chars', u'\n')
('chars', u'        ')
('element', u'Start', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028908>)
('/element', u'Start')
('chars', u'\n')
('chars', u'        ')
('element', u'End', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaaca86e60>)
('/element', u'End')
('chars', u'\n')
('chars', u'        ')
('element', u'Crop', <xml.sax.xmlreader.AttributesImpl instance at 0x2aaaac028908>)
('/element', u'Crop')
('chars', u'\n')
('chars', u'    ')
('/element', u'Edit')
('chars', u'\n')
('chars', u'    ')
('/element', u'EDL')
```
:::

::: {.section}
[What does it output?]{#what-does-it-output} {#405}
--------------------------------------------

What is output is effectively a simple, but useful, parsing of the XML.
It is a set of messages representing a subset of the python SAX
ContentHandler. All are in the form of a simple tuple where the first
term is always the type of \"thing\" identified - \'document\' start or
finish, \'element\' start or finish, or raw text characters:

**\`\`(\"document\", )\`\`**

-   Start of the XML document

**\`\`(\"/document\", )\`\`**

-   End of the XML document (not sent if shutdown with a
    shutdownMicroprocess() message)

**\`\`(\"element\", name, attributes)\`\`**

-   Start tag for an element. `name`{.docutils .literal} is the name of
    the element. `attributes`{.docutils .literal} is a SAX attributes
    object - which behaves just like a dictionary - mapping attribute
    names to strings of their values. For example:

    ``` {.literal-block}
    ("element", "img", {"src":"/images/mypic.jpg"})
    ```

**\`\`(\"/element\", name)\`\`**

-   End tag for an element. `name`{.docutils .literal} is the name of
    the element.

**\`\`(\"chars\", textfragment)\`\`**

-   Fragment of text from within an element. Note that the text
    contained in a single element be comprised of multiple fragments.
    They will include whitespace and newline characters.
:::

::: {.section}
[Behaviour]{#behaviour} {#406}
-----------------------

Send chunks of text making up an XML document to this component\'s
\"inbox\" inbox. The XML Parser used will output identified items from
its \"outbox\" outbox.

This component supports sending its output to a size limited inbox. If
the size limited inbox is full, this component will pause until it is
able to send out the data.

If a producerFinished message is received on the \"control\" inbox, this
component will complete parsing any data pending in its inbox, and
finish sending any resulting data to its outbox. It will then send the
producerFinished message on out of its \"signal\" outbox and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
this component will immediately send it on out of its \"signal\" outbox
and immediately terminate. It will not complete processing, or sending
on any pending data.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[XML](/Components/pydoc/Kamaelia.XML.html){.reference}.[SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.html){.reference}.[SimpleXMLParser](/Components/pydoc/Kamaelia.XML.SimpleXMLParser.SimpleXMLParser.html){.reference}
====================================================================================================================================================================================================================================================================================================

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
