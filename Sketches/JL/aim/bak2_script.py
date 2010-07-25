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

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

auth = 'login.oscar.aol.com'
port = 5190


#* 1
#channelid 1
#seqnum 2
#dataFieldLength 2
#protocolVersion 4

channel1 = '\x01'
channel2 = '\x02'
channel3 = '\x03'
channel4 = '\x04'
channel5 = '\x05'

sock.connect((auth, port))
seqnum = '\x00\x01'
fieldLen = '\x00\x04'
data = '\x00\x00\x00\x01'
flap = '*' + channel1 + seqnum + fieldLen + data
sock.send(flap)
print sock.recv(1000)
sock.close()
