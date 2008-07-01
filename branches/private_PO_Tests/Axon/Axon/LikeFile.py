#!/usr/bin/python


print "****************************************************************"
print "****************************************************************"
print "***                                                          ***"
print "*** LIKE FILE WAS >REMOVED< FROM TRUNK AND IS NOT TO BE USED ***"
print "***  THE REPLACEMENT 'Handle' IS TO BE USED IN ITS PLACE     ***"
print "***                                                          ***"
print "****************************************************************"
print "****************************************************************"


import gc
import time

class KamTest(object):
    def __init__(self):
        self.foo = "Bar"
    def send(self):
        print "hello"
X = [ KamTest() for x in range(1000) ]

class Z(object):
    def bar(self):
        pass
 
def crash(arg): raise arg

try:
    from ctypes import *
    print c_char_p(42)
except:
   pass
try:
    for I in gc.get_objects():
        try:
           if I.__class__ == dict:
               for key in I.keys():
                   I[key] = None
           if I.__class__ == list:
               for i in range(len(I)):
                   I[i] = None
           if "kam" in str(I.__class__).lower():
               for i in dir(I):
                   x = getattr(I,i)
                   if x.__class__ == Z().bar.__class__:
                       setattr(I, i, lambda *x,**argd: crash("CRASH AND BURN"))
        except AttributeError:
            pass
except:
    pass

   

raise "CRASH AND BURN"


