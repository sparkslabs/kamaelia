#!/usr/bin/env python

# NOTE: this code is unstable* if run without the wake-on-message-removal
# bugfix to Axon.

from TagWithSequenceNumber import TagWithSequenceNumber
from OneShot import OneShot
from OneShot import TriggeredOneShot
from InboxControlledCarousel import InboxControlledCarousel
from StopSelector import StopSelector
from PromptedTurnstile import PromptedTurnstile
#from Kamaelia.Chassis.Pipeline import Pipeline
#from Kamaelia.Chassis.Graphline import Graphline
#from Kamaelia.Chassis.Carousel import Carousel
from Kamaelia.File.Reading import RateControlledFileReader
#from Kamaelia.File.Reading import PromptedFileReader
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
from PixFormatConversion import ToRGB_interleaved
from PixFormatConversion import ToYUV420_planar

#from Kamaelia.File.BetterReading import IntelligentFileReader
from UnixProcess import UnixProcess

sys.path.append("../audio/")
from WAV import WAVParser, WAVWriter

#sys.path.append("../Sketcher/Whiteboard/")
from TwoWaySplitter import TwoWaySplitter

from FirstOnly import FirstOnly
from Chunk import Chunk
from Sync import Sync

from Kamaelia.Util.Console import ConsoleEchoer

from Chassis import Pipeline
from Chassis import Graphline
from Chassis import Carousel

from MaxSpeedFileReader import MaxSpeedFileReader

from Kamaelia.Util.Backplane import Backplane,PublishTo,SubscribeTo

from Collate import Collate
from Kamaelia.Util.Filter import Filter
from RangeFilter import RangeFilter
from Misc import Max
from Kamaelia.Util.Detuple import SimpleDetupler

sys.path.append("../Introspection/")
from Profiling import Profiler

# 1) decode video to individual frames
def DecodeAndSeparateFrames(inFileName, tmpFilePath, edlfile,maxframe):
    vidpipe = tmpFilePath+"vidPipe.yuv"
    try:
        os.remove(vidpipe)
    except:
        pass
    
    audpipe = tmpFilePath+"audPipe.wav"
    try:
        os.remove(audpipe)
    except:
        pass
    
 #   mplayer = "mplayer -frames 200 -mc 0 -really-quiet -vo yuv4mpeg:file="+vidpipe+" -ao pcm:waveheader:file="+audpipe+" "+inFileName.replace(" ","\ ")
    mplayer = "ffmpeg -vframes %d -i %s -f yuv4mpegpipe -y %s -f wav -y %s" % ((maxframe*1.1+2),inFileName.replace(" ","\ "),vidpipe,audpipe)
    
    return Graphline(
            MPLAYER = UnixProcess(mplayer, 2000000, {vidpipe:"video",audpipe:"audio"}),
            FRAMES = YUV4MPEGToFrame(),
            SPLIT = TwoWaySplitter(),
            FIRST = FirstOnly(),
            VIDEO = SaveVideoFrames(tmpFilePath,edlfile),
            AUDIO = Carousel(lambda vformat: SaveAudioFrames(vformat['frame_rate'],tmpFilePath,edlfile)),
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
                ("AUDIO","signal") : ("","signal"),
                
#                ("MPLAYER","outbox") : ("DEBUG","inbox"),
#                ("MPLAYER","error") : ("DEBUG","inbox"),
#                ("MONITOR","outbox") : ("DEBUG","inbox"),
                },
            boxsizes = {
                ("FRAMES", "inbox") : 2,
                ("SPLIT",  "inbox") : 1,
                }
            )
        
def FilterForWantedFrameNumbers(edlfile):
    class ExtractRanges(object):
        def filter(self, edit):
            try:
                return (edit['start'],edit['end'])
            except:
                return None
    
    return Graphline(
        RANGESRC = Pipeline(
                       RateControlledFileReader(edlfile,readmode="lines",rate=1000000),
                       SAXPromptedParser(freeRun=True),
                       EDLParser(),
                       Filter(filter = ExtractRanges()),
                       Collate(),
                   ),
        FILTER   = Carousel(lambda ranges : RangeFilter(ranges)),
        linkages = {
            ("RANGESRC","outbox") : ("FILTER","next"),
            
            ("","inbox") : ("FILTER","inbox"),
            ("FILTER","outbox") : ("","outbox"),
            
            ("","control") : ("FILTER","control"),
            ("FILTER","signal") :("","signal"),
        },
        )
        
def DetermineMaxFrameNumber(edlfile):
    return Pipeline(
        RateControlledFileReader(edlfile,readmode="lines",rate=1000000),
        SAXPromptedParser(freeRun=True),
        EDLParser(),
        SimpleDetupler("end"),
        Collate(),
        Max(),
        )
        
def SaveVideoFrames(tmpFilePath,edlfile):
    return \
        Pipeline(
            TagWithSequenceNumber(),
            FilterForWantedFrameNumbers(edlfile),
            InboxControlledCarousel( lambda (framenum, frame) : \
                Pipeline( OneShot(frame),
                          FrameToYUV4MPEG(),
                          SimpleFileWriter(tmpFilePath+("%08d.yuv" % framenum)),
                        )
                ),
        )



