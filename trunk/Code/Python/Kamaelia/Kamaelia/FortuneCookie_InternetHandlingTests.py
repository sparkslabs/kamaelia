#!/usr/bin/env python
#
# Simple test harness for integrating TCP clients and servers in one system, sharing selector components etc.
#
#

from Axon.Scheduler import scheduler as _scheduler
from FortuneCookieProtocol import FortuneCookieProtocol as _FortuneCookieProtocol
from SimpleServerComponent import SimpleServer as _SimpleServer
from TCPClient import TCPClient as _TCPClient
from ConsoleEcho import consoleEchoer as _consoleEchoer
import Axon as _Axon

from Axon.Component import component, scheduler
class InternetHandlingTest(component):
   def initialiseComponent(self):
      import random
      clientServerTestPort=random.randint(1500,1599)
      server=_SimpleServer(protocol=_FortuneCookieProtocol, port=clientServerTestPort).activate()
      self.server=server
      self.addChildren(server)

      conecho = _consoleEchoer()
      self.addChildren(conecho)

      client=_TCPClient("127.0.0.1",clientServerTestPort, chargen=1)
      self.addChildren(client)
      self.link((client,"outbox"), (conecho,"inbox"))
      return _Axon.Ipc.newComponent(*(self.children))

   def mainBody(self):
      self.pause()
      try:
         pass
         #print self.server.children[1]
      except IndexError:
         pass
      return 1
if __name__ == '__main__':
   t = InternetHandlingTest().activate()

   _scheduler.run.runThreads(slowmo=0)

