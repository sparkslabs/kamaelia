#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
#

import os
import sys
import Axon
import pygame
import cjson

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.ConnectedServer import SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient

from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Visualisation.PhysicsGraph.chunks_to_lines import chunks_to_lines
from Kamaelia.Util.NullSink import nullSinkComponent

from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.Util.Detuple import SimpleDetupler
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer

# Ticker
from Kamaelia.UI.Pygame.Ticker import Ticker

from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.Protocol.Framing import DataChunker, DataDeChunker

#
# The following application specific components will probably be rolled
# back into the repository.
#
from Kamaelia.Apps.Whiteboard.TagFiltering import TagAndFilterWrapper, FilterAndTagWrapper
from Kamaelia.Apps.Whiteboard.TagFiltering import TagAndFilterWrapperKeepingTag
from Kamaelia.Apps.Whiteboard.Tokenisation import tokenlists_to_lines, lines_to_tokenlists
from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Apps.Whiteboard.Painter import Painter
from Kamaelia.Apps.Whiteboard.SingleShot import OneShot
from Kamaelia.Apps.Whiteboard.CheckpointSequencer import CheckpointSequencer
from Kamaelia.Apps.Whiteboard.Entuple import Entuple
from Kamaelia.Apps.Whiteboard.Routers import Router, TwoWaySplitter, ConditionalSplitter
from Kamaelia.Apps.Whiteboard.Palette import buildPalette, colours
from Kamaelia.Apps.Whiteboard.Options import parseOptions
from Kamaelia.Apps.Whiteboard.UI import PagingControls, Eraser, ClearPage, SaveDeck, LoadDeck, ClearScribbles, Delete, Quit
from Kamaelia.Apps.Whiteboard.CommandConsole import CommandConsole
#from Kamaelia.Apps.Whiteboard.SmartBoard import SmartBoard
from Kamaelia.Apps.Whiteboard.Webcam import VideoCaptureSource, WebcamManager
from Kamaelia.Apps.Whiteboard.Email import Email
from Kamaelia.Apps.Whiteboard.Decks import Decks
from Kamaelia.Apps.Whiteboard.ProperSurfaceDisplayer import ProperSurfaceDisplayer

from Kamaelia.Apps.Whiteboard.Play import AlsaPlayer
from Kamaelia.Apps.Whiteboard.Record import AlsaRecorder

try:
    from Kamaelia.Codec.Speex import SpeexEncode,SpeexDecode
except Exception, e:
    print "Speex not available, using null components instead"
    SpeexEncode = nullSinkComponent
    SpeexDecode = nullSinkComponent

#try:
#    from Kamaelia.Apps.Whiteboard.Audio import SoundInput
#except ImportError:
#    print "SoundInput not available, using NullSink instead"
#    SoundInput = nullSinkComponent

#try:
#    from Kamaelia.Apps.Whiteboard.Audio import SoundOutput
#except ImportError:
#    print "SoundOutput not available, using NullSink instead"
#    SoundOutput = nullSinkComponent

#try:
#    from Kamaelia.Apps.Whiteboard.Audio import RawAudioMixer
#except ImportError:
#    print "RawAudioMixer not available, using NullSink instead"
#    RawAudioMixer = nullSinkComponent

defaults = {"email" : {"server" : "","port" : "","user" : "","pass": "","from" : ""},\
            "directories" : {"scribbles" : os.path.expanduser("~") + "/.kamaelia/Kamaelia.Apps.Whiteboard/Scribbles",\
                             "decks" : os.path.expanduser("~") + "/Whiteboard/Decks"},\
            "webcam" : {"device" : "/dev/video0"}}
