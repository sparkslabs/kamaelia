---
pagename: Components/pydoc/Kamaelia.Util.RateFilter.VariableByteRate_RequestControl
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Util](/Components/pydoc/Kamaelia.Util.html){.reference}.[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}.[VariableByteRate\_RequestControl](/Components/pydoc/Kamaelia.Util.RateFilter.VariableByteRate_RequestControl.html){.reference}
==========================================================================================================================================================================================================================================================================================================================

For examples and more explanations, see the [module level
docs.](/Components/pydoc/Kamaelia.Util.RateFilter.html){.reference}

------------------------------------------------------------------------

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
