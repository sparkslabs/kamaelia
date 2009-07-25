#!/usr/bin/env python
#
# Copyright (C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
"""\
==================================================
Reframing of videos for mobile (and other) devices
==================================================

This is a command line tool that decodes a video clip; applies edit decisisions
(cutting, cropping and scaling); and re-encodes it. The idea is to cut and crop
video to make it suitable for playback on a small screen mobile device by
zooming in onto just the important bit - such as the face of the interviewee.

You supply a set of edit decisions in an XML file, and the VideoReframer will
apply those to the source video file you provide, creating a new output video
file with the resolution you specify



Getting Started
---------------

Pre-requisites
~~~~~~~~~~~~~~

You must have an installed copy of the command line ffmpeg tool, which can be
obtained from here. Make sure you have all the codecs you need of course!


Running VideoReframer.py
~~~~~~~~~~~~~~~~~~~~~~~~

Run VideoReframer.py from the command line and you'll get usage information::

    > ./VideoReframer.py

    Usage:
        VideoReframer.py <infile> <edlfile> <outfile> width height <tmpdir>

    * width and height are even numbered pixel dimensions for output video

So, for example, if you run it with the following command line::

    ./VideoReframer.py myVideo.avi myEditDecisions.xml theResult.avi 240 160 /tmp/video_reframer_scratch

This will apply the edit decisions in the xml file to the input video file and
produce a result that is 240x160 pixels.

Note that you need to specify a temporary working directory for the reframer
to use, since it needs somewhere to decompress video frames into. This temporary
directory should not be being used by any other programs, including other
instances of VideoReframer, and there should be enough free disk space to hold,
in the worst case, the whole input video file when decompressed to raw frames
and audio.



Writing the edit decision XML file
----------------------------------

Write your edit decisions in an XML file, like this::

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <EDL xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MobileReframe.xsd">

        <FileID>File identifier</FileID>

        <Edit>
            <Start frame="0"  />
            <End   frame="24" />
            <Crop  x1="0" y1="0" x2="400" y2="100" />
        </Edit>
        <Edit>
             frame="25" />
               frame="49" />
              x1="80" y1="40" x2="480" y2="140" />
        </Edit>

    </EDL>

The format is pretty simple: simply specify a set of 'edits', in the order you
want them to appear in the resulting video.

Each edit is a chunk of the input video specified by a start and end frame
number, and then the bit of the video you want it cropped down to. Frames are
numbered from zero, and coordinates are specified in pixels where (0,0) is the
top left corner.

For example perhaps, for frames 25 to 49 inclusive (a 2 second chunk that starts
4 seconds into the video, assuming 25fps video) we want the video to be cropped
to a region in the lower left of the image::

    +-----------------------------------------+
    |(0,0)                                    |
    |                                         |
    |          Throw this bit away            |
    |                                         |
    |     +---------------------+             |
    |     |(100,150)            |             |
    |     |                     |             |
    |     |  Crop to this bit   |             |
    |     |                     |             |
    |     |            (500,450)|             |
    |     +---------------------+             |
    |                                         |
    |                                (719,575)|
    +-----------------------------------------+

Then to achieve this we would write, as part of our edit decisions::

    <Edit>
        <Start frame="25" />
        <End   frame="49" />
        <Crop  x1="100" y1="150" x2="500" y2="450" />
    </Edit>

You can write your edit decisions in any order - you don't have to preserve the
chronological order of the original video. For example, perhaps the video you
are editing has 10 seconds of titles 30 seconds in from the start. Your edit
decisions could specify that the output video should start with a few seconds of
those titles, then return to something closer to the beginning.

You don't have to use the whole video - you can use your edit decisions to cut
a video down into a shorter one.
"""

from Kamaelia.Util.TagWithSequenceNumber import TagWithSequenceNumber
from Kamaelia.Util.OneShot import OneShot
from Kamaelia.Util.OneShot import TriggeredOneShot
from Kamaelia.Util.PromptedTurnstile import PromptedTurnstile
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Util.Chooser import ForwardIteratingChooser
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

from Kamaelia.Codec.YUV4MPEG import YUV4MPEGToFrame
from Kamaelia.Codec.YUV4MPEG import FrameToYUV4MPEG
from Kamaelia.Video.CropAndScale import CropAndScale

from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved
from Kamaelia.Video.PixFormatConversion import ToYUV420_planar

from Kamaelia.File.UnixProcess2 import UnixProcess2

from Kamaelia.Codec.WAV import WAVParser, WAVWriter

from Kamaelia.Util.TwoWaySplitter import TwoWaySplitter

from Kamaelia.Util.FirstOnly import FirstOnly
from Kamaelia.Util.RateChunker import RateChunker
from Kamaelia.Util.Sync import Sync