config = defaults
emailavailable = False
# Load Config
try:
    wbdirs = ["/etc/kamaelia/Kamaelia.Apps.Whiteboard","/usr/local/etc/kamaelia/Kamaelia.Apps.Whiteboard",os.path.expanduser("~") + "/.kamaelia/Kamaelia.Apps.Whiteboard"]
    raw_config = False
    for directory in wbdirs:
        if os.path.isfile(directory + "/whiteboard.conf"):
            file = open(directory + "/whiteboard.conf")
            raw_config = file.read()
            file.close()
        if raw_config:
            try:
                temp_config = cjson.decode(raw_config)
                entries = ["email","directories", "webcam"]
                for entry in entries:
                    if temp_config.has_key(entry):
                        for key in temp_config[entry].keys():
                            config[entry][key] = temp_config[entry][key]
                        emailavailable = True
            except cjson.DecodeError, e:
                print("Could not decode config file in " + dir)
except IOError, e:
    print ("Failed to load config file")

if defaults['directories']['scribbles'] != config['directories']['scribbles']:
    # Remove trailing '/' if exists:
    if config['directories']['scribbles'][-1:] == "/":
        config['directories']['scribbles'] = config['directories']['scribbles'][0:-1]

    # Check directories exist
    if os.path.exists(config['directories']['scribbles']):
        if not os.path.isdir(config['directories']['scribbles']):
            print("You have a user configured Scribbles directory that can't be found. Please create it.")
            sys.exit(0)
    else:
        print("You have a user configured Scribbles directory that can't be found. Please create it.")
        sys.exit(0)
elif not os.path.exists(config['directories']['scribbles']):
    os.makedirs(config['directories']['scribbles'])  

if defaults['directories']['decks'] != config['directories']['decks']:
    # Remove trailing '/' if exists:
    if config['directories']['decks'][-1:] == "/":
        config['directories']['decks'] = config['directories']['decks'][0:-1]

    # Check directories exist
    if os.path.exists(config['directories']['decks']):
        if not os.path.isdir(config['directories']['decks']):
            print("You have a user configured Decks directory that can't be found. Please create it.")
            sys.exit(0)
    else:
        print("You have a user configured Decks directory that can't be found. Please create it.")
        sys.exit(0)
elif not os.path.exists(config['directories']['decks']):
    os.makedirs(config['directories']['decks'])


#
# Misplaced encapsulation --> Kamaelia.Apps.Whiteboard.Palette
#
colours_order = [ "black", "red", "orange", "yellow", "green", "turquoise", "blue", "purple", "darkgrey", "lightgrey" ]

num_pages = 0
for x in os.listdir(config['directories']['scribbles']):
    if (os.path.splitext(x)[1] == ".png"):
        num_pages += 1
if (num_pages < 1):
    num_pages = 1

def FilteringPubsubBackplane(backplaneID,**FilterTagWrapperOptions):
  """Sends tagged events to a backplane. Emits events not tagged by this pubsub."""
  return FilterAndTagWrapper(
            Pipeline(
                PublishTo(backplaneID),
                # well, should be to separate pipelines, this is lazier!
                SubscribeTo(backplaneID),
            ),
            **FilterTagWrapperOptions
         )


def clientconnector(whiteboardBackplane="WHITEBOARD", audioBackplane="AUDIO", port=1500):
    return Pipeline(
        chunks_to_lines(),
        lines_to_tokenlists(),
        Graphline(
            ROUTER = Router( ((lambda T : T[0]=="SOUND"), "audio"),
                             ((lambda T : T[0]!="SOUND"), "whiteboard"),
                           ),
            WHITEBOARD = FilteringPubsubBackplane(whiteboardBackplane),
            AUDIO = Pipeline(
                        SimpleDetupler(1),     # remove 'SOUND' tag
                        SpeexDecode(3),
                        FilteringPubsubBackplane(audioBackplane, dontRemoveTag=True),
                        PureTransformer(lambda x : x[1]),
                        #RawAudioMixer(),
                        SpeexEncode(3),
                        Entuple(prefix=["SOUND"],postfix=[]),
                    ),
            linkages = {
                # incoming messages go to a router
                ("self", "inbox") : ("ROUTER", "inbox"),
                # distribute messages to appropriate destinations
                ("ROUTER",      "audio") : ("AUDIO",      "inbox"),
                ("ROUTER", "whiteboard") : ("WHITEBOARD", "inbox"),
                # aggregate all output
                ("AUDIO",      "outbox") : ("self", "outbox"),
                ("WHITEBOARD", "outbox") : ("self", "outbox"),
                # shutdown routing, not sure if this will actually work, but hey!
                ("self", "control") : ("ROUTER", "control"),
                ("ROUTER", "signal") : ("AUDIO", "control"),
                ("AUDIO", "signal") : ("WHITEBOARD", "control"),
                ("WHITEBOARD", "signal") : ("self", "signal")
                },
            ),
        tokenlists_to_lines(),
        )

