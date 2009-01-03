#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: TK
# Adapted/cleaned up by MPS

"""\
======
Append
======

This component accepts data from it's inbox "inbox" and appends the data to
the end of the given file.

It takes four arguments, with these default values::

    filename = None
    forwarder = True
    blat_file = False
    hold_open = True

filename should be clear. If you don't supply this, it'll break.

forwarder - this component defaults to passing on a copy of the data it's
appending to the file. This makes this component useful for dropping in
between other components for logging/debugging what's going on.

blat_file - if this is true, the file is zapped before we start appending
data.

hold_open - This determines if the file is closed between instances of data
arriving. """

import Axon

class Append(Axon.Component.component):
    """\
    Appender() -> component that incrementally append data to the end of a file (think logging)
    
    Uses the following keyword argyments::
    
    * filename - File to append to (required)
    * forwarder - copy to outbox (default: True)
    * blat_file - write empty file (default: False)
    * hold_open - keep file open (default: True)
    """
    Inboxes = {
        "inbox"   : "data to append to the end of the file.",
        "control" : "Send any message here to shut this component down"
    }
    Outboxes = {
        "outbox"  : "a copy of the message is forwarded here",
        "signal"  : "passes on the message used to shutdown the component"
    }
    # Arguments

    filename = None
    forwarder = True
    blat_file = False
    hold_open = True

    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Append, self).__init__(**argd)

        if self.filename == None:
            raise ValueError("Expected a filename")
        self.F = None
        self.shutdown = Axon.Ipc.producerFinished()
        if self.blat_file:
            F=open(self.filename, "wb")
            F.close()
        
    def writeChunk(self,chunk):
        if self.hold_open:
            if self.F == None:
                self.F = open(self.filename, "a")

            self.F.write(chunk)
            self.F.flush()
        else:
            F = open(self.filename, "a")
            F.write(chunk)
            F.flush()
            F.close()

    def main(self):
        while not self.dataReady("control"):
            for chunk in self.Inbox("inbox"):
                 self.writeChunk(chunk)
                 if self.forwarder:
                      self.send(chunk, "outbox")
            if not self.anyReady():
                self.pause()
            yield 1
        self.shutdown = self.recv("control")
        self.stop()

    def stop(self):
        self.send(self.shutdown, "signal")
        if self.F != None:
            self.F.close()
            self.F = None
        super(Append, self).stop()

__kamaelia_components__  = ( Append, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    Pipeline(
        ConsoleReader(eol=""),
        Append(filename="demo.txt"),
        ConsoleEchoer()
    ).run()
