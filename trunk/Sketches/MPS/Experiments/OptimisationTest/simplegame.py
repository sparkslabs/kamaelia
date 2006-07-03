#!/usr/bin/python
#
# Experiment in two things:
#    * Linkage based performance increase. (In-place delivery rather than copying)
#    * How to convert a trivial pygame game to the component framework.
#
# Results:
#    * Relative to the hand crafted pygame version we've taken a 5% hit on
#      the framerate. However the code is significantly more re-usable, so
#      overall I'd view it as a gain.
#    * This also shows that this approach isn't necessarily a bad way to do
#      things from a performance perspective.
#
#    * One of things you *lose* is the understanding of the system
#      structure. One major loss as a result of this for example is the
#      ability for a delivery into any box to trigger an unpause event.
#      We really need this, so we need to re-create this effect by mapping
#      the geometry again. (Interestingly!)
#

import pygame
from pygame.locals import *
import pygame.mixer
import random
import os
pygame.init()
import time

banner_location = "banner.gif"
cat_location    = "cat.gif"
cat_pop_wav_file     = "hold.wav"
cat_appear_wav_file  = "KDE_Beep_Bottles.wav"

cat_pop_wav = pygame.mixer.Sound(cat_pop_wav_file)
cat_appear_wav = pygame.mixer.Sound(cat_appear_wav_file)

screensize      = (800,600)
back_colour     = (255,255,255)
border          = 40

#################################
#
# Microaxon.py, with optimised linkages
#
#################################

class microprocess(object):
   def __init__(self): pass
   def main(self):
      yield -1

class newComponent(object):
   def __init__(self, *components):
      self.components = components

class scheduler(microprocess):
   def __init__(self):
      self.active = []
   def main(self):
      t = time.time()
      while len(self.active)>0:
            newqueue = []
            for current in self.active:
               if not current.paused:
                  try:
                     result = current.runhook.next()
                     if result != -1:   
                        newqueue.append(current)
                        if isinstance(result, newComponent):
                           self.activateMicroprocess(result.components)
                  except StopIteration:
                     pass # Component exited normally
               else:
                  newqueue.append(current)
            self.active = newqueue
            yield 1
   def activateMicroprocess(self,someprocesses):
      for someprocess in someprocesses:
         x = someprocess.main()
         someprocess.runhook = x
         self.active.append(someprocess)

class component(microprocess):
   def __init__(self,**argd):
      self.boxes = { "inbox": [],  "outbox": [], "signal":[], "control":[]  }
      try:
         for box in self.__class__.Boxes:
            self.boxes[box] =  []
      except AttributeError:
         pass
      self.paused = 0
   def __repr__(self):
      return "COMPONENT: %s, %s" % (str(self.__class__), str(self.boxes))
   def send(self, boxname, value):
      "Appends the message to the named inbox"
      self.boxes[boxname].append(value)
      try:
         for reciever in reciever_mapping[str(id(self.boxes[boxname]))]:
            reciever.unpause()
      except KeyError:
         pass
   def recv(self,boxname):
      "Removes the first message in the named inbox"
      result = self.boxes[boxname][0]
      del self.boxes[boxname][0]
      return result
   def dataReady(self, boxname):
      "See if there's any messages returns True if there are any messages on the named inbox"
      return len(self.boxes[boxname])
   def receiveIfReady(self,boxname):
      "Return a piece of data if some is ready. Note that this returns 'None' in the absence of data"
      if self.dataReady(boxname):
         return self.recv(boxname)
      return None
   def pause(self):
      self.paused = 1
   def unpause(self):
      self.paused = 0

class send_one_component(component):
   def send(self, boxname, value):
      if len(self.boxes[boxname]) == 0:
        super(send_one_component,self).send(boxname, value)

reciever_mapping = {}