class StringToSurface(component):
    # This component converts strings to pygame surfaces

    Inboxes = {
        "inbox" : "Receives strings for conversion in the format",
        "control" : "",
    }
    Outboxes = {
        "outbox" : "Outputs pygame surfaces",
        "signal" : "",
    }
    
    def __init__(self,width=190,height=140):
        super(StringToSurface, self).__init__()
        self.width = width
        self.height = height

    def finished(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, "signal")
                return True
        return False
    
    def main(self):
        while not self.finished():
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                # Convert string to Pygame image using a particular size
                try: # Prevent crashing with malformed received images
                    image = pygame.image.fromstring(data,(self.width,self.height),"RGB")
                    self.send(image, "outbox")
                except Exception, e:
                    sys.stderr.write("Error converting string to PyGame surface in StringToSurface")
            self.pause()
            yield 1

def clientconnectorwc(webcamBackplane="WEBCAM", port=1501):
    # Connects webcams to the network
    return Pipeline(
        Graphline(
            WEBCAM = FilteringPubsubBackplane(webcamBackplane),
            STRINGCONVERTER = PureTransformer(lambda x: pygame.image.tostring(x,"RGB")),
            SURFACECONVERTER = StringToSurface(190,140),
            FRAMER = DataChunker(),
            CONSOLE = ConsoleEchoer(),
            DEFRAMER = DataDeChunker(),
            SIZER = PureTransformer(lambda x: pygame.transform.scale(x,(190,140))), # This is a temporary fix - we should really be sending full resolution images
            # The issue is that to do this we need to send the original size as metadata and this needs more work to include
            linkages = {
                # Receive data from the network - deframe and convert to image for display
                ("self", "inbox") : ("DEFRAMER", "inbox"),
                ("DEFRAMER", "outbox") : ("SURFACECONVERTER", "inbox"),
                # Send to display
                ("SURFACECONVERTER", "outbox") : ("WEBCAM", "inbox"),
                # Forward local images to the network - convert to strings and frame
                ("WEBCAM", "outbox") : ("SIZER", "inbox"),
                ("SIZER", "outbox") : ("STRINGCONVERTER", "inbox"),
                ("STRINGCONVERTER", "outbox") : ("FRAMER", "inbox"),
                # Send to network
                ("FRAMER", "outbox") : ("self", "outbox"),
                },
            ),
        )

#/-------------------------------------------------------------------------
# Server side of the system
#

def LocalEventServer(whiteboardBackplane="WHITEBOARD", audioBackplane="AUDIO", port=1500):
    def configuredClientConnector():
        return clientconnector(whiteboardBackplane=whiteboardBackplane,
                               audioBackplane=audioBackplane,
                               port=port)
    return SimpleServer(protocol=clientconnector, port=port)
    
def LocalWebcamEventServer(webcamBackplane="WEBCAM", port=1501):
    # Sets up the webcam server in a similar way to the one used for images and audio
    def configuredClientConnector():
        return clientconnectorwc(webcamBackplane=webcamBackplane,
                                 port=port)
    return SimpleServer(protocol=clientconnectorwc, port=port)

