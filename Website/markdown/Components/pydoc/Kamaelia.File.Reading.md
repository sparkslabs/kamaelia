---
pagename: Components/pydoc/Kamaelia.File.Reading
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}
====================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **prefab
    [FixedRateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.FixedRateControlledReusableFileReader.html){.reference}**
-   **component
    [PromptedFileReader](/Components/pydoc/Kamaelia.File.Reading.PromptedFileReader.html){.reference}**
-   **prefab
    [RateControlledFileReader](/Components/pydoc/Kamaelia.File.Reading.RateControlledFileReader.html){.reference}**
-   **prefab
    [RateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.RateControlledReusableFileReader.html){.reference}**
-   **prefab
    [ReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.ReusableFileReader.html){.reference}**
-   **component
    [SimpleReader](/Components/pydoc/Kamaelia.File.Reading.SimpleReader.html){.reference}**
:::

-   [Components for reading from files](#678){.reference}
    -   [PromptedFileReader](#679){.reference}
        -   [Example Usage](#680){.reference}
        -   [More detail](#681){.reference}
    -   [SimpleReader](#682){.reference}
        -   [Example Usage](#683){.reference}
        -   [More detail](#684){.reference}
    -   [RateControlledFileReader](#685){.reference}
        -   [Example Usage](#686){.reference}
        -   [More detail](#687){.reference}
    -   [ReusableFileReader](#688){.reference}
        -   [Example Usage](#689){.reference}
        -   [More detail](#690){.reference}
    -   [RateControlledReusableFileReader](#691){.reference}
        -   [Example Usage](#692){.reference}
        -   [More detail](#693){.reference}
    -   [FixedRateControlledReusableFileReader](#694){.reference}
        -   [Example Usage](#695){.reference}
        -   [More detail](#696){.reference}
    -   [Development history](#697){.reference}
:::

::: {.section}
Components for reading from files {#678}
=================================

These components provide various ways to read from files, such as manual
control of the rate at which the file is read, or reusing a file reader
to read from multiple files.

Key to this is a file reader component that reads data only when asked
to. Control over when data flows is therefore up to another component -
be that a simple component that requests data at a constant rate, or
something else that only requests data when required.

::: {.section}
[PromptedFileReader]{#promptedfilereader} {#679}
-----------------------------------------

This component reads bytes or lines from the specified file when
prompted.

Send the number of bytes/lines to the \"inbox\" inbox, and that data
will be read and sent to the \"outbox\" outbox.

::: {.section}
### [Example Usage]{#example-usage} {#680}

Reading 1000 bytes per second in 10 byte chunks from \'myfile\':

``` {.literal-block}
Pipeline(ByteRate_RequestControl(rate=1000,chunksize=10)
         PromptedFileReader("myfile", readmode="bytes")
        ).activate()
```
:::

::: {.section}
### [More detail]{#more-detail} {#681}

The component will terminate if it receives a shutdownMicroprocess
message on its \"control\" inbox. It will pass the message on out of its
\"signal\" outbox.

If unable to read all N bytes/lines requested (perhaps because we are
nearly at the end of the file) then those bytes/lines that were read
successfully are still output.

When the end of the file is reached, a producerFinished message is sent
to the \"signal\" outbox.

The file is opened only when the component is activated (enters its main
loop).

The file is closed when the component shuts down.
:::
:::

::: {.section}
[SimpleReader]{#simplereader} {#682}
-----------------------------

This is a simplified file reader that simply reads the given file and
spits it out \"outbox\". It also handles maximum pipewidths, enabling
rate limiting to be handled by a piped component.

::: {.section}
### [Example Usage]{#id1} {#683}

Usage is the obvious:

``` {.literal-block}
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.Reading import SimpleReader
from Kamaelia.Util.Console import ConsoleEchoer

Pipeline(
    SimpleReader("/etc/fstab"),
    ConsoleEchoer(),
).run()
```
:::

::: {.section}
### [More detail]{#id2} {#684}

This component will terminate if it receives a shutdownMicroprocess
message on its \"control\" inbox. It will pass the message on out of its
\"signal\" outbox.

If unable to send the message to the recipient (due to the recipient
enforcing pipewidths) then the reader pauses until the recipient is
ready and resends (or a shutdown message is recieved).

The file is opened only when the component is activated (enters its main
loop).

The file is closed when the component shuts down.
:::
:::

::: {.section}
[RateControlledFileReader]{#ratecontrolledfilereader} {#685}
-----------------------------------------------------

This component reads bytes/lines from a file at a specified rate. It is
performs the same task as the ReadFileAdapter component.

You can configure the rate, and the chunk size or frequency.

::: {.section}
### [Example Usage]{#id3} {#686}

Read 10 lines per second, in 2 chunks of 5 lines, and output them to the
console:

``` {.literal-block}
Pipeline(RateControlledFileReader("myfile", "lines", rate=10, chunksize=5),
         ConsoleEchoer()
        ).activate()
```
:::

::: {.section}
### [More detail]{#id4} {#687}

This component is a composition of a PromptedFileReader component and a
ByteRate\_RequestControl component.

The component will shut down after all data is read from the file,
emitting a producerFinished message from its \"signal\" outbox.

The component will terminate if it receives a shutdownMicroprocess
message on its \"control\" inbox. It will pass the message on out of its
\"signal\" outbox.

The inbox \"inbox\" is not wired and therefore does nothing.
:::
:::

::: {.section}
[ReusableFileReader]{#reusablefilereader} {#688}
-----------------------------------------

A reusable PromptedFileReader component, based on a Carousel component.
Send it a new filename and it will start reading from that file. Do this
as many times as you like.

Send it the number of bytes/lines to read and it will output that much
data, read from the file.

::: {.section}
### [Example Usage]{#id5} {#689}

Read data from a sequence of files, at 1024 bytes/second in 16 byte
chunks:

``` {.literal-block}
playlist = Chooser(["file1","file2","file3", ...]
rate = ByteRate_RequestControl(rate=1024,chunksize=16)
reader = ReusableFileReader("bytes")

playlist.link( (reader, "requestNext"), (playlist,"inbox") )
playlist.link( (playlist,"outbox"), (reader, "next") )

Pipeline(ratecontrol, reader).activate()
```

Or, with the Control-Signal path linked up properly, using the
JoinChooserToCarousel prefab:

``` {.literal-block}
playlist = Chooser(["file1","file2","file3", ...]
rate = ByteRate_RequestControl(rate=1024,chunksize=16)
reader = ReusableFileReader("bytes")

playlistreader = JoinChooserToCarousel(playlist, reader)

Pipeline(ratecontrol, playlistreader).activate()
```
:::

::: {.section}
### [More detail]{#id6} {#690}

Bytes or lines are read from the file on request. Send the number of
bytes/lines to the \"inbox\" inbox, and that data will be read and sent
to the \"outbox\" outbox.

This component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its \"control\" inbox. The message will be
passed on out of its \"signal\" outbox.

No producerFinished or shutdownMicroprocess type messages are sent by
this component between one file and the next.
:::
:::

::: {.section}
[RateControlledReusableFileReader]{#ratecontrolledreusablefilereader} {#691}
---------------------------------------------------------------------

A reusable file reader component, based on a Carousel component. Send it
a filename and the rate you want it to run at, and it will start reading
from that file at that rate. Do this as many times as you like.

::: {.section}
### [Example Usage]{#id7} {#692}

Read data from a sequence of files, at different rates:

``` {.literal-block}
playlist = Chooser([ ("file1",{"rate":1024}),
                     ("file2",{"rate":16}), ...])
reader = RateControlledReusableFileReader("bytes")

playlist.link( (reader, "requestNext"), (playlist,"inbox") )
playlist.link( (playlist,"outbox"), (reader, "next") )

reader.activate()
playlist.activate()
```

Or, with the Control-Signal path linked up properly, using the
JoinChooserToCarousel prefab:

``` {.literal-block}
playlist = Chooser([ ("file1",{"rate":1024}),
                     ("file2",{"rate":16}), ...])
reader = RateControlledReusableFileReader("bytes")

playlistreader = JoinChooserToCarousel(playlist, reader).activate()
```
:::

::: {.section}
### [More detail]{#id8} {#693}

The rate control is performed by a ByteRate\_RequestControl component.
The rate arguments should be those that are accepted by this component.

This component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its \"control\" inbox. The message will be
passed on out of its \"signal\" outbox.

No producerFinished or shutdownMicroprocess type messages are sent by
this component between one file and the next.
:::
:::

::: {.section}
[FixedRateControlledReusableFileReader]{#fixedratecontrolledreusablefilereader} {#694}
-------------------------------------------------------------------------------

A reusable file reader component that reads data from files at a fixed
rate. It is based on a Carousel component.

Send it a new filename and it will start reading from that file. Do this
as many times as you like.

::: {.section}
### [Example Usage]{#id9} {#695}

Read data from a sequence of files, at 10 lines a second:

``` {.literal-block}
playlist = Chooser(["file1", "file2", "file3", ... ])
reader = FixedRateControlledReusableFileReader("lines", rate=10, chunksize=1)

playlist.link( (reader, "requestNext"), (playlist,"inbox") )
playlist.link( (playlist,"outbox"), (reader, "next") )

reader.activate()
playlist.activate()
```

Or, with the Control-Signal path linked up properly, using the
JoinChooserToCarousel prefab:

``` {.literal-block}
playlist = Chooser(["file1", "file2", "file3", ... ])
reader = FixedRateControlledReusableFileReader("lines", rate=10, chunksize=1)

playlistreader = JoinChooserToCarousel(playlist, reader).activate()
```
:::

::: {.section}
### [More detail]{#id10} {#696}

The rate control is performed by a ByteRate\_RequestControl component.
The rate arguments should be those that are accepted by this component.

This component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its \"control\" inbox. The message will be
passed on out of its \"signal\" outbox.

No producerFinished or shutdownMicroprocess type messages are sent by
this component between one file and the next.
:::
:::

::: {.section}
[Development history]{#development-history} {#697}
-------------------------------------------

PromptedFileReader - developed as an alternative to ReadFileAdapter -
prototyped in /Sketches/filereading/ReadFileAdapter.py
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[FixedRateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.FixedRateControlledReusableFileReader.html){.reference}
============================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: FixedRateControlledReusableFileReader {#symbol-FixedRateControlledReusableFileReader}
---------------------------------------------

FixedRateControlledReusableFileReader(readmode, rateargs) -\> reusable
file reader component

A file reading component that can be reused. Based on a carousel - send
a filename to the \"next\" or \"inbox\" inboxes to start reading from
that file.

Data is read at the specified rate.

Keyword arguments: - readmode = \"bytes\" or \"lines\" - rateargs =
arguments for ByteRate\_RequestControl component constructor
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[PromptedFileReader](/Components/pydoc/Kamaelia.File.Reading.PromptedFileReader.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
class PromptedFileReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-PromptedFileReader}
----------------------------------------------------------------------------------------------------------

PromptedFileReader(filename\[,readmode\]) -\> file reading component

Creates a file reader component. Reads N bytes/lines from the file when
N is sent to its inbox.

Keyword arguments:

-   readmode \-- \"bytes\" or \"lines\"

::: {.section}
### [Inboxes]{#symbol-PromptedFileReader.Inboxes}

-   **control** : for shutdown signalling
-   **inbox** : requests to \'n\' read bytes/lines
:::

::: {.section}
### [Outboxes]{#symbol-PromptedFileReader.Outboxes}

-   **outbox** : data output
-   **signal** : outputs \'producerFinished\' after all data has been
    read
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
#### [\_\_init\_\_(self, filename\[, readmode\])]{#symbol-PromptedFileReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-PromptedFileReader.closeDownComponent}

Closes the file handle
:::

::: {.section}
#### [main(self)]{#symbol-PromptedFileReader.main}

Main loop
:::

::: {.section}
#### [readNBytes(self, n)]{#symbol-PromptedFileReader.readNBytes}

readNBytes(n) -\> string containing \'n\' bytes read from the file.

\"EOF\" raised if the end of the file is reached and there is no data to
return.
:::

::: {.section}
#### [readNLines(self, n)]{#symbol-PromptedFileReader.readNLines}

readNLines(n) -\> string containing \'n\' lines read from the file.

\"EOF\" raised if the end of the file is reached and there is no data to
return.
:::

::: {.section}
#### [shutdown(self)]{#symbol-PromptedFileReader.shutdown}

Returns True if a shutdownMicroprocess message is received.

Also passes the message on out of the \"signal\" outbox.
:::
:::

::: {.section}
:::
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[RateControlledFileReader](/Components/pydoc/Kamaelia.File.Reading.RateControlledFileReader.html){.reference}
==================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: RateControlledFileReader {#symbol-RateControlledFileReader}
--------------------------------

RateControlledFileReader(filename\[,readmode\]\[,\*\*rateargs\]) -\>
constant rate file reader

Creates a PromptedFileReader already linked to a
ByteRate\_RequestControl, to control the rate of file reading.

Keyword arguments:

-   readmode \-- \"bytes\" or \"lines\"
-   rateargs \-- arguments for ByteRate\_RequestControl component
    constructor
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[RateControlledReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.RateControlledReusableFileReader.html){.reference}
==================================================================================================================================================================================================================================================================================================================

::: {.section}
prefab: RateControlledReusableFileReader {#symbol-RateControlledReusableFileReader}
----------------------------------------

RateControlledReusableFileReader(readmode) -\> rate controlled reusable
file reader component.

A file reading component that can be reused. Based on a Carousel - send
(filename, rateargs) to the \"next\" inbox to start reading from that
file at the specified rate.

-   rateargs are the arguments for a ByteRate\_RequestControl component.

Keyword arguments: - readmode = \"bytes\" or \"lines\"
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[ReusableFileReader](/Components/pydoc/Kamaelia.File.Reading.ReusableFileReader.html){.reference}
======================================================================================================================================================================================================================================================================================

::: {.section}
prefab: ReusableFileReader {#symbol-ReusableFileReader}
--------------------------

ReusableFileReader(readmode) -\> reusable file reader component.

A file reading component that can be reused. Based on a Carousel - send
a filename to the \"next\" inbox to start reading from that file.

Must be prompted by another component - send the number of bytes/lines
to read to the \"inbox\" inbox.

Keyword arguments: - readmode = \"bytes\" or \"lines\"
:::

[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[Reading](/Components/pydoc/Kamaelia.File.Reading.html){.reference}.[SimpleReader](/Components/pydoc/Kamaelia.File.Reading.SimpleReader.html){.reference}
==========================================================================================================================================================================================================================================================================

::: {.section}
class SimpleReader([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-SimpleReader}
----------------------------------------------------------------------------------------------------

SimpleReader(filename\[,mode\]\[,buffering\]) -\> simple file reader

Creates a \"SimpleReader\" component.

Arguments:

-   filename \-- Name of the file to read
-   mode \-- This is the python readmode. Defaults to \"r\". (you may
    way \"rb\" occasionally)
-   buffering \-- The python buffer size. Defaults to 1. (see
    <http://www.python.org/doc/2.5.2/lib/built-in-funcs.html>)

::: {.section}
### [Inboxes]{#symbol-SimpleReader.Inboxes}
:::

::: {.section}
### [Outboxes]{#symbol-SimpleReader.Outboxes}
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
#### [\_\_init\_\_(self, filename, \*\*argd)]{#symbol-SimpleReader.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [main(self)]{#symbol-SimpleReader.main}

Main loop Simply opens the file, loops through it (using \"for\"),
sending data to \"outbox\". If the recipient has a maximum pipewidth it
handles that eventuallity resending by pausing and waiting for the
recipient to be able to recieve.

Shutsdown on shutdownMicroprocess.
:::

::: {.section}
#### [shutdown(self)]{#symbol-SimpleReader.shutdown}

Returns True if a shutdownMicroprocess message is received.

Also passes the message on out of the \"signal\" outbox.
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
