#!/usr/bin/python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
