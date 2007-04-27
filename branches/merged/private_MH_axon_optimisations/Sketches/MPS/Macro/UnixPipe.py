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

import Kamaelia.Internet.Selector as Selector
import Kamaelia.KamaeliaIPC as _ki

import subprocess
import fcntl
import os

def Chargen():
   import time
   t = time.time()
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
        t = time.time()
        while time.time() - t <0.1:
           yield 1
           self.send("hello\n", "outbox")
        self.send(Axon.Ipc.producerFinished(), "signal")

def makeNonBlocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)

class X(Axon.Component.component):
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
#        selectorService, newSelector = Selector.selectorComponent.getSelectorService(self.tracker)
#        
#        if newSelector:
#            self.addChildren(newSelector)
#        self.link((self, "_selectorSignal"),selectorService)
#             
        x = self.openSubprocess()
#        self.send(_ki.newWriter(self, (self,x.stdin,"WriteReady")), "_selectorSignal")
#        yield Axon.Ipc.newComponent(newSelector)
#

        shutdown = False
        exit_status = x.poll()
        while exit_status is None:
            if self.dataReady("inbox"):
                d = self.recv("inbox")
                count = os.write(x.stdin.fileno(), d)
                if count != len(d):
                    raise "Yay, we broke it"
            try:
                Y = os.read(x.stdout.fileno(),10)
                if len(Y)>0:
                    self.send(Y, "outbox")
            except OSError, e:
                pass
            
            if self.dataReady("control"):
                 shutdown = self.recv("control")
                 x.stdin.close()
            exit_status = x.poll()
            yield 1

        more_data = True
        while more_data:
            try:
                Y = os.read(x.stdout.fileno(),10)
                if len(Y)>0:
                    self.send(Y, "outbox")
                else:
                    more_data = False
            except OSError, e:
                more_data = False

        self.send(shutdown, "signal")

pipeline(
   ChargenComponent(),
   X("wc"),
   ConsoleEchoer(forwarder=True)
).run()




















