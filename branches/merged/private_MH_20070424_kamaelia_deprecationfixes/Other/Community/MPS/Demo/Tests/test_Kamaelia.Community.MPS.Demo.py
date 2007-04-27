#!/usr/bin/python

import Axon
import unittest
import Kamaelia.Community.MPS.Demo as Demo

class SmokeTests_SomeComponent(unittest.TestCase):
    def test_SmokeTest(self):
        """__init__ - Called with no arguments succeeds"""
        S = Demo.SomeComponent()
        self.assert_(isinstance(S, Axon.Component.component))

if __name__=="__main__":
    unittest.main()
