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

# An example of using likefile to pass audo data for on the fly compression.

import Axon.likefile, time
from Kamaelia.Audio.Codec.PyMedia.Encoder import Encoder
from Kamaelia.Internet.TCPClient import TCPClient
likefile.schedulerThread(slowmo=0.01).start()

infile = "./stereo.wav"
outfile = "./outfile.mp3"

enc = likefile.LikeFile(Encoder("mp3", bitrate=128000, sample_rate=44100, channels=2))

output = open(outfile, "w+b")

while True:
    data = output.read(1024)
    print "about to sleep"
    time.sleep(1)
    print "slept"
    enc.put(data)
    data = enc.get()
    output.write(data)