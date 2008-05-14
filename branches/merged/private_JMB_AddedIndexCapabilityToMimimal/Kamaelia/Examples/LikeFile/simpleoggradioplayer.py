#!/usr/bin/env python

from Axon.LikeFile import likefile, background
from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Internet.TCPClient import TCPClient
import ao
background(slowmo=0.001).start()

filename = "./snail.ogg"

playStream = likefile(Pipeline(VorbisDecode(), AOAudioPlaybackAdaptor()))
# set of components for playing the stream back.

host = "bbc.kamaelia.org"
port = 1500

client = likefile(TCPClient(host = host, port = port))
# component to grab a stream from the internet

filedump = open("streamdump.ogg", "w+b")

# Play the ogg data in the background
while True:
    data = client.get()
    filedump.write(data)
    # log the stream to disk
    playStream.put(data)
    # and play it.

# this could all be done entirely within kamaelia but using likefile
# makes it easier to hook in external programs.
