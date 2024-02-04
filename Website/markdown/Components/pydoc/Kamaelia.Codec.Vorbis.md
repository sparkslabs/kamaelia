---
pagename: Components/pydoc/Kamaelia.Codec.Vorbis
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Vorbis](/Components/pydoc/Kamaelia.Codec.Vorbis.html){.reference}
=====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.Codec.Vorbis.AOAudioPlaybackAdaptor.html){.reference}**
-   **component
    [VorbisDecode](/Components/pydoc/Kamaelia.Codec.Vorbis.VorbisDecode.html){.reference}**
:::
:::

::: {.section}
Simple Vorbis Decoder Component, and Audio Playback Adaptor
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Vorbis](/Components/pydoc/Kamaelia.Codec.Vorbis.html){.reference}.[AOAudioPlaybackAdaptor](/Components/pydoc/Kamaelia.Codec.Vorbis.AOAudioPlaybackAdaptor.html){.reference}
===============================================================================================================================================================================================================================================================================================

::: {.section}
class AOAudioPlaybackAdaptor([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-AOAudioPlaybackAdaptor}
--------------------------------------------------------------------------------------------------------------

AOAudioPlaybackAdaptor() -\> new AOAudioPlaybackAdaptor

Expects to recieve data from standard inbox, and plays it using libao.
When it recieves a message on the control port: Sends a producerConsumed
to its outbox. Then shutsdown.

**Requires** libao and pyao (python bindings)

**Example**

A simple player:

``` {.literal-block}
Pipeline(
    ReadFileAdaptor("somefile.ogg"),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
```

::: {.section}
### [Inboxes]{#symbol-AOAudioPlaybackAdaptor.Inboxes}

-   **control** : If a message is received here, the component shutsdown
-   **inbox** : Any raw PCM encoded data recieved here is played through
    the default oss playback device
:::

::: {.section}
### [Outboxes]{#symbol-AOAudioPlaybackAdaptor.Outboxes}

-   **outbox** : UNUSED
-   **signal** : When the component shutsdown, it sends a
    producerFinished message out this outbox
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
#### [\_\_init\_\_(self)]{#symbol-AOAudioPlaybackAdaptor.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-AOAudioPlaybackAdaptor.main}

Performs the logic described above
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[Vorbis](/Components/pydoc/Kamaelia.Codec.Vorbis.html){.reference}.[VorbisDecode](/Components/pydoc/Kamaelia.Codec.Vorbis.VorbisDecode.html){.reference}
===========================================================================================================================================================================================================================================================================

::: {.section}
class VorbisDecode([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-VorbisDecode}
----------------------------------------------------------------------------------------------------

VorbisDecode() -\> new VorbisDecoder

A Vorbis decoder accepts data on its inbox \"inbox\", as would be read
from an ogg vorbis file, decodes it and sends on the decompressed data
on out of its outbox \"outbox\". It doesn\'t provide any further
information at this stage, such as bitrate, or any other frills.

**Requires** libvorbissimple and python bindings (see kamaelia
downloads)

**Example**

A simple player:

``` {.literal-block}
Pipeline(
    ReadFileAdaptor("somefile.ogg"),
    VorbisDecode(),
    AOAudioPlaybackAdaptor(),
).run()
```

This component expects to recieve OGG VORBIS data as you would get from
a .ogg file containing vorbis data. (rather than raw vorbis data)

::: {.section}
### [Inboxes]{#symbol-VorbisDecode.Inboxes}

-   **control** : Receiving a message here causes component shutdown
-   **inbox** : Ogg wrapped vorbis data
:::

::: {.section}
### [Outboxes]{#symbol-VorbisDecode.Outboxes}

-   **outbox** : As data is decompresessed it is sent to this outbox
-   **signal** : When the component shuts down, it sends on a
    producerFinished message
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
#### [\_\_init\_\_(self)]{#symbol-VorbisDecode.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-VorbisDecode.main}

This contains no user serviceable parts :-)

Theory of operation is simple. It simply repeatedly asks the decoder
object for audio. That decoded audio is sent to the component\'s outbox.
If the decoder object responds with RETRY, the component retries. If the
decoder object responds with NEEDDATA, the component waits for data on
any inbox until some is available (from an inbox)
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
