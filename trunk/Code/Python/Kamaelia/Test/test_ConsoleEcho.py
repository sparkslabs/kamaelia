#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Full coverage testing of the NullPayloadRTP module.
#

# Test the module loads
import unittest
import sys ; sys.path.append("..")
import Kamaelia.Util.Console

class ConsoleEcho_Test(unittest.TestCase):
   def test_init_minArgs(self):
       """Smoke test with minimal arguments"""
       P = Kamaelia.Util.Console.ConsoleEchoer()
       self.assertEqual(P.__class__, Kamaelia.Util.Console.ConsoleEchoer, "Correctly initialised value created")
       self.assert_(not P.forwarder, "This is not a forwarder")
       self.assert_(P.init)

   def test_init_forwarder(self):
       """Smoke test creating a forwarder"""
       P = Kamaelia.Util.Console.ConsoleEchoer(forwarder=True)
       self.assertEqual(P.__class__, Kamaelia.Util.Console.ConsoleEchoer, "Correctly initialised value created")
       self.assert_(P.forwarder, "This is a forwarder")
       self.assert_(P.init)

if __name__=="__main__":
   unittest.main()
