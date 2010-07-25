#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
"""
"""
from Axon.Component import component, scheduler
import Axon
import ao
import vorbissimple
import sys

class AOPlayerComponent(component):
   def __init__(self, id=None):
      super(AOPlayerComponent, self).__init__()
      #if id is None:
      #   id = 'oss'
      #print "FOO1"
      self.dev = ao.AudioDevice("oss")

   def main(self):
      print "FOO"
      while 1:
         print "BAR"
         if self.dataReady("inbox"):
            buff = self.recv("inbox")
            bytes = len(buff)
            sys.stdout.write("\nARRGH\n")
            sys.stdout.flush()
            #self.dev.play(buff)
         yield 1

x= AOPlayerComponent()
gen = x.main()
while 1:
   gen.next()
