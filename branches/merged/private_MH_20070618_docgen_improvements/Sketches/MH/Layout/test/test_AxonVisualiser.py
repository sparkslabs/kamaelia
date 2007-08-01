#!/usr/bin/env python

# some test code for AxonVisualiser

import unittest
import sys ; sys.path.append("..")
from AxonVisualiser import *

class AxonVisualiser_Test(unittest.TestCase):

    def test_abbreviate(self):
        abbreviate_tests = [
        ("hello",       "H"),
        ("Hello",       "H"),
        ("HelloWorld",  "HW"),
        ("Hello1World", "H1W"),
        ("hello_world", "H_W"),
        ("CSA_123",     "CSA_123") ]
        
        for (input,output) in abbreviate_tests:
            self.assert_(abbreviate(input) == output, 'abbreviate("' + input + '") == "' + output + '"')

            
    def test_nearest45DegreeStep(self):
        from math import cos, sin, radians
        
        # test a range of angles
        for angle in range(0, 360, 45):
            for wobble in range(-22, +23, 8):
                for bigmag in range(2, 20, 4):
                    mag = bigmag / 10.0
                    dx = mag * cos(radians(angle+wobble))
                    dy = mag * sin(radians(angle+wobble))
                    self.assert_(nearest45DegreeStep( (dx,dy) ) == angle, "nearest45DegreeStep( ("+str(dx)+", "+str(dy)+") ) == "+str(angle))
                    
        # also check dx == 0, dy == 0
        dx = 0.0
        dy = 0.0
        angle = 0
        self.assert_(nearest45DegreeStep( (dx,dy) ) == angle, "nearest45DegreeStep( ("+str(dx)+", "+str(dy)+") ) == "+str(angle))                
        
        
if __name__=="__main__":
    unittest.main()
    