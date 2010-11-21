#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------

import unittest

import sys; sys.path.append("../")
from Rationals import rational, limit

class Rationals_Tests(unittest.TestCase):
    def test_Identities(self):
        self.assertEqual( (1,1), rational(1.0))
        self.assertEqual( (0,1), rational(0.0))
        self.assertEqual( (-1,1), rational(-1.0))

    def test_Integers(self):
        self.assertEqual( (2,1), rational(2.0))
        self.assertEqual( (-100,1), rational(-100.0))

    def test_EasyFractions(self):
        self.assertEqual( (1,2), rational(0.5))
        self.assertEqual( (1,4), rational(0.25))
        self.assertEqual( (-1,2), rational(-0.5))

    def test_NastyFractions(self):
        self.assertEqual( (1,3), rational(1.0/3))
        self.assertEqual( (10,3), rational(3+1.0/3))
        self.assertEqual( (-1,3), rational(-1.0/3))
        self.assertEqual( (-10,3), rational(-3-1.0/3))

    def test_OtherFractions(self):
        self.assertEqual( (337,218), rational(337.0/218))
        
if __name__=="__main__":
    unittest.main()

# RELEASE: MH, MPS
