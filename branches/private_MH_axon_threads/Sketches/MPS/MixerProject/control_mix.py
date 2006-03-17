#!/usr/bin/python
#
# Mix Control Client.
#

import traceback
import Axon

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Axon.ThreadedComponent import threadedcomponent

import sys
if len(sys.argv) > 2:
    controlport = int(sys.argv[2])
else:
    controlport = 1705

class ConsoleReader(threadedcomponent):
   def __init__(self, prompt=">>> "):
      super(ConsoleReader, self).__init__()
      self.prompt = prompt

   def run(self):
      while 1:
         line = raw_input(self.prompt)
         line = line + "\n"
         self.outqueues["outbox"].put(line)

def dumping_client():
    return pipeline(
        ConsoleReader("Connected to Mixer >> "),
        TCPClient("127.0.0.1", controlport),
        consoleEchoer(),
    )

dumping_client().run()