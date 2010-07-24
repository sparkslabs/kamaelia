#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
