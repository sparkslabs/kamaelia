---
pagename: Components/pydoc/Kamaelia.Codec.WAV.WAVParser
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[WAV](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}.[WAVParser](/Components/pydoc/Kamaelia.Codec.WAV.WAVParser.html){.reference}
============================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}

------------------------------------------------------------------------

::: {.section}
class WAVParser([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-WAVParser}
-------------------------------------------------------------------------------------------------

WAVParser() -\> new WAVParser component.

Send WAV format audio file data to its \"inbox\" inbox, and the raw
audio data will be sent out of the \"outbox\" outbox as binary strings.
The format of the audio data is also sent out of other outboxes as soon
as it is determined (before the data starts to flow).

::: {.section}
### [Inboxes]{#symbol-WAVParser.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Raw WAV file data
:::

::: {.section}
### [Outboxes]{#symbol-WAVParser.Outboxes}

-   **signal** : Shutdown signalling
-   **sample\_format** : Sample format of the audio (eg. \'S16\_LE\')
-   **channels** : Number of channels in the audio
-   **all\_meta** : Dict of \'sample\_format\', \'sample\_rate\', and
    \'channels\'
-   **sample\_rate** : The sample rate of the audio
-   **outbox** : Binary audio data strings
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
#### [\_\_init\_\_(self)]{#symbol-WAVParser.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkShutdown(self)]{#symbol-WAVParser.checkShutdown}

Collects any new shutdown messages arriving at the \"control\" inbox,
and returns \"NOW\" if immediate shutdown is required, or \"WHENEVER\"
if the component can shutdown when it has finished processing pending
data.
:::

::: {.section}
#### [main(self)]{#symbol-WAVParser.main}
:::

::: {.section}
#### [readbytes(self, size)]{#symbol-WAVParser.readbytes}

Generator.

Read the specified number of bytes from the stream of chunks of binary
string data arriving at the \"inbox\" inbox.

Any excess data is placed into self.remainder ready for the next call to
self.readline or self.readbytes.

Data is only read from the inbox when required. It is not preemptively
fetched.

The read data is placed into self.bytesread

If a shutdown is detected, self.bytesread is set to \"\" and this
generator immediately returns.
:::

::: {.section}
#### [readline(self)]{#symbol-WAVParser.readline}

Generator.

Read up to the next newline char from the stream of chunks of binary
string data arriving at the \"inbox\" inbox.

Any excess data is placed into self.remainder ready for the next call to
self.readline or self.readbytes.

Data is only read from the inbox when required. It is not preemptively
fetched.

The read data is placed into self.bytesread

If a shutdown is detected, self.bytesread is set to \"\" and this
generator immediately returns.
:::

::: {.section}
#### [readuptobytes(self, size)]{#symbol-WAVParser.readuptobytes}

Generator.

Reads up to the specified number of bytes from any remainder, or (if
there is no remainder) the next string that arrives at the \"inbox\"
inbox

Any excess data is placed into self.remainder ready for the next call to
self.readline or self.readbytes.

Data is only read from the inbox when required. It is not preemptively
fetched.

The read data is placed into self.bytesread

If a shutdown is detected, self.bytesread is set to \"\" and this
generator immediately returns.
:::

::: {.section}
#### [safesend(self, data, boxname)]{#symbol-WAVParser.safesend}

Generator.

Sends data out of the named outbox. If the destination is full
(noSpaceInBox exception) then it waits until there is space and retries
until it succeeds.

If a shutdownMicroprocess message is received, returns early.
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
