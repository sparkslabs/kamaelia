#!/usr/bin/python

import Axon
from Kamaelia.Chassis.ConnectedServer import FastRestartServer

class HelloWorld(Axon.Component.component):
    def main(self):
          self.send("Hello ", "outbox")
          self.send("World", "outbox")
          self.send("\r\n", "outbox") # Network end of line
          yield 1                     # To ensure a generator
          self.send(Axon.Ipc.producerFinished(), "signal")


FastRestartServer(protocol=HelloWorld, port=1500).run()



