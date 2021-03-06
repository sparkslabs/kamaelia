#!/usr/bin/env python
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
#
"""
====================
DataTx
====================
The DataTx packetises the data. It adds packet header to the


How it works?
---------------------
The DataTx adds a header to the data received on its inboxes "keyin" and
"inbox". The packet header contains packet type and packet length.
It is necessary to distinguish between encrypted data to be sent and
encrypted session keys because the client needs to be able to
distinguish between the two.
"""

import Axon
import struct

class DataTx(Axon.Component.component):
    """\   DataTx() -> new DataTx component
    Handles packetizing
    Keyword arguments: None
    """
    
    Inboxes = {"inbox" : "encrypted data",
               "keyIn" : "encrypted session key",
               "control" : "receive shutdown messages"}
    Outboxes = {"outbox" : "add header and send encrypted key and data packets",
                "signal" : "pass shutdown messages"}

    def __init__(self):
        super(DataTx,self).__init__()

    def main(self):
        KEY = 0x20
        DATA = 0x30
        while 1:
            #add header - packet type=4 bytes and packet length = 4 bytes
            while self.dataReady("keyIn"):
                data = self.recv("keyIn")
                header = struct.pack("!2L", KEY, len(data))
                packet = header + data
                self.send(packet, "outbox")
            yield 1

            if self.dataReady("inbox"):
                data = self.recv("inbox")
                header = struct.pack("!2L", DATA, len(data))
                packet = header + data
                self.send(packet, "outbox")
            yield 1
