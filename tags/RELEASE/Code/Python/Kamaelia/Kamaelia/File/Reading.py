#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
=================================
Components for reading from files
=================================

These components provide various ways to read from files, such as manual control
of the rate at which the file is read, or reusing a file reader to read from
multiple files.

Key to this is a file reader component that reads data only when asked to.
Control over when data flows is therefore up to another component - be that
a simple component that requests data at a constant rate, or something else that
only requests data when required.



PromptedFileReader
------------------

This component reads bytes or lines from the specified file when prompted.

Send the number of bytes/lines to the "inbox" inbox, and that data will be read
and sent to the "outbox" outbox.



Example Usage
^^^^^^^^^^^^^

Reading 1000 bytes per second in 10 byte chunks from 'myfile'::

    pipeline(ByteRate_RequestControl(rate=1000,chunksize=10)
             PromptedFileReader("myfile", readmode="bytes")
            ).activate()



More detail
^^^^^^^^^^^
The component will terminate if it receives a shutdownMicroprocess message on
its "control" inbox. It will pass the message on out of its "signal" outbox.

If unable to read all N bytes/lines requested (perhaps because we are
nearly at the end of the file) then those bytes/lines that were read
successfully are still output.

When the end of the file is reached, a producerFinished message is sent to the
"signal" outbox.

The file is opened only when the component is activated (enters its main loop).

The file is closed when the component shuts down.



RateControlledFileReader
------------------------

This component reads bytes/lines from a file at a specified rate. It is
performs the same task as the ReadFileAdapter component.

You can configure the rate, and the chunk size or frequency.



Example Usage
^^^^^^^^^^^^^

Read 10 lines per second, in 2 chunks of 5 lines, and output them to the console::

    pipeline(RateControlledFileReader("myfile", "lines", rate=10, chunksize=5),
             consoleEchoer()
            ).activate()



More detail
^^^^^^^^^^^
This component is a composition of a PromptedFileReader component and a
ByteRate_RequestControl component.

The component will shut down after all data is read from the file, emitting a
producerFinished message from its "signal" outbox.

The component will terminate if it receives a shutdownMicroprocess message on
its "control" inbox. It will pass the message on out of its "signal" outbox.

The inbox "inbox" is not wired and therefore does nothing.



ReusableFileReader
------------------

A reusable PromptedFileReader component, based on a Carousel component. Send it
a new filename and it will start reading from that file. Do this as many times
as you like.

Send it the number of bytes/lines to read and it will output that much data,
read from the file.



Example Usage
^^^^^^^^^^^^^

