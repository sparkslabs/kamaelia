#!/usr/bin/env python
import time, sys, Axon
from likefile import LikeFile, schedulerThread

schedulerThread().start()


class Reverser(Axon.Component.component):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox') # strings have no "reverse" method, hence this indexing 'hack'.
            else: self.pause()
            yield 1


# Unix's "rev" tool, implemented using likefile.

reverser = LikeFile(Reverser())

while True:
    line = sys.stdin.readline().rstrip() # get rid of the newline
    reverser.put(line)
    enil = reverser.get()
    print enil