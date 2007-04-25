#!/usr/bin/python

import time
import pickle
from Kamaelia.Util.Backplane import *
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Marshalling import *
from Kamaelia.Util.Console import *
from Kamaelia.Internet.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient

class Serialiser(object):
    def marshall(item): return pickle.dumps(item)
    marshall = staticmethod(marshall)

    def demarshall(item): return pickle.loads(item)
    demarshall = staticmethod(demarshall)

def NetworkOutbox(port):
    return
class Producer(threadedcomponent):
    # Lazy timed source
    def main(self):
        for i in xrange(1000):
            self.send(range(i), "outbox")
            time.sleep(1)

Pipeline( Producer(),
          Marshaller(Serialiser),
          SingleServer(port=1500),
        ).activate()

Pipeline( TCPClient("127.0.0.1", 1500),
          DeMarshaller(Serialiser),
          ConsoleEchoer()
        ).run()

