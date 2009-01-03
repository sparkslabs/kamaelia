import OSC
import Axon
import random
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Internet.UDP import SimplePeer

class NumberGen(Axon.Component.component):
    def __init__(self):
        super(NumberGen, self).__init__()
        random.seed()
        
    def main(self):
        while 1:
            self.send(random.random(), "outbox")
            yield 1

class OSCTest(Axon.Component.component):
    def __init__(self):
        super(OSCTest, self).__init__()
    
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                message = OSC.OSCMessage("/OSCTest")
                message.append(self.recv("inbox"))
                self.send(message.getBinary(), "outbox")
            yield 1

if __name__ == "__main__":
    Pipeline(NumberGen(), OSCTest(), SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000)).run()
