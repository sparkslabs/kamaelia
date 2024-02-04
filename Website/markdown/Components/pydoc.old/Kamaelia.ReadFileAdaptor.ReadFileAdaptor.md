---
pagename: Components/pydoc.old/Kamaelia.ReadFileAdaptor.ReadFileAdaptor
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia.ReadFileAdaptor.ReadFileAdaptor
========================================

class ReadFileAdaptor(Axon.Component.component)
-----------------------------------------------

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

        :   \"bitrate\" - read at a specified bitrate. \"line\" - read
            on a line by line basis \"block\" - read the file on a block
            by block basis.

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

Its interfaces are:

:   -   inboxes=\[\"inbox\"\] - not actually read at present
    -   outboxes=\[\"outbox\"\]) - When data is read, it is made
        available here.

#### Inboxes

-   control : Secondary inbox often used for signals. The closest
    analogy is unix signals
-   inbox : Default inbox for bulk data. Used in a pipeline much like
    stdin

#### Outboxes

-   outbox : Default data out outbox, used in a pipeline much like
    stdout
-   signal : The default signal based outbox - kinda like stderr, but
    more for sending singal type signals

Methods defined here
--------------------

::: {.boxright}
[Warning!]{style="font-weight:600"}
:::

### \_\_init\_\_(self, filename, command, readmode, readsize, steptime, bitrate, chunkrate, debug)

Standard constructor, see class docs for details

### closeDownComponent(self)

\#!!!! Called at component exit\...
:   Closes the file handle

### getDataByteLen(self)

This method attempts to read data of a specific block size from
:   the file handle. If null, the file is EOF. This method is never
    called directly. If the readmode is block or bitrate, then the
    attribute self.getData is set to this function, and then this
    function is called using self.getData(). The reason for this
    indirection is to make it so that the check for which readmode we
    are in is done once, and once only

### getDataReadline(self)

This method attempts to read a line of data from the file handle.
:   If null, the file is EOF. As with getDataByteLen, this method is
    never called directly. If the readmode is readline (or \"\"), then
    the attribute self.getData is set to this function, and then this
    function is called using self.getData(). Same reason for indirection
    as above.

### initialiseComponent(self)

Opens the appropriate file handle

### mainBody(self)

We check whether it\'s time to perform a new read, if it is, we
:   read some data. If we get some data, we put it in out outbox
    \"outbox\", and to stdout (if debugging). If we had an error state
    (eg EOF), we return 0, stopping this component, otherwise we return
    1 to live for another line/block.

------------------------------------------------------------------------

Feedback
--------

Got a problem with the documentation? Something unclear, could be
clearer? Want to help with improving? Constructive criticism, preferably
in the form of suggested rewording is very welcome.

Please leave the feedback [here, in reply to the documentation thread in
the Kamaelia
blog](http://kamaelia.sourceforge.net/cgi-bin/blog/blog.cgi?rm=addpostcomment&postid=1131454685).
