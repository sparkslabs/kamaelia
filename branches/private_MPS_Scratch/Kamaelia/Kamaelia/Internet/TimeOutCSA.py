#!/usr/bin/python

import time
import Axon
import sys
from Axon.Ipc import producerFinished
from Kamaelia.IPC import shutdownCSA
from Kamaelia.Chassis.Graphline import Graphline

class ResettableSender(Axon.ThreadedComponent.threadedcomponent):
    timeout=5
    message="NEXT"
    debug = False
    def main(self):
        # print "TIMEOUT", repr(self.timeout)
        now = time.time()
        while 1:
            time.sleep(1) # Yes, there's nicer ways of doing this, but this is clear :-)
            if self.dataReady("inbox"):
                while self.dataReady("inbox"):
                    self.recv("inbox")
                now = time.time()
            if time.time() - now > self.timeout:
                break
            elif self.debug:
                print "."
        self.send(self.message, "outbox")
        # print "SHUTDOWN", self.name

class ActivityMonitor(Axon.Component.component):
    Inboxes = {
        "inbox": "",
        "inbox2": "",
        "inbox3": "",
        "control": "",
    }
    Outboxes = {
        "outbox": "Forwards any messages received on the inbox 'inbox'",
        "outbox2": "Forwards any messages received on the inbox 'inbox2'",
        "outbox3": "Forwards any messages received on the inbox 'inbox3'",
        "signal": "Forwards any messages received on the inbox 'control' (also, shutsdown on usual messages",
        "observed" : "A message is emitted here whenever we see data on any inbox",
    }
    message="RESET"
    def main(self):
        shutdown = False
        while not shutdown:
            yield 1
            while not self.anyReady():
                self.pause()
                yield 1
            self.send(self.message, "observed")
            while self.dataReady("inbox"):
                self.send(self.recv("inbox"), "outbox")
            while self.dataReady("inbox2"):
                self.send(self.recv("inbox2"), "outbox2")
            while self.dataReady("inbox3"):
                self.send(self.recv("inbox3"), "outbox3")
            while self.dataReady("control"):
                p = self.recv("control")
                if isinstance(p, producerFinished):
                    shutdown = True
                elif isinstance(p, shutdownCSA):
                    shutdown = True
                else:
                    # print "IGNORING", type(p), self.name
                    pass
                self.send(p, "signal")

class PeriodicWakeup(Axon.ThreadedComponent.threadedcomponent):
    interval = 300
    def main(self):
        while not self.shutdown():
            time.sleep(self.interval)
            self.send("tick", "outbox")
    def shutdown(self):
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                self.send(data,"signal")
                return True
        return 0

class WakeableIntrospector(Axon.Component.component):
    def main(self):
        while 1:
            names = [ q.name for q in self.scheduler.listAllThreads() ]
            # print "*debug* THREADS", names
            if len(names)==3:
                names.sort()
                names = [ N[N.rfind(".")+1:] for N in names ]
                N = "".join(names)
                N = N.replace("5","")
                N = N.replace("6","")
                N = N.replace("7","")
                # print "FOO", N
                if N == "Graphline_PeriodicWakeup_WakeableIntrospector_":
                    break
            self.scheduler.debuggingon = False
            yield 1
            while not self.dataReady("inbox"):
                self.pause()
                yield 1
            while self.dataReady("inbox"): self.recv("inbox")
        self.send(producerFinished(), "signal")


def NoActivityTimeout(someclass, timeout=2, debug=False):
    def maker(self, *args,**argd):
        X = InactivityChassis(someclass(*args,**argd), timeout=timeout, debug=debug)
        return X
    return maker

def ExtendedInactivity(someclass):
    def maker(timeout=2, debug=False, *args,**argd):
        return InactivityChassis(someclass(*args,**argd), timeout=timeout, debug=debug)
    return maker

def InactivityChassis(somecomponent, timeout=2, debug=False):
    linkages = {
        ("SHUTTERDOWNER","outbox"):("OBJ","control"),

        ("self","inbox")    :("OBJ","inbox"),
        ("self","control")  :("OBJ","control"),
        ("self","ReadReady"):("OBJ","ReadReady"),
        ("self","SendReady"):("OBJ","SendReady"),

        ("OBJ","outbox"):("ACT","inbox"),
        ("OBJ","CreatorFeedback"):("ACT","inbox2"),
#        ("OBJ","_selectorSignal"):("ACT","inbox3"),
        ("OBJ","signal"):("ACT","control"),

        ("ACT","observed"):("SHUTTERDOWNER","inbox"),

        ("ACT","outbox") :("self","outbox"),
        ("ACT","outbox2"):("self","CreatorFeedback"),
#        ("ACT","outbox3"):("self","_selectorSignal"),
        ("ACT","signal") :("self","signal"),
    }
    return Graphline(
        OBJ=somecomponent,
        ACT=ActivityMonitor(),
        SHUTTERDOWNER=ResettableSender(debug=debug, message=producerFinished(), timeout=timeout),
        linkages = linkages
    )

import socket
from Kamaelia.Internet.ConnectedSocketAdapter import ConnectedSocketAdapter
from Kamaelia.Internet.TCPServer import TCPServer
from Kamaelia.Protocol.EchoProtocol import EchoProtocol
from Kamaelia.Chassis.ConnectedServer import MoreComplexServer

class EchoServer(MoreComplexServer):
    protocol=EchoProtocol
    port=1500
    socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    class TCPS(TCPServer):
        CSA = NoActivityTimeout(ConnectedSocketAdapter, timeout=2, debug=True)

if __name__ == "__main__":
    from Kamaelia.Util.Console import *
    from Kamaelia.Chassis.Pipeline import Pipeline
    EchoServer().run()
    
    sys.exit(0)
    
    if 0:
        ConsoleReader_inactivity=NoActivityTimeout(ConsoleReader, timeout=1, debug=True)
        ConsoleReader_ConfigurableInactivity=ExtendedInactivity(ConsoleReader)
    
        Pipeline(
            ConsoleReader_ConfigurableInactivity(timeout=1, debug=True),
            ConsoleEchoer(),
        ).run()
    
        Pipeline(
            ConsoleReader_inactivity(),
            ConsoleEchoer(),
        ).run()
    
        Pipeline(
            InactivityChassis(ConsoleReader(), timeout=1, debug=True),
            ConsoleEchoer(),
        ).run()
    
        Pipeline(
            NoActivityTimeout(ConsoleReader, timeout=1, debug=True)(),
            ConsoleEchoer(),
        ).run()

        Graphline(
            PW = PeriodicWakeup(interval=5),
            WI = WakeableIntrospector(),
            linkages = {
                ("PW","outbox"):("WI","inbox"),
                ("PW","signal"):("WI","control"),
                ("WI","outbox"):("PW","inbox"),
                ("WI","signal"):("PW","control"),
            }
        ).activate()
