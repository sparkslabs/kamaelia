#!/usr/bin/env python

# NOTE: this code is unstable* if run without the wake-on-message-removal
# bugfix to Axon.

from Misc import TagWithSequenceNumber
from Misc import PromptedTurnstile
from Misc import OneShot
from Misc import InboxControlledCarousel
from Misc import StopSelector
#from Kamaelia.Chassis.Pipeline import Pipeline
#from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.File.Reading import PromptedFileReader
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

from Kamaelia.File.BetterReading import IntelligentFileReader
from UnixProcess import UnixProcess

sys.path.append("../audio/")
from WAV import WavParser
from ToWAV import WavWriter

sys.path.append("../Sketcher/Whiteboard/")
from TwoWaySplitter import TwoWaySplitter

from Misc import FirstOnly
from Misc import Chunk
from Misc import Sync

from Kamaelia.Util.Console import ConsoleEchoer

from Chassis import Pipeline
from Chassis import Graphline

sys.path.append("../Introspection/")
from Profiling import Profiler

# 1) decode video to individual frames
def DecodeAndSeparateFrames(inFileName, tmpFilePath):
    vidpipe = tmpFilePath+"vidPipe"
    try:
        os.remove(vidpipe)
    except:
        pass
    
    audpipe = tmpFilePath+"audPipe"
    try:
        os.remove(audpipe)
    except:
        pass
    
    mplayer = "mplayer -mc 0 -frames 700 -really-quiet -vo yuv4mpeg:file="+vidpipe+" -ao pcm:waveheader:file="+audpipe+" "+inFileName.replace(" ","\ ")
    
    return Graphline(
            MPLAYER = UnixProcess(mplayer, 2000000, {vidpipe:"video",audpipe:"audio"}),
            FRAMES = YUV4MPEGToFrame(),
            SPLIT = TwoWaySplitter(),
            FIRST = FirstOnly(),
            VIDEO = SaveVideoFrames(tmpFilePath),
            AUDIO = Carousel(lambda vformat: SaveAudioFrames(vformat['frame_rate'],tmpFilePath)),
#            DEBUG = ConsoleEchoer(),
#            MONITOR = Profiler(10.0, 0.1),
            linkages = {
                ("MPLAYER","video") : ("FRAMES","inbox"),
                ("FRAMES","outbox") : ("SPLIT","inbox"),
                ("SPLIT","outbox") : ("VIDEO","inbox"),
                
                ("SPLIT","outbox2") : ("FIRST","inbox"),
                ("FIRST","outbox") : ("AUDIO","next"),
                ("MPLAYER","audio") : ("AUDIO","inbox"),
                
                ("MPLAYER","signal") : ("FRAMES","control"),
                ("FRAMES","signal") : ("SPLIT","control"),
                ("SPLIT","signal") : ("VIDEO","control"),
                ("SPLIT","signal2") : ("FIRST","control"),
                ("FIRST","signal") : ("AUDIO","control"),
                
#                ("MPLAYER","outbox") : ("DEBUG","inbox"),
#                ("MPLAYER","error") : ("DEBUG","inbox"),
#                ("MONITOR","outbox") : ("DEBUG","inbox"),
                },
            boxsizes = {
                ("FRAMES", "inbox") : 3,
                ("SPLIT",  "inbox") : 1,
                }
            )
        
def SaveVideoFrames(tmpFilePath):
    return \
        Pipeline(
            TagWithSequenceNumber(),
            InboxControlledCarousel( lambda (framenum, frame) : \
                Pipeline( OneShot(frame),
                          FrameToYUV4MPEG(),
                          SimpleFileWriter(tmpFilePath+("%08d.yuv" % framenum)),
                        )
                ),
            StopSelector(),
        )



