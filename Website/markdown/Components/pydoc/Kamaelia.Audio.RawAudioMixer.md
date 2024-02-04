---
pagename: Components/pydoc/Kamaelia.Audio.RawAudioMixer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.html){.reference}
===================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.RawAudioMixer.html){.reference}**
:::

-   [Multi-source Raw Audio Mixer](#549){.reference}
    -   [Example Usage](#550){.reference}
    -   [How does it work?](#551){.reference}
-   [Test documentation](#552){.reference}
:::

::: {.section}
Multi-source Raw Audio Mixer {#549}
============================

A component that mixes raw audio data from an unknown number of sources,
that can change at any time. Audio data from each source is buffered
until a minimum threshold amount, before it is included in the mix. The
mixing operation is a simple addition. Values are not scaled down.

::: {.section}
[Example Usage]{#example-usage} {#550}
-------------------------------

Mixing up to 3 sources of audio (sometimes a source is active, sometimes
it isn\'t):

``` {.literal-block}
Graphline(
    MIXER = RawAudioMixer( sample_rate=8000,
                           channels=1,
                           format="S16_LE",
                           readThreshold=1.0,
                           bufferingLimit=2.0,
                           readInterval=0.1),
                         ),
    A = pipeline( SometimesOn_RawAudioSource(), Entuple(prefix="A") ),
    B = pipeline( SometimesOn_RawAudioSource(), Entuple(prefix="B") ),
    C = pipeline( SometimesOn_RawAudioSource(), Entuple(prefix="C") ),

    OUTPUT = RawSoundOutput( sample_rate=8000,
                             channels=1
                             format="S16_LE",
                           ),
           linkages = {
               (A, "outbox") : (MIXER, "inbox"),
               (B, "outbox") : (MIXER, "inbox"),
               (C, "outbox") : (MIXER, "inbox"),

               (MIXER, "outbox") : (OUTPUT, "inbox"),
           },
         ).run()
```

Each source is buffered for 1 second before it is output. If more than 2
seconds of audio are buffered, then samples are dropped.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#551}
--------------------------------------

Send (id, raw-audio) tuples to RawAudioMixer\'s inbox. Where \'id\' is
any value that uniquely distinguishes each source of audio.

RawAudioMixer buffers each source of audio, and mixes them together
additively, outputting the resulting stream of audio data.

Constructor arguments:

> -   sample\_rate, channels, format The format of audio to be mixed.
>     The only format understood at the moment is \"S16\_LE\"
> -   readThreshold number of seconds of audio that will be buffered
>     before RawAudioMixer starts mixing it into its output.
> -   bufferingLimit maximum number of seconds of audio that will be
>     buffered. If more piles up then some audio will be lost.
> -   readInterval number of seconds between each time RawAudioMixer
>     outputs a chunk of audio data.

RawAudioMixer buffers each source of audio separately. If the amount of
audio in any buffer exceeds the \'buffering limit\' then the oldest
samples buffered will be lost.

When one or more buffered sources reaches the \'read threshold\' then
they are mixed together and output. How often audio is output is
determined by setting the \'read Interval\'.

Mixing is done additively and is *not* scaled down (ie. it is a sum()
function, not an average() ). Therefore, ensure that the sum of the
sources being mixed does not exceed the range of values that samples can
take.

Why the buffering, thresholds, and read intervals? It is done this way
so that RawAudioMixer can mix without needing to know what sources of
audio there are, and whether they are running or stopped. It also
enables RawAudioMixer to cope with audio data arriving from different
sources at different times.

You may introduce new audio sources at any time - simply send audio data
tagged with a new, unique identifier.

You may stop an audio source at any time too - simply stop sending audio
data. The existing buffered data will be output, until there is not
left.

If there is not enough audio in any of the buffers (or perhaps there are
no sources of audio) then RawAudioMixer will not output anything, not
even \'silence\'.

If a shutdownMicroprocess or producerFinished message is received on
this component\'s \"control\" inbox this component will cease reading in
data from any audio sources. If it is currently outputting audio from
any of its buffers, it will continue to do so until these are empty. The
component will then forward on the shutdown message it was sent, out of
its \"signal\" outbox and immediately terminate.

TODO:

> -   Needs a timeout mechanism to discard very old data (otherwise this
>     is effectively a memory leak!)
>     -   If an audio source sends less than the readThreshold amount of
>         audio data, then stops; then this data never gets flushed out.
:::

Test documentation {#552}
==================

Tests passed:

-   Multiple sources of audio will be mixed
-   If there is no input (no incoming audio data), there will be no
    output (no outgoing audio data)
-   A single source of audio will pass through
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.html){.reference}.[RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.RawAudioMixer.html){.reference}
==================================================================================================================================================================================================================================================================================================

::: {.section}
class RawAudioMixer([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-RawAudioMixer}
-------------------------------------------------------------------------------------------------------------------------------------

RawAudioMixer(\[sample\_rate\]\[,channels\]\[,format\]\[,readThreshold\]\[,bufferingLimit\]\[,readInterval\])
-\> new RawAudioMixer component.

Mixes raw audio data from an unknown number of sources, that can change
at any time. Audio data from each source is buffered until a minimum
threshold amount, before it is included in the mix. The mixing operation
is a simple addition. Values are not scaled down.

Send (uniqueSourceIdentifier, audioData) tuples to the \"inbox\" inbox
and mixed audio data will be sent out of the \"outbox\" outbox.

Keyword arguments:

-   sample\_rate \-- The sample rate of the audio in Hz (default=8000)
-   channels \-- Number of channels in the audio (default=1)
-   format \-- Sample format of the audio (default=\"S16\_LE\")
-   readThreshold \-- Duration to buffer audio before it starts being
    used in seconds (default=1.0)
-   bufferingLimit \-- Maximum buffer size for each audio source in
    seconds (default=2.0)
-   readInterval \-- Time between each output chunk in seconds
    (default=0.1)

::: {.section}
### [Inboxes]{#symbol-RawAudioMixer.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-RawAudioMixer.Outboxes}
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
#### [\_\_init\_\_(self\[, sample\_rate\]\[, channels\]\[, format\]\[, readThreshold\]\[, bufferingLimit\]\[, readInterval\])]{#symbol-RawAudioMixer.__init__}
:::

::: {.section}
#### [checkForShutdown(self)]{#symbol-RawAudioMixer.checkForShutdown}
:::

::: {.section}
#### [fillBuffer(self, buffers, data)]{#symbol-RawAudioMixer.fillBuffer}
:::

::: {.section}
#### [main(self)]{#symbol-RawAudioMixer.main}
:::

::: {.section}
#### [mix\_S16\_LE(self, sources, amount)]{#symbol-RawAudioMixer.mix_S16_LE}
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