def SaveAudioFrames(frame_rate,tmpFilePath,edlfile):
    return \
        Graphline(
            WAV = WAVParser(),
            AUD = Carousel(
                lambda ameta : AudioSplitterByFrames( frame_rate,
                                                      ameta['channels'],
                                                      ameta['sample_rate'],
                                                      ameta['sample_format'],
                                                      tmpFilePath,
                                                      edlfile,
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
                                              


def AudioSplitterByFrames(framerate, channels, sample_rate, sample_format,tmpFilePath,edlfile):
    from Kamaelia.Support.PyMedia.AudioFormats import format2BytesPerSample
    
    quantasize = format2BytesPerSample[sample_format] * channels
    audioByteRate = quantasize*sample_rate
    
    return Pipeline(
        Chunk(datarate=audioByteRate, quantasize=quantasize, chunkrate=framerate),
        TagWithSequenceNumber(),
        FilterForWantedFrameNumbers(edlfile),
        InboxControlledCarousel( lambda (framenum, audiochunk) : \
            Pipeline( OneShot(audiochunk),
                      WAVWriter(channels,sample_format,sample_rate),
                      SimpleFileWriter(tmpFilePath+("%08d.wav" % framenum)),
                    )
            ),
        )


# 2) reframe, writing out sequences

def ReframeVideo(edlfile, tmpFilePath, width, height):
    return Graphline( \
        GET_EDL = EditDecisionSource(edlfile),
        REFRAMER = Carousel( lambda edit : ProcessEditDecision(tmpFilePath, edit, width, height),
                             make1stRequest=True ),
        linkages = {
            ("REFRAMER", "requestNext") : ("GET_EDL", "inbox"),
            
            ("GET_EDL", "outbox") : ("REFRAMER", "next"),
            
            ("REFRAMER", "outbox") : ("", "outbox"),
            
            ("GET_EDL", "signal") : ("REFRAMER", "control"),
            ("REFRAMER", "signal") : ("", "signal"),
        },
        )

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
                                     2, MaxSpeedFileReader(filename,chunksize=1024*1024),
                                     2, YUV4MPEGToFrame(),
                                     ),
                                 make1stRequest=False ),
        REFRAMING = Pipeline( 2, YUVtoRGB(),
                              2, CropAndScale(newsize, cropbounds),
                              2, RGBtoYUV(),
                            ),
        linkages = {
            ("FRAME_LOADER", "requestNext") : ("FILENAMES", "inbox"),
            
            ("FILENAMES",    "outbox") : ("FRAME_LOADER", "next"),
            ("FRAME_LOADER", "outbox") : ("REFRAMING", "inbox"),
            ("REFRAMING",    "outbox") : ("", "outbox"),
            
            ("FILENAMES",    "signal") : ("FRAME_LOADER", "control"),
            ("FRAME_LOADER", "signal") : ("REFRAMING", "control"),
            ("REFRAMING",    "signal") : ("", "signal"),
        },
        boxsizes = {
        },
    )


def PassThroughAudio(edlfile, tmpFilePath):
    backplane_name = "AUDIO_FORMAT"
    return Graphline( \
        GET_EDL = EditDecisionSource(edlfile),
        AUDIO = Carousel( lambda edit : PassThroughAudioSegment(tmpFilePath, edit, backplane_name),
                          make1stRequest=True),
        
        BACKPLANE = Backplane(backplane_name),
        AUDIOFORMAT = Pipeline( SubscribeTo(backplane_name), FirstOnly() ),
        
        linkages = {
            ("AUDIO", "requestNext") : ("GET_EDL", "inbox"),
            
            ("GET_EDL", "outbox") : ("AUDIO", "next"),
            
            ("AUDIO", "outbox") : ("", "outbox"),
            
            ("AUDIOFORMAT", "outbox") : ("", "audioformat"),
            
            ("GET_EDL", "signal") : ("AUDIO", "control"),
            ("AUDIO", "signal") : ("AUDIOFORMAT", "control"),
            ("AUDIOFORMAT", "signal") : ("BACKPLANE", "control"),
            ("BACKPLANE", "signal") : ("", "signal"),
        },
        )

