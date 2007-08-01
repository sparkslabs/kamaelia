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

import Kamaelia.KamaeliaIPC as _ki
from Axon.Ipc import shutdown
from Kamaelia.KamaeliaIPC import newReader, newWriter
from Kamaelia.KamaeliaIPC import removeReader, removeWriter

from Kamaelia.Internet.Selector import Selector

import subprocess
import fcntl
import os
import sys

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

class Pipethrough(Axon.Component.component):
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
        super(Pipethrough, self).__init__()
        self.command = command

    def openSubprocess(self):
        p = subprocess.Popen(self.command, 
                             shell=True, 
                             bufsize=32768, 
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

        selectorService, selectorShutdownService, S = Selector.getSelectorServices(self.tracker)
        if S:
           S.activate()
        yield 1
        yield 1
        yield 1
        self.link((self, "selector"), (selectorService))
#        self.link((self, "selectorsignal"), (selectorShutdownService))

        x = self.openSubprocess()
        self.send(newWriter(self,((self, "stdinready"), x.stdin)), "selector")
        self.send(newReader(self,((self, "stderrready"), x.stderr)), "selector")
        self.send(newReader(self,((self, "stdoutready"), x.stdout)), "selector")
        
        # Assume all ready
        stdin_ready = 1
        stdout_ready = 1
        stderr_ready = 1

        exit_status = x.poll()       # while x.poll() is None
        success = 0
        while exit_status is None:
            exit_status = x.poll()

            if (not self.anyReady()) and not (stdin_ready + stdout_ready + stderr_ready):
                \
print self.name,"Mighty Foo", stdin_ready, stdout_ready, stderr_ready, len(self.inboxes["inbox"]), len(writeBuffer)
                self.pause()
                yield 1
                continue

            while self.dataReady("inbox"):
                d = self.recv("inbox")
                writeBuffer.append(d)

            if self.dataReady("stdinready"):
                self.recv("stdinready")
                stdin_ready = 1

            if self.dataReady("stdoutready"):
                self.recv("stdoutready")
                stdout_ready = 1

            if self.dataReady("stderrready"):
                self.recv("stderrready")
                stderr_ready = 1

            if len(writeBuffer)>10000:
                writeBuffer=writeBuffer[-10000:]
            if stdin_ready:
                while len(writeBuffer) >0:
                    d = writeBuffer[0]
#                    d = writeBuffer.pop(0)
                    try:
                        count = os.write(x.stdin.fileno(), d)
                        writeBuffer.pop(0)
                        success +=1
                    except OSError, e:
                        success -=1
                        \
print self.name,"Mighty FooBar", len(self.inboxes["inbox"]), len(writeBuffer)
                        # Stdin wasn't ready. Let's send through a newWriter request
                        # Want to wait
                        stdin_ready = 0
                        writeBuffer=writeBuffer[len(writeBuffer)/2:]
                        self.send(newWriter(self,((self, "stdinready"), x.stdin)), "selector")
                        \
print self.name,"OK, we're waiting....", len(self.inboxes["inbox"]), len(writeBuffer)
                        break # Break out of this loop
                    except:
                        \
print self.name,"Unexpected error whilst trying to write to stdin:"
                        print sys.exc_info()[0]
                        break
#                    if count != len(d):
#                        raise "Yay, we broke it"

            if stdout_ready:
                try:
                    Y = os.read(x.stdout.fileno(),2048)
                    if len(Y)>0:
                        self.send(Y, "outbox")
                except OSError, e:
#                    print "Mighty Bingle", len(self.inboxes["inbox"]), len(writeBuffer)
                    # stdout wasn't ready. Let's send through a newReader request
                    stdout_ready = 0
                    self.send(newReader(self,((self, "stdoutready"), x.stdout)), "selector")
                except:
                    \
print self.name,"Unexpected error whilst trying to read stdout:"
                    print sys.exc_info()[0]
                    pass

            if stderr_ready: # FIXME: This needs fixing before release
                try:
                    Y = os.read(x.stderr.fileno(),2048)
# TEMPORARY DIVERSION OF STDERR TO OUTBOX TOO
                    \
if len(Y)>0: self.send(Y,"outbox")
# No particular plans for stderr
                except OSError, e:
                    \
print self.name,"Mighty Jibble", len(self.inboxes["inbox"]), len(writeBuffer)
                    # stdout wasn't ready. Let's send through a newReader request
                    stderr_ready = 0
                    self.send(newReader(self,((self, "stderrready"), x.stderr)), "selector")
                except:
                    \
print self.name,"Unexpected error whilst trying to read stderr:"
                    print sys.exc_info()[0]
                    pass


            if self.dataReady("control"):
                 shutdownMessage = self.recv("control")
                 self.send(removeWriter(self,(x.stdin)), "selector")
                 yield 1
                 x.stdin.close()

            yield 1

        \
print self.name,"UnixPipe finishing up"
        while  self.dataReady("stdoutready"):
            \
print self.name,"flushing"
            self.recv("stdoutready")
            try:
                Y = os.read(x.stdout.fileno(),10)
                while Y:
                    self.send(Y, "outbox")
                    Y = os.read(x.stdout.fileno(),10)
                \
print self.name,"Mighty Floogly"
            except OSError, e:
                continue
            except:
                break
            yield 1

        # remove now closed file handles from the selector, so it doesn't stay
        # upset
        self.send(removeReader(self,(x.stderr)), "selector")
        self.send(removeReader(self,(x.stdout)), "selector")
        self.send(removeWriter(self,(x.stdin)), "selector")
        \
print self.name,"sending shutdown"
        if not shutdownMessage:
            \
print self.name,"new signal"
            self.send(Axon.Ipc.producerFinished(), "signal")
            \
print self.name,"...sent"
        else:
            \
print self.name,"old signal"
            self.send(shutdownMessage, "signal")
#            \
#print "...sent"
#        self.send(shutdown(), "selectorsignal")


if __name__=="__main__":
    pipeline(
       ChargenComponent(),
       Pipethrough("wc"),
       ConsoleEchoer(forwarder=True)
    ).run()
