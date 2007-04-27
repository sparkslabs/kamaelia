#!/usr/bin/env python

from Misc import TagWithSequenceNumber
from Misc import PromptedTurnstile
from Misc import OneShot
from Misc import InboxControlledCarousel
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.Chooser import ForwardIteratingChooser
from SAX import SAXPromptedParser
from EDL import EDLParser

import sys
sys.path.append("../Video/")

from YUV4MPEG import YUV4MPEGToFrame
from YUV4MPEG import FrameToYUV4MPEG
from CropAndScale import CropAndScale

sys.path.append("../pixformatConversion/")
from VideoSurface import YUVtoRGB
from VideoSurface import RGBtoYUV



# 1) decode video to individual frames
def DecodeAndSeparateFrames(inFileName, tmpFilePath):
    return Pipeline(
        RateControlledFileReader(inFileName, readmode="bytes",rate=10000000),       #  or mencoder
        YUV4MPEGToFrame(),
        TagWithSequenceNumber(),
        InboxControlledCarousel( lambda (framenum, frame) : \
                  Pipeline( OneShot(frame),
                            FrameToYUV4MPEG(),
                            SimpleFileWriter(tmpFilePath+("%08d.yuv" % framenum)),
                          )
                )
        )


# 2) reframe, writing out sequences

def Reframing(edlfile, tmpFilePath, width, height):
    return Graphline( \
        GET_EDL = EditDecisionSource(edlfile),
        REFRAMER = Carousel( lambda edit : ProcessEditDecision(tmpFilePath, edit, width, height),
                             make1stRequest=True ),
        linkages = {
            ("REFRAMER", "requestNext") : ("GET_EDL", "inbox"),
            ("GET_EDL", "outbox") : ("REFRAMER", "next"),
            ("GET_EDL", "signal") : ("REFRAMER", "control"),
            ("REFRAMER", "signal") : ("", "signal"),
            ("REFRAMER", "outbox") : ("", "outbox"),
        })

def EditDecisionSource(edlfile):
    return Graphline( \
        PARSING = Pipeline( RateControlledFileReader(edlfile,readmode="lines",rate=1000000),
                            SAXPromptedParser(freeRun=True),
                            EDLParser(),
                          ),
        GATE = PromptedTurnstile(),
        linkages = {
            ("", "inbox") : ("GATE", "next"),

            ("PARSING", "outbox") : ("GATE", "inbox"),
            ("GATE",    "outbox") : ("",     "outbox"),
            
            ("PARSING", "signal") : ("GATE", "control"),
            ("GATE",    "signal") : ("", "signal"),

        } )


def ProcessEditDecision(tmpFilePath, edit, width, height):
    print "   ",edit
    filenames = [ tmpFilePath+"%08d.yuv" % i for i in range(edit["start"], edit["end"]+1) ]
    newsize = (width,height)
    cropbounds = (edit["left"], edit["top"], edit["right"], edit["bottom"])

    return Graphline( \
        FILENAMES = ForwardIteratingChooser(filenames),
        FRAME_LOADER = Carousel( lambda filename : 
                                 Pipeline(
                                     RateControlledFileReader(filename,readmode="bytes",rate=100000000,chunksize=1000000),
                                     YUV4MPEGToFrame(),
                                     ),
                                 make1stRequest=False ),
        REFRAMING = Pipeline( YUVtoRGB(),
                              CropAndScale(newsize, cropbounds),
                              RGBtoYUV(),
                            ),
        linkages = {
            ("FRAME_LOADER", "requestNext") : ("FILENAMES", "inbox"),
            
            ("FILENAMES",    "outbox") : ("FRAME_LOADER", "next"),
            ("FRAME_LOADER", "outbox") : ("REFRAMING", "inbox"),
            ("REFRAMING",    "outbox") : ("", "outbox"),
            
            ("FILENAMES",    "signal") : ("FRAME_LOADER", "control"),
            ("FRAME_LOADER", "signal") : ("REFRAMING", "control"),
            ("REFRAMING",    "signal") : ("", "signal"),
        }
    )


# 3) concatenate sequences and reencode
def ReEncode(outFileName):
    return Pipeline( FrameToYUV4MPEG(),
                     SimpleFileWriter(outFileName),       # or mencoder
                   )


# NOW RUN THE SYSTEM

import sys,os

if len(sys.argv) != 7:
    sys.stderr.write("Usage:\n")
    sys.stderr.write("    MobileReframer.py <infile> <edlfile> <outfile> width height <tmpdir>\n")
    sys.stderr.write("\n")
    sys.stderr.write("* width and height are even numbered pixel dimensions for output video\n")
    sys.stderr.write("\n")
    sys.exit(1)
else:
    inFileName = sys.argv[1]
    edlfile = sys.argv[2]
    outFileName = sys.argv[3]
    output_width  = int(sys.argv[4])
    output_height = int(sys.argv[5])
    tmpFilePath = sys.argv[6]
    
    if tmpFilePath[-1] != os.sep:
        tmpFilePath += os.sep
        
    if (output_width % 1) or (output_height % 1):
        sys.stderr.write("width and height must be even numbered pixel dimensions for output video\n")
        sys.exit(1)
        
    
# inFileName = "/data/stream.yuv"
# outFileName = "/data/result.yuv"
# tmpFilePath = "/tmp/mobile_reframer/"
# output_width=64
# output_height=48
# edlfile = "TestEDL.xml"

try:
    os.mkdir(tmpFilePath[:-1])
except:
    pass

print "Separating frames..."
DecodeAndSeparateFrames(inFileName, tmpFilePath).run()
print "Processing Edits..."
Pipeline( Reframing(edlfile, tmpFilePath, output_width, output_height),
          ReEncode(outFileName),
        ).run()

print "Cleaning up..."
# clean up
for file in os.listdir(tmpFilePath):
    os.remove(tmpFilePath+file)
print "DONE"



