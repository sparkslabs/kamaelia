#!/usr/bin/python

import time
import socket
import Axon
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Util.Console import *
from Kamaelia.Chassis.Seq import Seq
from Kamaelia.Internet.TCPClient import TCPClient

class Echo(Axon.Component.component):
   def main(self):
       print "CLIENT CONNECT", self.peer, self.peerport
       while not self.dataReady("control"):
           for msg in self.Inbox("inbox"):
               print "msg", self.peer, self.peerport
               self.send(msg, "outbox")
           yield 1       
       self.send(self.recv("control"), "signal")

class Pause(Axon.ThreadedComponent.threadedcomponent):
    delay = 1
    def main(self):
        time.sleep(self.delay)

if 1: # Server
    ServerCore(protocol=Echo, 
               port=2345,
               socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
              ).activate()

if 1:  # Client
    Pipeline(
        Seq(
            Pause(delay=0.1),
            OneShot("Hello\n"),
        ),
        TCPClient("127.0.0.1", 2345),
        ConsoleEchoer(),
    ).run()

if 0:  # Client Doesn't Connect
    Pipeline(
        OneShot("Hello\n"),
        TCPClient("127.0.0.1", 2345),
        ConsoleEchoer(),
    ).run()

