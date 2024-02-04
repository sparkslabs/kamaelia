---
pagename: Docs/UtilityModules
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Utility Modules]{style="font-size: 24pt; font-weight: 600;"}

This is a small collection of utility components. They perform various
universally useful functions, ranging from Console input and output to
simple data filtering and transformations.

**Console I/O (standard input and output)**\

[Kamaelia.Util.Console](/Components/pydoc/Kamaelia.Util.Console)
contains the ConsoleReader and ConsoleEchoer components for reading from
standard input and writing to standard output respectively.

**Backplanes, Splitters, Fanouts (ways to distribute data to multiple
receipient components)**\

-   [Kamaelia.Util.Backplane](/Components/pydoc/Kamaelia.Util.Backplane)
-   [Kamaelia.Util.Splitter](/Components/pydoc/Kamaelia.Util.Splitter)
-   [Kamaelia.Util.Fanout](/Components/pydoc/Kamaelia.Util.Fanout)

The [Splitter](/Components/pydoc/Kamaelia.Util.Splitter) and
[Fanout](/Components/pydoc/Kamaelia.Util.Fanout) components are both
very similar - send one item of data to them and it gets replicated to
multiple destinations. The Splitter module is the more actively
maintained with a wider range of components in it.

The [Backplane](/Components/pydoc/Kamaelia.Util.Backplane) module built
on them by providing a way to \"publish\" data under a name, and allow
other components to \"subscribe\" to it.

**Data filtering, processing, transforming**\

-   [Kamaelia.Util.Detuple](/Components/pydoc/Kamaelia.Util.Detuple) -
    extract term from a tuple\
-   [Kamaelia.Util.Filter](/Components/pydoc/Kamaelia.Util.Filter) -
    filter data\
-   [Kamaelia.Util.Marshalling](/Components/pydoc/Kamaelia.Util.Marshalling) -
    marshall/demarshall data\
-   [Kamaelia.Util.PureTransformer](/Components/pydoc/Kamaelia.Util.PureTransformer) -
    apply a function to data\
-   [Kamaelia.Util.SequentialTransformer](/Components/pydoc/Kamaelia.Util.SequentialTransformer) -
    apply a sequence of function\
-   [Kamaelia.Util.Stringify](/Components/pydoc/Kamaelia.Util.Stringify) -
    convert data to strings\
-   [Kamaelia.Util.UnseenOnly](/Components/pydoc/Kamaelia.Util.UnseenOnly) -
    only let through unique items

There is a whole range of components for performing simple functions,
ranging from de-tupling data (eg. extracting one of the terms from a
tuple it is sent) to converting data to strings or applying an arbitrary
transformation (function) to data.\

**Processing streams of data**\

-   [Kamaelia.Util.Chunkifier](/Components/pydoc/Kamaelia.Util.Chunkifier)
-   [Kamaelia.Util.ChunkNamer](/Components/pydoc/Kamaelia.Util.ChunkNamer)
-   [Kamaelia.Util.LineSplit](/Components/pydoc/Kamaelia.Util.LineSplit)
-   [Kamaelia.Util.Tokenisation](/Components/pydoc/Kamaelia.Util.Tokenisation)

There are also components for tagging or chunking data or splitting
strings by newline characters or tokenising strings.\
\
**Timing, Regulating and controlling**\

-   [Kamaelia.Util.Chooser](/Components/pydoc/Kamaelia.Util.Chooser)
-   [Kamaelia.Util.Clock](/Components/pydoc/Kamaelia.Util.Clock)
-   [Kamaelia.Util.DataSource](/Components/pydoc/Kamaelia.Util.DataSource)
-   [Kamaelia.Util.LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector)
-   [Kamaelia.Util.RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter)

This fairly maverick bunch of modules contain components that perform
various functions that can be used to control or regulate a system.\
\
[Chooser](/Components/pydoc/Kamaelia.Util.Chooser) components serve up
data one item at a time on demand - a way to iterate through a
collection of data items, values or even instructions.
[DataSource](/Components/pydoc/Kamaelia.Util.DataSource) is a simplified
way of injecting data into a system; and
[LossyConnector](/Components/pydoc/Kamaelia.Util.LossyConnector)
provides a way to \'loose it\' if there is too much clogging up!\
\
[Clock](/Components/pydoc/Kamaelia.Util.Clock) and
[RateFilter](/Components/pydoc/Kamaelia.Util.RateFilter) contain
components for generating or regulating the timing or flow of data - for
example, generating regular timing pulses, or buffering and regulating
the flow of data, perhaps to maintain a frame rate.\
\
\

\-- Matt, April 2007\