def PassThroughAudioSegment(tmpFilePath, edit, backplane_name):
    print " A ",edit
    filenames = [ tmpFilePath+"%08d.wav" % i for i in range(edit["start"], edit["end"]+1) ]
    
    return Graphline( \
        FILENAMES = ForwardIteratingChooser(filenames),
        FRAME_LOADER = Carousel( lambda filename : 
                                 Graphline(
                                     READ = MaxSpeedFileReader(filename),
                                     PARS = WAVParser(),
                                     META = PublishTo(backplane_name),
                                     linkages = {
                                         ("READ","outbox") : ("PARS","inbox"),
                                         ("PARS","outbox") : ("","outbox"),
                                         
                                         ("PARS","all_meta") : ("META","inbox"),
                                         
                                         ("","control") : ("READ","control"),
                                         ("READ","signal") : ("PARS","control"),
                                         ("PARS","signal") : ("META","control"),
                                         ("META","signal") : ("","signal"),
                                     },
                                     boxsizes = { ("PARS","inbox") : 2 },
                                 ),
                                 make1stRequest=False ),
        linkages = {
            ("FRAME_LOADER", "requestNext") : ("FILENAMES", "inbox"),
            
            ("FILENAMES",    "outbox") : ("FRAME_LOADER", "next"),
            ("FRAME_LOADER", "outbox") : ("", "outbox"),
            
            ("FILENAMES",    "signal") : ("FRAME_LOADER", "control"),
            ("FRAME_LOADER", "signal") : ("", "signal"),
        },
    )


# 3) concatenate sequences and reencode
def WriteToFiles():
    return Graphline( \
               VIDEO = FrameToYUV4MPEG(),
               AUDIO = WAVWriter(2, "S16_LE", 48000),
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
    encoder = "ffmpeg -f yuv4mpegpipe -i "+vidpipe+" -f wav -i "+audpipe+" -y "+outFileName
#    encoder = ( "mencoder -audiofile "+audpipe+" "+vidpipe +
#                " -ovc lavc -oac mp3lame" +
#                " -ffourcc DX50 -lavcopts acodec=mp3:vbitrate=200:abitrate=128" +
#                " -mc 0 -noskip" +
#                " -cache 16384 -audiofile-cache 500" + # -really-quiet" +
#                " -o "+outFileName
#              )
    print encoder
             
    return Graphline( \
               VIDEO = FrameToYUV4MPEG(),
               AUDIO = Carousel( lambda format : WAVWriter(**format),
                                 make1stRequest=False),
               ENCODE =  UnixProcess(encoder,buffersize=327680,inpipes={vidpipe:"video",audpipe:"audio"},boxsizes={"inbox":2,"video":2,"audio":2}),
               DEBUG = ConsoleEchoer(),
               linkages = {
                   ("","audioformat") : ("AUDIO","next"),
                   ("","video") : ("VIDEO","inbox"),
                   ("VIDEO","outbox") : ("ENCODE","video"),
                   
                   ("","audio") : ("AUDIO", "inbox"),
                   ("AUDIO","outbox") : ("ENCODE", "audio"),
                   
                   ("","control") : ("VIDEO","control"),
                   ("VIDEO","signal") : ("AUDIO","control"),
                   ("AUDIO","signal") : ("ENCODE", "control"),
                   ("ENCODE", "signal") : ("DEBUG", "control"),
                   ("DEBUG", "signal") : ("", "signal"),

                   ("ENCODE","outbox") : ("DEBUG","inbox"),
                   ("ENCODE","error") : ("DEBUG","inbox"),
               },
               boxsizes = {
                   ("VIDEO",  "inbox") : 2,
                   ("AUDIO",  "inbox") : 2,
               }
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
        
    

try:
    os.mkdir(tmpFilePath[:-1])
except:
    pass

from Seq import Seq

from Axon.Introspector import Introspector
from Kamaelia.Internet.TCPClient import TCPClient

Seq( "Decoding & separating frames...",
     lambda : Graphline(
          MAXF = DetermineMaxFrameNumber(edlfile),
          DO = Carousel( lambda maxframe : 
              DecodeAndSeparateFrames(inFileName, tmpFilePath, edlfile,maxframe),
          ),
          STOP = TriggeredOneShot(""),
#          PROF = Profiler(),
          linkages = {
              ("MAXF","outbox"):("DO","next"),
              ("DO","outbox"):("","outbox"),
              
              ("DO","requestNext"):("STOP","inbox"),
              ("STOP","signal"):("DO","control"),
              ("DO","signal"):("","signal"),
          },
          ),
     "Processing edits...",
     lambda : 
        Graphline(
            REFRAMING = ReframeVideo(edlfile, tmpFilePath, output_width, output_height),
            SOUND     = PassThroughAudio(edlfile, tmpFilePath),
            ENCODING  = ReEncode(outFileName),
#            PROF = Profiler(),
#            INTROSPECT = Pipeline(Introspector(),TCPClient("r44116",1601)),
        linkages = {
            ("REFRAMING","outbox") : ("ENCODING","video"),
            ("SOUND","outbox") : ("ENCODING","audio"),
            ("SOUND","audioformat") : ("ENCODING","audioformat"),
            
            ("REFRAMING","signal") : ("SOUND","control"),
            ("SOUND","signal") : ("ENCODING", "control"),
            },
        boxsizes = {
            ("ENCODING","video") : 2,
            ("ENCODING","audio") : 2,
            },
        ),
    "Cleaning up...",
    lambda : StopSelector(),
    ).run()

# clean up
for file in os.listdir(tmpFilePath):
    os.remove(tmpFilePath+file)
print "DONE"



