#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
=========================
Chunk Distributor
=========================

A component that controls TorrentMaker, instructing it to build a metadata
.torrent file for each message received in "inbox".

This component does not terminate.
"""

from Axon.Component import component

class ChunkDistributor(component):
    """\
    ChunkDistributor() -> new ChunkDistributor component.
   
    Gives a filename to the chunk and sends it in the form [filename, contents],
    e.g. to a WholeFileWriter component.
   
    Keyword arguments:
    - chunksize  -- Chunk size in bytes
    """
   
    Inboxes = {  "inbox" : "Chunks to be saved",
                #"filecompletion" : "Names of chunk files written, one per message"
                 "control" : "UNUSED" }
    Outboxes = { "outbox" : "List: [file name, file contents]",
                #"filecompletion" : "Names of chunk files written, one per message"
                 "signal" : "UNUSED" }

    def __init__(self, basepath = ""):
        super(ChunkDistributor,self).__init__()
        self.basepath = basepath
        
    def main(self):
        buffer = ""
        chunknumber = 0
        while 1:
            yield 1
            while self.dataReady("inbox"):
                chunknumber += 1
                data = self.recv("inbox")
                command = [ self.basepath + "chunk" + `chunknumber`, data ]
                self.send( command, "outbox" )
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    return
            self.pause()
