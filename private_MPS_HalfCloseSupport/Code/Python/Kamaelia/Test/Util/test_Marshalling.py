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
#

import unittest
import sys ; sys.path.append("..")
from Marshalling import Marshaller, DeMarshaller

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
                for i in xrange(1,100):
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

           for _ in xrange(0,10):
               component.next()
               
           result = component._collect("outbox")
           expected = testData[src]
           self.assert_(result == expected, "With example integer serialiser, "+repr(src)+" should "+actiontype+" to "+repr(expected)+"")


# ----------------
             
if __name__ == "__main__":
    unittest.main()
