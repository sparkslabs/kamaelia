---
pagename: Components/pydoc/Kamaelia.File.ReadFileAdaptor
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[ReadFileAdaptor](/Components/pydoc/Kamaelia.File.ReadFileAdaptor.html){.reference}
====================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [ReadFileAdaptor](/Components/pydoc/Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor.html){.reference}**
:::

-   [ReadFileAdaptor Component](#698){.reference}
    -   [Example Usage](#699){.reference}
    -   [How to use it](#700){.reference}
    -   [To do](#701){.reference}
:::

::: {.section}
ReadFileAdaptor Component {#698}
=========================

A simple component that reads data from a file, line by line, or in
chunks of bytes, at a constant rate that you specify.

::: {.section}
[Example Usage]{#example-usage} {#699}
-------------------------------

Read one line at a time from a text file every 0.2 seconds, outputting
to standard output:

``` {.literal-block}
Pipeline( ReadFileAdaptor("myfile.text", readmode='line', readsize=1, steptime=0.2),
          ConsoleEchoer(),
        ).run()
```

Read from a file at 1 Kilobits per second, in chunks of 256 bytes and
send it to a server over a TCP network socket:

``` {.literal-block}
Pipeline( ReadFileAdaptor("myfile.data", readmode='bitrate', readsize=1, bitrate=1024*10),
          TCPClient("remoteServer.provider.com", port=1500),
        ).run()
```
:::

::: {.section}
[How to use it]{#how-to-use-it} {#700}
-------------------------------

This component takes input from the outside world, and makes it
available on it\'s outbox. It can take input from the following data
sources:

> -   A specific file
> -   The output of a command
> -   stdin

In all cases, it can make the data available in the following modes:

:   -   On a line by line basis
    -   On a \"block by block\" basis.
    -   At an attempted (not guaranteed) bit rate.
    -   If at a bit rate, also a \"frame rate\". (eg if you want
        1Mbit/s, do you want that as 1x1Mbit block, 4x250Kbit blocks,
        25x 40Kbit blocks, or what, each second?
    -   A \"step time\" to define how often to read 0 == as often/fast
        as possible 0.1 == every 0.1 seconds, 0.5 = every 0.5 seconds, 2
        = every 2 seconds etc.

Clearly some of these modes are mutually exclusive!

Once ReadFileAdaptor has finished reading from the file, it finishes by
sending a producerFinished() message out of its \"signal\" outbox, then
immediately terminates.

There is no way to tell ReadFileAdaptor to prematurely stop. It ignores
all messages sent to its \"control\" inbox.
:::

::: {.section}
[To do]{#to-do} {#701}
---------------

The default standalone behaviour is to read in from stdin, and dump to
stdout in a teletype fashion the data it recieves. It \_may\_ gain
command line parsing at some point, which would be wacky. (And probably
a good way of initialising components - useful standalone & externally)

XXX TODO: Signal EOF on an external output to allow clients to destroy
us. XXX Implement the closeDown method - ideally add to the component
XXX framework.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[ReadFileAdaptor](/Components/pydoc/Kamaelia.File.ReadFileAdaptor.html){.reference}.[ReadFileAdaptor](/Components/pydoc/Kamaelia.File.ReadFileAdaptor.ReadFileAdaptor.html){.reference}
========================================================================================================================================================================================================================================================================================================

::: {.section}
class ReadFileAdaptor([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-ReadFileAdaptor}
-------------------------------------------------------------------------------------------------------

An instance of this class is a read file adaptor component. It\'s
constructor arguments are all optional. If no arguments are provided,
then the default is to read from stdin, one line at a time, as fast as
possible. Note that this will cause the outbox to fill at the same rate
as stdin can provide data. (Be wary of memory constraints this will
cause!)

Arguments & meaning:

:   -   filename=\"filename\" - the name of the file to read. If you
        want stdin, do not provide a filename! If you want the output
        from a command, also leave this blank\...

    -   command=\"command\" - the name of the command you want the
        output from. Leave the filename blank if you use this!

    -   

        readmode - possible values:

        :   -   \"bitrate\" - read at a specified bitrate.
            -   \"line\" - read on a line by line basis
            -   \"block\" - read the file on a block by block basis.

    -   If bitrate mode is set, you should set bitrate= to your desired
        bitrate (unless you want 64Kbit/s), and chunkrate= to your
        desired chunkrate (unless you want 24 fps). You are expected to
        be able to handle the bit rate you request!

    -   If block mode is set then you should set readsize (size of the
        block in bytes), and steptime (how often you want bytes). If
        steptime is set to zero, you will read blocks at the speed the
        source device can provide them. (be wary of memory constraints)

After setting the ReadFileAdaptor in motion, you can then hook it into
your linkages like any other component.

::: {.section}
### [Inboxes]{#symbol-ReadFileAdaptor.Inboxes}

-   **control** : NOT USED
-   **inbox** : NOT USED
:::

::: {.section}
### [Outboxes]{#symbol-ReadFileAdaptor.Outboxes}

-   **outbox** : When data is read, it is made available here.
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
#### [\_\_init\_\_(self\[, filename\]\[, command\]\[, readmode\]\[, readsize\]\[, steptime\]\[, bitrate\]\[, chunkrate\]\[, debug\])]{#symbol-ReadFileAdaptor.__init__}

Standard constructor, see class docs for details
:::

::: {.section}
#### [closeDownComponent(self)]{#symbol-ReadFileAdaptor.closeDownComponent}

\#!!!! Called at component exit\... Closes the file handle
:::

::: {.section}
#### [getDataByteLen(self)]{#symbol-ReadFileAdaptor.getDataByteLen}

This method attempts to read data of a specific block size from the file
handle. If null, the file is EOF. This method is never called directly.
If the readmode is block or bitrate, then the attribute self.getData is
set to this function, and then this function is called using
self.getData(). The reason for this indirection is to make it so that
the check for which readmode we are in is done once, and once only
:::

::: {.section}
#### [getDataReadline(self)]{#symbol-ReadFileAdaptor.getDataReadline}

This method attempts to read a line of data from the file handle. If
null, the file is EOF. As with getDataByteLen, this method is never
called directly. If the readmode is readline (or \"\"), then the
attribute self.getData is set to this function, and then this function
is called using self.getData(). Same reason for indirection as above.
:::

::: {.section}
#### [initialiseComponent(self)]{#symbol-ReadFileAdaptor.initialiseComponent}

Opens the appropriate file handle
:::

::: {.section}
#### [mainBody(self)]{#symbol-ReadFileAdaptor.mainBody}

We check whether it\'s time to perform a new read, if it is, we read
some data. If we get some data, we put it in out outbox \"outbox\", and
to stdout (if debugging). If we had an error state (eg EOF), we return
0, stopping this component, otherwise we return 1 to live for another
line/block.
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
