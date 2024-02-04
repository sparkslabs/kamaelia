---
pagename: Components/pydoc/Kamaelia.Util.RateChunker
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.html){.reference}
============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.RateChunker.html){.reference}**
:::

-   [Breaks data into chunks matching a required chunk
    rate](#235){.reference}
    -   [Example Usage](#236){.reference}
    -   [Behaviour](#237){.reference}
:::

::: {.section}
Breaks data into chunks matching a required chunk rate {#235}
======================================================

Send data, such as binary strings to this component and it will break it
down to roughly constant sized chunks, to match a required \'rate\' of
chunk emission.

This is not about \'real time\' chunking of a live data source, but is
instead about precisely chunking data that you know has been generated,
or will be consumed, at a particular rate.

You specify the \'rate\' of the incoming data and the rate you want
chunks sent out at. RateChunker will determine what size the chunks need
to be, applying dynamic rounding to precisely match the rate without
drift over time.

::: {.section}
[Example Usage]{#example-usage} {#236}
-------------------------------

Chunking a stream of 48KHz 16bit stereo audio into 25 chunks per second
of audio data (one chunk for each frame of a corresponding piece of
25fps video):

``` {.literal-block}
bps = bytesPerSample = 2*2

Pipeline( AudioSource(),
          RateChunker(datarate=48000*bps, quantasize=bps, chunkrate=25),
          ...
        )
```

The quanta size ensures that the chunks RateChunker sends out always
contain a whole number of samples (4 bytes per sample).
:::

::: {.section}
[Behaviour]{#behaviour} {#237}
-----------------------

At initialisation, specify:

> -   the rate of the incoming data (eg. bytes/second)
> -   the required rate of outgoing chunks of data
> -   the minimum quanta size (see below)

Send slicable data items, such as strings containing binary data to the
\"inbox\" inbox. The same data is sent out of the \"outbox\" outbox,
rechunked to meet the required chunk rate.

The outgoing chunk sizes are dynamically varied to match the required
chunk rate as accurately as possible. The quantasize parameter dictates
the minimum unit by which the chunksize will be varied.

For example, for 16bit stereo audio data, there are 4 bytes per sample,
so a quantasize of 4 should be specified, to make sure samples remain
whole.

If a producerFinished or shutdownMicroprocess message is received on the
\"control\" inbox. It is immediately sent on out of the \"signal\"
outbox and the component then immediately terminates.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.html){.reference}.[RateChunker](/Components/pydoc/Kamaelia.Util.RateChunker.RateChunker.html){.reference}
====================================================================================================================================================================================================================================================================================

::: {.section}
class RateChunker([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-RateChunker}
---------------------------------------------------------------------------------------------------

RateChunker(datarate,quantasize,chunkrate) -\> new Chunk component.

Alters the chunksize of incoming data to match a desired chunkrate.

Keyword arguments:

-   datarate \-- rate of the incoming data
-   quantasize \-- minimum granularity with which the data can be split
-   chunkrate \-- desired chunk rate

::: {.section}
### [Inboxes]{#symbol-RateChunker.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items
:::

::: {.section}
### [Outboxes]{#symbol-RateChunker.Outboxes}

-   **outbox** : Rechunked data items
-   **signal** : Shutdown signalling
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
#### [\_\_init\_\_(self, datarate, quantasize, chunkrate)]{#symbol-RateChunker.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [checkShutdown(self)]{#symbol-RateChunker.checkShutdown}
:::

::: {.section}
#### [main(self)]{#symbol-RateChunker.main}

Main loop
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
