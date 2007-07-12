#!/usr/bin/env python

# An example of using likefile to pass audo data for on the fly compression.

import likefile, time
from Kamaelia.Audio.Codec.PyMedia.Encoder import Encoder
from Kamaelia.Internet.TCPClient import TCPClient
likefile.schedulerThread(slowmo=0.01).start()

infile = "./file.wav"
outfile = "./outfile.mp3"

enc = likefile.LikeFile(Encoder("mp3", bitrate=128000, sample_rate=16000, channels=1))
enc.activate()

output = file(outfile, "w+b")

for line in file(infile, "r+b"):
    enc.put(line)
    data = enc.get()
    output.write(data)