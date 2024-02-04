---
pagename: Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.Decoder
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Audio.Codec.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.html){.reference}.[Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.html){.reference}.[Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.Decoder.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.html){.reference}

------------------------------------------------------------------------

::: {.section}
class Decoder([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Decoder}
-----------------------------------------------------------------------------------------------

Decoder(fileExtension) -\> new pymedia Audio Decoder.

Send raw data from a compressed audio file (which had the specified
extension) to the \"inbox\" inbox, and decompressed blocks of raw audio
data are emitted from the \"outbox\" outbox.

Keyword arguments:

-   codec \-- The codec (ones supported depend on your local
    installation)

::: {.section}
### [Inboxes]{#symbol-Decoder.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : compressed audio data
:::

::: {.section}
### [Outboxes]{#symbol-Decoder.Outboxes}

-   **outbox** : raw audio samples
-   **signal** : Shutdown signalling
-   **needData** : requests for more data (value is suggested minimum
    number of bytes
-   **format** : dictionary detailing sample\_rate, sample\_format and
    channels
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
#### [\_\_init\_\_(self, codec)]{#symbol-Decoder.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Decoder.main}
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
