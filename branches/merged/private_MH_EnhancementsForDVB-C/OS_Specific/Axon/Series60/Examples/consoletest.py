#!/usr/bin/env python2.3

from Kamaelia.Util.ConsoleEcho import  consoleEchoer
from Kamaelia.Internet.ThreadedTCPClient import ThreadedTCPClient
from Axon.Component import component
from Axon.Scheduler import scheduler
import Axon
#from Axon.ThreadedComponent import threadedcomponent
from time import sleep
import e32


class testHarness(component): # Spike component to test interoperability with TCPServer
   def __init__(self):
      super(testHarness,self).__init__() # I wonder if this can get forced to be called automagically?
      self.display = consoleEchoer()
      self.displayerr = consoleEchoer()
      self.client = ThreadedTCPClient("132.185.133.18",4444)
      self.count = 0

   def initialiseComponent(self):
      self.addChildren(self.display, self.client, self.displayerr)
#         self.addChildren(self.server, self.display)
      self.link((self.client, "outbox"),(self.display, "inbox"),pipewidth = 10)
      self.link((self.client, "signal"),(self.displayerr, "inbox"), pipewidth = 10)
      return Axon.Ipc.newComponent(*(self.children))

   def mainBody(self):
      return 1

t = testHarness()
t.activate()
scheduler.run.runThreads(slowmo=0)