#/-------------------------------------------------------------------------
# Client side of the system
#
def EventServerClients(rhost, rport, 
                       whiteboardBackplane="WHITEBOARD",
                       audioBackplane="AUDIO"):
    # plug a TCPClient into the backplane
    
    loadingmsg = "Fetching sketch from server..."

    return Graphline(
            # initial messages sent to the server, and the local whiteboard
            GETIMG = Pipeline(
                        OneShot(msg=[["GETIMG"]]),
                        tokenlists_to_lines()
                    ),
            BLACKOUT =  OneShot(msg="CLEAR 0 0 0\r\n"
                                    "WRITE 100 100 24 255 255 255 "+loadingmsg+"\r\n"),
            NETWORK = TCPClient(host=rhost,port=rport),
            APPCOMMS = clientconnector(whiteboardBackplane=whiteboardBackplane,
                                       audioBackplane=audioBackplane),
            linkages = {
                ("GETIMG",   "outbox") : ("NETWORK",    "inbox"), # Single shot out
                ("APPCOMMS", "outbox") : ("NETWORK", "inbox"), # Continuous out

                ("BLACKOUT", "outbox") : ("APPCOMMS", "inbox"), # Single shot in
                ("NETWORK", "outbox") : ("APPCOMMS", "inbox"), # Continuous in
            } 
        )
        
def WebcamEventServerClients(rhost, rport, 
                       webcamBackplane="WEBCAM"):
    # Allows retrieval of remote cam images from the network
    # plug a TCPClient into the backplane

    return Graphline(
            NETWORK = TCPClient(host=rhost,port=rport),
            APPCOMMS = clientconnectorwc(webcamBackplane=webcamBackplane),
            linkages = {
                ("APPCOMMS", "outbox") : ("NETWORK", "inbox"), # Continuous out
                ("NETWORK", "outbox") : ("APPCOMMS", "inbox"), # Continuous in
            } 
        )
#/-------------------------------------------------------------------------

class LocalPageEventsFilter(ConditionalSplitter): # This is a data tap/siphon/demuxer
    def condition(self, data):
        return (data == [["prev"]]) or (data == [["next"]])
    def true(self,data):
        self.send((data[0][0], "local"), "true")

SLIDESPEC = config['directories']['scribbles'] +"/slide.%d.png"





