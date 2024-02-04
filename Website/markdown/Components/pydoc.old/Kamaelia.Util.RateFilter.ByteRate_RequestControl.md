---
pagename: Components/pydoc.old/Kamaelia.Util.RateFilter.ByteRate_RequestControl
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.Util.RateFilter.ByteRate\_RequestControl
=================================================

class ByteRate\_RequestControl(Axon.Component.component)
--------------------------------------------------------

ByteRate\_RequestControl(\[rate\]\[,chunksize\]\[,chunkrate\]\[,allowchunkaggregation\])
-\> new ByteRate\_RequestControl component.

Controls rate of a data source by, at a controlled rate, emitting
integers saying how much data to emit.

Keyword arguments: - rate \-- qty of data items per second
(default=100000) - chunksize \-- None or qty of items per \'chunk\'
(default=None) - chunkrate \-- None or number of chunks per second
(default=10) - allowchunkaggregation \-- if True, chunksize will be
enlarged if \'catching up\' is necessary (default=False)

Specify either chunksize or chunkrate, but not both.

#### Inboxes

-   control : Shutdown signalling
-   inbox : NOT USED

#### Outboxes

-   outbox : requests for \'n\' items
-   signal : Shutdown signalling

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, rate, chunksize, chunkrate, allowchunkaggregation)

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature

### getChunksToSend(self)

Generator. Returns the size of chunks to be requested (if any) to
\'catch up\' since last time this method was called.

### main(self)

Main loop.

### resetTiming(self)

Resets the timing variable used to determine when the next time to send
a request is.

### shutdown(self)

Returns True if shutdown message received.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
