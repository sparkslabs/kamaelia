#!/usr/bin/env python
import time, sys, Axon
from Axon.Handle import Handle
from Axon.background import background
try:
   import Queue
   queue = Queue # Python 3 compatibility change
except ImportError:
   # Python 3 compatibility change
   import queue

background().start()


class Reverser(Axon.Component.component):
    def main(self):
        while True:
            if self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send(item[::-1], 'outbox') # strings have no "reverse" method, hence this indexing 'hack'.
            else: self.pause()
            yield 1


sys.stderr.write("""_Similar_ to Unix's "rev" tool, implemented using likefile., type stuff, it reverses it\n""")

reverser = Handle(Reverser()).activate()

while True:
    line = sys.stdin.readline()
    if line == "":
       break
    line = line.rstrip() # get rid of the newline (Doesn't just strip newline, so rev(rev()) would not work 'correctly')
    reverser.put(line, "inbox")

    while 1:
        try:
            enil = reverser.get("outbox")
            break
        except queue.Empty:
            time.sleep(0.1)
            
    print (enil) # This is doesn't necessarily put the right whitespace back