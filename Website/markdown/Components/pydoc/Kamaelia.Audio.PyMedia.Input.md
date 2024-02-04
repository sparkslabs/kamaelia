---
pagename: Components/pydoc/Kamaelia.Audio.PyMedia.Input
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}.[Input](/Components/pydoc/Kamaelia.Audio.PyMedia.Input.html){.reference}
================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Input](/Components/pydoc/Kamaelia.Audio.PyMedia.Input.Input.html){.reference}**
:::

-   [Audio Capture using PyMedia](#540){.reference}
    -   [Example Usage](#541){.reference}
    -   [How does it work?](#542){.reference}
:::

::: {.section}
Audio Capture using PyMedia {#540}
===========================

This component captures raw audio using the pymedia library, and outputs
it out of its \"outbox\" outbox.

::: {.section}
[Example Usage]{#example-usage} {#541}
-------------------------------

Recording telephone quality audio to a file:

``` {.literal-block}
Pipeline( Input(sample_rate=8000, channels=1, format="S16_LE"),
          SimpleFileWriter("recording.raw"),
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#542}
--------------------------------------

Input uses the PyMedia library to capture audio from the currently
selected audio capture device.

It outputs to its \"outbox\" outbox raw binary audio data in strings.

This component supports sending to a size limited inbox. If the size
limited inbox is full, this component will pause until it is able to
send out the data.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}.[Input](/Components/pydoc/Kamaelia.Audio.PyMedia.Input.html){.reference}.[Input](/Components/pydoc/Kamaelia.Audio.PyMedia.Input.Input.html){.reference}
===============================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Input([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-Input}
-----------------------------------------------------------------------------------------------------------------------------

Input(\[sample\_rate\]\[,channels\]\[,format\]) -\> new Input component.

Captures audio using the PyMedia library and sends the raw audio data
out of its \"outbox\" outbox.

Keyword arguments:

-   sample\_rate \-- Sample rate in Hz (default = 44100)
-   channels \-- Number of channels (default = 2)
-   format \-- Sample format (default = \"S16\_LE\")

::: {.section}
### [Inboxes]{#symbol-Input.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Input.Outboxes}

-   **outbox** : raw audio samples
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self\[, sample\_rate\]\[, channels\]\[, format\])]{#symbol-Input.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Input.main}
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
