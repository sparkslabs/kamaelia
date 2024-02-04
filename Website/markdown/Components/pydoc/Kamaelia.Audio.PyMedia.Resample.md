---
pagename: Components/pydoc/Kamaelia.Audio.PyMedia.Resample
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}.[Resample](/Components/pydoc/Kamaelia.Audio.PyMedia.Resample.html){.reference}
======================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Resample](/Components/pydoc/Kamaelia.Audio.PyMedia.Resample.Resample.html){.reference}**
:::

-   [Resampling Audio using PyMedia](#537){.reference}
    -   [Example Usage](#538){.reference}
    -   [How does it work?](#539){.reference}
:::

::: {.section}
Resampling Audio using PyMedia {#537}
==============================

This component resamples raw audio data sent to its \"inbox\" inbox,
changing it to a different sample rate and/or number of channels, and
outputting it from its \"outbox\" outbox. It does this using the pymedia
library.

::: {.section}
[Example Usage]{#example-usage} {#538}
-------------------------------

Capturing CD quality audio and playing it at telephone quality (8KHz,
mono):

``` {.literal-block}
Pipeline( Input(sample_rate=44100, channels=2, format="S16_LE"),
          Resample(44100, 2, 8000, 1),
          Output(sample_rate=8000, channels=1, format="S16_LE"),
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#539}
--------------------------------------

Resample uses the PyMedia library to change the sample rate and/or
number of channels of audio.

Send raw binary audio data strings to its \"inbox\" inbox. It will be
resampled and the resulting raw binary audio data strings are sent out
of its \"outbox\" outbox.

Note that resampling can change the sample rate or number of channels,
but *not* the sample format. The sample format output will be the same
as the input.

Resampling is done by duplicating/dropping samples. No interpolation
takes place. This is therefore not a good quality resample, but it is
reasonably fast.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}.[Resample](/Components/pydoc/Kamaelia.Audio.PyMedia.Resample.html){.reference}.[Resample](/Components/pydoc/Kamaelia.Audio.PyMedia.Resample.Resample.html){.reference}
==============================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Resample([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-Resample}
------------------------------------------------------------------------------------------------

Resample(sample\_rate,channels,to\_sample\_rate,to\_channels) -\> new
Resample component.

Resamples audio to a different sample rate and/or number of channels
using the pymedia library.

Keyword arguments:

-   sample\_rate \-- Input sample rate in Hz
-   channels \-- Input number of channels
-   to\_sample\_rate \-- Desired sample rate in Hz
-   to\_channels \-- Desired number of channels

::: {.section}
### [Inboxes]{#symbol-Resample.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Resample.Outboxes}
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
#### [\_\_init\_\_(self, sample\_rate, channels, to\_sample\_rate, to\_channels)]{#symbol-Resample.__init__}
:::

::: {.section}
#### [main(self)]{#symbol-Resample.main}
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
