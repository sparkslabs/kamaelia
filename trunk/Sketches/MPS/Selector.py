#!/usr/bin/python
#

import Axon

class Selector(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent): # SmokeTests_Selector.test_SmokeTest
    def main(self):
        while 1: # SmokeTests_Selector.test_RunsForever
            self.pause()
            yield 1
