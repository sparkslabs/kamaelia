#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Mix Client. Passes received data onto stdout. Allows piping into a streaming server.
#
# IMPORTANT:
# If the mix client is not receiving any audio data, it MUST send zero data to cover the gap.
# This must be at a datarate of 44100Hz, 2 byte samples, 2 stereo samples. 
#
# Ie:
#   44100 Hz
#  *    2 2 channel (stereo)
#  *    2 2 bytes per word (16 bit audio)
#  *    8 Bytes -> bits
#  ie 1411200b/s
#  ie 1.3Mbit/s
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

import sys
if len(sys.argv) > 4:
    mockserverport = int(sys.argv[2])
else:
    mockserverport = 1700


class printer(Axon.Component.component):
    def main(self):
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                sys.stdout.write(data)
                sys.stdout.flush()
            yield 1

def dumping_client():
    return pipeline(
        TCPClient("132.185.131.178", 1700),
        printer(),   
    )

dumping_client().run()