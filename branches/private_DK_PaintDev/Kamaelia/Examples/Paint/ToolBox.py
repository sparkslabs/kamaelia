#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
=============
Paint ToolBox.
=============

This is the "Tool box" window for Kamaelia: Paint, it brings together
all the widgets used by the paint app and places them on a surface.
Much like the one in Gimp or Photoshop (but less complex and more fun :))

"""
import pygame
import Axon
import os
from Axon.Ipc import producerFinished, WaitComplete
from Kamaelia.UI.Pygame.Display import PygameDisplay
from Kamaelia.UI.Pygame.Button import ImageButton
from ColourSelector import ColourSelector
from Slider import Slider

class ToolBox(Axon.Component.component):
    Inboxes = {"inbox"    : "Receive events from Pygame Display",
               "control"  : "For shutdown messages",
               "callback" : "Receive callbacks from Pygame Display",
               "buttons" : "Recieve interrupts from the buttons"
              }
              
    Outboxes = {"outbox" : "XY positions emitted here",
                "signal" : "For shutdown messages",
                "display_signal" : "Outbox used for communicating to the display surface"
               }
    def __init__(self, position=None, size=(500,500)):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(ToolBox,self).__init__()
        self.size = size
        self.dispRequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": self.size,
                           "transparency" : None }
        if not position is None:
            self.dispRequest["position"] = position
            
    def waitBox(self,boxname):
        """Generator. yields 1 until data ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname): return
            else: yield 1
    
    def main(self):
        """Main loop."""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send( self.dispRequest,
                    "display_signal")
        for _ in self.waitBox("callback"): yield 1
        self.display = self.recv("callback")
        
        # tool buttons
        circleb = ImageButton(caption=(os.path.join('icons', 'EllipseToolIcon.png')),position=(10,10), bgcolour = (235,235,235), msg = (("Tool", "Circle"),)).activate()
        eraseb = ImageButton(caption=(os.path.join('icons', 'EraserToolIcon.png')),position=(100,10), bgcolour = (235,235,235), msg = (("Tool", "Eraser"),)).activate()
        lineb = ImageButton(caption=(os.path.join('icons', 'PaintBrushToolIcon.png')),position=(10,50), bgcolour = (235,235,235), msg = (("Tool", "Line"),)).activate()
        bucketb = ImageButton(caption=(os.path.join('icons', 'PaintBucketIcon.png')),position=(10,90), bgcolour = (235,235,235), msg = (("Tool", "Bucket"),)).activate()
        eyeb = ImageButton(caption=(os.path.join('icons', 'ColorPickerToolIcon.png')),position=(10,130), bgcolour = (235,235,235), msg = (("Tool", "Eyedropper"),)).activate()
        addlayerb = ImageButton(caption=(os.path.join('icons', 'PlusButtonIcon.png')),position=(10,540), bgcolour = (235,235,235), msg = (("Layer", "Add"),)).activate()
        prevlayerb = ImageButton(caption=(os.path.join('icons', 'MenuLayersMoveLayerDownIcon.png')),position=(80,540), bgcolour = (235,235,235), msg = (("Layer", "Prev"),)).activate()
        nextlayerb = ImageButton(caption=(os.path.join('icons', 'MenuLayersMoveLayerUpIcon.png')),position=(110,540), bgcolour = (235,235,235), msg = (("Layer", "Next"),)).activate()
        dellayerb = ImageButton(caption=(os.path.join('icons', 'MinusButtonIcon.png')),position=(35,540), bgcolour = (235,235,235), msg = (("Layer", "Delete"),)).activate()
        saveb = ImageButton(caption=(os.path.join('icons', 'MenuFileSaveIcon.png')),position=(100,130), bgcolour = (235,235,235), msg = (("Save", "Test"),)).activate()
        self.link( (circleb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (eraseb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (lineb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (bucketb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (eyeb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (addlayerb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (prevlayerb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (nextlayerb,"outbox"), (self,"outbox"), passthrough = 2 )
        self.link( (dellayerb,"outbox"), (self,"outbox"), passthrough = 2 )
        colSel = ColourSelector(position = (10,170), size = (255,255)).activate()
        self.link( (colSel,"outbox"), (self,"outbox"), passthrough = 2 )
        SizeSlider = Slider(size=(255, 50), messagePrefix = "Size", position = (10, 460), default = 9).activate()
        self.link( (SizeSlider,"outbox"), (self,"outbox"), passthrough = 2 )
        AlphaSlider = Slider(size=(255, 10), messagePrefix = "Alpha", position = (10, 515), default = 255).activate()
        self.link( (AlphaSlider,"outbox"), (self,"outbox"), passthrough = 2 )

        
        
        self.drawBG()
        done = False
        while not done:
            if not self.anyReady():
                self.pause()
            yield 1

    def drawBG(self):
        self.display.fill( (255,255,255) )

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer
    Pipeline(ToolBox(size = (275,600)), ConsoleEchoer()).run()
    
   # ToolBox(size = (275,600)).activate()
    Axon.Scheduler.scheduler.run.runThreads()
        
        
        

