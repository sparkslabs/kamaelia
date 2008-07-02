#!/usr/bin/python

from Axon.experimental.Process import ProcessPipeline
from Axon.experimental.Process import ProcessGraphline
from Kamaelia.Chassis.Graphline import Graphline

import Axon
import time

from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Chassis.Pipeline import Pipeline

class seq(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        while 1:
            self.send(str(time.time())+"\n", "outbox")
            time.sleep(1)

if 0:
    Pipeline(
        seq(), 
        PureTransformer(lambda a : ("a", a)),
        ConsoleEchoer(forwarder=True),
        PureTransformer(lambda (_,b) : ("b", b)),
        ConsoleEchoer(forwarder=True),
        PureTransformer(lambda (_,c) : ("c", c)),
        ConsoleEchoer(forwarder=True),
        PureTransformer(lambda (_,d) : ("d", d)),
        ConsoleEchoer(forwarder=True),
    ).run()

if 0:
    Pipeline(
        seq(), 
        PureTransformer(lambda a : ("a", a)),
        ConsoleEchoer(forwarder=True),
        PureTransformer(lambda (_,b) : ("b", b)),
        ConsoleEchoer(forwarder=True),
        Pipeline(
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,d) : ("d", d)),
            ConsoleEchoer(forwarder=True),
        ),
    ).run()

if 0:
    Pipeline(
        Pipeline(
            seq(), 
            PureTransformer(lambda a : ("a", a)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,b) : ("b", b)),
            ConsoleEchoer(forwarder=True),
        ),
        Pipeline(
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,d) : ("d", d)),
            ConsoleEchoer(forwarder=True),
        ),
    ).run()

if 0:
    Pipeline(
        seq(), 
        PureTransformer(lambda a : ("a", a)),
        ConsoleEchoer(forwarder=True),
        Pipeline(
            PureTransformer(lambda (_,b) : ("b", b)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
        ),
        PureTransformer(lambda (_,d) : ("d", d)),
        ConsoleEchoer(forwarder=True),
    ).run()

if 0:
    Pipeline(
        seq(), 
        Pipeline(
            PureTransformer(lambda a : ("a", a)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,b) : ("b", b)),
            ConsoleEchoer(forwarder=True),
        ),
        Pipeline(
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,d) : ("d", d)),
            ConsoleEchoer(forwarder=True),
        ),
    ).run()

if 0:
    ProcessPipeline(
        seq(), 
        Pipeline(
            PureTransformer(lambda a : ("a", a)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,b) : ("b", b)),
            ConsoleEchoer(forwarder=True),
        ),
        Pipeline(
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,d) : ("d", d)),
            ConsoleEchoer(forwarder=True),
        ),
    ).run()

if 0:
    Graphline(
        A =seq(), 
        B = Pipeline(
            PureTransformer(lambda a : ("a", a)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,b) : ("b", b)),
            ConsoleEchoer(forwarder=True),
        ),
        C = Pipeline(
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,d) : ("d", d)),
            ConsoleEchoer(forwarder=True),
        ),
        linkages = {
            ("A","outbox"): ("B","inbox"),
            ("B","outbox"): ("C","inbox"),
        }
    ).run()

if 1:
    ProcessGraphline(
        A =seq(), 
        B = Pipeline(
            PureTransformer(lambda a : ("a", a)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,b) : ("b", b)),
            ConsoleEchoer(forwarder=True),
        ),
        C = Pipeline(
            PureTransformer(lambda (_,c) : ("c", c)),
            ConsoleEchoer(forwarder=True),
            PureTransformer(lambda (_,d) : ("d", d)),
            ConsoleEchoer(forwarder=True),
        ),
        linkages = {
            ("A","outbox"): ("B","inbox"),
            ("B","outbox"): ("C","inbox"),
        }
    ).run()
