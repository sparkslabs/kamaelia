#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