from Kamaelia.Util.Console import ConsoleEchoer

from Kamaelia.Experimental.Chassis import Pipeline
from Kamaelia.Experimental.Chassis import Graphline
from Kamaelia.Experimental.Chassis import Carousel
from Kamaelia.Experimental.Chassis import InboxControlledCarousel
from Kamaelia.Chassis.Seq import Seq

from Kamaelia.File.MaxSpeedFileReader import MaxSpeedFileReader

from Kamaelia.Util.Backplane import Backplane,PublishTo,SubscribeTo

from Kamaelia.Util.Collate import Collate
from Kamaelia.Util.Filter import Filter
from Kamaelia.Util.RangeFilter import RangeFilter
from Kamaelia.Util.Max import Max
from Kamaelia.Util.Detuple import SimpleDetupler

from StopSelector import StopSelector
from EDL import EDLParser


import sys

# 1) decode video to individual frames
def DecodeAndSeparateFrames(inFileName, tmpFilePath, edlfile,maxframe):
    """\
    Prefab.
    
    Decompresses audio and video from the specified file (using ffmpeg) and
    saves them as individual files into the provided temp directory. Only
    reads up to maxframes frames from the video file.
    
    Arguments:
    
    - inFileName   -- The video file to be decompressed
    - tmpFilePath  -- temp directory into which frames of audio and video should be saved
    - edlfile      -- full filepathname of the EDL xml file
    - maxframe     -- the number of frames to decompress
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
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
    
    mplayer = "ffmpeg -vframes %d -i %s -f yuv4mpegpipe -y %s -f wav -y %s" % ((maxframe+25),inFileName.replace(" ","\ "),vidpipe,audpipe)
    print mplayer
    
    return Graphline(
            DECODER = UnixProcess2(mplayer, 2000000, {vidpipe:"video",audpipe:"audio"}),
            FRAMES = YUV4MPEGToFrame(),
            SPLIT = TwoWaySplitter(),
            FIRST = FirstOnly(),
            VIDEO = SaveVideoFrames(tmpFilePath,edlfile),
            AUDIO = Carousel(lambda vformat: SaveAudioFrames(vformat['frame_rate'],tmpFilePath,edlfile)),
            linkages = {
                ("DECODER","video") : ("FRAMES","inbox"),
                ("FRAMES","outbox") : ("SPLIT","inbox"),
                ("SPLIT","outbox") : ("VIDEO","inbox"),
                
                ("SPLIT","outbox2") : ("FIRST","inbox"),
                ("FIRST","outbox") : ("AUDIO","next"),
                ("DECODER","audio") : ("AUDIO","inbox"),
                
                ("DECODER","signal") : ("FRAMES","control"),
                ("FRAMES","signal") : ("SPLIT","control"),
                ("SPLIT","signal") : ("VIDEO","control"),
                ("SPLIT","signal2") : ("FIRST","control"),
                ("FIRST","signal") : ("AUDIO","control"),
                ("AUDIO","signal") : ("","signal"),
                },
            boxsizes = {
                ("FRAMES", "inbox") : 2,
                ("SPLIT",  "inbox") : 1,
                ("FIRST", "inbox") : 2,
                ("VIDEO", "inbox") : 2,
                ("AUDIO", "inbox") : 10,
                }
            )
        
def FilterForWantedFrameNumbers(edlfile):
    """\
    Prefab.
    
    Send messages of the form (framenum, data) to the "inbox" inbox. Items with
    a frame number that isn't in the edit decision list are dropped. Other items
    with frame numbers that are in the edit decision list are passed through out
    of the "outbox" outbox.
    
    Arguments:
    
    - edlfile  -- full filepathname of the EDL xml file
    
    Inboxes:
    
    - "inbox"    -- (framenum, data) items to be filtered
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- items not filtered out
    - "signal"  -- Shutdown signalling
    """
    class ExtractRanges(object):
        def filter(self, edit):
            try:
                return (edit['start'],edit['end'])
            except:
                return None
    
    return Graphline(
        RANGESRC = Pipeline(
                       RateControlledFileReader(edlfile,readmode="lines",rate=1000000),
                       SimpleXMLParser(),
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
    """\
    Prefab.
    
    "outbox" sends out the highest frame number referenced in the EDL xml file.
    Then terminates immediately and sends out a producerFinished() message from
    the "signal" outbox.
    
    Arguments:
    
    - edlfile  -- full filepathname of the EDL xml file
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- sends out the highest frame number referenced in the EDL file
    - "signal"  -- Shutdown signalling
    """
    return Pipeline(
        RateControlledFileReader(edlfile,readmode="lines",rate=1000000),
        SimpleXMLParser(),
        EDLParser(),
        SimpleDetupler("end"),
        Collate(),
        Max(),
        )
        
def SaveVideoFrames(tmpFilePath,edlfile):
    """\
    Prefab.
    
    Saves video frames sent to the "inbox" inbox into the specified temp
    directory. Only saves those frames actually referenced in the EDL file.
    
    Frames are saved in individual files in YUV4MPEG2 format. They are named
    sequentially "00000001.yuv", "00000002.yuv", "00000003.yuv", etc - being
    assigned frame numbers as they arrive, starting at 1.
    
    Arguments:
    
    - tmpFilePath  -- temp directory into which frames should be saved
    - edlfile      -- full filepathname of the EDL xml file
    
    Inboxes:
    
    - "inbox"    -- video frames to be saved
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
    return \
        Pipeline(
            1, TagWithSequenceNumber(),
            1, FilterForWantedFrameNumbers(edlfile),
            1, InboxControlledCarousel( lambda (framenum, frame) : \
                Pipeline( OneShot(frame),
                          1, FrameToYUV4MPEG(),
                          1, SimpleFileWriter(tmpFilePath+("%08d.yuv" % framenum)),
                        ),
                boxsize=1,
                ),
        )



