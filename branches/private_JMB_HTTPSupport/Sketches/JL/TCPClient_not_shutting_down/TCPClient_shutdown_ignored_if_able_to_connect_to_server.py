#! /usr/bin/env python

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess

server = 'localhost'
port = 50000

class Terminator(component):
    def main(self):
        for i in range(10):
            print i
            self.send(str(i))
            yield 1            
        self.send(shutdownMicroprocess(), "signal")


print "Connecting to nonexistent server, sending 10 messages"
Pipeline(Terminator(), TCPClient('localhost', 50001)).run()

##print "Sending 10 messages to google.com on port 80"
##Pipeline(Terminator(), TCPClient('google.com', 80)).run()

#never gets to this code
#run ./TerminatingServer.py or ./NonTerminatingServer.py.
print "Sending 10 messages to server on localhost"
Pipeline(Terminator(), TCPClient('localhost', 50000)).run()

print "We'll never get here, but the server will kick us off"
Pipeline(Terminator(), TCPClient('login.oscar.aol.com', 5190)).run()

