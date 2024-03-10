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

from Axon.background import background
from Axon.Handle import Handle
from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Internet.TCPClient import TCPClient
import time
import queue
import ao
background(slowmo=0.001).start()

filename = "./snail.ogg"

playStream = Handle(Pipeline(VorbisDecode(), AOAudioPlaybackAdaptor())).activate()
# set of components for playing the stream back.

host = "bbc.kamaelia.org"
port = 1500

client = Handle(TCPClient(host = host, port = port)).activate()
# component to grab a stream from the internet

filedump = open("streamdump.ogg", "w+b")

def get_item(handle):
    while 1:
        try:
            X = handle.get("outbox")
            return X
        except queue.Empty:
            time.sleep(0.001)

# Play the ogg data in the background
while True:
    data = get_item(client)
    filedump.write(data)
    # log the stream to disk
    playStream.put(data,"inbox")
    # and play it.

# this could all be done entirely within kamaelia but using likefile
# makes it easier to hook in external programs.
