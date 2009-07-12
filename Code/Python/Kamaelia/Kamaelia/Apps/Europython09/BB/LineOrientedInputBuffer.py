#!/usr/bin/python

import Axon
from Kamaelia.Apps.Europython09.BB.Exceptions import GotShutdownMessage

class LineOrientedInputBuffer(Axon.Component.component):
    def main(self):
        linebuffer = []
        gotline = False
        line = ""
        try:
            while 1:
                # Get a line
                while (not gotline):
                    if self.dataReady("control"):
                        raise GotShutdownMessage()

                    if self.dataReady("inbox"):
                        msg = self.recv("inbox")
                        if "\r\n" in msg:
                           linebuffer.append( msg[:msg.find("\r\n")+2] )
                           line = "".join(linebuffer)
                           gotline = True
                           linebuffer = [ msg[msg.find("\r\n")+2:] ]
                        else:
                           linebuffer.append( msg )
                    yield 1
                if self.dataReady("control"):
                    raise GotShutdownMessage()

                # Wait for receiver to be ready to accept the line
                while len(self.outboxes["outbox"]) > 0:
                    self.pause()
                    yield 1
                    if self.dataReady("control"):
                        raise GotShutdownMessage()

                # Send them the line, then rinse and repeat.
                self.send(line, "outbox")
                yield 1
                gotline = False
                line = ""

        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")
            return

        self.send(producerFinished(), "signal")