def linkage(source,sink):
   try:
      source_component, source_box = source
   except TypeError:
      source_component = source
      source_box  = "outbox"
   try:
      sink_component, sink_box = sink
   except TypeError:
      sink_component = sink
      sink_box  = "inbox"  
   sink_component.boxes[sink_box] = source_component.boxes[source_box]
   theBox = str(id(source_component.boxes[source_box]))
   try:
      reciever_mapping[theBox].append(sink_component)
   except KeyError:
      reciever_mapping[theBox] = [ sink_component ]


##################################################
#
# Collection of generators representing various behaviours available when
# measured.
#
#
class bouncingFloat(send_one_component):
   def __init__(self,scale_speed):
      super(bouncingFloat, self).__init__()
      self.scale_speed = scale_speed
   def main(self):
      scale = 1.0
      direction = 1
      while 1:
         scale = scale + (0.1 * self.scale_speed * direction)
         if scale >1.0:
            scale = 1.05
            direction = direction * -1
         if scale <0.1:
            scale = 0.05
            direction = direction * -1
         self.send("outbox", scale)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
            if data == "togglepause":
               self.pause()
            if data == "unpause":
               self.unpause()
         yield 1

class cartesianPingPong(send_one_component):
   def __init__(self,point, width,height,border):
      super(cartesianPingPong, self).__init__()
      self.point = point
      self.width = width
      self.height = height
      self.border = border
   def main(self):
      delta_y = 10
      delta_x = 10
      while 1 :
         self.point[0] = self.point[0]+delta_x
         self.point[1] = self.point[1]+delta_y
         if self.point[0] > self.width-self.border: delta_x = -10
         if self.point[0] < self.border: delta_x = 10
         if self.point[1] > self.height-self.border: delta_y = -10
         if self.point[1] < self.border: delta_y = 10
         self.send("outbox", self.point)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
            if data == "togglepause":
               self.pause()
            if data == "unpause":
               self.unpause()
         yield 1

class loopingCounter(send_one_component):
   def __init__(self,increment,modulo=360):
      super(loopingCounter, self).__init__()
      self.increment = increment
      self.modulo = modulo
   def main(self):
      total = 0
      while 1:
         total = (total + self.increment) % self.modulo
         self.send("outbox", total)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
            if data == "togglepause":
               self.pause()
         yield 1

class continuousIdentity(send_one_component):
   def __init__(self, original,*args):
      super(continuousIdentity, self).__init__()
      self.original = original
   def main(self):
      while 1:
         self.send("outbox",self.original)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
#            if data == "togglepause":
#               self.pause()
            if data == "unpause":
               self.unpause()
         yield 1

class continuousZero(send_one_component):
   def __init__(self, *args):
      super(continuousZero, self).__init__()
   def main(self):
      while 1:
         self.send("outbox", 0)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
            if data == "unpause":
               self.unpause()
         yield 1

class continuousOne(send_one_component):
   def __init__(self, *args):
      super(continuousOne, self).__init__()
   def main(self):
      while 1:
         self.send("outbox", 1)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
            if data == "unpause":
               self.unpause()
         yield 1

class fanout(component):
   Boxes = []
   def __init__(self, boxnames):
      self.__class__.Boxes = boxnames
      super(fanout, self).__init__()
   def main(self):
      while 1:
         if self.dataReady("inbox"):
            data = self.recv("inbox")
            for boxname in self.__class__.Boxes:
               self.send(boxname, data)
         if self.dataReady("control"):
            data = self.recv("control")
            if data == "shutdown":
               self.send("signal", "shutdown")
               return
         yield 1


def makeAndInitialiseBackground(banner_location, screensize, screen_surface,back_colour):
   #
   # Load images for background
   #
   banner_surface = pygame.image.load(banner_location)
   banner = banner_surface.convert()
   surface = banner_surface
   width = banner_surface.get_width()
   height = banner_surface.get_height()

   #
   # Calculate position for image, relative to screen size.
   # This is calculated as a rectangle
   #
   horizonal_to_move = (screensize[0] - width)/2
   vertical_to_move = (screensize[1] - height)/2
   rect = banner_surface.get_rect()
   rect = rect.move([horizonal_to_move,vertical_to_move])

   #
   # Create the actual background, and then insert the image(s) into the
   # background.
   #
   background = pygame.Surface(screen_surface.get_size())
   background = background.convert()
   background.fill(back_colour)
   background.blit(banner_surface, rect)

   #
   # Finally, return the completed background.
   #
   return background

