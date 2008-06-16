#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

import unittest

import KamExpectMatcher

class KamExpectMatcherTestCase(unittest.TestCase):
    def testMatcherString(self):
        matcher = KamExpectmatcher.matcheser("hello")
        self.assertTrue(  matcher.matches("hello"))
        self.assertFalse( matcher.matches("hellosomething"))
        self.assertFalse( matcher.matches("somethinghello"))
        self.assertFalse( matcher.matches("something"))
        self.assertFalse( matcher.matches(None))
        self.assertFalse( matcher.matches(5))
        
    def testMatcherInt(self):
        matcher = KamExpectmatcher.matcheser(5)
        self.assertTrue(  matcher.matches(5))
        self.assertTrue(  matcher.matches(5.0))
        self.assertFalse( matcher.matches(4))
        self.assertFalse( matcher.matches(6))
        self.assertFalse( matcher.matches("something"))
        self.assertFalse( matcher.matches(None))
        
    def testMatcherRegexpBasic(self):
        matcher = KamExpectMatcher.RegexpMatcher("hello")
        self.assertTrue(  matcher.matches("hello"))
        self.assertTrue(  matcher.matches("hellosomething"))
        self.assertFalse( matcher.matches("somethinghello"))
        self.assertFalse( matcher.matches("somethinghellosomething"))
        self.assertFalse( matcher.matches("something"))
        self.assertFalse( matcher.matches(None))
        
    def testMatcherRegexpSubstr(self):
        matcher = KamExpectMatcher.RegexpMatcher(".*hello.*")
        self.assertTrue(  matcher.matches("hello"))
        self.assertTrue(  matcher.matches("hellosomething"))
        self.assertTrue(  matcher.matches("somethinghello"))
        self.assertTrue(  matcher.matches("somethinghellosomething"))
        self.assertFalse( matcher.matches("something"))
        self.assertFalse( matcher.matches(None))

    def testMatcherRegexpFixed(self):
        matcher = KamExpectMatcher.RegexpMatcher("^hello$")
        self.assertTrue(  matcher.matches("hello"))
        self.assertFalse( matcher.matches("hellosomething"))
        self.assertFalse( matcher.matches("somethinghello"))
        self.assertFalse( matcher.matches("somethinghellosomething"))
        self.assertFalse( matcher.matches("something"))
        self.assertFalse( matcher.matches(None))

if __name__ == '__main__':
    unittest.main()
