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

'''
This file contains a demonstration of how to use the 
Kamaelia.Apps.SA.Chassis.TTL component
'''

# Checked 2024/03/24

import time
import Axon

from Kamaelia.Apps.SA.Chassis import TTL

class WellBehaved1(Axon.Component.component):
    def main(self):
        t = time.time()
        while not self.dataReady("control"):
            if time.time() - t>0.3:
                self.send("hello", "outbox")
                print(self)
                t = time.time()
            yield 1
        self.send(self.recv("control"), "signal")

TTL( WellBehaved1(), 1 ).run()

class WellBehaved2(Axon.Component.component):
    Inboxes = {
        "inbox"   : "Foo Bar",
        "control" : "Foo Bar",
    }
    Outboxes = {
        "outbox" : "Foo Bar",
        "signal" : "Foo Bar",
    }
    def main(self):
        t = time.time()
        while not self.dataReady("control"):
            if time.time() - t>0.3:
                self.send("hello", "outbox")
                print(self)
                t = time.time()
            yield 1
        self.send(self.recv("control"), "signal")

TTL( WellBehaved2(), 1 ).run()

class WellBehaved3(Axon.Component.component):
    Inboxes = [ "inbox", "control" ]
    Outboxes = [ "outbox", "signal" ]
    def main(self):
        t = time.time()
        while not self.dataReady("control"):
            if time.time() - t>0.3:
                self.send("hello", "outbox")
                print( self )
                t = time.time()
            yield 1
        self.send(self.recv("control"), "signal")

TTL( WellBehaved3(), 1 ).run()

class WellBehaved4(Axon.Component.component):
    Inboxes = [ "inbox", "control" ]
    Outboxes = {
        "outbox" : "Foo Bar",
        "signal" : "Foo Bar",
    }
    def main(self):
        t = time.time()
        while not self.dataReady("control"):
            if time.time() - t>0.3:
                self.send("hello", "outbox")
                print( self )
                t = time.time()
            yield 1
        self.send(self.recv("control"), "signal")

TTL( WellBehaved4(), 1 ).run()

class BadlyBehaved1(Axon.Component.component):
    Inboxes = [ ]
    Outboxes = [ ]
    def main(self):
        t = time.time()
        while 1:
            if time.time() - t>0.3:
                print( self )
                t = time.time()
            yield 1

TTL( BadlyBehaved1(), 1 ).run()
