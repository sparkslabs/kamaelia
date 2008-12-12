import rtmidi
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class Midi(Axon.Component.component):
    def __init__(self, portNumber=0, **argd):
        super(Midi, self).__init__(**argd)
        self.output = rtmidi.RtMidiOut()
        self.output.openPort(portNumber)
        
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                self.output.sendMessage(*self.recv("inbox"))
            if self.dataReady("control"):
                msg = self.recv("control")
                if (isinstance(msg, producerFinished) or                    
                    isinstance(msg, shutdownMicroprocess)):
                    if isinstance(msg, producerFinished):
                        for item in self.Inbox('inbox'):
                            self.output.sendMessage(*item)
                    self.output.closePort()
                    self.send(msg, "signal")
                    break
            if not self.anyReady():
                self.pause()
            yield 1

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.OneShot import OneShot
    Pipeline(OneShot((0x90, 36, 127)), Midi(0)).run()

