#! /usr/bin/env python
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
import pickle
import socket
import struct
from oscarutil import *
from Axon.Component import component
from Axon.Ipc import WaitComplete, shutdownMicroprocess
from Kamaelia.Internet.TCPClient import TCPClient

CHANNEL_SNAC = 2
class SNACEngine(component):
    def __init__(self, list_o_funcs):
        super(SNACEngine, self).__init__()
        self.seed = ("version number and TLV 0X06 go here", 1)
        self.lst = list_o_funcs
        self.end = None

    def main(self):
        self.send((self.seed, CHANNEL_SNAC))
        for func in self.lst[1:]:
            while not self.dataReady():
                yield 1
            recvdflap = self.recv()
            s_header, s_body = readSNAC(recvdflap[1])
            send = SNAC(snac_type, func(s_body))
            self.send((send, CHANNEL_SNAC))

#replace with likefile
class ServerEmulator(component):
    lst = ["snacheaderthis is the first response",
           "snacheader\x01\x02\xab",
           "snacheaderthe quick brown fox jumped over the lazy dog",
           "snacheaderit's messing with the plan",
           ]
    def main(self):
        for msg in self.lst:
            yield 1
            self.send(('flap-header', msg))

def fa(reply):
    return "The length of %s is %i" % (reply, len(reply))

def fb(reply):
    return reply

def fc(reply):
    return reply[::2]

def fd(reply):
    return reply.split()[2]

from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Chassis.Pipeline import Pipeline
Pipeline(ServerEmulator(), SNACEngine(["0", fa, fb, fc, fd]), ConsoleEchoer()).run()