def SaveAudioFrames(frame_rate,tmpFilePath):
    return \
        Graphline(
            WAV = WavParser(),
            AUD = Carousel(
                lambda ameta : AudioSplitterByFrames( frame_rate,
                                                      ameta['channels'],
                                                      ameta['sample_rate'],
                                                      ameta['sample_format'],
                                                      tmpFilePath
                                                    )
                ),
            linkages = {
                # incoming WAV file passed to decoder
                ("", "inbox") : ("WAV", "inbox"),
                # raw audio sent to the carousel for splitting and writing
                ("WAV", "outbox") : ("AUD", "inbox"),
                
                # pass audio format info to the carousel
                ("WAV", "all_meta") : ("AUD", "next"),
                
                ("", "control") : ("WAV", "control"),
                ("WAV", "signal") : ("AUD", "control"),
            }
        )
                                              


def AudioSplitterByFrames(framerate, channels, sample_rate, sample_format,tmpFilePath):
    from Kamaelia.Support.PyMedia.AudioFormats import format2BytesPerSample
    
    quanta = format2BytesPerSample[sample_format] * channels
    audioByteRate = quanta*sample_rate
    
    return Pipeline(
        Chunk(datarate=audioByteRate, quanta=quanta, chunkrate=framerate),
        TagWithSequenceNumber(),
        InboxControlledCarousel( lambda (framenum, audiochunk) : \
            Pipeline( OneShot(audiochunk),
                      WavWriter(channels,sample_format,sample_rate),
                      SimpleFileWriter(tmpFilePath+("%08d.wav" % framenum)),
                    )
            ),
        )


# 2) reframe, writing out sequences