def randomFromRangeExcludingZero(min,max):
   result = 0
   while result == 0:
      result = random.randint(min,max)
   return result

def make_cat(cat_location, screensize, border ):
      # Get the cat again!
      files = [ x for x in os.listdir("pictures") if x not in ("README","CVS",".svn") ]
      image_location = files[random.randint(0,len(files)-1)]
      print "XXX", image_location
      cat_surface = pygame.image.load("pictures/"+image_location)
#      cat_surface = pygame.image.load(cat_location)
      cat = cat_surface.convert()
#      colorkey = cat.get_at((0,0))
      cat.set_colorkey((255,255,255), RLEACCEL)
      
      rotation_speed = randomFromRangeExcludingZero(-2,2)  
      scale_speed = float(randomFromRangeExcludingZero(-1,1))
#      rotation_speed = randomFromRangeExcludingZero(-12,12)
#      scale_speed = float(randomFromRangeExcludingZero(-3,3))
      position = [random.randint(border,screensize[0]-border),random.randint(border,screensize[1]-border)]
      
      rotator = loopingCounter(rotation_speed)
      translation = cartesianPingPong(position,screensize[0],screensize[1],border)
      scaler = bouncingFloat(scale_speed)  
      imaging = continuousIdentity(cat)
      shutdown_fanout = fanout(["rotator","translation","scaler", "imaging","self_shutdown"])
      
      newCat = BasicSprite(image=cat)

      linkage(rotator, (newCat, "rotator"))
      linkage(translation, (newCat, "translation"))
      linkage(scaler, (newCat, "scaler"))
      linkage(imaging, (newCat, "imaging"))

      linkage((newCat, "signal"), (shutdown_fanout, "inbox"))
      linkage((shutdown_fanout, "rotator"), (rotator, "control"))
      linkage((shutdown_fanout, "translation"), (translation, "control"))
      linkage((shutdown_fanout, "scaler"), (scaler, "control"))
      linkage((shutdown_fanout, "imaging"), (imaging, "control"))
      linkage((shutdown_fanout, "self_shutdown"), (shutdown_fanout, "control"))

      return newCat,(rotator, translation, scaler, imaging,shutdown_fanout)

def make_cats(cat_location, screensize, border, numberCats=20):
   cat_sprites = []
   for i in range(numberCats):
      # Need to load the image separately for each sprite...
      newCat = make_cat(cat_location, screensize, border)
      cat_sprites.append(newCat)
   return cat_sprites

