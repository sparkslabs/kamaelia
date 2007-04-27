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
# VariableRateControl tests

import unittest
import sys ; sys.path.append("..")
from RateFilter import VariableByteRate_RequestControl as VariableRateControl

import time

class VariableRateControl_Internal_InitialisationTests(unittest.TestCase):

   def test_Instantiate_Defaults(self):
      """No arguments is okay for __init__()"""
      r=VariableRateControl()


   def test_Instantiate_SpecifyChunkSize(self):
       """Specifying only rate and chunksize is okay as arguments for __init__()"""
       r=VariableRateControl(rate = 100, chunksize = 25)

       self.assert_(r.chunksize == 25, "__init__ VariableRateControl.chunksize is as specified")
       self.assert_(r.timestep  == 0.25,  "__init__ VariableRateControl.timestep calculated correctly")

   def test_Instantiate_SpecifyChunkRate(self):
       """Specifying only rate and chunkrate is okay as arguments for __init__()"""
       r=VariableRateControl(rate = 100, chunkrate = 8)

       self.assert_(r.chunksize == 12.5, "__init__ VariableRateControl.chunksize calculated correctly")
       self.assert_(r.timestep  == 0.125,  "__init__ VariableRateControl.timestep is as specified")


   def test_Instantiate_SpecifyBoth(self):
       """You can't specify both chunkrate and chunksize as arguments for __init__()"""
       try:
           r=VariableRateControl(rate = 100, chunksize = 25, chunkrate = 4)
           self.fail("Should have failed")
       except:
           pass


# ----------------