def SaveAudioFrames(frame_rate,tmpFilePath,edlfile):
    """\
    Prefab.
    
    Saves WAV audio data sent to the "inbox" inbox into the specified temp
    directory. Chunks the audio into frames, as per the specified frame-rate.
    Only saves those frames actually referenced in the EDL file.
    
    Frames are saved in individual files in WAV format. They are named
    sequentially "00000001.wav", "00000002.wav", "00000003.wav", etc - being
    assigned frame numbers as they arrive, starting at 1.
    
    Arguments:
    
    - frame_rate   -- the frame rate to chunk the audio into for saving
    - tmpFilePath  -- temp directory into which frames should be saved
    - edlfile      -- full filepathname of the EDL xml file
    
    Inboxes:
    
    - "inbox"    -- WAV format audio data
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
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
            },
            boxsizes = {
                ("WAV", "inbox") : 10,
                ("AUD", "inbox") : 10,
            },
        )
                                              

def AudioSplitterByFrames(framerate, channels, sample_rate, sample_format,tmpFilePath,edlfile):
    """\
    Prefab.
    
    Saves raw audio data in the specified (chanels,sample_rate,sample_format)
    format sent to the "inbox" inbox into the specified temp
    directory. Chunks the audio into frames, as per the specified frame-rate.
    Only saves those frames actually referenced in the EDL file.
    
    Frames are saved in individual files in WAV format. They are named
    sequentially "00000001.wav", "00000002.wav", "00000003.wav", etc - being
    assigned frame numbers as they arrive, starting at 1.
    
    Arguments:
    
    - frame_rate   -- the frame rate to chunk the audio into for saving
    - channels     -- number of channels in the audio data
    - sample_rate  -- sample rate of the audio data
    - sample_format  -- sample format of the audio data
    - tmpFilePath  -- temp directory into which frames should be saved
    - edlfile      -- full filepathname of the EDL xml file
    
    Inboxes:
    
    - "inbox"    -- raw audio data
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
    from Kamaelia.Support.PyMedia.AudioFormats import format2BytesPerSample
    
    quantasize = format2BytesPerSample[sample_format] * channels
    audioByteRate = quantasize*sample_rate

    return Pipeline(
        10, RateChunker(datarate=audioByteRate, quantasize=quantasize, chunkrate=framerate),
        1, TagWithSequenceNumber(),
        1, FilterForWantedFrameNumbers(edlfile),
        1, InboxControlledCarousel( lambda (framenum, audiochunk) : \
            Pipeline( 1, OneShot(audiochunk),
                      1, WAVWriter(channels,sample_format,sample_rate),
                      1, SimpleFileWriter(tmpFilePath+("%08d.wav" % framenum)),
                    ),
                    boxsize=1,
            ),
        )


# 2) reframe, writing out sequences

