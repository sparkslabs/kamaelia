#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: RJL

"""\
===========
Chunk Namer
===========

A component that labels each message with a unique filename for that message.
e.g. "A" ... "B" ... --> ["chunk1", "A"] ... ["chunk2", "B"] ...

Example Usage
-------------

Save each line entered to the console to a separate file::

    pipeline(
        ConsoleReader(),
        ChunkNamer("test", ".txt"),
        WholeFileWriter()
    ).run()

"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class ChunkNamer(component):
    """\
    ChunkNamer() -> new ChunkNamer component.
   
    Gives a filename to the chunk and sends it in the form [filename, contents],
    e.g. to a WholeFileWriter component.
   
    Keyword arguments:
    -- basepath - the prefix to apply to the filename
    -- suffix - the suffix to apply to the filename
    """
   
    Inboxes = {
        "inbox"   : "Chunks to be saved",
        "control" : "Shut me down"
    }
        
    Outboxes = {
        "outbox"  : "List: [file name, file contents]",
        "signal"  : "signal when I've shut down"
    }

    def __init__(self, basepath = "", suffix = ""):
        super(ChunkNamer, self).__init__()
        self.basepath = basepath
        self.suffix = suffix
        
    def main(self):
        buffer = ""
        chunknumber = 0
        while 1:
            yield 1
            while self.dataReady("inbox"):
                chunknumber += 1
                data = self.recv("inbox")
                
                # create list of form [filename, contents]
                command = [self.basepath + "chunk" + str(chunknumber) + self.suffix, data]
                self.send(command, "outbox")
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), "signal")
                    return

            self.pause()

__kamaelia_components__  = ( ChunkNamer, )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.File.WholeFileWriter import WholeFileWriter
    from Kamaelia.Util.Console import ConsoleReader
    pipeline(
        ConsoleReader(),
        ChunkNamer("test", ".txt"),
        WholeFileWriter()
    ).run()
