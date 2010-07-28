#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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

import Axon

from Kamaelia.Chassis.Graphline import Graphline

from Kamaelia.UI.OpenGL.OpenGLDisplay import OpenGLDisplay
from Kamaelia.UI.OpenGL.PygameWrapper import PygameWrapper
from Kamaelia.UI.OpenGL.SimpleTranslationInteractor import SimpleTranslationInteractor

from Kamaelia.Util.Console import ConsoleReader

from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle
from Kamaelia.UI.PygameDisplay import PygameDisplay
from Kamaelia.UI.Pygame.Ticker import Ticker

from Kamaelia.Apps.Whiteboard.Canvas import Canvas
from Kamaelia.Apps.Whiteboard.Painter import Painter
from Kamaelia.Apps.Whiteboard.Palette import buildPalette, colours
from Kamaelia.Apps.Whiteboard.UI import Eraser, ClearPage

#from Webcam import Webcam
from Webcam import VideoCaptureSource

#from BlankCanvas import BlankCanvas


if __name__=="__main__":
    width = 1024
    height = 768
    top = 0
    left = 0
    colours_order = [ "black", "red", "orange", "yellow", "green", "turquoise", "blue", "purple", "darkgrey", "lightgrey" ]
    ogl_display = OpenGLDisplay(title="Kamaelia Whiteboard",width=width,height=height,background_colour=(255,255,255))
    ogl_display.activate()
    OpenGLDisplay.setDisplayService(ogl_display)
    
    ogl_display = OpenGLDisplay.getDisplayService()
    PygameDisplay.setDisplayService(ogl_display[0])
    
    #PygameDisplay.setDisplayService(ogl_display)
    CANVAS = Canvas( position=(left,top+32),width=1200,height=(900-(32+15)),notepad="Test" ).activate() #(replace width with 'width' and height with 'height-(32+15)'
    PAINTER = Painter().activate()
    CANVAS_WRAPPER = PygameWrapper(wrap=CANVAS, position=(0,0,-10), rotation=(0,0,0)).activate() 
    ERASER  = Eraser(left,top).activate()
    PALETTE = buildPalette( cols=colours, order=colours_order, topleft=(left+64,top), size=32 ).activate()
    CLEAR = ClearPage(left+(64*5)+32*len(colours),top).activate()
    #PALETTE_WRAPPER = PygameWrapper(wrap=PALETTE, position=(4,1,-10), rotation=(-20,15,3)).activate()
    
    #PAINTER_WRAPPER = PygameWrapper(wrap=PAINTER, position=(4,1,-10), rotation=(-20,15,3)).activate()
    CANVAS.link( (PAINTER,"outbox"), (CANVAS, "inbox") )
    PAINTER.link( (CANVAS,"eventsOut"), (PAINTER, "inbox") )
    PAINTER.link( (PALETTE,"outbox"), (PAINTER, "colour") )
    PAINTER.link( (ERASER, "outbox"), (PAINTER, "erase") )
    PAINTER.link( (CLEAR, "outbox"), (CANVAS, "inbox") )
              
    WEBCAM = VideoCaptureSource().activate()
    BLANKCANVAS = Canvas( position=(left,top+32),width=(63*3+2),height=140,notepad="Test",bgcolour=(200,200,200) ).activate()
    #BLANKCANVAS = BlankCanvas().activate()
    BLANKCANVAS.link( (WEBCAM, "outbox"), (BLANKCANVAS, "inbox") )
    WEBCAM_WRAPPER = PygameWrapper(wrap=BLANKCANVAS, position=(3.7,2.7,-9), rotation=(-1,-5,-5)).activate()
    
    #WEBCAMWRAPPER = PygameWrapper(wrap=WEBCAM, position=(0,0,-9), rotation=(0,0,0)).activate()
    #WEBCAM = Webcam().activate()            
    #WEBCAMWRAPPER = PygameWrapper(wrap=WEBCAM, position=(0,0,-9), rotation=(0,0,0)).activate()
    #PAINTER_WRAPPER = PygameWrapper(wrap=PAINTER, position=(4,1,-10), rotation=(-20,15,3)).activate()
    #TICKER = Ticker(size = (150, 150)).activate()
    #TICKER_WRAPPER = PygameWrapper(wrap=TICKER, position=(4, 1,-10), rotation=(-20,15,3)).activate()
    #MAGNADOODLE = MagnaDoodle(size=(200,200)).activate()
    #MAGNADOODLEWRAPPER = PygameWrapper(wrap=MAGNADOODLE, position=(3,-2,-8), rotation=(1,-1,0)).activate()
    i1 = SimpleTranslationInteractor(target=WEBCAM_WRAPPER).activate()
    #READER = ConsoleReader().activate()
    
    #READER.link( (READER,"outbox"), (TICKER, "inbox") )
    
    Axon.Scheduler.scheduler.run.runThreads()  