#!/usr/bin/python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""
This module provides a set of components and convienience functions for making a
CSA time out.  To use it, simply call the function InactivityChassis with a timeout
period and the CSA to wrap.  This will send a producerFinished signal to the CSA
if it does not send a message on its outbox or CreatorFeedback boxes before the
timeout expires.
"""
import time
import Axon
import sys
from Axon.Ipc import producerFinished
from Kamaelia.IPC import shutdownCSA
from Kamaelia.Chassis.Graphline import Graphline

class ResettableSender(Axon.ThreadedComponent.threadedcomponent):
    """
    This component represents a simple way of making a timed event occur.  By default,
    it is set up to send a timeout message "NEXT" within 5 seconds.  If it receives
    a message on its inbox, the timer will be reset.  This component will ignore
    any input on its control inbox.
    """
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
    """
    This is intended to wrap a component such that it may be monitored by another
    component.  To use it, connect any of the three inboxes to outboxes on the
    component to be monitored.  The messages that are sent to those inboxes will
    be forwarded to their respective out box.  For example, suppose "HELLO" was
    received on 'inbox2'.  self.message ("RESET" by default) will be sent on the
    'observed' outbox and "HELLO" will be sent out on 'outbox2'.  An ActivityMonitor
    will shut down upon receiving a producerFinished or shutdownCSA message on
    its control inbox.

    Please note that this can't wrap adaptive components properly as of yet.
    """
    # XXXX FIXME: This should be an adaptive component, and only proxy inboxes and outboxs that
    # XXXX FIXME: are NOT preceded by an underscore. If it is wrapping an AdaptiveCommsComponent,
    # XXXX FIXME: we ought to warn we can't necessarily wrap those properly yet(!)
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
        "signal": "Forwards any messages received on the inbox 'control' (also, shutsdown on usual messages)",
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
    """
    This component is basically just a Cheap and cheerful clock that
    may be shut down.  You may specify the interval and message to be
    sent.  The component will sleep for self.interval seconds and then
    emit self.message before checking its control inbox for any shutdown
    messages and then going back to sleep.
    """
    interval = 300
    message = 'tick'
    def main(self):
        while not self.shutdown():
            time.sleep(self.interval)
            self.send(self.message, "outbox")
    def shutdown(self):
        while self.dataReady("control"):
            data = self.recv("control")
            if isinstance(data, producerFinished) or isinstance(data, shutdownMicroprocess):
                self.send(data,"signal")
                return True
        return 0

class WakeableIntrospector(Axon.Component.component):
    """
    This component serves to check if it is the only component in the scheduler
    other than a graphline and PeriodicWakeup.  If it is, it will send out a
    producerFinished signal on its signal outbox.  It will ignore any input on
    its inbox or control box, however it is useful to send it a message to its
    inbox to wake it up.
    """
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
    """
    This is a factory function that will return a new function object that will
    produce an InactivityChassis with the given timeout and debug values.  The
    values specified in timeout, debug, and someclass will be used in all future
    calls to the returned function object.

    someclass - the class to wrap in an InactivityChassis
    timeout - the amount of time to wait before sending the shutdown signal
    debug - the debugger to use
    """
    def maker(self, *args,**argd):
        X = InactivityChassis(someclass(*args,**argd), timeout=timeout, debug=debug)
        return X
    return maker

def ExtendedInactivity(someclass):
    """
    A factory function that will return a new function object that will create an
    InactivityChassis wrapped in someclass without storing the debug and timeout
    arguments.
    """
    def maker(timeout=2, debug=False, *args,**argd):
        return InactivityChassis(someclass(*args,**argd), timeout=timeout, debug=debug)
    return maker

def InactivityChassis(somecomponent, timeout=2, debug=False):
    """
    This convenience function will link a component up to an ActivityMonitor and
    a ResettableSender that will emit a producerFinished signal within timeout
    seconds if the component does not send any messages on its outbox or
    CreatorFeedback boxes.  To link the specified component to an external component
    simply link it to the returned chassis's outbox or CreatorFeedback outboxes.
    """
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
