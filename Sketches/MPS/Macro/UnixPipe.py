#!/usr/bin/python
"""
The purpose behind this component is to allow the following to occur:

pipeline(
   dataSource(),
   ExternalPipeThrough("command", *args),
   dataSink(),
).run()

More specificaly, the longer term interface of this component will be:

ExternalPipeThrough:
   inbox - data recieved here is sent to the program's stdin
   outbox - data sent here is from the program's stdout
   control - at some point we'll define a mechanism for describing
      control messages - these will largely map to SIG* messages
      though. We also need to signal how we close our writing pipe.
      This can happen using the normal producerFinished message.
   signal - this will be caused by things like SIGPIPE messages. What
      this will look like is yet to be defined. (Let's see what works
      first.

Initially this will be python 2.4 only, but it would be nice to support
older versions of python (eg 2.2.2 - for Nokia mobiles).

For the moment I'm going to send STDERR to dev null, however things won't
stay that way.
"""

import Axon
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Console import ConsoleEchoer

#import Kamaelia.Internet.Selector as Selector
import Kamaelia.KamaeliaIPC as _ki
from Axon.Ipc import shutdown
from Kamaelia.KamaeliaIPC import newReader, newWriter
from Kamaelia.KamaeliaIPC import removeReader, removeWriter

from Selector import Selector

import subprocess
import fcntl
import os

def Chargen():
   import time
   ts = t = time.time()
   while time.time() - t <1:
      yield "hello\n"

def run_command(command, datasource):
    x = subprocess.Popen(command, shell=True, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE, close_fds=True)
    for d in datasource:
        x.stdin.write(d)

    x.stdin.close()
    print x.stdout.read()

class ChargenComponent(Axon.Component.component):
    def main(self):
        import time
        ts = t = time.time()
        b = 0
        while time.time() - t <0.1:
           yield 1
           self.send("hello\n", "outbox")
           b += len("hello\n")
           if time.time() - ts >3:
               break
        self.send(Axon.Ipc.producerFinished(), "signal")
        print "total sent", b

def makeNonBlocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)

class X(Axon.Component.component):
    Inboxes = {
            "inbox" : "We receive data here to send to the sub process",
            "control" : "We receive shutdown messages here",
            "stdinready" : "We're notified here when we can write to the sub-process",
            "stderrready" : "We're notified here when we can read errors from the sub-process",
            "stdoutready" : "We're notified here when we can read from the sub-process",
    }
    Outboxes = {
        "signal" : "not used",
        "outbox" : "data from the sub command is output here",
        "selector" : "We send messages to the selector here, requesting it tell us when file handles can be read from/written to",
        "selectorsignal" : "To send control messages to the selector",
    }
    def __init__(self,command):
        super(X, self).__init__()
        self.command = command

    def openSubprocess(self):
        p = subprocess.Popen(self.command, 
                             shell=True, 
                             bufsize=1024, 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, 
                             stderr = subprocess.PIPE, 
                             close_fds=True)

        makeNonBlocking( p.stdin.fileno() )
        makeNonBlocking( p.stdout.fileno() )
        makeNonBlocking( p.stderr.fileno() )
        return p

    def main(self):
        writeBuffer = []
        shutdownMessage = False

        S = Selector()
        S.activate()
        yield 1
        self.link((self, "selector"), (S, "notify"))
        self.link((self, "selectorsignal"), (S, "control"))

        x = self.openSubprocess()
        self.send(newWriter(self,((self, "stdinready"), x.stdin)), "selector")
        self.send(newReader(self,((self, "stderrready"), x.stderr)), "selector")
        self.send(newReader(self,((self, "stdoutready"), x.stdout)), "selector")

        exit_status = x.poll()       # while x.poll() is None
        while exit_status is None:
            if self.dataReady("inbox"):
                d = self.recv("inbox")
                writeBuffer.append(d)

            if self.dataReady("stdinready"):
                self.recv("stdinready")
                while len(writeBuffer) >0:
                    d = writeBuffer.pop(0)
                    count = os.write(x.stdin.fileno(), d)
                    if count != len(d):
                        raise "Yay, we broke it"

            if self.dataReady("stdoutready"):
                self.recv("stdoutready")
                try:
                    Y = os.read(x.stdout.fileno(),10)
                    if len(Y)>0:
                        self.send(Y, "outbox")
                except OSError, e:
                    pass

            if self.dataReady("control"):
                 shutdownMessage = self.recv("control")
                 self.send(removeWriter(self,(x.stdin)), "selector")
                 yield 1
                 x.stdin.close()
            exit_status = x.poll()
            yield 1

        more_data = True # idiom for do...while
        while more_data:
            if self.dataReady("stdoutready"):
                self.recv("stdoutready")
                try:
                    Y = os.read(x.stdout.fileno(),10)
                    if len(Y)>0:
                        self.send(Y, "outbox")
                    else:
                        more_data = False
                except OSError, e:
                    more_data = False
            yield 1

        self.send(removeReader(self,(x.stderr)), "selector")
        self.send(removeReader(self,(x.stdout)), "selector")
        if not shutdownMessage:
            self.send(Axon.Ipc.producerFinished(), "signal")
        else:
            self.send(shutdownMessage, "signal")
        self.send(shutdown(), "selectorsignal")

pipeline(
   ChargenComponent(),
   X("wc"),
   ConsoleEchoer(forwarder=True)
).run()
