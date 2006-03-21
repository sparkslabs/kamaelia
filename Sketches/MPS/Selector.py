#!/usr/bin/python
#

import Axon
from Axon.Ipc import shutdown

class Selector(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    def main(self):
        while 1: # SmokeTests_Selector.test_RunsForever
            self.pause()
            if self.dataReady("control"):
                message = self.recv("control")
                if isinstance(message,shutdown):
                   return
            yield 1
