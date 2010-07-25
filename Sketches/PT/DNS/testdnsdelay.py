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

import time
from Axon.Component import component
from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline

class HelloPusher(component):
    def __init__(self):
        self.time = time.time() + 0.1
        super(HelloPusher, self).__init__()
    def main(self):
        while True:
            if time.time() > self.time:
                self.time = time.time() + 0.1
                self.send("hello, world!\n", 'outbox')
            yield 1


Pipeline(HelloPusher(), ConsoleEchoer(), ConsoleReader(">>> ", ""),SimpleHTTPClient(),ConsoleEchoer()).run()

#
# A comment - the first two items in the pipeline will spam the console whenever the scheduler is running normally. The rest
# of the pipeline is processing http requests normally. However, with an imposed delay on DNS lookups, the entire scheduler halts.
# Somewhere in simpleHTTPClient, then, gethostbyname() is being called directly.
#


# For reference - here is what I used to delay DNS lookups:

# in /etc/resolv.conf:
# # 192.168.0.1
# 127.0.0.1

# in a terminal:

# mknod backpipe p
# sudo nc -l -u -p 53 0<backpipe | nc -u -i 1 192.168.0.1 53 1>backpipe

# these commands create a bidirectional UDP proxy with a 1-second delay, making localhost a DNS server with a 1-second delay.
