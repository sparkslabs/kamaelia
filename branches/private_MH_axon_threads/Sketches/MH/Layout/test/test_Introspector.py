#!/usr/bin/env python

# some test code for AxonVisualiser

import unittest
import sys ; sys.path.append("..")
import Axon as _Axon
from Introspector import *

from Kamaelia.Util.ConsoleEcho import consoleEchoer

class AxonVisualiser_Test(unittest.TestCase):

    def test_selfintrospection(self):
        from Axon.Scheduler import scheduler
        i = Introspector()
        
        i.activate()
        
        class IntrospectorExaminer(_Axon.Component.component):
            Inboxes = ["inbox"]
            Outboxes = []
            def __init__(self, ut, i):
                super(IntrospectorExaminer, self).__init__()
                
                self.ut = ut
                self.i = i
            def main(self):
                yield 1
                yield 1
                # check the first thing the introspector sends is a "DEL ALL" command
                expectedmsgs = [ 'DEL ALL' ]
                self.ut.assert_(self.dataReady("inbox"), "Receiving initial message from Introspector")
                data = self.recv("inbox")
                data = data.split("\n")
                for line in data:
                    line = line.strip()
                    if line != "":
                        self.ut.assert_(line in expectedmsgs, "Didn't expect message: "+line)
                        expectedmsgs.remove(line)
                yield 1
                self.ut.assert_(expectedmsgs == [], "All messages received, post Introspector and IntrospectorExaminer creation")
                
                
                components, postboxes, linkages = self.i.introspect()

                # check no linkages found        
                self.ut.assert_(linkages   == {(i.id,"o","outbox"):(self.id,"i","inbox")}, "runtime, found linkage from i/outbox to self/inbox")
                
                # check the components found are self and i, only
                self.ut.assert_(len(components) == 2, "Runtime, found components: only 2 components")
                for c in [i,self]:
                    self.ut.assert_( components[c.id] == c.name, "Runtime, found component: component "+str(c.id)+" with name "+str(components[c.id]))

                # check the postboxes found are the 4 belonging to i only and 1 to self
                for p in [ (self.id, "i", "inbox"),
                           (i.id,    "i", "inbox"),
                           (i.id,    "i", "control"),
                           (i.id,    "o", "outbox"),
                           (i.id,    "o", "signal") ]:
                    self.ut.assert_( p in postboxes, "Runtime, found postbox: "+str(p))
                    postboxes.remove(p)
                self.ut.assert_(len(postboxes) == 0, "Runtime, only the intended postboxes found")
                
                # check the first stream of data to come out of Introspector
                yield 1
                yield 1
                _s  = '"'+str(self.id)+'"'
                _i  = '"'+str(i.id)+'"'
                _si = '"'+str((self.id,"i","inbox"))+'"'
                _ii = '"'+str((i.id,"i","inbox"))+'"'
                _ic = '"'+str((i.id,"i","control"))+'"'
                _io = '"'+str((i.id,"o","outbox"))+'"'
                _is = '"'+str((i.id,"o","signal"))+'"'
                expectedmsgs = [ 'ADD NODE '+_i+' "'+str(i.name)+'" randompos component',
                                 'ADD NODE '+_s+' "'+str(self.name)+'" randompos component',
                                 'ADD NODE '+_ii+' "inbox" randompos inbox',
                                 'ADD NODE '+_ic+' "control" randompos inbox',
                                 'ADD NODE '+_io+' "outbox" randompos outbox',
                                 'ADD NODE '+_is+' "signal" randompos outbox',
                                 'ADD NODE '+_si+' "inbox" randompos inbox',
                                 'ADD LINK '+_i+' '+_ii,
                                 'ADD LINK '+_i+' '+_io,
                                 'ADD LINK '+_i+' '+_is,
                                 'ADD LINK '+_i+' '+_ic,
                                 'ADD LINK '+_s+' '+_si,
                                 'ADD LINK '+_io+' '+_si ]
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    data = data.split("\n")
                    for line in data:
                        line = line.strip()
                        if line != "":
                            self.ut.assert_(line in expectedmsgs, "Didn't expect message: "+line)
                            expectedmsgs.remove(line)
                    yield 1
                self.ut.assert_(expectedmsgs == [], "All messages received, post Introspector and IntrospectorExaminer creation")
                
                # check thats all
                yield 1
                yield 1
                self.ut.assert_(not self.dataReady("inbox"), "No more messages, post Introspector and IntrospectorExaminer creation.")
                
                # create and activate another component
                e = consoleEchoer()
                e.activate()
                # check for new messages
                yield 1
                yield 1
                _e = '"'+str(e.id)+'"'                
                _ei = '"'+str((e.id,"i","inbox"))+'"'
                _ec = '"'+str((e.id,"i","control"))+'"'
                _eo = '"'+str((e.id,"o","outbox"))+'"'
                _es = '"'+str((e.id,"o","signal"))+'"'
                expectedmsgs = [ 'ADD NODE '+_e+' "'+str(e.name)+'" randompos component',
                                 'ADD NODE '+_ei+' "inbox" randompos inbox',
                                 'ADD NODE '+_ec+' "control" randompos inbox',
                                 'ADD NODE '+_eo+' "outbox" randompos outbox',
                                 'ADD NODE '+_es+' "signal" randompos outbox',
                                 'ADD LINK '+_e+' '+_ei,
                                 'ADD LINK '+_e+' '+_eo,
                                 'ADD LINK '+_e+' '+_es,
                                 'ADD LINK '+_e+' '+_ec ]
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    data = data.split("\n")
                    for line in data:
                        line = line.strip()
                        if line != "":
                            self.ut.assert_(line in expectedmsgs, "Didn't expect message: "+line)
                            expectedmsgs.remove(line)
                self.ut.assert_(expectedmsgs == [], "All messages received, post consoleEchoer creation")
                                                
                # check thats all
                yield 1
                yield 1
                self.ut.assert_(not self.dataReady("inbox"), "No more messages, post Introspector and IntrospectorExaminer creation.")

                # create link to console echoer
                i.link( (i,"signal"), (e,"inbox") )
                # check for new messages
                yield 1
                yield 1
                expectedmsgs = [ 'ADD LINK '+_is+' '+_ei ]
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    data = data.split("\n")
                    for line in data:
                        line = line.strip()
                        if line != "":
                            self.ut.assert_(line in expectedmsgs, "Didn't expect message: "+line)
                            expectedmsgs.remove(line)
                self.ut.assert_(expectedmsgs == [], "All messages received, post linking Introspector/signal to consoleEchoer/inbox")
                                               
                # check thats all
                yield 1
                yield 1
                self.ut.assert_(not self.dataReady("inbox"), "No more messages, post Introspector and IntrospectorExaminer creation.")

                # disconnect Introspector from consoleEchoer
                for l in i.postoffice.linkages:
                    if ((l.source, l.sourcebox), (l.sink, l.sinkbox)) == ((i, "signal"), (e, "inbox")):
                        i.postoffice.deregisterlinkage( thecomponent=None, thelinkage=l )
                        
                # check for new messages
                yield 1
                yield 1
                expectedmsgs = [ 'DEL LINK '+_is+' '+_ei ]
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    data = data.split("\n")
                    for line in data:
                        line = line.strip()
                        if line != "":
                            self.ut.assert_(line in expectedmsgs, "Didn't expect message: "+line)
                            expectedmsgs.remove(line)
                self.ut.assert_(expectedmsgs == [], "All messages received, post unlinking Introspector/signal from consoleEchoer/inbox")
                
                # check thats all
                yield 1
                yield 1
                self.ut.assert_(not self.dataReady("inbox"), "No more messages, post Introspector and IntrospectorExaminer creation.")

                # terminate console echoer
                e._deliver(message=shutdownMicroprocess(), boxname="control")
                yield 1
                yield 1

                # check for new messages
                yield 1
                yield 1
                expectedmsgs = [ 'DEL NODE '+_e,
                                 'DEL NODE '+_ei,
                                 'DEL NODE '+_ec,
                                 'DEL NODE '+_eo,
                                 'DEL NODE '+_es ]
                while self.dataReady("inbox"):
                    data = self.recv("inbox")
                    data = data.split("\n")
                    for line in data:
                        line = line.strip()
                        if line != "":
                            self.ut.assert_(line in expectedmsgs, "Didn't expect message: "+line)
                            expectedmsgs.remove(line)
                self.ut.assert_(expectedmsgs == [], "All messages received, post termination of consoleEchoer")
                
                # check thats all
                yield 1
                yield 1
                self.ut.assert_(not self.dataReady("inbox"), "No more messages, post Introspector and IntrospectorExaminer creation.")

                
                                
                # terminate
                self.i._deliver(message=shutdownMicroprocess(), boxname="control")

        
        
        ex = IntrospectorExaminer(self, i)
        ex.activate()
        
        i.link((i,"outbox"), (ex,"inbox"))
        
        scheduler.run.runThreads(slowmo=0)


        
if __name__=="__main__":
    unittest.main()
    