#!/usr/bin/python

"""
To create a a file that this program can decode...
    ffmpeg -i <some camera file>.avi -pix_fmt yuvj420p -s cif bar.yuv
    dirac_encoder -qf 2 -CIF -verbose bar.yuv bar.drc

"""

import os
import time
from dirac_parser import *

infile = open("bar.drc", "rb")
outfile = open("baz.yuv", "wb")

decoder = DiracParser(verbose = None)
framecount = 0
tstart = time.time()
while True:
    try:
        frame = decoder.getFrame()
        framecount += 1
        tnow = time.time()
        decode_fps = float(framecount) / (tnow-tstart)
        print "Got Frame", frame.keys()
        print "         ", "frame number#", framecount
        print "         ", "decode fps   ", decode_fps
        print "         ", "chroma_type  ", frame["chroma_type"]
        print "         ", "topfieldfirst", frame["topfieldfirst"]
        print "         ", "frame_rate   ", frame["frame_rate"]
        print "         ", "pixel_aspect ", frame["pixel_aspect"]
        print "         ", "interlaced   ", frame["interlaced"]
        print "         ", "chroma_size  ", frame["chroma_size"]
        print "         ", "size         ", frame["size"]
        print "         ", "y/u/v sizes  ", len(frame["yuv"][0]), len(frame["yuv"][1]), len(frame["yuv"][2]) 
        print
        outfile.write(frame["yuv"][0])
        outfile.write(frame["yuv"][1])
        outfile.write(frame["yuv"][2])
    except DiracException, de:
        reason = de.args[0]
        if reason == "NEEDDATA":
            data = infile.read(409600)
            decoder.sendBytesForDecode(data)
        elif reason == "SEQINFO":
            print "SEQINFO", decoder.getSeqData()
            print "       ", decoder.getSrcData()
        elif reason == "END":
            break
        else:
            raise
        
infile.close()
outfile.close()

# print "Playing back using : mplayer /home/kamaelian/baz.yuv -demuxer rawvideo -rawvideo w=352:h=288"
print "Playing back using : mplayer baz.yuv -demuxer rawvideo -rawvideo w=352:h=288"
os.system("mplayer baz.yuv -demuxer rawvideo -rawvideo w=352:h=288")