class VariableRateControl_TimingTests(unittest.TestCase):

    def test_SimpleCase(self):
        """Setting rate and chunksize to cleanly divisible values will result in a
        consistent stream of output.

        Eg. if rate=100 and chunksize=25 then '25' will be emitted exactly every 0.25 seconds
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                    0.001,
                                    [ (0.0,   "receive", [25]),
                                      (0.25,  "receive", [25]),
                                      (0.50,  "receive", [25]),
                                      (0.75,  "receive", [25]),
                                      (1.00,  "receive", [25]),
                                      (1.25,  "receive", [25]),
                                      (1.50,  "receive", [25])
                                    ] )



    def test_DelayCatchupWithAggregation(self):
        """With allowchunkaggregation turned on, if emission gets behind, it will catch up by
        emitting a single large value.

        Eg. if rate=100 and chunksize=25 and there is a 'freeze' for 1 second, then there will
        be a single 'catchup' emission of a value of 100.
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                    0.001,
                                    [ (0.0,   "receive", [25]),
                                      (0.25,  "receive", [25]),
#                                      (0.28,  "freeze", 1.0),
                                      (1.25,  "receive", [100]),
                                      (1.50,  "receive", [25]),
                                      (1.75,  "receive", [25])
                                    ] )

    def test_DelayCatchupWithoutAggregation(self):
        """With allowchunkaggregation turned off, if emission gets behind, it will catch up by
        emitting a succession of values, of chunksize.

        Eg. if rate=100 and chunksize=25 and there is a 'freeze' for 1 second, then there will
        be a 4 'catchup' emissions of the value 25.
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":False},
                                    0.001,
                                    [ (0.0,   "receive", [25]),
                                      (0.25,  "receive", [25]),
#                                      (0.28,  "freeze", 1.0),
                                      (1.28,  "receive", [25,25,25,25]),
                                      (1.50,  "receive", [25]),
                                      (1.75,  "receive", [25])
                                    ] )

    def test_ChunkSizeRounding(self):
        """If the chunksize is non integer, then with allowchunkaggregation turned on, over time
        it will even out by sometimes emitting a value 1 greater.

        Eg. if rate=100 and chunkrate=3 then 2/3rds of values emitted with be 33, and the remaining
        1/3rd will be 34.
        """
        self.do_test_EventSequence( {"rate":100, "chunkrate":3, "allowchunkaggregation":True},
                                  0.001,
                                  [ (0.0,     "receive", [33]),
                                    (0.3333,  "receive", [33]),
                                    (0.6666,  "receive", [34]),
                                    (1.0000,  "receive", [33]),
                                    (1.3333,  "receive", [33]),
                                    (1.6666,  "receive", [34]),
                                    (2.0000,  "receive", [33]),
                                    (2.3333,  "receive", [33]),
                                    (2.6666,  "receive", [34]),
                                  ] )

    def test_RateChangeNoChange(self):
        """Changing the rate, between symbol emissions, to the same as it currently is will have
        no effect on what is emitted, no matter how many times it is changed."""
        self.do_test_EventSequence( {"rate":100, "chunksize":25, "allowchunkaggregation":True},
                                    0.001,
                                    [ (0.0,   "receive", [25]),
                                      (0.25,  "receive", [25]),
                                      (0.50,  "receive", [25]),
                                      (0.75,  "receive", [25]),
                                      (0.85,  "newrate", 100),
                                      (1.00,  "receive", [25]),
                                      (1.05,  "newrate", 100),
                                      (1.10,  "newrate", 100),
                                      (1.15,  "newrate", 100),
                                      (1.25,  "receive", [25]),
                                      (1.50,  "receive", [25])
                                    ] )
    

    def test_RateChangeBetweenEmissions(self):
        """Changing the rate, between emissions, will act as if the old rate held until
        the exact time at which the change occurred.

        eg. if emmissions occur every 0.5 seconds, and the rate is doubled halfway between emissions,
        the next emission will occur 0.125 seconds later, continuning every 0.25 of a second.
        """
        self.do_test_EventSequence( {"rate":100, "chunksize":50, "allowchunkaggregation":True},
                                    0.0001,
                                    [ (0.0,   "receive", [50]),
                                      (0.50,  "receive", [50]),
                                      (1.00,  "receive", [50]),
                                      (1.50,  "receive", [50]),
                                      (2.00,  "receive", [50]),
                                      (2.25,  "newrate", 200),
                                      (2.375, "receive", [50]),
                                      (2.625, "receive", [50]),
                                      (2.875, "receive", [50])
                                    ] )

    def test_MultipleRateChangeBetweenEmissions(self):
        """Changing the rate multiple times, between emissions, will act as if each rate
        holds for the exact durations between the times the rate change events occurred.

        eg. if emmissions occur once a second, and the rate is briefly doubled for 1/2 a second
        before being reset to the original rate, all further emissions will occur 1/4 second
        earlier than they would have originally.
        """
        self.do_test_EventSequence( {"rate":10, "chunksize":10, "allowchunkaggregation":True},
                                    0.0001,
                                    [ (0.0,  "receive", [10]),
                                      (1.00, "receive", [10]),
                                      (2.00, "receive", [10]),
                                      (2.15, "newrate", 20),  # brief doubling of rate
                                      (2.4,  "newrate", 10),
                                      (2.75, "receive", [10]),
                                      (3.75, "receive", [10]),
                                      (4.75, "receive", [10])
                                    ] )


    # - - - - - -

    def do_test_EventSequence(self, argDict, tolerance, schedule):
        """Do a timing test for the rate control component.

        argDict = arguments passed to VariableRateControl.__init__()
        tolerance = tolerance of timings for the test (+ or -) this amount acceptable
        schedule = list of events (in chronological order).
                    Each list item is a tuple:
                    (relative_time, action, actionarg)

                    t, action, arg:
                        t, "receive", List - at time 't' since start of test, expect VariableRateControl
                                            to send the items in the list consecutively, nothing more, nothing less
                                            this will also test at t + tolerance that nothing
                                            else comes out

        Test will succeed if and only if, all 'expect' events occur (within the timing tolerance specified)
        and no other events occur at other times
        """
        r=VariableRateControl(**argDict)

        starttime = time.time()  # a positive start time offset
        r.resetTiming(starttime)

        chunklist = []
        for (reltime, action, arg) in schedule:
            e = "t="+str(reltime)+" : "

            if action == "receive":
#                # test time fractionally before
#                chunklist = list( r.getChunksToSend(starttime+reltime-tolerance) )
#                self.assert_( [] == chunklist, e+"VariableRateControl emits nothing just before time "+str(reltime)+" in this test (not "+str(chunklist)+")")

                # now test what we receive at the time itself
                chunklist = list( r.getChunksToSend(starttime+reltime+0.001) )
                self.assert_( arg == chunklist, e+"VariableRateControl emits "+repr(arg)+" at time "+str(reltime)+" in this test (not "+str(chunklist)+")")

                # test time fractionally after
                chunklist = list( r.getChunksToSend(starttime+reltime+tolerance) )
                self.assert_( [] == chunklist, e+"VariableRateControl emits nothing just after time "+str(reltime)+" in this test (not "+str(chunklist)+")")

            elif action == "newrate":
                r.changeRate(arg, starttime+reltime)


# - - - - - - - -



# ----------------
             
if __name__ == "__main__":
    unittest.main()
