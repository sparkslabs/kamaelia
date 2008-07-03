#!/usr/bin/python
#...x....1....x....2....x....3....x....4....x....5....x.
import Axon
from Axon.Scheduler import scheduler
import Axon.LikeFile
import pprocess
import time
import pprint

class ProcessWrapComponent(object):
  def __init__(self, somecomponent):
    self.wrapped = somecomponent.__class__.__name__
    print "wrapped a", self.wrapped
    self.exchange = pprocess.Exchange()
    self.channel = None
    self.inbound = []
    self.C = somecomponent
    self.ce = None
    self.tick = time.time()

  def _print(self, *args):
      print self.wrapped," ".join([str(x) for x in args])

  def tick_print(self, *args):
      if time.time() - self.tick > 0.5:
          self._print(*args)
          self.tick = time.time()

  def run(self, channel):
    self.exchange.add(channel)
    self.channel = channel
    from Axon.LikeFile import likefile, background
    background(zap=True).start()
    time.sleep(0.1)

    self.ce = likefile(self.C)
    for i in self.main():
      pass

  def activate(self):
    channel = pprocess.start(self.run)
    return channel

  def getDataFromReadyChannel(self):
    chan = self.exchange.ready(0)[0]
    D = chan._receive()
    return D

  def passOnDataToComponent(self, D):
    self._print("pwc:- SEND", D, "TO", self.C.name)
    self.ce.put(*D)
    self._print("SENT")

  def main(self):
    while 1:
        self.tick_print("")
        if self.exchange.ready(0):
            D = self.getDataFromReadyChannel()
            self.passOnDataToComponent(D)
        D = self.ce.anyReady()
        if D:
            for boxname in D:
                D = self.ce.get(boxname)
                self.channel._send((D, boxname))
        yield 1
        if self.channel.closed:
            self._print(self.channel.closed)

def ProcessPipeline(*components):
  exchange = pprocess.Exchange()
  debug = False
  chans = []
  print "TESTING ME"
  for comp in components:
    A = ProcessWrapComponent( comp )
    chan = A.activate()
    chans.append( chan )
    exchange.add(chan )

  mappings = {}
  for i in xrange(len(components)-1):
    ci, cin = chans[i], chans[i+1]
    mappings[ (ci, "outbox") ] = (cin, "inbox")
    mappings[ (ci, "signal") ] = (cin, "control")

  while 1:
    for chan in exchange.ready(0):
      D = chan._receive()
      try:
        dest = mappings[ ( chan, D[1] ) ]
        dest[0]._send( (D[0], dest[1] ) )
        print "FORWARDED", D
      except KeyError:
        if debug:
          print "WARNING: unlinked box sent data"
          print "This may be an error for your logic"
          print "chan, D[1] D[0]", 
          print chan, D[1], repr(D[0])
          pprint.pprint( mappings )

    time.sleep(0.1)
