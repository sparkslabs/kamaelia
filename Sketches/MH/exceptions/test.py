#!/usr/bin/env python
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

from Axon.Component import component
from Kamaelia.Chassis.Pipeline import Pipeline
from Axon.Ipc import *

import sys, traceback

class Producer(component):
   def main(self):
      self.send("a")
      yield 1
      self.send("b")
      yield 2
      self.send("c")
      yield 3
      self.send("d")
      yield 4
      self.send("e")
 
class ProducerMakesException(component):
   def main(self):
      self.send("a")
      yield 1
      self.send("b")
      yield 2
      self.send("c")
      yield 3
      raise Exception("spam","eggs")
      yield 4
      self.send("d")
 
class Consumer(component):
   def main(self):
      try:
        while 1:
           while self.dataReady("inbox"):
               print "Received: ", self.recv("inbox")
           yield 1
      except producerFinished:
           print "It finished"
      except:
           print "MC2 Caught exception..."
           info = sys.exc_info()
           print info[1]
           print "".join(traceback.format_exception(*info))

print "==========================================="
print "Running first system ... normal termination"
print "==========================================="
Pipeline(Producer(), Consumer()).run()

print "===================================================================="
print "Running second system ... first node in pipeline throws an exception"
print "===================================================================="
Pipeline(ProducerMakesException(), Consumer()).run()

