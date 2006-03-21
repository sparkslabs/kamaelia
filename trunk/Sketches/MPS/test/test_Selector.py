#!/usr/bin/python

import unittest

import sys; sys.path.append("../")
from Selector import Selector

import Axon

class SmokeTests_Selector(unittest.TestCase):
    def test_SmokeTest(self):
        """__init__ - Called with no arguments succeeds"""
        S = Selector()
        self.assert_(isinstance(S, Axon.Component.component))

if __name__=="__main__":
    unittest.main()
