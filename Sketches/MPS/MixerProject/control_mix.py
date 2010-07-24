#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Mix Control Client.
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
#

import traceback
import Axon

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.Graphline import Graphline
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Axon.ThreadedComponent import threadedcomponent

import sys
if len(sys.argv) > 2:
    controlport = int(sys.argv[2])
else:
    controlport = 1705

class ConsoleReader(threadedcomponent):
   def __init__(self, prompt=">>> "):
      super(ConsoleReader, self).__init__()
      self.prompt = prompt

   def run(self):
      while 1:
         line = raw_input(self.prompt)
         line = line + "\n"
         self.send(line, "outbox")

def dumping_client():
    return pipeline(
        ConsoleReader("Connected to Mixer >> "),
        TCPClient("127.0.0.1", controlport),
        consoleEchoer(),
    )

dumping_client().run()