def makeBasicSketcher(left=0,top=0,width=1024,height=768,is_client=False):
    if is_client:
        # This is a temporary addition to prevent slide synchronisation issues between server and client
        # This could be removed should full synchronisation of files between clients and servers be achieved
        CLEAR = nullSinkComponent()
        SAVEDECK = nullSinkComponent()
        LOADDECK = nullSinkComponent()
        DELETE = nullSinkComponent()
        CLOSEDECK = nullSinkComponent()
        PAGINGCONTROLS = nullSinkComponent()
    else:
        CLEAR = ClearPage(left+(64*5)+32*len(colours)+1,top)                 
        SAVEDECK = SaveDeck(left+(64*8)+32*len(colours)+1,top)
        LOADDECK = LoadDeck(left+(64*7)+32*len(colours)+1,top)
        DELETE = Delete(left+(64*6)+32*len(colours)+1,top)
        CLOSEDECK = ClearScribbles(left+(64*9)+32*len(colours)+1,top)
        PAGINGCONTROLS = PagingControls(left+64+32*len(colours)+1,top)
    return Graphline( CANVAS  = Canvas( position=(left,top+32+1),size=(width-192,(height-(32+15)-1)),bgcolour=(255,255,255) ),
                      PAINTER = Painter(),
                      PALETTE = buildPalette( cols=colours, order=colours_order, topleft=(left+64,top), size=32 ),
                      ERASER  = Eraser(left,top),
                      CLEAR = CLEAR,
                      
                      SAVEDECK = SAVEDECK,
                      LOADDECK = LOADDECK,
                      
                      DECKMANAGER = Decks(config['directories']['scribbles'],config['directories']['decks'],emailavailable),
                      
  #                    SMARTBOARD = SmartBoard(),
                      
                      DELETE = DELETE,
                      CLOSEDECK = CLOSEDECK,
                      QUIT = Quit(left+(64*10)+32*len(colours)+1,top),

                      PAGINGCONTROLS = PAGINGCONTROLS,
                      #LOCALPAGINGCONTROLS = LocalPagingControls(left+(64*6)+32*len(colours),top),
                      LOCALPAGEEVENTS = LocalPageEventsFilter(),

                      HISTORY = CheckpointSequencer(lambda X: [["LOAD", SLIDESPEC % (X,), 'nopropogate']],
						    lambda X: [["LOAD", SLIDESPEC % (X,)]],
                                                    lambda X: [["SAVE", SLIDESPEC % (X,)]],
                                                    lambda X: [["NEW"]],
                                                    initial = 1,
                                                    last = num_pages,
                                ),

                      PAINT_SPLITTER = TwoWaySplitter(),
                      #LOCALEVENT_SPLITTER = TwoWaySplitter(),
                      DEBUG   = ConsoleEchoer(),
                      
                      TICKER = Ticker(position=(left,top+height-15),background_colour=(220,220,220),text_colour=(0,0,0),text_height=(17),render_right=(width),render_bottom=(15)),

                      EMAIL = Email(config['email']['server'],config['email']['port'],config['email']['from'],config['email']['user'],config['email']['pass']),

                      linkages = {
                          ("CANVAS",  "eventsOut") : ("PAINTER", "inbox"),
                          ("PALETTE", "outbox")    : ("PAINTER", "colour"),
                          ("ERASER", "outbox")     : ("PAINTER", "erase"),

                          ("PAINTER", "outbox")    : ("PAINT_SPLITTER", "inbox"),
                          ("CLEAR","outbox")       : ("PAINT_SPLITTER", "inbox"),
                          ("PAINT_SPLITTER", "outbox")  : ("CANVAS", "inbox"),
                          ("PAINT_SPLITTER", "outbox2") : ("self", "outbox"), # send to network
                          
                          ("SAVEDECK", "outbox") : ("DECKMANAGER", "inbox"),
                          ("LOADDECK", "outbox") : ("DECKMANAGER", "inbox"),
                          
                          ("CLOSEDECK", "outbox") : ("DECKMANAGER", "inbox"),
                          ("DELETE", "outbox") : ("HISTORY", "inbox"),
                          
                          ("DECKMANAGER", "toTicker") : ("TICKER", "inbox"),
                          ("DECKMANAGER", "toCanvas") : ("CANVAS", "inbox"),
                          ("DECKMANAGER", "toSequencer") : ("HISTORY", "inbox"),
                          ("QUIT", "outbox") : ("DECKMANAGER", "inbox"),
                          
                          #("LOCALPAGINGCONTROLS","outbox")  : ("LOCALEVENT_SPLITTER", "inbox"),
                          #("LOCALEVENT_SPLITTER", "outbox2"): ("", "outbox"), # send to network
                          #("LOCALEVENT_SPLITTER", "outbox") : ("LOCALPAGEEVENTS", "inbox"),
                          ("self", "inbox")        : ("LOCALPAGEEVENTS", "inbox"),
                          ("LOCALPAGEEVENTS", "false")  : ("CANVAS", "inbox"),
                          ("LOCALPAGEEVENTS", "true")  : ("HISTORY", "inbox"),

                          ("PAGINGCONTROLS","outbox") : ("HISTORY", "inbox"),
                          ("HISTORY","outbox")     : ("CANVAS", "inbox"),
                          
                          ("HISTORY","toDecks")     : ("DECKMANAGER", "inbox"),

                          ("CANVAS", "outbox")     : ("self", "outbox"),
                          ("CANVAS","surfacechanged") : ("HISTORY", "inbox"),
                          
#                          ("SMARTBOARD", "colour") : ("PAINTER", "colour"),
#                          ("SMARTBOARD", "erase") : ("PAINTER", "erase"),
#                          ("SMARTBOARD", "toTicker") : ("TICKER", "inbox"),

                          ("DECKMANAGER", "toEmail") : ("EMAIL", "inbox"),
                          ("EMAIL", "outbox") : ("DECKMANAGER", "fromEmail"),
                          },
                    )