##############################################
#
# Basic Pygame wrapper classes
#
class EventHandler(object):
   def __init__(self, trace=1):
      self.trace = trace
   def dispatch(self, event, where):
      if event.type == QUIT: self.quit(where)
      if event.type == ACTIVEEVENT: self.active(event.gain, event.state, where)
      if event.type == KEYDOWN: self.keydown(event.unicode, event.key, event.mod, where)
      if event.type == KEYUP: self.keyup(event.key, event.mod, where)
      if event.type == MOUSEMOTION: self.mousemotion(event.pos, event.rel, event.buttons, where)
      if event.type == MOUSEBUTTONUP: self.mousebuttonup(event.pos, event.button, where)
      if event.type == MOUSEBUTTONDOWN: self.mousebuttondown(event.pos, event.button, where)
      if event.type == JOYAXISMOTION: self.joyaxismotion(event.joy, event.axis, event.value, where)
      if event.type == JOYBALLMOTION: self.joyballmotion(event.joy, event.ball, event.rel, where)
      if event.type == JOYHATMOTION: self.joyhatmotion(event.joy, event.hat, event.value, where)
      if event.type == JOYBUTTONUP: self.joybuttonup(event.joy, event.button, where)
      if event.type == JOYBUTTONDOWN: self.joybuttondown(event.joy, event.button, where)
      if event.type == VIDEORESIZE: self.videoresize(event.size, where)
      if event.type == VIDEOEXPOSE: self.videoexpose(where)
      if event.type == USEREVENT: self.userevent(event.code,where)

   def quit(self, where): 
      if self.trace:
         print "QUIT: (", ")"

   def active(self, gain, state ,where): 
      if self.trace:
         print "ACTIVE: (", gain, state, ")"

   def keydown(self, unicode, key, mod, where):
      if self.trace:
         print "KEYDOWN: (", repr(unicode), key, mod, ")"

   def keyup(self, key, mod, where):
      if self.trace:
         print "KEYUP: (", key, mod, ")"

   def mousemotion(self, pos, rel, buttons, where):
      if self.trace:
         print "MOUSEMOTION: (", pos, rel, buttons, ")"

   def mousebuttonup(self, pos, button, where):
      if self.trace:
         print "MOUSEBUTTONUP: (", pos, button, ")"

   def mousebuttondown(self, pos, button, where):
      if self.trace:
         print "MOUSEBUTTONDOWN: (", pos, button, ")"

   def joyaxismotion(self, joy, axis, value, where):
      if self.trace:
         print "JOYAXISMOTION: (", joy, axis, value, ")"

   def joyballmotion(self, joy, ball, rel, where):
      if self.trace:
         print "JOYBALLMOTION: (", joy, ball, rel, ")"

   def joyhatmotion(self, joy, hat, value, where):
      if self.trace:
         print "JOYHATMOTION: (", joy, hat, value, ")"

   def joybuttonup(self, joy, button, where):
      if self.trace:
         print "JOYBUTTONUP: (", joy, button, ")"

   def joybuttondown(self, joy, button, where):
      if self.trace:
         print "JOYBUTTONDOWN: (", joy, button, ")"

   def videoresize(self, size, where):
      if self.trace:
         print "VIDEORESIZE: (", size, ")"

   def videoexpose(self, where):
      if self.trace:
         print "VIDEOEXPOSE: (", ")"

   def userevent(self, code, where): 
      if self.trace:
         print "USEREVENT: (", code, ")"

class MyGamesEvents(EventHandler):
   def __init__(self, cat_args, trace=1, ):
      self.trace = 0
      self.cat_args = cat_args
   def mousebuttondown(self, pos, button, where):
      if button == 1:
         channel = cat_appear_wav.play()
         newCat = make_cat(*self.cat_args)
         cat_sprite, rest = newCat
         where.allsprites.add(cat_sprite)
         where.send("inbox", rest)
      if button == 2:
         sprites = where.allsprites.sprites()
         for sprite in sprites:
            if sprite.rect.collidepoint(*pos):
               sprite.togglePause()
               print "Hit a sprite!"  
      if button == 3:
         # Make a sprite disappear
         channel = cat_pop_wav.play()
         sprites = where.allsprites.sprites()
         popped = 0
         for sprite in sprites:
            if sprite.rect.collidepoint(*pos):
               spriteToZap = sprite
               spriteToZap.shutdown()
               where.allsprites.remove(spriteToZap)
               return
         try:
            spriteToZap = sprites[len(sprites)-1]
         except IndexError:
            pass
         else:
            spriteToZap.shutdown()
            where.allsprites.remove(spriteToZap)
   def keydown(self, unicode, key, mod, where):
      print "KEY", key
      if key == 112: # "P"
         print "PAUSE ALL MOVEMENT"
         for sprite in where.allsprites.sprites():
            sprite.pause()
      if key == 113: # "Q"
         raise "QUIT"
      if key == 117: # "U"
         print "UNPAUSE ALL MOVEMENT"
         for sprite in where.allsprites.sprites():
            sprite.unpause()
      if key == 116: # "T"
         print "Toggle PAUSE ALL MOVEMENT"
         for sprite in where.allsprites.sprites():
            sprite.togglePause()


