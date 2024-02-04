---
pagename: Components/pydoc/Kamaelia.Util.Chunkifier
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.Chunkifier.html){.reference}**
:::

-   [Chunkifier](#250){.reference}
    -   [Example Usage](#251){.reference}
    -   [How does it work?](#252){.reference}
:::

::: {.section}
Chunkifier {#250}
==========

A component that fixes the message size of an input stream to a given
value, outputting blocks of that size when sufficient input has
accumulated. This component\'s input is stream orientated - all messages
received are concatenated to the interal buffer without divisions.

::: {.section}
[Example Usage]{#example-usage} {#251}
-------------------------------

Chunkifying a console reader:

``` {.literal-block}
pipeline(
    ConsoleReader(eol=""),
    Chunkifier(20),
    ConsoleEchoer()
).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#252}
--------------------------------------

Messages received on the \"inbox\" are buffered until at least N bytes
have been collected. A message containing those first N bytes is sent
out \"outbox\". A CharacterFIFO object is used to do this in linear
time.

The usual sending of a producerFinished/shutdown to the \"control\"
inbox will shut it down.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.html){.reference}.[Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier.Chunkifier.html){.reference}
===============================================================================================================================================================================================================================================================================

::: {.section}
class Chunkifier([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Chunkifier}
--------------------------------------------------------------------------------------------------

Chunkifier(\[chunksize\]) -\> new Chunkifier component.

Flow controller - collects incoming data and outputs it only as quanta
of a given length in bytes (chunksize), unless the input stream ends
(producerFinished).

Keyword arguments: - chunksize \-- Chunk size in bytes - nodelay \-- if
set to True, partial chunks will be output rather than buffering up data
while waiting for more to arrive.

::: {.section}
### [Inboxes]{#symbol-Chunkifier.Inboxes}

-   **control** : Shut me down
-   **inbox** : Data stream to be split into chunks
:::

::: {.section}
### [Outboxes]{#symbol-Chunkifier.Outboxes}

-   **outbox** : Each message is a chunk
-   **signal** : I\'ve shut down
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
#### [\_\_init\_\_(self\[, chunksize\]\[, nodelay\])]{#symbol-Chunkifier.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-Chunkifier.main}
:::

::: {.section}
#### [sendChunk(self)]{#symbol-Chunkifier.sendChunk}
:::

::: {.section}
#### [sendPartialChunk(self)]{#symbol-Chunkifier.sendPartialChunk}
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