if __name__=="__main__":

    left = 0
    top = 0
    width = 1024
    height = 768
    
    BACKGROUND = ProperSurfaceDisplayer(displaysize = (width, height), position = (left, top), bgcolour=(0,0,0)).activate()
    
    rhost, rport, serveport = parseOptions()
    
    if rhost and rport:
        is_client = True
    else:
        is_client = False
    
    mainsketcher = \
        Graphline( SKETCHER = makeBasicSketcher(left,top+1,width,height-1,is_client),
                   CONSOLE = CommandConsole(),
                   linkages = { ('self','inbox'):('SKETCHER','inbox'),
                                ('SKETCHER','outbox'):('self','outbox'),
                                ('CONSOLE','outbox'):('SKETCHER','inbox'),
                              }
                     )

    camera = Graphline( LOCALWEBCAM = VideoCaptureSource(config['webcam']['device']),
                        WCMANAGER = WebcamManager(camerasize = (190,140), vertical = True),
                        DISPLAY = ProperSurfaceDisplayer(displaysize = (190,height-34), position=(1024-191,32+2), bgcolour=(0,0,0)),
                        CAM_SPLITTER = TwoWaySplitter(),
                        CONSOLE = ConsoleEchoer(),
                        linkages = { ('self','inbox'):('WCMANAGER','inbox'),
                            ('LOCALWEBCAM','outbox'):('CAM_SPLITTER','inbox'),
                            ('CAM_SPLITTER','outbox2'):('WCMANAGER','inbox'),
                            ('WCMANAGER','outbox'):('DISPLAY','inbox'),
                            ('CAM_SPLITTER','outbox'):('self','outbox'),
                          }
                      )
        
    # primary whiteboard
    Pipeline( SubscribeTo("WHITEBOARD"),
              TagAndFilterWrapper(mainsketcher),
              PublishTo("WHITEBOARD")
            ).activate()
            
    # primary sound IO - tagged and filtered, so can't hear self
    Pipeline( SubscribeTo("AUDIO"),
              TagAndFilterWrapper(
                  Pipeline(
                      #RawAudioMixer(),
                      #PureTransformer(lambda x : x[1]),
                      AlsaPlayer(),
                      ######
                      AlsaRecorder(),
                  ),
              ),
              PublishTo("AUDIO"),
            ).activate()
            
    # primary webcam - capture > to jpeg > framing > backplane > TCPC > Deframing > etc
    Pipeline( SubscribeTo("WEBCAM"),
              TagAndFilterWrapperKeepingTag(camera),
              PublishTo("WEBCAM"),
            ).activate()

    # setup a server, if requested
    if serveport:
        LocalEventServer("WHITEBOARD", "AUDIO", port=serveport).activate()
        LocalWebcamEventServer("WEBCAM", port=(serveport+1)).activate()


    # connect to remote host & port, if requested
    if rhost and rport:
        EventServerClients(rhost, rport, "WHITEBOARD", "AUDIO").activate()
        WebcamEventServerClients(rhost, (rport + 1), "WEBCAM").activate()

#    sys.path.append("../Introspection")
#    from Profiling import FormattedProfiler
#    
#    Pipeline(FormattedProfiler( 20.0, 1.0),
#             ConsoleEchoer()
#            ).activate()


    Backplane("WHITEBOARD").activate()
    
    Backplane("WEBCAM").activate()
    
    Backplane("AUDIO").run()
    

    
