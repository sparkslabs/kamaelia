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

# Checked: 2024/03/24

import Axon
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Internet.SingleServer import SingleServer
from Kamaelia.Util.PureTransformer import PureTransformer
 
class Cat(Axon.Component.component):
    def __init__(self, messages):
        super(Cat, self).__init__()
        self.messages = messages
    def main(self):
        for message in self.messages:
            self.send(message, "outbox")
        while 1:
            self.pause()
            yield 1

port = 1602
Pipeline(
     Cat([
         "Hello World", "Hello World", "Hello World", "Hello World",
         "Hello World", "Hello World", "Hello World", "Hello World",
         "Hello World", "Hello World", "Hello World", "Hello World",
     ]),
     MessageRateLimit(2, 1),
     PureTransformer(lambda x: x.encode("utf8")),
     SingleServer(port=port),
).activate()

Pipeline(
    TCPClient("127.0.0.1", port),
    PureTransformer(lambda x: x.decode("utf8")),
    ConsoleEchoer(),
).run()