def Reframing(edlfile, tmpFilePath, width, height):
    return Graphline( \
        GET_EDL = EditDecisionSource(edlfile),
        REFRAMER = Carousel( lambda edit : ProcessEditDecision(tmpFilePath, edit, width, height),
                             make1stRequest=True ),
        AUDIO = Carousel( lambda edit : PassThroughAudioSegment(tmpFilePath, edit),
                          make1stRequest=True),
        SPLIT = TwoWaySplitter(),
        SYNC = Sync(n=2),
        linkages = {
            ("REFRAMER", "requestNext") : ("SYNC", "inbox"),
            ("AUDIO", "requestNext")    : ("SYNC", "inbox"),
            ("SYNC", "outbox") : ("GET_EDL", "inbox"),
            
            ("GET_EDL", "outbox") : ("SPLIT","inbox"),
            ("SPLIT", "outbox") : ("REFRAMER", "next"),
            ("SPLIT", "outbox2") : ("AUDIO", "next"),
            
            ("REFRAMER", "outbox") : ("", "video"),
            ("AUDIO", "outbox") : ("", "audio"),
            
            ("GET_EDL", "signal") : ("SPLIT", "control"),
            ("SPLIT", "signal") : ("REFRAMER", "control"),
            ("SPLIT", "signal2") : ("AUDIO", "control"),
            ("AUDIO", "signal") : ("SYNC", "control"),
            ("REFRAMER", "signal") : ("", "signal"),
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
    print " V ",edit
    filenames = [ tmpFilePath+"%08d.yuv" % i for i in range(edit["start"], edit["end"]+1) ]
    newsize = (width,height)
    cropbounds = (edit["left"], edit["top"], edit["right"], edit["bottom"])

    return Graphline( \
        FILENAMES = ForwardIteratingChooser(filenames),
        FRAME_LOADER = Carousel( lambda filename : 
                                 Pipeline(
                                     RateControlledFileReader(filename,readmode="bytes",rate=100000000,chunksize=65536),
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


def PassThroughAudioSegment(tmpFilePath, edit):
    print " A ",edit
    filenames = [ tmpFilePath+"%08d.wav" % i for i in range(edit["start"], edit["end"]+1) ]
    
    return Graphline( \
        FILENAMES = ForwardIteratingChooser(filenames),
        FRAME_LOADER = Carousel( lambda filename : 
                                 Pipeline(
                                     RateControlledFileReader(filename,readmode="bytes",rate=100000000,chunksize=65536),
                                     WavParser(),
                                     ),
                                 make1stRequest=False ),
        linkages = {
            ("FRAME_LOADER", "requestNext") : ("FILENAMES", "inbox"),
            
            ("FILENAMES",    "outbox") : ("FRAME_LOADER", "next"),
            ("FRAME_LOADER", "outbox") : ("", "outbox"),
            
            ("FILENAMES",    "signal") : ("FRAME_LOADER", "control"),
            ("FRAME_LOADER", "signal") : ("", "signal"),
        }
    )


# 3) concatenate sequences and reencode
def WriteToFiles():
    return Graphline( \
               VIDEO = FrameToYUV4MPEG(),
               AUDIO = WavWriter(2, "S16_LE", 44100),
               TEST = SimpleFileWriter("test.yuv"),
               TESTA = SimpleFileWriter("test.wav"),
               linkages = {
                   ("","video") : ("VIDEO","inbox"),
                   ("VIDEO","outbox") : ("TEST","inbox"),
                   
                   ("","audio") : ("AUDIO", "inbox"),
                   ("AUDIO","outbox") : ("TESTA","inbox"),
                   
                   ("","control") : ("VIDEO","control"),
                   ("VIDEO","signal") : ("AUDIO","control"),
                   ("AUDIO","signal") : ("TEST", "control"),
                   ("TEST", "signal") : ("TESTA", "control"),
                   ("TESTA", "signal") : ("", "signal"),
               },
           )
    
def ReEncode(outFileName):
    vidpipe = tmpFilePath+"vidPipe2.yuv"
    try:
        os.remove(vidpipe)
    except:
        pass
    
    audpipe = tmpFilePath+"audPipe2.wav"
    try:
        os.remove(audpipe)
    except:
        pass
    
    vidpipe=vidpipe.replace(" ","\ ")
    audpipe=audpipe.replace(" ","\ ")
    outFileName=outFileName.replace(" ","\ ")
    
#    encoder = "cat "+vidpipe+" > test2.yuv"
#    encoder = "ffmpeg -f yuv4mpegpipe -i "+vidpipe+" -i "+audpipe+" -y "+outFileName
    encoder = ( "mencoder -audiofile "+audpipe+" "+vidpipe +
                " -ovc lavc -oac mp3lame" +
                " -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128" +
#                " -mc 0 -noskip" +
                " -cache 16384 -audiofile-cache 500 -really-quiet" +
                " -o "+outFileName.replace(" ","\ ")
              )
             
    return Graphline( \
               VIDEO = FrameToYUV4MPEG(),
               AUDIO = WavWriter(2, "S16_LE", 48000),
               ENCODE = UnixProcess(encoder,buffersize=327680,inpipes={vidpipe:"video",audpipe:"audio"}),
               DEBUG = ConsoleEchoer(),
               STOP = StopSelector(),
               linkages = {
                   ("","video") : ("VIDEO","inbox"),
                   ("VIDEO","outbox") : ("ENCODE","video"),
                   
                   ("","audio") : ("AUDIO", "inbox"),
                   ("AUDIO","outbox") : ("ENCODE", "audio"),
                   
                   ("","control") : ("VIDEO","control"),
                   ("VIDEO","signal") : ("AUDIO","control"),
                   ("AUDIO","signal") : ("ENCODE", "control"),
                   ("ENCODE", "signal") : ("STOP", "control"),
                   ("STOP", "signal") : ("DEBUG", "control"),
                   ("DEBUG", "signal") : ("", "signal"),

                   ("ENCODE","outbox") : ("DEBUG","inbox"),
                   ("ENCODE","error") : ("DEBUG","inbox"),
               },
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
Graphline(
    REFRAMING = Reframing(edlfile, tmpFilePath, output_width, output_height),
    ENCODING  = ReEncode(outFileName),
#    ENCODING = WriteToFiles(),
#    PROF = Profiler(),
    linkages = {
        ("REFRAMING","video") : ("ENCODING","video"),
        ("REFRAMING","audio") : ("ENCODING","audio"),
        ("REFRAMING","signal") : ("ENCODING", "control"),
        }
    ).run()

print "Cleaning up..."
# clean up
for file in os.listdir(tmpFilePath):
    os.remove(tmpFilePath+file)
print "DONE"



