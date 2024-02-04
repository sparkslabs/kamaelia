---
pagename: Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Audio.Codec.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.html){.reference}.[Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.html){.reference}
=================================================================================================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.Decoder.html){.reference}**
:::

-   [Compressed audio decoding using PyMedia](#543){.reference}
    -   [Example Usage](#544){.reference}
    -   [How does it work?](#545){.reference}
:::

::: {.section}
Compressed audio decoding using PyMedia {#543}
=======================================

Decodes compressed audio data sent to its \"inbox\" inbox and outputs
the raw audio data from its \"outbox\" outbox. Decoding done using the
PyMedia library.

::: {.section}
[Example Usage]{#example-usage} {#544}
-------------------------------

Playing a MP3 file, known to be 128bkps, 44100Hz 16bit stereo:

``` {.literal-block}
Pipeline( RateControlledFileReader("my.mp3", readmode="bytes", rate=128*1024/8),
          Decoder("mp3"),
          Output(44100, 2, "S16_LE"),
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#545}
--------------------------------------

Set up Decoder by specifying the filetype/codec to the initializer. What
codecs are supported depends on your PyMedia installation.

Send raw binary data strings containing the compressed audio data to the
\"inbox\" inbox, and raw binary data strings containing the uncompressed
raw audio data will be sent out of the \"outbox\" outbox.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Audio.Codec.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.html){.reference}.[Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.html){.reference}.[Decoder](/Components/pydoc/Kamaelia.Audio.Codec.PyMedia.Decoder.Decoder.html){.reference}
============================================================================================================================================================================================================================================================================================================================================================================================================================================

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
