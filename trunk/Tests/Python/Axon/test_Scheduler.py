#!/usr/bin/python
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
# Aim: Full coverage testing of the
#

# Test the module loads
import unittest

# import preconditions record values
from Axon.Scheduler import *

class scheduler_Test(unittest.TestCase):
   def setUp(self):
      pass
   def test_importsuccess(self):
      self.failUnless(microprocess.schedulerClass is scheduler)
      self.failUnless(scheduler.run)
   def test_SmokeTest_NoArguments(self):
      "__init__ - Called with no arguments ... "
      scheduler.run = None
      s=scheduler()
      self.failUnless(scheduler.run is s)
      
   def test_sensiblestructure(self):
      "Conceptual issue to discuss"
      self.fail("""Rip out the slowmo stuff from the the scheduler.
                Option 1: instead make a component that blocks the right amount
                of time to slow down the system.  This would leave a
                far simpler system and make dynamic control easier.
                Option 2: Allow the implementation of simpler ways for running the scheduler
                Option 3: move slowmo into runThreads instead.
                etc.""")
      

if __name__=='__main__':
   unittest.main()
