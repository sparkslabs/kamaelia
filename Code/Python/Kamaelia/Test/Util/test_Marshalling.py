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
#

import unittest
import sys ; sys.path.append("..")
from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

class SerialiseInt:

    def marshall(int):
        return str(int)
    marshall = staticmethod(marshall)

    def demarshall(string):
        return int(string)
    demarshall = staticmethod(demarshall)



def make_SmokeTests(klass,name):
    
    class MySmokeTests(unittest.TestCase):
        """Basic smoke tests"""
    
        def test_InstantiateComponent(self):
            """ instantiates when passed an object with __str__ and fromString methods"""
            k=klass(SerialiseInt)
            k.activate()

        def test_Shutdown(self):
            """ forwards a producerFinished or shutdownMicroprocess message and shuts down immediately"""
            from Axon.Ipc import producerFinished, shutdownMicroprocess

            for msgtype in [producerFinished, shutdownMicroprocess]:
                k=klass(SerialiseInt)
                k.activate()

                # let it run for a bit, checking nothing silly comes out
                for i in range(1,100):
                    k.next()
                    self.assert_(0==len(k.outboxes["outbox"]))
                    self.assert_(0==len(k.outboxes["signal"]))

                # send it a shutdown message
                msg = msgtype(self)
                k._deliver( msg, "control")

                # should immediately stop
                self.assertRaises(StopIteration, k.next)

                # check shutdown message was forwarded
                self.assert_( 1 == len(k.outboxes["signal"]) )
                self.assert_( msg == k._collect("signal") )
                

    # stick class name labels on the front of all doc strings
    for doc in [ x for x in MySmokeTests.__dict__ if x[:5]=="test_" ]:
        MySmokeTests.__dict__[doc].__doc__ = name + MySmokeTests.__dict__[doc].__doc__
        
    return MySmokeTests
        

t1 = make_SmokeTests(Marshaller, "Marshaller")
t2 = make_SmokeTests(DeMarshaller, "DeMarshaller")



class Marshalling_ActionTests(unittest.TestCase):

    def test_Marshalling(self):
       """Ummm. Marshaller should marshall""" 
       self.dotest_inout( Marshaller(SerialiseInt),
                          { 5:"5", 0:"0", 999:"999" },
                          "marshall",
                        )

    def test_DeMarshalling(self):
       """Ummm. DeMarshaller should demarshall""" 
       self.dotest_inout( DeMarshaller(SerialiseInt),
                          { "5":5, "0":0, "999":999 },
                          "demarshall",
                        )


    def dotest_inout(self, component, testData, actiontype):
       component.activate()

       for src in testData:
           component._deliver( src, "inbox" )

           for _ in range(0,10):
               component.next()
               
           result = component._collect("outbox")
           expected = testData[src]
           self.assert_(result == expected, "With example integer serialiser, "+repr(src)+" should "+actiontype+" to "+repr(expected)+"")


# ----------------
             
if __name__ == "__main__":
    unittest.main()
