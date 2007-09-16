#!/usr/bin/env python
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------

# An example of using likefile to pass audo data for on the fly compression.

import Axon.LikeFile, time
from Kamaelia.Audio.Codec.PyMedia.Encoder import Encoder
from Kamaelia.Internet.TCPClient import TCPClient
Axon.LikeFile.background(slowmo=0.01).start()

infile = "./stereo.wav"
outfile = "./outfile.mp3"

enc = Axon.LikeFile.likefile(Encoder("mp3", bitrate=128000, sample_rate=44100, channels=2))

input1 = open(infile, "r+b")
output = open(outfile, "w+b")

while True:
    data = input1.read(1024)
    print "about to sleep"
    time.sleep(1)
    print "slept"
    enc.put(data)
    data = enc.get()
    output.write(data)
