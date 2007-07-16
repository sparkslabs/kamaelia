#!/usr/bin/env python

from likefile import LikeFile, schedulerThread
from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
import ao
schedulerThread(slowmo=0.001).start()

filename = "./snail.ogg"

playStream = LikeFile(Pipeline(VorbisDecode(), AOAudioPlaybackAdaptor()))
playStream.activate()

# Play the ogg data in the background
oggdata = open(filename, "r+b").read()
playStream.put(oggdata)
while True:
    playStream.get()
    # there's no data produced but this will prevent us from exiting immediately.
