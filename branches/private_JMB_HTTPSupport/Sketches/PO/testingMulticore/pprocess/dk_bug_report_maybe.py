#!/usr/bin/python

import Axon
import time
from MultiPipeline import ProcessPipeline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Util.Console import ConsoleEchoer

class InfiniteSource(Axon.Component.component):
   a = (1,2,3)
   b = (4,5,6)
   def main(self):
       while 1:
           self.send( self.a, "outbox")
           yield 1
           time.sleep(1)
           self.send( self.b, "outbox")
           yield 1
           time.sleep(1)

if 0: # Works
    Pipeline(
       InfiniteSource(),
       ConsoleEchoer(use_repr=True),
    ).run()

if 0: # Works
    ProcessPipeline(
       InfiniteSource(),
       ConsoleEchoer(use_repr=True),
    ).run()

if 0: # Works
    ProcessPipeline(
       InfiniteSource(a=(7,8,9), b=(10,11,12)),
       ConsoleEchoer(use_repr=True),
    ).run()

if 0: # Works
    ProcessPipeline(
       InfiniteSource(a=("1","2","3"), b=("4","5","6")),
       ConsoleEchoer(use_repr=True),
    ).run()

if 0: # Works
    ProcessPipeline(
       InfiniteSource(a=("123",), b=("456",)),
       ConsoleEchoer(use_repr=True),
    ).run()

if 1: # Works
    ProcessPipeline(
       InfiniteSource(a=("123","456","789"), b=("abc","def","ghi")),
       ConsoleEchoer(use_repr=True),
    ).run()
