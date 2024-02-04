---
pagename: Components/pydoc/Kamaelia.File.UnixProcess2
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.html){.reference}
==============================================================================================================================================================================================
:::

::: {.section}
::: {.container}
-   **component
    [UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.UnixProcess2.html){.reference}**
:::

-   [Unix sub processes with communication through
    pipes](#702){.reference}
    -   [How is this different to UnixProcess?](#703){.reference}
    -   [Example Usage](#704){.reference}
    -   [Behaviour](#705){.reference}
    -   [How does it work?](#706){.reference}
    -   [XXX Fix Me](#707){.reference}
:::

::: {.section}
Unix sub processes with communication through pipes {#702}
===================================================

UnixProcess2 allows you to start a separate process and send data to it
and receive data from it using the standard input/output/error pipes and
optional additional named pipes.

This component works on \*nix platforms only. It is almost certainly not
Windows compatible. Tested only under Linux.

::: {.section}
[How is this different to UnixProcess?]{#how-is-this-different-to-unixprocess} {#703}
------------------------------------------------------------------------------

UnixProcess2 differs from UnixProcess in the following ways:

-   UnixProcess2 does not drop data if there is a backlog.
-   UnixProcess2 allows you to set up extra named input and output
    pipes.
-   UnixProcess2 supports sending data to size limited inboxes. The
    subprocess will be blocked if its output is going into an inbox that
    is full. This enables you to use size limited inboxes to regulate
    the subprocess.
-   UnixProcess2 does not take data from its inboxes until it is able to
    deliver it to the subprocess. If the inboxes are set to be size
    limiting, this can therefore be used to limit the rate of execution
    of upstream components.
:::

::: {.section}
[Example Usage]{#example-usage} {#704}
-------------------------------

Using the \'wc\' word count GNU util to count the number of lines in
some data:

``` {.literal-block}
Pipeline( RateControlledFileReader(filename, ... ),
          UnixProcess2("wc -l"),
          ConsoleEchoer(),
        ).run()
```

Feeding separate audio and video streams to ffmpeg, and taking the
encoded output:

``` {.literal-block}
Graphline(
    ENCODER = UnixProcess2( "ffmpeg -i audpipe -i vidpipe -",
                           inpipes = { "audpipe":"audio",
                                       "vidpipe":"video",
                                     },
                           boxsizes = { "audio":2, "video":2 }
                         ),
    VIDSOURCE = MaxSpeedFileReader(...),
    AUDSOURCE = MaxSpeFileReader(...),
    SINK = SimpleFileWriter("encodedvideo"),
    linkages = {
        ("VIDSOURCE","outbox") : ("ENCODER","video"),
        ("AUDSOURCE","outbox") : ("ENCODER","audio"),
        ("ENCODER","outbox") : ("SINK", "inbox"),
        }
    ).run()
```
:::

::: {.section}
[Behaviour]{#behaviour} {#705}
-----------------------

At initialisation, specify:

> -   the command to invoke the sub process
> -   the size limit for internal buffers
> -   additional named input and output pipes
> -   box size limits for any input pipe\'s inbox, including \"inbox\"
>     for STDIN

Named input pipes must all use different inbox names. They must not use
\"inbox\" or \"control\". Named output pipes may use any outbox name
they wish. More than one named ouput pipe can use the same outbox,
including \"outbox\".

The pipe files needed for named pipes are created automatically at
activation and are deleted at termination.

Activate UnixProcess2 and the sub process will be started. Use the
inboxes and outboxes of UnixProcess2 to communicate with the sub
process. For example:

``` {.literal-block}
UnixProcess2( "ffmpeg -i /tmp/inpipe -f wav /tmp/outpipe",
             inpipes  = { "/tmp/inpipe" :"in"  },
             outpipes = { "/tmp/outpipe":"out" },
           )
        ________________________________________________
       |                UnixProcess2                     |
       |             _______________________            |
       |            |   "ffmpeg -i ..."     |           |
---> "inbox" ---> STDIN                  STDOUT ---> "outbox" --->
       |            |                    STDERR ---> "error"  --->
       |            |                       |           |
---> "in"    ---> "/tmp/inpipe"  "/tmp/outpipe" ---> "out"    --->
       |            |_______________________|           |
       |________________________________________________|
```

Send binary string data to the \"inbox\" inbox and it will be sent to
STDIN of the proces.

Binary string data from STDOUT and STDERR is sent out of the \"outbox\"
and \"error\" outboxes respectively.

To send to a named pipe, send binary string data to the respective inbox
you specified.

Data written by the sub process to a named output pipe will be sent out
of the respective outbox.

The specified buffering size sets a maximum limit on the amount of data
that can be buffered on the inputs and outputs to and from the sub
process. It also determines the chunk size in which data coming from the
sub process will emerge. Note therefore that data may languish in an
output buffer indefinitely until the process terminates. Do not assume
that data coming from a sub process will emerge the moment it is
generated.

UnixProcess2 will leave data in its inboxes until it is able to send it
to the required pipe. If a destination box is full (noSpaceInBox
exception) then UnixProces will wait and retry until it succeeds in
sending the data.

If the sub process closes its pipes (STDIN, STDOUT, STDERR) then
UnixProcess2 will close its named input and output pipes too, and will
send a producerFinished message out of its \"signal\" outbox then
immediately terminate.

If a producerFinished message is received on the \"control\" inbox,
UnixProcess2 will finish passing any pending data waiting in inboxes
into the sub process and will finish passing on any pending data waiting
to come from the sub process onto destination outboxes. Once this is
complete, UnixProcess2 will close all pipes and send a producerFinished
message out of its \"signal\" outbox and immediately terminate.

If a shutdownMicroprocess message is received on the \"control\" inbox,
UnixProcess2 will close all pipes as soon as possible and send the
message on out of its \"signal\" outbox and immediately terminate.
:::

::: {.section}
[How does it work?]{#how-does-it-work} {#706}
--------------------------------------

The UnixProcess2 component itself is primarily just the initiator of the
sub process and a container for other child components that handle the
actual I/O with pipes. It uses \_ToFileHandle and \_FromFileHandle
components for each input and output pipe respectively.

For each specified named pipe, the specified pipe file is created if
required (using mkfifo).

The shutdown signalling boxes of all child components are daisy chained.
Shutdown messages sent to the \"control\" inbox of UnixProcess2 are
routed to the \"control\" inbox of the component handling STDIN. The
shutdown message is then propagated to named output pipes and then named
input pipes.

If STDOUT close it causes STDERR to close. If STDERR closes then the
shutdown message is propagated to STDIN and then onto named pipes as
described above.

When the process exits, it is assumed the STDIN, STDOUT and STDERR will
close by themselves in due course. However an explicit shutdown message
is sent to the named pipes.
:::

::: {.section}
[XXX Fix Me]{#xxx-fix-me} {#707}
-------------------------

If UnixProcess2 is terminated by receiving shutdown messages, it
doesn\'t currently explicitly terminate the sub process.
:::
:::

------------------------------------------------------------------------

::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[File](/Components/pydoc/Kamaelia.File.html){.reference}.[UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.html){.reference}.[UnixProcess2](/Components/pydoc/Kamaelia.File.UnixProcess2.UnixProcess2.html){.reference}
=========================================================================================================================================================================================================================================================================================

::: {.section}
class UnixProcess2([Axon.Component.component](/Docs/Axon/Axon.Component.component.html){.reference}) {#symbol-UnixProcess2}
----------------------------------------------------------------------------------------------------

UnixProcess2(command\[,buffersize\]\[,outpipes\]\[,inpipes\]\[,boxsizes\])
-\> new UnixProcess2 component.

Starts the specified command as a separate process. Data can be sent to
stdin and received from stdout. Named pipes can also be created for
extra channels to get data to and from the process.

Keyword arguments:

``` {.literal-block}
- command     -- command line string that will invoke the subprocess
- buffersize  -- bytes size of buffers on the pipes to and from the process (default=32768)
- outpipes    -- dict mapping named-pipe-filenames to outbox names (default={})
- inpipes     -- dict mapping named-pipe-filenames to inbox names (default={})
- boxsizes    -- dict mapping inbox names to box sizes (default={})
```

::: {.section}
### [Inboxes]{#symbol-UnixProcess2.Inboxes}

-   **control** : Shutdown signalling
-   **inbox** : Binary string data to go to STDIN of the process.
:::

::: {.section}
### [Outboxes]{#symbol-UnixProcess2.Outboxes}

-   **outbox** : Binary string data from STDOUT of the process
-   **signal** : Shutdown signalling
-   **\_shutdownPipes** : For shutting down any named pipes used for
    output
-   **error** : Binary string data from STDERR of the process
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
#### [\_\_init\_\_(self, command\[, buffersize\]\[, outpipes\]\[, inpipes\]\[, boxsizes\])]{#symbol-UnixProcess2.__init__}

x.\_\_init\_\_(\...) initializes x; see x.\_\_class\_\_.\_\_doc\_\_ for
signature
:::

::: {.section}
#### [childrenDone(self)]{#symbol-UnixProcess2.childrenDone}

Unplugs any children that have terminated, and returns true if there are
no running child components left (ie. their microproceses have finished)
:::

::: {.section}
#### [main(self)]{#symbol-UnixProcess2.main}

main loop
:::

::: {.section}
#### [setupNamedInPipes(self, pipeshutdown)]{#symbol-UnixProcess2.setupNamedInPipes}
:::

::: {.section}
#### [setupNamedOutPipes(self, pipeshutdown)]{#symbol-UnixProcess2.setupNamedOutPipes}
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
