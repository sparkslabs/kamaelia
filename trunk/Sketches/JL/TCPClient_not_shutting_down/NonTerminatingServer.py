#! /usr/bin/env python

from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Protocol.FortuneCookieProtocol import FortuneCookieProtocol
from Axon.Ipc import shutdownMicroprocess 
from Axon.Component import component
import time

class NonTerminatingProtocol(component):
    """runs for five cycles of the scheduler"""
    def main(self):
        while True:
            yield 1
            if self.dataReady():
                print self.recv()
        
port = 50000
SimpleServer(protocol=NonTerminatingProtocol, port=port).run()
