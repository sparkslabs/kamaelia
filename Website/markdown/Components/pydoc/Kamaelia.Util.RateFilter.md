---
pagename: Components/pydoc/Kamaelia.Util.RateFilter
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}
==========================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.ByteRate_RequestControl.html){.reference}**
-   **component
    [MessageRateLimit](/Components/pydoc/Kamaelia.Util.RateFilter.MessageRateLimit.html){.reference}**
-   **component
    [OnDemandLimit](/Components/pydoc/Kamaelia.Util.RateFilter.OnDemandLimit.html){.reference}**
-   **component
    [VariableByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.VariableByteRate_RequestControl.html){.reference}**
:::

-   [Message Rate limiting](#168){.reference}
    -   [Example Usage](#169){.reference}
    -   [How does it work?](#170){.reference}
-   [Rate Control](#171){.reference}
    -   [Example Usage](#172){.reference}
    -   [How does it work?](#173){.reference}
-   [Flow limiting by request](#174){.reference}
    -   [Example Usage](#175){.reference}
    -   [How does it work?](#176){.reference}
:::

::: {.section}
These components limit the rate of data flow, either by buffering or by
taking charge and requesting data at a given rate.

::: {.section}
[Message Rate limiting]{#message-rate-limiting} {#168}
-----------------------------------------------

This component buffers incoming messages and limits the rate at which
they are sent on.

::: {.section}
### [Example Usage]{#example-usage} {#169}

Regulating video to a constant framerate, buffering 2 seconds of data
before starting to emit frames:

``` {.literal-block}
Pipeline( RateControlledFileReader(...),
          DiracDecoder(),
          MessageRateLimit(messages_per_second=framerate, buffer=2*framerate),
          VideoOverlay(),
        ).activate()
```
:::

::: {.section}
### [How does it work?]{#how-does-it-work} {#170}

Data items sent to this component\'s \"inbox\" inbox are buffered. Once
the buffer is full, the component starts to emit items at the specified
rate to its \"outbox\" outbox.

If there is a shortage of data in the buffer, then the specified rate of
output will, obviously, not be sustained. Items will be output when they
are available.

The specified rate serves as a ceiling limit - items will never be
emitted faster than that rate, though they may be emitted slower.

Make sure you choose a sufficient buffer size to handle any expected
jitter/temporary shortages of data.

If a producerFinished or shutdownMicroprocess message is received on the
components\' \"control\" inbox, it is sent on out of the \"signal\"
outbox. The component will then immediately terminate.
:::
:::

::: {.section}
[Rate Control]{#rate-control} {#171}
-----------------------------

These components control the rate of a system by requesting data at a
given rate. The \'variable\' version allows this rate to the changed
whilst running.

::: {.section}
### [Example Usage]{#id1} {#172}

Reading from a file at a fixed rate:

``` {.literal-block}
Graphline( ctrl   = ByteRate_RequestControl(rate=1000, chunksize=32),
           reader = PromptedFileReader(filename="myfile", readmode="bytes"),
           linkages = {
                ("ctrl", "outbox") : ("reader","inbox"),
                ("reader", "outbox") : ("self", "outbox"),

                ("self", "control") : ("reader", "control"),
                ("reader", "signal") : ("ctrl", "control"),
                ("ctrl, "signal") : ("self", "signal"),
              }
```

Note that the \"signal\"-\"control\" path goes in the opposite direction
so that when the file is finished reading, the ByteRate\_RequestControl
component receives a shutdown message.

Reading from a file at a varying rate (send new rates to the \"inbox\"
inbox):

``` {.literal-block}
Graphline( ctrl   = VariableByteRate_RequestControl(rate=1000, chunksize=32),
           reader = PromptedFileReader(filename="myfile", readmode="bytes"),
           linkages = {
                  ("self", "inbox") : ("ctrl", "inbox"),
                  ("ctrl", "outbox") : ("reader","inbox"),
                  ("reader", "outbox") : ("self", "outbox"),

                  ("self", "control") : ("reader", "control"),
                  ("reader", "signal") : ("ctrl", "control"),
                  ("ctrl, "signal") : ("self", "signal"),
              }
         ).activate()
```

Note that the \"signal\"-\"control\" path goes in the opposite direction
so that when the file is finished reading, the
VariableByteRate\_RequestControl component receives a shutdown message.
:::

::: {.section}
### [How does it work?]{#id2} {#173}

These components emit from their \"outbox\" outboxes, requests for data
at the specified rate. Each request is an integer specifying the number
of items.

Rates are in no particular units (eg. bitrate, framerate) - you can use
it for whatever purpose you wish. Just ensure your values fit the units
you are working in.

At initialisation, you specify not only the rate, but also the chunk
size or chunk rate. For example, a rate of 12 and chunksize of 4 will
result in 3 requests per second, each for 4 items. Conversely,
specifying a rate of 12 and a chunkrate of 2 will result in 2 requests
per second, each for 6 items.

The rate and chunk size or chunk rate you specify does not have to be
integer or divide into integers. For example, you can specify a rate of
10 and a chunksize of 3. Requests will then be emitted every 0.3
seconds, each for 3 items.

When requests are emitted, they will always be for an integer number of
items. Rounding errors are averaged out over time, and should not
accumulate. Rounding will occur if chunksize, either specified, or
calculated from chunkrate, is non-integer.

At initialisation, you can also specify that chunk \'aggregation\' is
permitted. If permitted, then the component can choose to exceed the
specified chunksize. For example if, for some reason, the component gets
behind, it might aggregate two requests together - the next request will
be for twice as many items.

Another example would be if you, for example, specify a rate of 100 and
chunkrate of 3. The 3 requests emitted every second will then be for 33,
33 and 34 items.

The VariableByteRate\_RequestControl component allows the rate to be
changed on-the-fly. Send a new rate to the component\'s \"inbox\" inbox
and it will be adopted immediately. You cannot change the chunkrate or
chunksize.

The new rate is adopted at the instant it is received. There will be no
glitches in the apparent rate of requests due to your changing the rate.

If a producerFinished or shutdownMicroprocess message is received on the
components\' \"control\" inbox, it is sent on out of the \"signal\"
outbox. The component will then immediately terminate.
:::
:::

::: {.section}
[Flow limiting by request]{#flow-limiting-by-request} {#174}
-----------------------------------------------------

This component buffers incoming data and emits it one item at a time,
whenever a \"NEXT\" request is received.

::: {.section}
### [Example Usage]{#id3} {#175}

An app that reads data items from a file, then does something with then
one at a time when the user clicks a visual button in pygame:

``` {.literal-block}
Graphline( source   = RateControlledFileReader(..., readmode="lines"),
           limiter  = OnDemandLimit(),
           trigger  = Button(caption="Click for next",msg="NEXT"),
           dest     = consumer(...),
           linkages = {
                   ("source", "outbox") : ("limiter", "inbox"),
                   ("limiter", "outbox") : ("dest", "inbox"),
                   ("trigger", "outbox") : ("limiter", "slidecontrol")
               }
         ).activate()
```
:::

::: {.section}
### [How does it work?]{#id4} {#176}

Data items sent to the component\'s \"inbox\" inbox are buffered in a
queue. Whenever a \"NEXT\" message is received on the component\'s
\"slidecontrol\" inbox, an item is taken out of the queue and sent out
of the \"outbox\" outbox.

Items come out in the same order they go in.

If a \"NEXT\" message is received but there are no items waiting in the
queue, the \"NEXT\" message is discarded and nothing is emitted.

If a producerFinished message is received on the components\'
\"control\" inbox, it is sent on out of the \"signal\" outbox. The
component will then immediately terminate.
:::
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}.[ByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.ByteRate_RequestControl.html){.reference}
==========================================================================================================================================================================================================================================================================================================

::: {.section}
class ByteRate\_RequestControl([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ByteRate_RequestControl}
----------------------------------------------------------------------------------------------------------------

ByteRate\_RequestControl(\[rate\]\[,chunksize\]\[,chunkrate\]\[,allowchunkaggregation\])
-\> new ByteRate\_RequestControl component.

Controls rate of a data source by, at a controlled rate, emitting
integers saying how much data to emit.

Keyword arguments:

-   rate \-- qty of data items per second (default=100000)
-   chunksize \-- None or qty of items per \'chunk\' (default=None)
-   chunkrate \-- None or number of chunks per second (default=10)
-   allowchunkaggregation \-- if True, chunksize will be enlarged if
    \'catching up\' is necessary (default=False)

Specify either chunksize or chunkrate, but not both.

::: {.section}
### [Inboxes]{#symbol-ByteRate_RequestControl.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-ByteRate_RequestControl.Outboxes}

-   **outbox** : requests for \'n\' items
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
#### [\_\_init\_\_(self\[, rate\]\[, chunksize\]\[, chunkrate\]\[, allowchunkaggregation\])]{#symbol-ByteRate_RequestControl.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [getChunksToSend(self)]{#symbol-ByteRate_RequestControl.getChunksToSend}

Generator. Returns the size of chunks to be requested (if any) to
\'catch up\' since last time this method was called.
:::

::: {.section}
#### [main(self)]{#symbol-ByteRate_RequestControl.main}

Main loop.
:::

::: {.section}
#### [resetTiming(self)]{#symbol-ByteRate_RequestControl.resetTiming}

Resets the timing variable used to determine when the next time to send
a request is.
:::

::: {.section}
#### [shutdown(self)]{#symbol-ByteRate_RequestControl.shutdown}

Returns True if shutdown message received.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}.[MessageRateLimit](/Components/pydoc/Kamaelia.Util.RateFilter.MessageRateLimit.html){.reference}
===========================================================================================================================================================================================================================================================================================

::: {.section}
class MessageRateLimit([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-MessageRateLimit}
--------------------------------------------------------------------------------------------------------

MessageRateLimit(messages\_per\_second\[, buffer\]) -\> new
MessageRateLimit component.

Buffers messages and outputs them at a rate limited by the specified
rate once the buffer is full.

Keyword arguments:

-   messages\_per\_second \-- maximum output rate
-   buffer \-- size of buffer (0 or greater) (default=60)

::: {.section}
### [Inboxes]{#symbol-MessageRateLimit.Inboxes}

-   **control** : NOT USED
-   **inbox** : Incoming items/messages
:::

::: {.section}
### [Outboxes]{#symbol-MessageRateLimit.Outboxes}

-   **outbox** : Items/messages limited to specified maximum output rate
-   **signal** : NOT USED
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
#### [\_\_init\_\_(self, messages\_per\_second, buffer, \*\*argd)]{#symbol-MessageRateLimit.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-MessageRateLimit.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}.[OnDemandLimit](/Components/pydoc/Kamaelia.Util.RateFilter.OnDemandLimit.html){.reference}
=====================================================================================================================================================================================================================================================================================

::: {.section}
class OnDemandLimit([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-OnDemandLimit}
-----------------------------------------------------------------------------------------------------

OnDemandLimit() -\> new OnDemandLimit component.

A component that receives data items, but only emits them on demand, one
at a time, when \"NEXT\" messages are received on the \"slidecontrol\"
inbox.

::: {.section}
### [Inboxes]{#symbol-OnDemandLimit.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Data items to be passed on, on demand.
-   **slidecontrol** : \'NEXT\' requests to emit a data item.
:::

::: {.section}
### [Outboxes]{#symbol-OnDemandLimit.Outboxes}

-   **outbox** : Data items, when requested.
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
#### [main(self)]{#symbol-OnDemandLimit.main}

Main loop.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}.[VariableByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.VariableByteRate_RequestControl.html){.reference}
==========================================================================================================================================================================================================================================================================================================================

::: {.section}
class VariableByteRate\_RequestControl([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-VariableByteRate_RequestControl}
------------------------------------------------------------------------------------------------------------------------

ByteRate\_RequestControl(\[rate\]\[,chunksize\]\[,chunkrate\]\[,allowchunkaggregation\])
-\> new ByteRate\_RequestControl component.

Controls rate of a data source by, at a controlled rate, emitting
integers saying how much data to emit. Rate can be changed at runtime.

Keyword arguments: - rate \-- qty of data items per second
(default=100000) - chunksize \-- None or qty of items per \'chunk\'
(default=None) - chunkrate \-- None or number of chunks per second
(default=10) - allowchunkaggregation \-- if True, chunksize will be
enlarged if \'catching up\' is necessary (default=False)

Specify either chunksize or chunkrate, but not both.

::: {.section}
### [Inboxes]{#symbol-VariableByteRate_RequestControl.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : New rate
:::

::: {.section}
### [Outboxes]{#symbol-VariableByteRate_RequestControl.Outboxes}

-   **outbox** : requests for \'n\' items
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
#### [\_\_init\_\_(self\[, rate\]\[, chunksize\]\[, chunkrate\]\[, allowchunkaggregation\])]{#symbol-VariableByteRate_RequestControl.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [changeRate(self, newRate, now)]{#symbol-VariableByteRate_RequestControl.changeRate}

Change the rate.

Guaranteed to not cause a glitch in the rate of output.
:::

::: {.section}
#### [getChunksToSend(self, now)]{#symbol-VariableByteRate_RequestControl.getChunksToSend}

Generator. Returns the size of chunks to be requested (if any) to
\'catch up\' since last time this method was called.
:::

::: {.section}
#### [main(self)]{#symbol-VariableByteRate_RequestControl.main}

Main loop.
:::

::: {.section}
#### [resetTiming(self, now)]{#symbol-VariableByteRate_RequestControl.resetTiming}

Resets the timing variable used to determine when the next time to send
a request is.
:::

::: {.section}
#### [shutdown(self)]{#symbol-VariableByteRate_RequestControl.shutdown}

Returns True if shutdown message received.
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
