---
pagename: Components/pydoc/Kamaelia.Audio.RawAudioMixer.RawAudioMixer
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.html){.reference}.[RawAudioMixer](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.RawAudioMixer.html){.reference}
==================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Audio.RawAudioMixer.html){.reference}

------------------------------------------------------------------------

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