Read data from a sequence of files, at 1024 bytes/second in 16 byte chunks::

    playlist = Chooser(["file1","file2","file3", ...]
    rate = ByteRate_RequestControl(rate=1024,chunksize=16)
    reader = ReusableFileReader("bytes")

    playlist.link( (reader, "requestNext"), (playlist,"inbox") )
    playlist.link( (playlist,"outbox"), (reader, "next") )
    
    pipeline(ratecontrol, reader).activate()

    
Or, with the Control-Signal path linked up properly, using the
JoinChooserToCarousel prefab::

    playlist = Chooser(["file1","file2","file3", ...]
    rate = ByteRate_RequestControl(rate=1024,chunksize=16)
    reader = ReusableFileReader("bytes")

    playlistreader = JoinChooserToCarousel(playlist, reader)
    
    pipeline(ratecontrol, playlistreader).activate()

    

More detail
^^^^^^^^^^^    

Bytes or lines are read from the file on request. Send the number of bytes/lines
to the "inbox" inbox, and that data will be read and sent to the "outbox"
outbox.

This component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its "control" inbox. The message will be passed on
out of its "signal" outbox.

No producerFinished or shutdownMicroprocess type messages are sent by this
component between one file and the next.



RateControlledReusableFileReader
--------------------------------

A reusable file reader component, based on a Carousel component. Send it a
filename and the rate you want it to run at, and it will start reading from that
file at that rate. Do this as many times as you like.



Example Usage
^^^^^^^^^^^^^

Read data from a sequence of files, at different rates::

    playlist = Chooser([ ("file1",{"rate":1024}),
                         ("file2",{"rate":16}), ...])
    reader = RateControlledReusableFileReader("bytes")

    playlist.link( (reader, "requestNext"), (playlist,"inbox") )
    playlist.link( (playlist,"outbox"), (reader, "next") )
    
    reader.activate()
    playlist.activate()

    
Or, with the Control-Signal path linked up properly, using the
JoinChooserToCarousel prefab::

    playlist = Chooser([ ("file1",{"rate":1024}),
                         ("file2",{"rate":16}), ...])
    reader = RateControlledReusableFileReader("bytes")

    playlistreader = JoinChooserToCarousel(playlist, reader).activate()



More detail
^^^^^^^^^^^

The rate control is performed by a ByteRate_RequestControl component. The rate
arguments should be those that are accepted by this component.

This component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its "control" inbox. The message will be passed on
out of its "signal" outbox.

No producerFinished or shutdownMicroprocess type messages are sent by this
component between one file and the next.



FixedRateControlledReusableFileReader
-------------------------------------

A reusable file reader component that reads data from files at a fixed rate. It
is based on a Carousel component.

Send it a new filename and it will start reading from that file. Do this as many
times as you like.



Example Usage
^^^^^^^^^^^^^

Read data from a sequence of files, at 10 lines a second::

    playlist = Chooser(["file1", "file2", "file3", ... ])
    reader = FixedRateControlledReusableFileReader("lines", rate=10, chunksize=1)

    playlist.link( (reader, "requestNext"), (playlist,"inbox") )
    playlist.link( (playlist,"outbox"), (reader, "next") )
    
    reader.activate()
    playlist.activate()

    
Or, with the Control-Signal path linked up properly, using the
JoinChooserToCarousel prefab::

    playlist = Chooser(["file1", "file2", "file3", ... ])
    reader = FixedRateControlledReusableFileReader("lines", rate=10, chunksize=1)

    playlistreader = JoinChooserToCarousel(playlist, reader).activate()



More detail
^^^^^^^^^^^

The rate control is performed by a ByteRate_RequestControl component. The rate
arguments should be those that are accepted by this component.

This component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its "control" inbox. The message will be passed on
out of its "signal" outbox.

No producerFinished or shutdownMicroprocess type messages are sent by this
component between one file and the next.



Development history
-------------------

PromptedFileReader
- developed as an alternative to ReadFileAdapter
- prototyped in /Sketches/filereading/ReadFileAdapter.py

"""


from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Util.RateFilter import ByteRate_RequestControl
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.Util.Graphline import Graphline

class PromptedFileReader(component):
    """\
    PromptedFileReader(filename[,readmode]) -> file reading component

    Creates a file reader component. Reads N bytes/lines from the file when
    N is sent to its inbox.

    Keyword arguments:
    - readmode = "bytes" or "lines"
    """
    Inboxes = { "inbox" : "requests to 'n' read bytes/lines",
                "control" : "for shutdown signalling"
              }
    Outboxes = { "outbox" : "data output",
                 "signal" : "outputs 'producerFinished' after all data has been read"
               }
    
    def __init__(self, filename, readmode="bytes"):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PromptedFileReader, self).__init__()

        self.filename = filename
        
        if readmode == "bytes":
            self.read = self.readNBytes
        elif readmode == "lines":
            self.read = self.readNLines
        else:
            raise ValueError("readmode must be 'bytes' or 'lines'")
    

    def readNBytes(self, n):
        """\
        readNBytes(n) -> string containing 'n' bytes read from the file.
    
        "EOF" raised if the end of the file is reached and there is no data to
        return.
        """
        data = self.file.read(n)
        if not data:
            raise "EOF"
        return data
    
    
    def readNLines(self, n):
        """\
        readNLines(n) -> string containing 'n' lines read from the file.

        "EOF" raised if the end of the file is reached and there is no data to
        return.
        """
        data = ""
        for i in xrange(0,n):
            data += self.file.readline()
        if not data:
            raise "EOF"
        return data
    
    def main(self):
        """Main loop"""
        self.file = open(self.filename, "rb",0)
        
        done = False
        while not done:
            yield 1
    
            while self.dataReady("inbox"):
                n = int(self.recv("inbox"))
                try:
                    data = self.read(n)
                    self.send(data,"outbox")
                except:
                    self.send(producerFinished(self), "signal")
                    done = True
    
            if self.shutdown():
                done = True
            else:
                self.pause()
    
    def shutdown(self):
        """\
        Returns True if a shutdownMicroprocess message is received.

        Also passes the message on out of the "signal" outbox.
        """
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
    
    def closeDownComponent(self):
        """Closes the file handle"""
        self.file.close()


        
def RateControlledFileReader(filename, readmode = "bytes", **rateargs):
    """\
    RateControlledFileReader(filename[,readmode][,**rateargs]) -> constant rate file reader

    Creates a PromptedFileReader already linked to a ByteRate_RequestControl, to
    control the rate of file reading.
    
    Keyword arguments:
    - readmode = "bytes" or "lines"
    - **rateargs = arguments for ByteRate_RequestControl component constructor
    """
    return Graphline(RC  = ByteRate_RequestControl(**rateargs),
                    RFA = PromptedFileReader(filename, readmode),
                    linkages = { ("RC",  "outbox")  : ("RFA", "inbox"),
                                ("RFA", "outbox")  : ("self", "outbox"),
                                ("RFA", "signal")  : ("RC",  "control"),
                                ("RC",  "signal")  : ("self", "signal"),
                                ("self", "control") : ("RFA", "control")
                                }
    )


def ReusableFileReader(readmode):
    """\
    ReusableFileReader(readmode) -> reusable file reader component.

    A file reading component that can be reused. Based on a Carousel - send a
    filename to the "next" inbox to start reading from that file.

    Must be prompted by another component - send the number of bytes/lines to
    read to the "inbox" inbox.

    Keyword arguments:
    - readmode = "bytes" or "lines"
    """
    def PromptedFileReaderFactory(filename):
        """PromptedFileReaderFactory(filename) -> new PromptedFileReader component"""
        return PromptedFileReader(filename=filename, readmode=readmode)

    return Carousel(PromptedFileReaderFactory)



def RateControlledReusableFileReader(readmode):
    """\
    RateControlledReusableFileReader(readmode) -> rate controlled reusable file reader component.
    
    A file reading component that can be reused. Based on a Carousel - send
    (filename, rateargs) to the "next" inbox to start reading from that file at
    the specified rate.

    - rateargs are the arguments for a ByteRate_RequestControl component.

    Keyword arguments:
    - readmode = "bytes" or "lines"
    """
    def RateControlledFileReaderFactory(args):
        """RateControlledFileReaderFactory((filename,rateargs)) -> new RateControlledFileReader component"""
        filename, rateargs = args
        return RateControlledFileReader(filename, readmode, **rateargs)

    return Carousel( RateControlledFileReaderFactory )



def FixedRateControlledReusableFileReader(readmode = "bytes", **rateargs):
    """\
    FixedRateControlledReusableFileReader(readmode, rateargs) -> reusable file reader component

    A file reading component that can be reused. Based on a carousel - send a
    filename to the "next" or "inbox" inboxes to start reading from that file.

    Data is read at the specified rate.
    
    Keyword arguments:
    - readmode = "bytes" or "lines"
    - **rateargs = arguments for ByteRate_RequestControl component constructor
    """
    return Graphline(RC       = ByteRate_RequestControl(**rateargs),
                     CAR      = ReusableFileReader(readmode),
                     linkages = {
                        ("self", "inbox")      : ("CAR", "next"),
                        ("self", "control")    : ("RC", "control"),
                        ("RC", "outbox")       : ("CAR", "inbox"),
                        ("RC", "signal")       : ("CAR", "control"),
                        ("CAR", "outbox")      : ("self", "outbox"),
                        ("CAR", "signal")      : ("self", "signal"),
                        ("CAR", "requestNext") : ("self", "requestNext"),
                        ("self", "next")       : ("CAR", "next")
                    }
        )

__kamaelia_components__ = ( PromptedFileReader, )
__kamaelia_prefab__ = ( RateControlledFileReader, ReusableFileReader, RateControlledReusableFileReader, FixedRateControlledReusableFileReader, )

if __name__ == "__main__":
    pass
    
    





