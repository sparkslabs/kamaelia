#!/usr/bin/python


import Axon

class CheckpointSequencer(Axon.Component.component):
    def __init__(self, rev_access_callback = None,
                       rev_checkpoint_callback = None,
                       initial = 1,
                       highest = 1):
        super(CheckpointSequencer, self).__init__()
        if rev_access_callback: self.loadMessage = rev_access_callback
        if rev_checkpoint_callback: self.saveMessage = rev_checkpoint_callback
        self.initial = initial
        self.highest = highest

    def loadMessage(self, current): return current
    def saveMessage(self, current): return current

    def main(self):
        current = 1
        highest = 1
        self.send( self.loadMessage(current), "outbox")
        while 1:
            while self.dataReady("inbox"):
                command = self.recv("inbox")
                if command == "prev\n":
                    if current >1:
                        current -= 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "next\n":
                    if current <highest:
                        current += 1
                        self.send( self.loadMessage(current), "outbox")
                if command == "new\n":
                    highest += 1
                    current = highest
                    self.send( self.saveMessage(current), "outbox")
                if command == "undo\n":
                    self.send( self.loadMessage(current), "outbox")

            if not self.anyReady():
                yield 1


if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

    def loadMessage(current): return [["LOAD", "slide.%d.png" % (current,)]]
    def saveMessage(current): return [["SAVE", "slide.%d.png" % (current,)]]

    #pipeline(
        #ConsoleReader(),
        #CheckpointSequencer(loadMessage, 
                            #saveMessage),
        #ConsoleEchoer(),
    #).run()
    pipeline(
        ConsoleReader(),
        CheckpointSequencer(lambda X: [["LOAD", "slide.%d.png" % (X,)]],
                            lambda X: [["SAVE", "slide.%d.png" % (X,)]]
                           ),
        ConsoleEchoer(),
    ).run()





































