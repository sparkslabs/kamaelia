#!/usr/bin/python


import Axon

class CheckpointSequencer(Axon.Component.component):
    def __init__(self, rev_access_callback = None,
                       rev_checkpoint_callback = None,
                       blank_slate_callback = None,
                       initial = 1,
                       highest = 1):
        super(CheckpointSequencer, self).__init__()
        if rev_access_callback: self.loadMessage = rev_access_callback
        if rev_checkpoint_callback: self.saveMessage = rev_checkpoint_callback
        if blank_slate_callback: self.newMessage = blank_slate_callback
        self.initial = initial
        self.highest = highest

    def loadMessage(self, current): return current
    def saveMessage(self, current): return current
    def newMessage(self, current): return current

    def main(self):
        current = self.initial
        highest = self.highest
        self.send( self.loadMessage(current), "outbox")
        dirty = False
        while 1:
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command == "prev":
                    if current >1:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current -= 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "next":
                    if current <highest:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current += 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "checkpoint":
                    highest += 1
                    current = highest
                    self.send( self.saveMessage(current), "outbox")
                if command == "new":
                    self.send( self.saveMessage(current), "outbox")
                    highest += 1
                    current = highest
                    self.send( self.newMessage(current), "outbox")
                    self.send( self.saveMessage(current), "outbox")
                if command == "undo":
                    self.send( self.loadMessage(current), "outbox")
                if command == "dirty":
                    print "OK, got dirty message"
                    dirty = True
#                    self.send( self.loadMessage(current), "outbox")

                if command == ("prev", "local"):
                    if current >1:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current -= 1
                        mess = self.loadMessage(current)
                        mess[0].append("nopropogate")
                        self.send( mess, "outbox")

                if command == ("next", "local"):
                    if current <highest:
                        if dirty:
                            self.send( self.saveMessage(current), "outbox")
                            dirty = False
                        current += 1
                        mess = self.loadMessage(current)
                        mess[0].append("nopropogate")
                        self.send( mess, "outbox")
#                        self.send( self.loadMessage(current), "outbox")


            if not self.anyReady():
                self.pause()
                yield 1

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    def loadMessage(current): return [["LOAD", "slide.%d.png" % (current,)]]
    def saveMessage(current): return [["SAVE", "slide.%d.png" % (current,)]]

    pipeline(
        ConsoleReader(">>>", ""),
        CheckpointSequencer(lambda X: [["LOAD", "slide.%d.png" % (X,)]],
                            lambda X: [["SAVE", "slide.%d.png" % (X,)]],
                            initial=0,
                            highest=0,
                           ),
        ConsoleEchoer(),
    ).run()



if __name__ == "__OLDmain__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    def loadMessage(current): return [["LOAD", "slide.%d.png" % (current,)]]
    def saveMessage(current): return [["SAVE", "slide.%d.png" % (current,)]]

    pipeline(
        ConsoleReader(">>>", ""),
        CheckpointSequencer(lambda X: [["LOAD", "slide.%d.png" % (X,)]],
                            lambda X: [["SAVE", "slide.%d.png" % (X,)]],
                            initial=0,
                            highest=0,
                           ),
        ConsoleEchoer(),
    ).run()





































