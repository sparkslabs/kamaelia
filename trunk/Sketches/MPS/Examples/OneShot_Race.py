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

import sys
class Raw(Axon.Component.component):
    def main(self):
        while 1:
            for i in self.Inbox("inbox"):
                sys.stdout.write(repr(i)+"\n")
                sys.stdout.flush()
            yield 1


from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Experimental.PythonInterpreter import InterpreterTransformer

def NetInterpreter(*args, **argv):
    return Pipeline(
                PureTransformer(lambda x: str(x).rstrip()),
                PureTransformer(lambda x: str(x).replace("\r","")),
                InterpreterTransformer(),
                PureTransformer(lambda x: str(x)+"\r\n>>> "),
           )

ServerCore(protocol=NetInterpreter,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=8765).activate()




if 1: # Server
    ServerCore(protocol=Echo, 
               port=2345,
               socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
              ).activate()

if 1:  # Client
    Pipeline(
        Seq(
            Pause(delay=0.1),
            OneShot("Hello1\r\n"),
            OneShot("Hello2\r\n"),
            OneShot("Hello3\r\n"),
            OneShot("Hello4\r\n"),
            OneShot("Hello5\r\n"),
            OneShot("Hello6\r\n"),
            OneShot("Hello7\r\n"),
            OneShot("Hello8\r\n"),
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

