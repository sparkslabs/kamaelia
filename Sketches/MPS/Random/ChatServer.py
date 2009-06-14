#!/usr/bin/python


import socket
import Axon
from Kamaelia.Chassis.ConnectedServer import ServerCore

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import *
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Apps.Grey.PeriodicWakeup import PeriodicWakeup
from Kamaelia.Apps.Grey.WakeableIntrospector import WakeableIntrospector


class Echo(Axon.Component.component):
    def main(self):
        while not self.dataReady("control"):
            for i in self.Inbox("inbox"):
                self.send(i, "outbox")
            self.pause()
            yield 1
        self.send(self.recv("control"), "signal")


class WakeableIntrospector(Axon.Component.component):
    def main(self):
        while not self.dataReady("control"):
            Q = [ q.name for q in self.scheduler.listAllThreads() ]
            Q.sort()
            self.send(Q, "outbox")
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            while self.dataReady("inbox"): self.recv("inbox")
        self.send(self.recv("control"), "signal")

class Uniq(Axon.Component.component):
    def main(self):
        last = None
        while not self.dataReady("control"):
            for msg in self.Inbox("inbox"):
                if msg != last:
                    self.send(msg, "outbox")
                    last = msg
            self.pause()
            yield 1
        self.send(self.recv("control"), "signal")

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

Pipeline(
    PeriodicWakeup(interval=1),
    WakeableIntrospector(),
    PureTransformer(lambda x: str(len(x))+" "+str(x)+"\n"),
    Uniq(),
    ConsoleEchoer(),
).activate()


ServerCore(protocol=Echo, 
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
           port=1234).run()