class BasicSprite(pygame.sprite.Sprite, component):
   Boxes=["rotator","translation","scaler", "imaging"]
   def __init__(self, **argd):
      pygame.sprite.Sprite.__init__(self)
      component.__init__(self)

      self.image = argd["image"]
      self.original = self.image
      self.rect = self.image.get_rect()
      self.size = (self.rect.right-self.rect.left, self.rect.bottom-self.rect.top)
      self.area = pygame.display.get_surface().get_rect()
      self.rect.topleft = argd.get("position",(10,10))
      self.paused = False
      self.update = self.logic().next

   def logic(self):
      center = list(self.rect.center)
      self.image = self.original
      current = self.image
      scale = 1.0
      angle = 1
      pos = center
      while 1:
         if not self.paused:
            self.image = current
            if self.dataReady("imaging"):
               self.image = self.recv("imaging")
               current = self.image

            if self.dataReady("scaler"):
               # Scaling
               scale = self.recv("scaler")
            w,h = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (w*scale, h*scale))

            if self.dataReady("rotator"):
               angle = self.recv("rotator")
               # Rotation
            self.image = pygame.transform.rotate(self.image, angle)

            if self.dataReady("translation"):
               # Translation
               pos = self.recv("translation")
            self.rect = self.image.get_rect()
            self.rect.center = pos

         yield 1
   def shutdown(self):
      self.send("signal", "shutdown")
   def togglePause(self):
      if self.paused:
         self.unpause()
      else:
         self.pause()

   def unpause(self):
      self.paused = False
      self.send("signal", "unpause")
   def pause(self):    
      self.paused = True
      self.send("signal", "togglepause")

class SimpleGame(component):
   def __init__(self, cat_args, cat_sprites, background, screen_surface, eventHandler=EventHandler):
      super(SimpleGame,self).__init__()
      self.allsprites = []
      self.cat_args = cat_args
      self.cat_sprites = cat_sprites
      self.background = background
      self.screen_surface = screen_surface

   def main(self):
      event_handler = MyGamesEvents(self.cat_args)
      cat_sprites = []
      for cat_sprite,components in self.cat_sprites:
         cat_sprites.append(cat_sprite)
         yield newComponent(*components)
      self.allsprites = pygame.sprite.RenderPlain(cat_sprites)
      measureFramerate = 1
      if measureFramerate:
         t = time.time()
         ts = t
         f = 0
         fa = f
      while 1:
         for event in pygame.event.get():
            event_handler.dispatch(event,self)
         #
         # Essentially a specialised scheduler:
         #
         self.allsprites.update()
         self.screen_surface.blit(background, (0, 0))
         self.allsprites.draw(self.screen_surface)
         f += 1
         pygame.display.flip()
         if measureFramerate:
            if time.time() - t >2:
               tnow = time.time()
               tdiff = tnow - t
               fa = fa + f
               print "FRAMERATE:", float(f)/tdiff, float(fa)/(tnow-ts)
               f = 0
               t = time.time()
         if self.dataReady("inbox"):
            components = self.recv("inbox")
            yield newComponent(*components)
         yield 1

screen_surface = pygame.display.set_mode(screensize)#, DOUBLEBUF|FULLSCREEN)
background = makeAndInitialiseBackground(banner_location, screensize, screen_surface,back_colour)
cat_sprites = make_cats(cat_location, screensize, border,1)
cat_args = (cat_location, screensize, border)
game = SimpleGame(cat_args, cat_sprites, background, screen_surface)

myscheduler = scheduler()

myscheduler.activateMicroprocess((game,))
for i in myscheduler.main():
   pass