def ReframeVideo(edlfile, tmpFilePath, width, height):
    """\
    Prefab.
    
    Goes through the specified edit decision list file and reads in video frames
    applying the reframing instructions in sequence. Outputs the reframed video
    frames out of the "outbox" outbox.
    
    Arguments:
    
    - tmpFilePath  -- temp directory into which video frames have been saved
    - edlfile      -- full filepathname of the EDL xml file
    - width        -- width (in pixels) for output video frames
    - height       -- height (in pixels) for output video frames
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
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
    """\
    Prefab.
    
    Reads in the edit decisions from the edit decision list file; then sends
    then out, one at a time, out of the "outbox" outbox whenever a message is
    sent to the "inbox" inbox. The message sent to the inbox does not matter.
    
    Edit decisions are of the form::
    
        { "start"  : start frame number for this edit decision
          "end"    : end frame number for this edit decision
          "left"   : left edge to crop to (in pixels)
          "top"    : top edge to crop to (in pixels)
          "right"  : right edge to crop to (in pixels)
          "bottom" : bottom edge to crop to (in pixels)
        }
    
    Arguments:
    
    - edlfile      -- full filepathname of the EDL xml file
    
    Inboxes:
    
    - "inbox"    -- Messages to trigger sending out of edit decisions
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- Individual edit decisions
    - "signal"  -- Shutdown signalling
    """
    return Graphline( \
        PARSING = Pipeline( RateControlledFileReader(edlfile,readmode="lines",rate=1000000),
                            SimpleXMLParser(),
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
    """\
    Prefab.
    
    Applies an edit decision - reading in the relevant video frames and applying
    the reframing. Outputs the reframed video frames out of the "outbox" outbox.
    
    Arguments:
    
    - tmpFilePath  -- temp directory into which video frames have been saved
    - edit         -- the edit instruction (dictionary containing: "start","end","left","top","right","bottom")
    - width        -- width (in pixels) for output video frames
    - height       -- height (in pixels) for output video frames
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
    print " Video segment: ",edit
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
        REFRAMING = Pipeline( 2, ToRGB_interleaved(),
                              2, CropAndScale(newsize, cropbounds),
                              2, ToYUV420_planar(),
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
    """\
    Prefab.
    
    Goes through the specified edit decision list file and reads in the audio
    frames corresponding to the video frames referred to in the reframing
    instructions in sequence. Outputs the audio frames out of the "outbox"
    outbox.
    
    Arguments:
    
    - edlfile      -- full filepathname of the EDL xml file
    - tmpFilePath  -- temp directory into which video frames have been saved
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- raw audio data, chunked by frames
    - "signal"  -- Shutdown signalling
    """
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
    """\
    Prefab.
    
    For a particular edit decision; reads in the audio frames corresponding to
    the video frames referred to in the reframing instructions in sequence.
    Outputs the audio frames out of the "outbox" outbox.
    
    Arguments:
    
    - edlfile      -- full filepathname of the EDL xml file
    - tmpFilePath  -- temp directory into which video frames have been saved
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    
    Outboxes:
    
    - "outbox"  -- raw audio data, chunked by frames
    - "signal"  -- Shutdown signalling
    """
    print " Audio segment: ",edit
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
    """\
    Prefab.
    
    Takes in audio and video frames and writes them as a single YUV4MPEG2 and
    WAV files ("test.yuv" and "test.wav").
    
    Used for testing
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    - "video"    -- Video frames to be saved
    - "audio"    -- Auio frames to be saved
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
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
    """\
    Prefab.
    
    Takes in audio and video frames and encodes them to a compressed video file
    using ffmpeg to do the compression.
    
    Inboxes:
    
    - "inbox"    -- NOT USED
    - "control"  -- Shutdown signalling
    - "video"    -- Video frames to be saved
    - "audio"    -- Auio frames to be saved
    
    Outboxes:
    
    - "outbox"  -- NOT USED
    - "signal"  -- Shutdown signalling
    """
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
    
    encoder = "ffmpeg -f yuv4mpegpipe -i "+vidpipe+" -f wav -i "+audpipe+" -y "+outFileName
    print encoder
             
    return Graphline( \
               VIDEO = FrameToYUV4MPEG(),
               AUDIO = Carousel( lambda format : WAVWriter(**format),
                                 make1stRequest=False),
               ENCODE =  UnixProcess2(encoder,buffersize=327680,inpipes={vidpipe:"video",audpipe:"audio"},boxsizes={"inbox":2,"video":2,"audio":2}),
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
    sys.stderr.write("    VideoReframer.py <infile> <edlfile> <outfile> width height <tmpdir>\n")
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


Seq( "Decoding & separating frames...",
     Graphline(
          MAXF = DetermineMaxFrameNumber(edlfile),
          DO = Carousel( lambda maxframe : 
              DecodeAndSeparateFrames(inFileName, tmpFilePath, edlfile,maxframe),
          ),
          STOP = TriggeredOneShot(""),
          linkages = {
              ("MAXF","outbox"):("DO","next"),
              ("DO","outbox"):("","outbox"),
              
              ("DO","requestNext"):("STOP","inbox"),
              ("STOP","signal"):("DO","control"),
              ("DO","signal"):("","signal"),
          },
          ),
     "Processing edits...",
        Graphline(
            REFRAMING = ReframeVideo(edlfile, tmpFilePath, output_width, output_height),
            SOUND     = PassThroughAudio(edlfile, tmpFilePath),
            ENCODING  = ReEncode(outFileName),
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
    StopSelector(),
    ).run()

# clean up
for file in os.listdir(tmpFilePath):
    os.remove(tmpFilePath+file)
print "DONE"



