---
pagename: Components/pydoc/Kamaelia.Codec.WAV
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[WAV](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}
===============================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [WAVParser](/Components/pydoc/Kamaelia.Codec.WAV.WAVParser.html){.reference}**
-   **component
    [WAVWriter](/Components/pydoc/Kamaelia.Codec.WAV.WAVWriter.html){.reference}**
:::

-   [Reading and writing simple WAV audio files](#91){.reference}
    -   [Example Usage](#92){.reference}
    -   [WAVParser behaviour](#93){.reference}
    -   [WAVWriter behaviour](#94){.reference}
    -   [Development history](#95){.reference}
:::

::: {.section}
Reading and writing simple WAV audio files {#91}
==========================================

Read and write WAV file format audio data using the WAVParser and
WAVWriter components, respectively.

::: {.section}
[Example Usage]{#example-usage} {#92}
-------------------------------

Playing a WAV file, where we don\'t know the format until we play it:

``` {.literal-block}
from Kamaelia.Audio.PyMedia.Output import Output
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel

def makeAudioOutput(format_info):
    return Output( sample_rate = format_info['sample_rate'],
                   format      = format_info['sample_format'],
                   channels    = format_info['channels']
                 )

Graphline(
    SRC = RateControlledFileReader("test.wav",readmode="bytes",rate=44100*4),
    WAV = WAVParser(),
    DST = Carousel(makeAudioOutput),
    linkages = {
        ("SRC","outbox") : ("WAV","inbox"),
        ("SRC","signal") : ("WAV","control"),
        ("WAV","outbox") : ("DST","inbox"),
        ("WAV","signal") : ("DST","control"),
        ("WAV","all_meta") : ("DST","next"),
    }
    ).run()
```

Capturing audio and writing it to a WAV file:

``` {.literal-block}
from Kamaelia.Audio.PyMedia.Input import Input
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline

Pipeline( Input(sample_rate=44100, channels=2, format="S16_LE"),
          WAVWriter(sample_rate=44100, channels=2, format="S16_LE"),
          SimpleFileWriter("captured_audio.wav"),
        ).run()
```
:::

::: {.section}
[WAVParser behaviour]{#wavparser-behaviour} {#93}
-------------------------------------------

Send binary data as strings containing a WAV file to the \"inbox\"
inbox.

As soon as the format of the audio data is determined (from the headers)
it is sent out the \"all\_meta\" outbox as a dictionary, for example:

``` {.literal-block}
{ "sample_format" : "S16_LE",
  "channels"      : 2,
  "sample_rate"   : 44100,
}
```

The individual components are also sent out the \"sample\_format\",
\"channels\" and \"sample\_rate\" outboxes.

The raw audio data from the incoming WAV data is sent out of the
\"outbox\" outbox, until the end of the WAV file is reached. If the WAV
headers specify an audio size of zero, then it is assumed to be of
indefinite length, otherwise the value is assumed to be the actual size,
and this component will terminate and send out a producerFinished()
message when it thinks it has reached the end.

This component supports sending the raw audio data to a size limited
inbox. If the size limited inbox is full, this component will pause
until it is able to send out the data.

If a producerFinished message is received on the \"control\" inbox, this
component will complete parsing any data pending in its inbox, and
finish sending any resulting data to its outbox. It will then send the
producerFinished message on out of its \"signal\" outbox and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
this component will immediately send it on out of its \"signal\" outbox
and immediately terminate. It will not complete processing, or sending
on any pending data.
:::

::: {.section}
[WAVWriter behaviour]{#wavwriter-behaviour} {#94}
-------------------------------------------

Initialise this component, specifying the format the audio data will be
in.

Send raw audio data (in the format you specified!) as binary strings to
the \"inbox\" inbox, and this component will write it out as WAV file
format data out of the \"outbox\" outbox.

The WAV format headers will immediately be sent out of the \"outbox\"
outbox as soon as this component is initialised and activated (ie.
before you even start sending it audio data to write out). The size of
the audio data is set to zero as the component has no way of knowing the
duration of the audio.

This component supports sending data out of its outbox to a size limited
inbox. If the size limited inbox is full, this component will pause
until it is able to send out the data.

If a producerFinished message is received on the \"control\" inbox, this
component will complete parsing any data pending in its inbox, and
finish sending any resulting data to its outbox. It will then send the
producerFinished message on out of its \"signal\" outbox and terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
this component will immediately send it on out of its \"signal\" outbox
and immediately terminate. It will not complete processing, or sending
on any pending data.
:::

::: {.section}
[Development history]{#development-history} {#95}
-------------------------------------------

WAVWriter is based on code by Ryn Lothian developed during summer 2006.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[WAV](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}.[WAVParser](/Components/pydoc/Kamaelia.Codec.WAV.WAVParser.html){.reference}
============================================================================================================================================================================================================================================================

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

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Codec](/Components/pydoc/Kamaelia.Codec.html){.reference}.[WAV](/Components/pydoc/Kamaelia.Codec.WAV.html){.reference}.[WAVWriter](/Components/pydoc/Kamaelia.Codec.WAV.WAVWriter.html){.reference}
============================================================================================================================================================================================================================================================

::: {.section}
class WAVWriter([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-WAVWriter}
-------------------------------------------------------------------------------------------------

WAVWriter(channels, sample\_format, sample\_rate) -\> new WAVWriter
component.

Send raw audio data as binary strings to the \"inbox\" inbox and WAV
format audio data will be sent out of the \"outbox\" outbox as binary
strings.

::: {.section}
### [Inboxes]{#symbol-WAVWriter.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-WAVWriter.Outboxes}
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
#### [\_\_init\_\_(self, channels, sample\_format, sample\_rate)]{#symbol-WAVWriter.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [canStop(self)]{#symbol-WAVWriter.canStop}
:::

::: {.section}
#### [handleControl(self)]{#symbol-WAVWriter.handleControl}
:::

::: {.section}
#### [main(self)]{#symbol-WAVWriter.main}
:::

::: {.section}
#### [mustStop(self)]{#symbol-WAVWriter.mustStop}
:::

::: {.section}
#### [waitSend(self, data, boxname)]{#symbol-WAVWriter.waitSend}
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
