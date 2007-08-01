#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""

"""
from Axon.Component import component, scheduler
import pygame
import time
import random
pygame.init()

class PygameDisplay(component):
   Inboxes=["inbox"]   # List of inbox names if different
   Outboxes=["outbox"] # List of outbox names if different

   def __init__(self,width=840,height=400):
      super(PygameDisplay,self).__init__()
      self.screen = pygame.display.set_mode((width, height))

class FlashingPygameDisplay(PygameDisplay):
   def drawUpdate(self):
      self.screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      return 1

   def mainBody(self):
      self.screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      if self.drawUpdate():
         pygame.display.update()
      return 1

class dispatcherMixin(object):
   def dispatch(self):
      if self.dataReady("inbox"):
          command, args = self.recv("inbox")
          try:
             f = self.commands[command]
          except KeyError, e:
             print "sent unknown command"
          else:
             f(args)

class ProgrammableDisplay(PygameDisplay,dispatcherMixin):
   def __init__(self):
      super(ProgrammableDisplay, self).__init__()
      self.commands = {}

   def addCommand(self, command, callback):
      self.commands[command] = callback

   def main(self):
      while 1:
         #if self.dataReady("inbox"):
         #    command, args = self.recv("inbox")
         self.dispatch()
         yield 1

class BackgroundDisplay(ProgrammableDisplay):
   def __init__(self):
      super(BackgroundDisplay, self).__init__()
      self.addCommand("background",self.background)
      self.ball = Ball()
      self.allsprites = pygame.sprite.RenderPlain((self.ball,))

   def main(self):
      while 1:
         self.dispatch()
         yield 1

   def background(self,args):
      self.screen.fill(args)
      pygame.display.update()

class RandomBackgroundDisplay(ProgrammableDisplay):
   def __init__(self):
      super(RandomBackgroundDisplay, self).__init__()
      self.addCommand("random_background",self.random)

   def random(self,args):
      self.screen.fill( (random.randint(0,255),random.randint(0,255),random.randint(0,255)) )
      pygame.display.update()

class Ball(pygame.sprite.Sprite):
    def load_image(self, fullname, colorkey=None):
       try:
           image = pygame.image.load(fullname)
       except pygame.error, message:
           print 'Cannot load image:', fullname
           raise SystemExit, message
       image = image.convert()
       if colorkey is not None:
           if colorkey is -1:
               colorkey = image.get_at((0,0))
           image.set_colorkey(colorkey, RLEACCEL)
       return image, image.get_rect()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = self.load_image('/usr/share/frozen-bubble/gfx/balls/bubble-5.gif')

    def update(self):
        "move the ball based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

def colour_fader():
   import random
   base = [127,127,127]
   d=[0,0,0]
   while 1:
      yield tuple(base)
      x=random.randint(0,2)
      d[x]=d[x]+(random.randint(0,1)*2)-1
      if d[x] > 10: d[x] = 10
      if d[x] < -10: d[x] = -10
      base[x] +=d[x]
      if base[x] < 0: base[x] = 0
      if base[x] > 255: base[x] = 255

if __name__ =="__main__":
   colour_faderG = colour_fader()
   import time
   class Mixture(RandomBackgroundDisplay,BackgroundDisplay): pass
   PygameTest = BackgroundDisplay
   X=PygameTest()
   B=Ball()
   X.activate()
   t = time.time()
   while 1:
      X._deliver(("background",colour_faderG.next())  ,"inbox")
      X.next()
