#!/usr/bin/env python

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