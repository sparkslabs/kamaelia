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
