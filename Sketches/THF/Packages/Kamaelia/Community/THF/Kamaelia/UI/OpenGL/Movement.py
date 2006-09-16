#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===============================================
A collection of movement components and classes
===============================================

Contained components:

- PathMover
- WheelMover
- SimpleRotator
- SimpleBuzzer

Contained classes:

- LinearPath

For a description of these classes have a look at their class
documentation.

Example Usage
-------------
The following example show the usage of most of the components in this
file (for an example how to use the WheelMover, see the TorrentOpenGLGUI
example)::

    points = [(3,3,-20),
              (4,0,-20),
              (3,-3,-20),
              (0,-4,-20),
              (-3,-3,-20),
              (-4,0,-20),
              (-3,3,-20),
              (0,4,-20),
              (3,3,-20),
             ]
    path = LinearPath(points, 1000)

    cube1 = SimpleCube(size=(1,1,1)).activate()
    pathmover = PathMover(path).activate()
    pathmover.link((pathmover,"outbox"), (cube1,"position"))

    cube2 = SimpleCube(size=(1,1,1)).activate()
    simplemover = SimpleMover().activate()
    simplemover.link((simplemover,"outbox"), (cube2,"position"))

    cube3 = SimpleCube(size=(1,1,1), position=(-1,0,-15)).activate()
    rotator = SimpleRotator().activate()
    rotator.link((rotator,"outbox"), (cube3,"rel_rotation"))

    cube4 = SimpleCube(size=(1,1,1), position=(1,0,-15)).activate()
    buzzer = SimpleBuzzer().activate()
    buzzer.link((buzzer,"outbox"), (cube4,"scaling"))

    Axon.Scheduler.scheduler.run.runThreads()  

