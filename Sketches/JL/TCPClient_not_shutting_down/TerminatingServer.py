#! /usr/bin/env python

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
from Axon.Ipc import shutdownMicroprocess 
from Axon.Component import component
import time
class TerminatingProtocol(component):
    """runs for five cycles of the scheduler"""
    def main(self):
        lasttime = time.time()
        life = 1 #runs for 1 seconds
        while time.time() < lasttime + life:
            yield 1
            if self.dataReady():
                print self.recv()
        self.send(shutdownMicroprocess(), "signal") #close the socket
        print "shutdownMicroprocess sent"
        yield 1

port = 50000
SimpleServer(protocol=TerminatingProtocol, port=port).run()
