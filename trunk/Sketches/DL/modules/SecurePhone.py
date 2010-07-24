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

from Kamaelia.Util.PipelineComponent import pipeline
from Alsa import AlsaRecorder, AlsaPlayer
from Kamaelia.SingleServer import SingleServer
from Kamaelia.Internet.TCPClient import TCPClient
from Integrity import IntegrityStamper, IntegrityChecker, DisruptiveComponent
#from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller
from DL_Util import Pickle, UnPickle
from Speex import SpeexEncode, SpeexDecode
#from DVB_Multicast import dataRateMeasure
from Axon.Component import component
from Encryption import Encryptor, Decryptor

import time
class dataRateMeasure(component):
    def main(self):
        size = 0
        c = 0
        t = time.time()
        while 1:
            while self.dataReady("inbox"):
                c += 1
                data = self.recv("inbox")
                size += len(data)
                self.send(data, "outbox")
            if (c % 20) == 0:
                t_dash = time.time()
                if t_dash - t > 1:
                    print int((size/(t_dash - t))*8)
                    t = t_dash
                    size = 0
            yield 1


pipeline(
    AlsaRecorder(),
    SpeexEncode(3),
#   Encryptor("1234567812345678", "AES"),
    dataRateMeasure(),
    SingleServer(port=1601),
).activate()

pipeline(
    TCPClient("127.0.0.1", 1601),
#    Decryptor("1234567812345678", "AES"),
    SpeexDecode(3),
    AlsaPlayer(),
).run()
