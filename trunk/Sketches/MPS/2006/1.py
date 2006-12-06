#!/usr/bin/python


import pygame
import time
import Axon
from Kamaelia.UI.GraphicDisplay import PygameDisplay


class Cat(Axon.Component.component):
    Inboxes = {
        "inbox" : "default data inbox",
        "control": "default control data (eg shutdown) inbox",
        "callback" : "The display system sends us a surface here",
    } 
    Outboxes = {
        "outbox" : "default data outbox",
        "signal" : "outbox customarily used for passing on feedback",
        "display_signal" : "outbox we use to talk to the display service",
    }
    def __init__(self):
        super(Cat, self).__init__()
        self.img = pygame.image.load("cat.gif")
        
        self.disprequest = { "DISPLAYREQUEST" : True,
                            "callback" : (self,"callback"),
                            "size": (self.img.get_width(),self.img.get_height())}

    def init_cat(self):
        self.img = self.img.convert()

    def main(self):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self,"display_signal"), displayservice)
        self.send(self.disprequest, "display_signal")
        while not self.dataReady("callback"):
            self.pause()
            yield 1

        self.init_cat() # can only do this after we have a display!
        surface = self.recv("callback")
        surface.blit(self.img, (0,0))
        self.send({"REDRAW":True, "surface":surface}, "display_signal")
        self.send({ "CHANGEDISPLAYGEO" : True,
                    "surface" : surface,
                    "position": (100,100) }, "display_signal")
        yield 1
        while 1:
            for i in xrange(100,800,10):
                self.send({ "CHANGEDISPLAYGEO" : True,
                            "surface" : surface,
                            "position": (i,100) }, "display_signal")
                time.sleep(0.02)
                yield 1

            for i in xrange(100,600,10):
                self.send({ "CHANGEDISPLAYGEO" : True,
                            "surface" : surface,
                            "position": (800,i) }, "display_signal")
                time.sleep(0.02)
                yield 1

            for i in xrange(800,100,-10):
                self.send({ "CHANGEDISPLAYGEO" : True,
                            "surface" : surface,
                            "position": (i,600) }, "display_signal")
                time.sleep(0.02)
                yield 1


            for i in xrange(600,100,-10):
                self.send({ "CHANGEDISPLAYGEO" : True,
                            "surface" : surface,
                            "position": (100,i) }, "display_signal")
                time.sleep(0.02)
                yield 1

PygameDisplay(width=1024,height=768,fullscreen=0).activate()
Cat().run()




