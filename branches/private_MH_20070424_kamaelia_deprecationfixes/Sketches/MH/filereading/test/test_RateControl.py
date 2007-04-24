#!/usr/bin/python
# RETIRED
print """
/Sketches/filereading/test/test.*Rate*:

 This file has been retired.
 It is retired because it is now part of the main code base.
 If you want to use this, you should be using Kamaelia.Util.RateFilter

 This file now deliberately exits to encourage you to fix your code :-)
"""
import sys
sys.exit(0)


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
      """No arguments is okay for __init__()"""
      r=RateControl()


   def test_Instantiate_SpecifyChunkSize(self):
       """Specifying only rate and chunksize is okay as arguments for __init__()"""
       r=RateControl(rate = 100, chunksize = 25)

       self.assert_(r.chunksize == 25, "__init__ RateControl.chunksize is as specified")
       self.assert_(r.timestep  == 0.25,  "__init__ RateControl.timestep calculated correctly")

   def test_Instantiate_SpecifyChunkRate(self):
       """Specifying only rate and chunkrate is okay as arguments for __init__()"""
       r=RateControl(rate = 100, chunkrate = 8)

       self.assert_(r.chunksize == 12.5, "__init__ RateControl.chunksize calculated correctly")
       self.assert_(r.timestep  == 0.125,  "__init__ RateControl.timestep is as specified")


   def test_Instantiate_SpecifyBoth(self):
       """You can't specify both chunkrate and chunksize as arguments for __init__()"""
       try:
           r=RateControl(rate = 100, chunksize = 25, chunkrate = 4)
           self.fail("Should have failed")
       except:
           pass


# ----------------

class RateControl_TimingTests(unittest.TestCase):

    def test_SimpleCase(self):
        """Setting rate and chunksize to cleanly divisible values will result in a
        consistent stream of output.

        Eg. if rate=100 and chunksize=25 then '25' will be emitted exactly every 0.25 seconds
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                    0.01,
                                    [ (0.0,   "expect", 25),
                                      (0.25,  "expect", 25),
                                      (0.50,  "expect", 25),
                                      (0.75,  "expect", 25),
                                      (1.00,  "expect", 25),
                                      (1.25,  "expect", 25),
                                      (1.50,  "expect", 25)
                                    ] )



    def test_DelayCatchupWithAggregation(self):
        """With allowchunkaggregation turned on, if emission gets behind, it will catch up by
        emitting a single large value.

        Eg. if rate=100 and chunksize=25 and there is a 'freeze' for 1 second, then there will
        be a single 'catchup' emission of a value of 100.
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                    0.01,
                                    [ (0.0,   "expect", 25),
                                      (0.25,  "expect", 25),
                                      (0.28,  "freeze", 1.0),
                                      (1.28,  "expect", 100),
                                      (1.50,  "expect", 25),
                                      (1.75,  "expect", 25)
                                    ] )

    def test_DelayCatchupWithoutAggregation(self):
        """With allowchunkaggregation turned off, if emission gets behind, it will catch up by
        emitting a succession of values, of chunksize.

        Eg. if rate=100 and chunksize=25 and there is a 'freeze' for 1 second, then there will
        be a 4 'catchup' emissions of the value 25.
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":False},
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

    def test_ChunkSizeRounding(self):
        """If the chunksize is non integer, then with allowchunkaggregation turned on, over time
        it will even out by sometimes emitting a value 1 greater.

        Eg. if rate=100 and chunkrate=3 then 2/3rds of values emitted with be 33, and the remaining
        1/3rd will be 34.
        """
        self.do_test_EventSequence( {"rate":100, "chunkrate":3, "allowchunkaggregation":True},
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

    # - - - - - -

    def do_test_EventSequence(self, argDict, tolerance, schedule):
        """Do a timing test for the rate control component.

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



# - - - - - - - -



# ----------------
             
if __name__ == "__main__":
    unittest.main()