"""

import Axon
from Vector import Vector
from math import *


class LinearPath:
    """\
    LinearPath(...) -> A new LinearPath object.
    
    LinearPath generates a linearly interpolated Path which can be used
    by the Pathmover component to control component movement.
    
    It provides basic list functionality by providing a __getitem__() as
    well as a __len__() method for accessing the path elements.
    
    Keyword arguments:
    
    - points    -- a list of points in the path
    - steps     -- number of steps to generate between the path endpoints (default=1000)
    """
    def __init__(self, points = [], steps = 1000):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        if steps == 0:
            steps = len(points)
        
        if steps == len(points):
            self.points = [Vector(*p) for p in points]
        else:
            totallen = 0.0
            p1 = Vector(*points[0])
            for p2 in points[1:]:
                p2 = Vector(*p2)
                totallen += (p2-p1).length()
                p1=p2
#            print "totallen", totallen
            steplen = totallen/float(steps)
#            print steplen
            prelen = 0.0
            postlen = 0.0
            proclen = 0.0
            addedpoints = 0
            
            p1 = Vector(*points[0])
            self.points = []
            for p2 in points[1:]:
                p2 = Vector(*p2)
                v = p2-p1
                vlen = v.length()
                postlen += vlen
#                print proclen
                while proclen <= postlen and addedpoints < steps:
                    self.points.append(p1+v*((proclen-prelen)/vlen))
                    proclen += steplen
                    addedpoints += 1
                prelen += vlen
                p1 = p2
            self.points.append(p2)
#        for v in self.points:print str(v)
#        print
            
    def __getitem__(self, key):
        return self.points[key].toTuple()
        
    def __len__(self):
        return len(self.points)


class PathMover(Axon.Component.component):
    """\
    PathMover(...) -> A new PathMover object.

    PathMover can be used to move a 3d object along a path.
    
    It can be controlled by sending commands to its inbox. These
    commands can be one of "Play", "Stop", "Next", "Previous", "Rewind", 
    "Forward" and "Backward".
    
    If the pathmover reaches the beginning or the end of a path it
    generates a status message which is sent to the "status" outbox. This
    message can be "Finish" or "Start".
    
    Keyword arguments:
    
    - path   -- A path object (e.g. LinearPath) or a list of points
    - repeat -- Boolean indication if the Pathmover should repeat the path if it reaches an end (default=True)
    """
    
    Inboxes = {
       "inbox": "Commands are received here",
       "control": "ignored",
    }
    
    Outboxes = {
        "outbox" : "Outbox for sending Control3D commands",
        "status": "Used to send status messages",
    }
    def __init__(self, path, repeat=True):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PathMover, self).__init__()
        self.path = path
        self.repeat = repeat
        
        self.running = True
        self.currentIndex = 0
        self.lastIndex = 0
        self.flipped = False
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    return

            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                if msg == "Play":
                    self.running = True
                if msg == "Stop":
                    self.running = False
                if msg == "Next":
                    self.currentIndex += 1
                if msg == "Previous":
                    self.currentIndex -= 1
                if msg == "Rewind":
                    if not self.flipped:
                        self.currentIndex = 0
                    else:
                        self.currentIndex = len(self.path)-1
                if msg == "Forward":
                    self.flipped = False
                if msg == "Backward":
                    self.flipped = True
            
            if self.running:
                if not self.flipped:
                    self.currentIndex += 1
                else:
                    self.currentIndex -= 1
                
            if self.currentIndex >= len(self.path):
                self.send("Finish", "status")
                if self.repeat:
                    self.currentIndex = 0
                else:
                    self.currentIndex -=1
                    self.running = False
            elif self.currentIndex < 0:
                self.send("Start", "status")
                if self.repeat:
                    self.currentIndex = len(self.path)-1
                else:
                    self.currentIndex = 0
                    self.running = False
                
            if self.currentIndex != self.lastIndex:
                self.send( self.path[self.currentIndex], "outbox")
                self.lastIndex = self.currentIndex



class WheelMover(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    """\
    WheelMover(...) -> A new WheelMover component.
    
    A component to arrange several OpenGlComponents in the style of a
    big wheel rotating around the X axis. Can be used to switch between
    components.
    
    Components can be added and removed during operation using the
    "notify" inbox. Messages sent to it are expected to be a dictionary of
    the following form::
    
        {
            "APPEND_CONTROL" :True,
            "objectid": id(object),
            "control": (object,"position")
        }

    for adding components and::

        {
            "REMOVE_CONTROL" :True,
            "objectid": id(object),
        }
    
    for removing components.
    
    If components are added when the wheel is already full (number of
    slots exhausted) they are simply ignored.

    The whole wheel can be controlles by sending messages to the
    "switch" inbox. The commands can be either "NEXT" or "PREVIOUS".

    Keyword arguments:
    
    - steps     -- number of steps the wheel is subdivided in (default=400)
    - center    -- center of the wheel (default=(0,0,-13))
    - radius    -- radius of the wheel (default=5)
    - slots     -- number of components which can be handled (default=20)
    """
    
    Inboxes = {
       "inbox": "not used",
       "control": "ignored",
       "notify": "For appending and removing components",
       "switch": "For reception of switching commands",
    }
    
    Outboxes = {
        "outbox" : "Outbox for sending position updates",
    }
    
    def __init__(self, steps=400, center=(0,0,-13), radius=5, slots=20):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(WheelMover, self).__init__()
    
        self.slots = slots
        self.distance = steps/slots
        
        stepangle = 2*pi/steps
    
        self.points = []
        for i in range(steps):
            angle = i*stepangle
            x = cos(angle)*float(radius)
            y = sin(angle)*float(radius)
            
            self.points.append((Vector(0,y,x)+Vector(*center)).toTuple())
            
    def main(self):
        self.objects = []
        self.comms = {}        
        self.current_positions = {}
        self.target_positions = {}

        self.currentobject = 0
        
        self.nextpos = 0
        
        while 1:
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    return

            while self.dataReady("notify"):
                msg = self.recv("notify")
                if msg.get("APPEND_CONTROL", None) and len(self.objects) < self.slots:
                    objectid = msg.get("objectid")
                    service = msg.get("control")
                    
                    self.objects.append(objectid)
                    comms = self.addOutbox("control")
                    self.comms[objectid] = comms
                    self.link( (self, comms), service)
                    
                    self.current_positions[objectid] = self.nextpos
                    self.target_positions[objectid] = self.nextpos
                    self.send(self.points[ self.current_positions[objectid] ], self.comms[objectid])
                    
                    self.nextpos += self.distance
                    
                elif msg.get("REMOVE_CONTROL", None):
                    objectid = msg.get("objectid")
                    
                    self.objects.remove(objectid)
                    self.unlink(self,self.comms[objectid])
                    self.comms.popitem(objectid)
                    self.current_position.popitem(objectid)
                    deleted_pos = self.target_position.popitem(objectid)
                    
                    for o in self.objects:
                        if self.target_position[o] > deleted_pos:
                            self.target_position[0] -= self.distance
                
            while self.dataReady("switch"):
                msg = self.recv("switch")
                if msg == "NEXT" and self.currentobject < 0:
                    for objectid in self.objects:
                        self.target_positions[objectid] += self.distance
                    self.currentobject += 1
                    self.nextpos += self.distance
                    
                if msg == "PREVIOUS" and self.currentobject > -len(self.objects)+1:
                    for objectid in self.objects:
                        self.target_positions[objectid] -= self.distance
                    self.currentobject -= 1
                    self.nextpos -= self.distance

            for objectid in self.objects:
                if self.current_positions[objectid]>self.target_positions[objectid]:
                    self.current_positions[objectid]-= 1
                    self.send(self.points[ self.current_positions[objectid] ], self.comms[objectid])
                elif self.current_positions[objectid]<self.target_positions[objectid]:
                    self.current_positions[objectid]+= 1
                    self.send(self.points[ self.current_positions[objectid] ], self.comms[objectid])
                    
            yield 1


class SimpleRotator(Axon.Component.component):
    """\
    SimpleRotator(...) -> A new SimpleRotator component.
    
    A simple rotator component mostly for testing. Rotates
    OpenGLComponents by the amount specified if connected to their
    "rel_rotation" boxes.
    
    Keyword arguments:
    
    - amount    -- amount of relative rotation sent (default=(0.1,0.1,0.1))
    """    
    def __init__(self, amount=(0.1,0.1,0.1)):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleRotator, self).__init__()
        self.amount = amount
        
    def main(self):

        while 1:
            yield 1
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    return
                    
            self.send(self.amount, "outbox")


class SimpleMover(Axon.Component.component):
    """\
    SimpleMover(...) -> A new SimpleMover component.

    A simple mover component mostly for testing. Moves OpenGLComponents
    between the specified borders if connected to their "position" boxes.
    The amount of movement every frame and the origin can also be specified.
    
    Keyword arguments:
    
    - amount    -- amount of movement every frame sent (default=(0.03,0.03,0.03))
    - borders   -- borders of every dimension (default=(5,5,5))
    - origin    -- origin of movement (default=(0,0,-20))
    """
    def __init__(self, amount=(0.03,0.03,0.03), borders=(5,5,5), origin=(0.0,0.0,-20.0)):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleMover, self).__init__()
        self.borders = borders
        self.amount = amount
        self.origin = origin

    def main(self):
        (x,y,z) = self.origin
        (dx,dy,dz) = self.amount
        while 1:
            yield 1
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    return

            self.send( (x, y, z), "outbox")
            x += dx
            y += dy
            z += dz
            if abs(x)> self.borders[0]: dx = -dx
            if abs(y)> self.borders[1]: dy = -dy
            if (abs(z-self.origin[2]))> self.borders[2]: dz = -dz


class SimpleBuzzer(Axon.Component.component):
    """\
    SimpleBuzzer(...) -> A new SimpleBuzzer component.

    A simple buzzer component mostly for testing. Changes the scaling of
    OpenGLComponents it connected to their "scaling" boxes.
    """
    def main(self):
        r = 1.00
        f = 0.01
        while 1:
            yield 1
            while self.dataReady("control"):
                cmsg = self.recv("control")
                if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
                    self.send(cmsg, "signal")
                    return

            if  r>1.0: f -= 0.001
            else: f += 0.001
            r += f
            
            self.send( (r, r, r), "outbox")


__kamaelia_components__ = (PathMover, WheelMover, SimpleRotator, SimpleBuzzer, )
    
        
if __name__=='__main__':
    from SimpleCube import SimpleCube

    points = [(3,3,-20),
              (4,0,-20),
              (3,-3,-20),
              (0,-4,-20),
              (-3,-3,-20),
              (-4,0,-20),
              (-3,3,-20),
              (0,4,-20),
              (3,3,-20),
             ]
    path = LinearPath(points, 1000)

    cube1 = SimpleCube(size=(1,1,1)).activate()
    pathmover = PathMover(path).activate()
    pathmover.link((pathmover,"outbox"), (cube1,"position"))
    
    cube2 = SimpleCube(size=(1,1,1)).activate()
    simplemover = SimpleMover(borders=(3,5,7)).activate()
    simplemover.link((simplemover,"outbox"), (cube2,"position"))

    cube3 = SimpleCube(size=(1,1,1), position=(-1,0,-15)).activate()
    rotator = SimpleRotator().activate()
    rotator.link((rotator,"outbox"), (cube3,"rel_rotation"))
    
    cube4 = SimpleCube(size=(1,1,1), position=(1,0,-15)).activate()
    buzzer = SimpleBuzzer().activate()
    buzzer.link((buzzer,"outbox"), (cube4,"scaling"))

    Axon.Scheduler.scheduler.run.runThreads()  
# Licensed to the BBC under a Contributor Agreement: THF
