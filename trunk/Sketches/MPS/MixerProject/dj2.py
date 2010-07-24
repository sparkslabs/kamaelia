#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Mock source for DJ 2
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

import Axon
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Util.ConsoleEcho import consoleEchoer
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.SingleServer import SingleServer

import sys
if len(sys.argv) > 1:
   dj2port = int(sys.argv[1])
else:
   dj2port = 1702

class ConsoleReader(threadedcomponent):
   def run(self):
      while 1:
         line = raw_input("DJ2-> ")
         line = line + "\n"
         self.send(line, "outbox")

class message_source(Axon.Component.component):
    def main(self):
        while 1:
            self.send("hello", "outbox")
            yield 1

pipeline(
     ReadFileAdaptor("audio.2.raw", readmode="bitrate", bitrate =1536000),
     TCPClient("127.0.0.1", dj2port),
).run()

if 0:
    pipeline(
         ConsoleReader(),
         TCPClient("127.0.0.1", dj2port),
    ).run()
