#!/usr/bin/python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# RateControl tests

import unittest
import sys ; sys.path.append("..")
from RateControl import RateControl

import time

class RateControl_Internal_InitialisationTests(unittest.TestCase):

   def test_Instantiate_Defaults(self):
      """__init__ - no args is okay"""
      r=RateControl()


   def test_Instantiate_SpecifyChunkSize(self):
       """__init__ - specifying only rate and chunksize is okay"""
       r=RateControl(rate = 100, chunksize = 25)

       self.assert_(r.chunksize == 25, "__init__ RateControl.chunksize is as specified")
       self.assert_(r.timestep  == 0.25,  "__init__ RateControl.timestep calculated correctly")

   def test_Instantiate_SpecifyChunkRate(self):
       """__init__ - specifying only rate and chunkrate is okay"""
       r=RateControl(rate = 100, chunkrate = 8)

       self.assert_(r.chunksize == 12.5, "__init__ RateControl.chunksize calculated correctly")
       self.assert_(r.timestep  == 0.125,  "__init__ RateControl.timestep is as specified")


   def test_Instantiate_SpecifyBoth(self):
       """__init__ = can't specify both chunkrate and chunksize"""
       try:
           r=RateControl(rate = 100, chunksize = 25, chunkrate = 4)
           self.fail("Should have failed")
       except:
           pass


# ----------------

def Make_RateControl_TimingTest(argDict, tolerance, schedule):
    """Make a timing test for the rate control component.

       argDict = arguments passed to RateControl.__init__()
       tolerance = tolerance of timings for the test (+ or -) this amount acceptable
       schedule = list of events (in chronological order).
                  Each list item is a tuple:
                  (relative_time, action, actionarg)

                  t, action, arg:
                     t, "expect", N   - at time 't' since start of test, expect RateControl to send 'N'
                     t, "freeze", N   - at time 't' freeze (don't call RateControl) for 'N' seconds

       Test will succeed if and only if, all 'expect' events occur (within the timing tolerance specified)
       and no other events occur at other times
    """
    class RateControl_TimingTests(unittest.TestCase):

        def test_EventSequence(self):
            """Testing rate control timing"""
            r=RateControl(**argDict)

            r.resetTiming()
            starttime = time.time()

            chunklist = []
            event = 0
            for (reltime, action, arg) in schedule:
                event += 1
                e = "["+str(event)+"] "

                if action == "expect":
                    expectedFound = False
                    while not expectedFound and (time.time() < starttime + reltime + tolerance):
                        if not chunklist:
                            chunklist = list(r.getChunksToSend())
                            
                        if chunklist:
                            chunksize = chunklist[0]
                            chunklist = chunklist[1:]
                            
                            now = time.time() - starttime
                            if now >= reltime-tolerance:
                                self.assert_(chunksize == arg, e+"RateControl emits request for chunksize of "+str(arg)+" (not "+str(chunksize)+") at time "+str(now)+" in this test")
                                expectedFound = True
                            else:
                                self.fail(e+"RateControl shouldn't emit 'chunksize' of "+str(chunksize)+" at time "+now+" in this test")

                    self.assert_(expectedFound, e+"RateControl didn't emit request at time "+str(reltime)+" as required in this test")

                elif action == "freeze":
                    while (time.time() < starttime + reltime + tolerance):
                        for chunksize in r.getChunksToSend():
                            now = time.time() - starttime
                            self.fail(e+"RateControl shouldn't emit 'chunksize' of "+str(chunksize)+" at time "+now+" in this test")

                    # we've waited until reltime + tolerance (to catch any spurious 'emissions' from RateControl
                    # so when we now 'freeze' we must compensate the sleep duration
                    time.sleep(arg - tolerance)



    return RateControl_TimingTests
        

# - - - - - - - -


# test simple
t1 = Make_RateControl_TimingTest( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                  0.01,
                                  [ (0.0,   "expect", 25),
                                    (0.25,  "expect", 25),
                                    (0.50,  "expect", 25),
                                    (0.75,  "expect", 25),
                                    (1.00,  "expect", 25),
                                    (1.25,  "expect", 25),
                                    (1.50,  "expect", 25)
                                  ] )

# test delay catchup with aggregation
t2 = Make_RateControl_TimingTest( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                  0.01,
                                  [ (0.0,   "expect", 25),
                                    (0.25,  "expect", 25),
                                    (0.28,  "freeze", 1.0),
                                    (1.28,  "expect", 100),
                                    (1.50,  "expect", 25),
                                    (1.75,  "expect", 25)
                                  ] )

# test delay catchup without aggregation
t3 = Make_RateControl_TimingTest( {"rate":100, "chunksize":25, "allowchunkaggregation":False},
                                  0.01,
                                  [ (0.0,   "expect", 25),
                                    (0.25,  "expect", 25),
                                    (0.28,  "freeze", 1.0),
                                    (1.28,  "expect", 25),
                                    (1.28,  "expect", 25),
                                    (1.28,  "expect", 25),
                                    (1.28,  "expect", 25),
                                    (1.50,  "expect", 25),
                                    (1.75,  "expect", 25)
                                  ] )

# test rounding of chunk sizes
t4 = Make_RateControl_TimingTest( {"rate":100, "chunkrate":3, "allowchunkaggregation":True},
                                  0.01,
                                  [ (0.0,     "expect", 33),
                                    (0.3333,  "expect", 33),
                                    (0.6666,  "expect", 34),
                                    (1.0000,  "expect", 33),
                                    (1.3333,  "expect", 33),
                                    (1.6666,  "expect", 34),
                                    (2.0000,  "expect", 33),
                                    (2.3333,  "expect", 33),
                                    (2.6666,  "expect", 34),
                                  ] )

# ----------------
             
if __name__ == "__main__":
    unittest.main()