#!/usr/bin/python

import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper
from Kamaelia.UI.OpenGL.MatchedTranslationInteractor import MatchedTranslationInteractor
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.Pygame.Button import Button
from Kamaelia.UI.Pygame.Text import Textbox, TextDisplayer

from Kamaelia.UI.Pygame.VideoSurface import VideoSurface
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved

# override pygame display service
ogl_display = OpenGLDisplay.getDisplayService(fullscreen=True)
PygameDisplay.setDisplayService(ogl_display[0])

READER = Textbox(size = (400, 300),text_height=30).activate()
WRITER = TextDisplayer(size = (400, 300),text_height=30).activate()

SCREEN = VideoSurface().activate()


Pipeline(
         ReadFileAdaptor("../TestMaterial/TrainWindow.drc", readmode="bitrate",
                         bitrate = 1000000),
         DiracDecoder(),
         MessageRateLimit(10),
         ToRGB_interleaved(),
         SCREEN,
).activate()

R_ = PygameWrapper(
    wrap=READER, position=(-2, -2,-10), rotation=(20,10,0)
).activate()

W_ = PygameWrapper(
    wrap=WRITER, position=(2, 2,-10), rotation=(20,10,0)
).activate()

S_ = PygameWrapper(
    wrap=SCREEN, position=(-2, 2,-10), rotation=(20,10,0)
).activate()

i1 = MatchedTranslationInteractor(target=R_).activate()
i2 = MatchedTranslationInteractor(target=W_).activate()
i3 = MatchedTranslationInteractor(target=S_).activate()

button1 = Button(caption="QUIT",msg="QUIT").activate()

class Quitter(Axon.Component.component):
    def main(self):
        self.pause()
        yield 1
        self.scheduler.stop()

Pipeline(
    READER,
    WRITER,
).activate()

Pipeline(
    button1 ,
    Quitter(),
).activate()

Axon.Scheduler.scheduler.run.runThreads()  
