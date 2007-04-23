#!/usr/bin/python

import time
import pickle
from Kamaelia.Util.Backplane import *
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Marshalling import *
from Kamaelia.Util.Console import *

class Serialiser(object):
    def marshall(item): return pickle.dumps(item)
    marshall = staticmethod(marshall)

    def demarshall(item): return pickle.loads(item)
    demarshall = staticmethod(demarshall)

Backplane("inprocesscomms").activate()

class Producer(threadedcomponent):
    # Lazy timed source
    def main(self):
        for i in xrange(1000):
            self.send(i, "outbox")
            time.sleep(1)

Pipeline( Producer(),
          Marshaller(Serialiser),
          PublishTo("inprocesscomms")
        ).activate()

Pipeline( SubscribeTo("inprocesscomms"),
          DeMarshaller(Serialiser),
          ConsoleEchoer()
        ).run()

