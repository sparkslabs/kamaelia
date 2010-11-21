#!/usr/bin/env python2.3
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
