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
from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer

class linesender(Axon.Component.component):
    def __init__(self, *lines):
        super(linesender, self).__init__()
        self.lines = lines[:]
    def main(self):
        for line in self.lines:
           self.send(line+"\r\n", "outbox")
           yield 1

pipeline(
    linesender("GET /cgi-bin/blog/feed.cgi HTTP/1.0",
               "Host: 127.0.0.1",
               ""),
    TCPClient("127.0.0.1", 80),
    ConsoleEchoer(),
).run()
