#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#
# Tests __str__ for different classes
#

import unittest

class str_Test(unittest.TestCase):
   classtotest=None

   def test___str__(self):
      if not self.__class__ is str_Test:
         a = self.__class__.classtotest()
         b = self.__class__.classtotest()
         self.failIf(str(a)==str(b), "str does not produce a result unique to" + self.__class__.classtotest.__name__ +" instance.")
         self.failUnless(str(a)==str(a),"str does not produce a consistent result")

