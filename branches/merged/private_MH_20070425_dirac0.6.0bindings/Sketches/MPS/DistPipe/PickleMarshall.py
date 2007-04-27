#!/usr/bin/python

import time
import pickle
from Kamaelia.Util.Backplane import *
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Marshalling import *
from Kamaelia.Util.Console import *
from Kamaelia.Internet.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient

class Serialiser(object):
    def marshall(item): return pickle.dumps(item)
    marshall = staticmethod(marshall)

    def demarshall(item): return pickle.loads(item)
    demarshall = staticmethod(demarshall)

class Producer(threadedcomponent):
    # Lazy timed source
    def main(self):
        for i in xrange(1000):
            self.send(range(i), "outbox")
            time.sleep(1)

def NetworkOutbox(port):
    return Pipeline( Marshaller(Serialiser),
                     SingleServer(port=port),
                   ).activate()

def NetworkInbox(port):
    return Pipeline( SingleServer(port=port),
                     DeMarshaller(Serialiser),
                   ).activate()

def NetworkLinkage(ip1, port1, ip2, port2):
    return Graphline(
              PIPE = Pipeline(
                         TCPClient(ip1, port1),
                         TCPClient(ip2, port2),
              ),
              linkages = {
                 ("PIPE", "outbox"): ("PIPE", "inbox"),
                 ("PIPE", "signal"): ("PIPE", "control"),
              }
           )
if 1:
    Pipeline( Producer(),
              NetworkOutbox(1500)
            ).activate()
            
    Pipeline( NetworkInbox(1501),
              ConsoleEchoer()
            ).activate()

    NetworkLinkage("127.0.0.1", 1500, "127.0.0.1", 1501).run()

if 0:
    Pipeline( Producer(),
            Marshaller(Serialiser),
            SingleServer(port=1500),
            ).activate()
    
    Pipeline( TCPClient("127.0.0.1", 1500),
            DeMarshaller(Serialiser),
            ConsoleEchoer()
            ).run()
    
