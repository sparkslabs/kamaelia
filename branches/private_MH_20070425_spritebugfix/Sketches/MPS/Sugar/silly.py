#!/usr/bin/python
#
# Inspired by Damian Conway's syntax for encoding 
# Flying Spaghetti Monsters in C++
#
# This is valid python code. See the end for how/why/runnable code.
"""
Source(1)*outbox(box="outbox")
Source(1)*outbox(box="outbox") - Sink(1)*inbox(box="inbox")
Source(1)*outbox() ------- inbox("control")*Sink()*outbox("signal") -------- Sink(1)*inbox()
Source(1)---Filter(1)----Sink(1)
"""
#

class component(object):
   def __init__(self, *args, **argd):
      self.__dict__.update(argd)
      self.args = args
   def __neg__(self):
      "pass through the previous expression unchanged"
      return self
   def __sub__(self, other):
      print "SELF, OTHER", self, other
      return self*outbox()-self*inbox()
   def __radd__(self, other):
      print "Self, other", self, other
      return service(other,self)

class service(object):
   def __init__(self, Component, Box):
      self.Component = Component
      self.Box = Box
   def __neg__(self):
      "pass through the previous expression unchanged"
      return self
   def __sub__(self, other):
      return link(self, other)

class link(service):
   def __init__(self, source, sink):
      self.source = source
      self.sink = sink

class box(object):
   def __init__(self, box=None):
      self.box = box
   def __rmul__(self, other):
      print self.box, other
      return service(other,self)
   def __mul__(self, other):
      print self.box, other
      return service(other,self)
   def __neg__(self):
      "pass through the previous expression unchanged"
      return self

class inbox(box):
   def __init__(self, box="inbox"):
      self.box = box

class outbox(box):
   def __init__(self, box="outbox"):
      self.box = box

class Source(component): pass
class Filter(component): pass
class Sink(component): pass

Source(1)*outbox(box="outbox")
Source(1)*outbox(box="outbox") - Sink(1)*inbox(box="inbox")
Source(1)*outbox() ------- inbox("control")*Sink()*outbox("signal") -------- Sink(1)*inbox()
Source(1)---Filter(1)----Sink(1)






