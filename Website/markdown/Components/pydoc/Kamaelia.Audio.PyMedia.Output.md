---
pagename: Components/pydoc/Kamaelia.Audio.PyMedia.Output
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}.[Output](/Components/pydoc/Kamaelia.Audio.PyMedia.Output.html){.reference}
==================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [Output](/Components/pydoc/Kamaelia.Audio.PyMedia.Output.Output.html){.reference}**
:::

-   [Audio Playback using PyMedia](#534){.reference}
    -   [Example Usage](#535){.reference}
    -   [How does it work?](#536){.reference}
:::

::: {.section}
Audio Playback using PyMedia {#534}
============================

This component plays raw audio sent to its \"inbox\" inbox using the
pymedia library.

::: {.section}
[Example Usage]{#example-usage} {#535}
-------------------------------

Playing 8KHz 16 bit mono raw audio from a file:

``` {.literal-block}
Pipeline( RateControlledFileReader("recording.raw", readmode="bytes", rate=8000*2/8,
          Output(sample_rate=8000, channels=1, format="S16_LE"),
        ).run()
```
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#536}
--------------------------------------

Output uses the PyMedia library to play back audio to the current audio
playback device.

Send raw binary audio data strings to its \"inbox\" inbox.

This component will terminate if a shutdownMicroprocess or
producerFinished message is sent to the \"control\" inbox. The message
will be forwarded on out of the \"signal\" outbox just before
termination.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Audio](/Components/pydoc/Kamaelia.Audio.html){.reference}.[PyMedia](/Components/pydoc/Kamaelia.Audio.PyMedia.html){.reference}.[Output](/Components/pydoc/Kamaelia.Audio.PyMedia.Output.html){.reference}.[Output](/Components/pydoc/Kamaelia.Audio.PyMedia.Output.Output.html){.reference}
====================================================================================================================================================================================================================================================================================================================================================

::: {.section}
class Output([Axon.ThreadedComponent.threadedcomponent](/Docs/Axon/Axon.ThreadedComponent.threadedcomponent.html){.reference}) {#symbol-Output}
------------------------------------------------------------------------------------------------------------------------------

Output(\[sample\_rate\]\[,channels\]\[,format\]) -\> new Output
component.

Outputs (plays) raw audio data sent to its \"inbox\" inbox using the
PyMedia library.

Keyword arguments:

-   sample\_rate \-- Sample rate in Hz (default = 44100)
-   channels \-- Number of channels (default = 2)
-   format \-- Sample format (default = \"S16\_LE\")

::: {.section}
### [Inboxes]{#symbol-Output.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-Output.Outboxes}
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
#### [\_\_init\_\_(self\[, sample\_rate\]\[, channels\]\[, format\]\[, maximumLag\])]{#symbol-Output.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-Output.main}
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
