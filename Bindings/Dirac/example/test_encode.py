#!/usr/bin/python
"""
This example expects a 420p yuv file which is 352x288 to exist to encode.

You can create such a beast like this:
    ffmpeg -i <some camera file>.avi -pix_fmt yuvj420p -s cif bar.yuv

Additionally, test_decode.py takes bar.drc and creates baz.yuv which is
a suitable file. Hence this example defaults to reading baz.yuv, though
this will exhibit artefacts due to cascaded transcode.
"""

import os
import sys
import time
from dirac.dirac_encoder import *

def rawYUVFrameReader(raw_data_source, size):
    """
        - raw_data_source needs to be an iterable - eg a generator
        - size - needs to be a tuple. eg 352x288
        
        This ONLY handles 420planar at present
    """
    planes = { "y":"", "u":"", "v":"" }
    sizes = {
              "y" : ( size[0] * size[1] ),
              "u" : ( size[0] * size[1] ) / 4,
              "v" : ( size[0] * size[1] ) / 4
            }

    for raw in raw_data_source:
        while raw:
            filled = False
            for plane in ['y','u','v']:
                remainder = sizes[plane] - len(planes[plane])
                filled = len(raw) >= remainder
                topupsize = min( len(raw), remainder )
                if topupsize:
                    planes[plane] += raw[:topupsize]
                    raw = raw[topupsize:]

            if filled:
                """Send out a frame, flushing buffers"""
                frame = { "pixformat": "YUV420_planar",
                          "size": size,
                          "yuv":(planes['y'], planes['u'], planes['v'])
                        }
                planes['y'] = ""
                planes['u'] = ""
                planes['v'] = ""

                yield frame         # self.send( frame, "outbox" )


def encode_source(frame_source, outfile, preset="CIF"):
    """
     - Initialises an encoder based on presets - default is CIF
     - Reads frames from frame_source and encodes them
     - Writes the bit stream to outfile
    """
    encoder = DiracEncoder(preset=preset, bufsize=1024*1024, verbose=False, allParams={})

    done = False
    msg = None
    framecount = 0

    for frame in frame_source:
        # get some frame data in a form that allows this:
        framecount +=1

        print "                          FRAME", framecount
        print "                              Y", len(frame["yuv"][0])
        print "                              U", len(frame["yuv"][1])
        print "                              V", len(frame["yuv"][2])

        data = "".join(frame['yuv'])
        encoder.sendFrameForEncode(data)

        while True:  # Loops until more data is needed from the file - indicated by "needdata"
            try:
                bytes = encoder.getCompressedData()
                print "BYTES TO WRITE", len(bytes)
                outfile.write(bytes)

            except DiracEncodeException, e:
                reason = e.args[0]
                print "          looping", reason
                if reason =="NEEDDATA":
                   break
                elif reason =="ENCODERERROR":
                    print "Encoder Error"
                    raise RuntimeError("ENCODERERROR")
                elif reason =="INTERNALFAULT":
                    print "Internal Fault"
                    raise RuntimeError("INTERNALFAULT")
                else:
                    sys.stderr.write("FAIL\n\n")
                    sys.stderr.write(repr(reason) +"\n\n")
                    sys.stderr.write(repr(dir(reason)) +"\n\n")
                    sys.stderr.flush()
                    raise

infile = open("baz.yuv", "rb")
outfile = open("quux.drc", "wb")

frame_source = rawYUVFrameReader(infile, (352,288)) 

encode_source(frame_source, outfile, preset="CIF")

infile.close()
outfile.close()
