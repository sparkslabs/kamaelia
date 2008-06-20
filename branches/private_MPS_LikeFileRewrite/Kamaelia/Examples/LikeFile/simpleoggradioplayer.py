#!/usr/bin/env python

from Axon.background import background
from Axon.LikeFile import LikeFile
from Kamaelia.Codec.Vorbis import VorbisDecode, AOAudioPlaybackAdaptor
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Internet.TCPClient import TCPClient
import time
import Queue
import ao
background(slowmo=0.001).start()

filename = "./snail.ogg"

playStream = LikeFile(Pipeline(VorbisDecode(), AOAudioPlaybackAdaptor())).activate()
# set of components for playing the stream back.

host = "bbc.kamaelia.org"
port = 1500

client = LikeFile(TCPClient(host = host, port = port)).activate()
# component to grab a stream from the internet

filedump = open("streamdump.ogg", "w+b")

def get_item(handle):
    while 1:
        try:
            X = handle.get("outbox")
            return X
        except Queue.Empty:
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
