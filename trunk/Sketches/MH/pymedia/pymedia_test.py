#!/usr/bin/env python

# test to understand how pymedia 1.3.5 works

import time

filename="/home/matteh/music/Philip Glass/Solo Piano/01 - Metamorphosis One.mp3"
#filename="/home/matteh/music/Rodeohead.mp3"

extension = filename.split(".")[-1]
extension = extension.lower()

import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound

f=open(filename,"rb")
data=f.read(99999999)

dm = muxer.Demuxer(extension)
frames = dm.parse(data)

rawout=[]

frame0 = True
for frame in frames:
    if frame0:
        stream_index = frame[0]
        dec = acodec.Decoder(dm.streams[stream_index])
        raw = dec.decode(frame[1])
        snd =sound.Output(raw.sample_rate, raw.channels, sound.AFMT_S16_LE)
        print len(dm.streams),raw.channels, raw.sample_rate
        print dm.streams
        print dm.getHeaderInfo()
        frame0 = False

    rawout.append(str(raw.data))
#    snd.play(raw.data)
    raw = dec.decode(frame[1])


import time

#allraw = "".join(rawout)
CHUNKSIZE=4096

print snd.getSpace()
for chunk in rawout:
#  print len(chunk), snd.getSpace()
  for i in xrange(0,len(chunk),CHUNKSIZE):
      t=time.time()
      snd.play(chunk[i:i+CHUNKSIZE])
      print time.time()-t, snd.getSpace()
#  snd.play(chunk)
#  print "flob",time.time()
