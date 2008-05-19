#!/usr/bin/env python2.3
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
Chunkifier
=========================

A component that fixes the message size of an input stream to a given value,
outputting blocks of that size when sufficient input has accumulated. This
component's input is stream orientated - all messages receives are
concatenated to the interal buffer without divisions.

Example Usage
-------------

Chunkifying a console reader::

    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.ConsoleEcho import consoleEchoer

class ReducedConsoleReader(threadedcomponent):
   def __init__(self):
      super(ConsoleReader, self).__init__()

   def run(self):
      while 1:
         self.outqueues["outbox"].put( raw_input(self.prompt) )
    
    pipeline( ReducedConsoleReader(), Chunkifier(20), consoleEchoer(), ).run()


How does it work?
-----------------

Messages received on the "inbox" are buffered until at least N bytes have
been collected. A message containing those first N bytes is sent out "outbox"
and those front N bytes in the buffer are removed.

Any messages sent to the "control" inbox are ignored. The "signal"
outbox is not used.

This component does not terminate.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Chunkifier(component):
    """\
    Chunkifier([chunksize]) -> new Chunkifier component.
    
    Flow controller - collects incoming data and outputs it only as quanta of
    a given length in bytes (chunksize), unless the input stream ends (producerFinished). 
    
    Keyword arguments:
    - chunksize  -- Chunk size in bytes
    """
    
    Inboxes = { "inbox" : "Data stream to be split into chunks",
                "control": "UNUSED" }
    Outboxes = { "outbox" : "Each message is a chunk",
                "signal": "UNUSED" }

    def __init__(self, chunksize = 1048576, nodelay = false):
        super(Chunkifier, self).__init__()
        self.chunksize = chunksize
        self.nodelay = nodelay
    def main(self):
        buffer = ""
        while 1:
            yield 1
            while self.dataReady("inbox"):
                buffer += self.recv("inbox")
                while len(buffer) >= self.chunksize: #send out a full chunk
                    self.send(buffer[0:self.chunksize], "outbox")
                    buffer = buffer[self.chunksize:]
            
            if self.nodelay:
                self.send(buffer)
                
            while self.dataReady("control"):
                msg = self.recv("control")
                if isinstance(msg, producerFinished):
                    self.send(buffer, "outbox") #remainder of the buffer
                    self.send(msg, "signal")
                    return
                elif isinstance(msg, shutdownMicroprocess):
                    self.send(msg, "signal")
                    return
            self.pause()

if __name__ == '__main__':
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.Util.ConsoleEcho import consoleEchoer
    from Axon.ThreadedComponent import threadedcomponent
    from time import sleep
    from Lagger import Lagger

    class ReducedConsoleReader(threadedcomponent):
        def run(self):
            while 1:
                self.outqueues["outbox"].put( raw_input("> ") )
    
    pipeline( Lagger(), ReducedConsoleReader(), Chunkifier(20), consoleEchoer() ).run()
