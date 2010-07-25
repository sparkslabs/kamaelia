#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
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

import sys; sys.path.append("../pprocess/"); sys.path.append(".."); 

# To be used
#from MultiPipeline import ProcessPipeline
#from MultiPipeline import ProcessGraphline

import Axon
from Axon.Ipc import producerFinished
import Kamaelia.Testing.KamTestCase as KamTestCase
import Kamaelia.Testing.KamExpectMatcher as KamExpectMatcher
from Kamaelia.Chassis.Pipeline import Pipeline

import time

class BasicDuplicator(Axon.Component.component):
    def __init__(self, times, *argv, **kargv):
        super(BasicDuplicator, self).__init__(*argv, **kargv)
        self._times = times
        
    def main(self):
        n = 0
        while True:
            n += 1
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                # Sending it self._times times
                for _ in xrange(self._times):
                    self.send(data, 'outbox')
            if self.dataReady('control'):
                data = self.recv('control')
                self.send(data, 'signal')
                return
            if not self.anyReady():
                self.pause()
            yield 1

class MessagingThroughPipelineTestCase(KamTestCase.KamTestCase):
    def setUp(self):
        # Every message will be forwarder 6 times
        # (so we are sure that it's going through both duplicators)
        self.pipeline = Pipeline(
            BasicDuplicator(2), 
            BasicDuplicator(3)
        )
        self.times = 2 * 3
        self.initializeSystem(self.pipeline)
        
    def _genericTestPipeline(self, testdata):
        for msg in testdata:
            self.put(msg, 'inbox')
            for pos in xrange(self.times):
                try:
                    data = self.get('outbox', timeout=5)
                except Exception, e:
                    print "fail!", time.time()
                    raise
                self.assertEquals(msg, data, 
                    'Message number %s was different: %s != %s' % (pos, msg, data)
                )
                
        finishMessage = producerFinished()
        self.put(finishMessage, 'control')
        data = self.get('signal', timeout=5)
        self.assertEquals(finishMessage, data)
        self.assertOutboxEmpty('outbox')
        self.assertOutboxEmpty('signal')
    
    def testPipelineEmpty(self):
        testdata = ()
        self._genericTestPipeline(testdata)
        
    def testPipelineListOfNumbers(self):
        testdata = [1,2,3,4,5]
        self._genericTestPipeline(testdata)
        
    def testPipelineListOfLists(self):
        testdata = [[1,2],[3,4],[5,6]]
        self._genericTestPipeline(testdata)
        
    def testPipelineListOfTuples(self):
        testdata = [(1,2),(3,4), (5,6), (7,8)]
        self._genericTestPipeline(testdata)
        
    def testPipelineListOfDictionaries(self):
        testdata = [{ (1,2):(3,4)} , {(5,6):(7,8)}]
        self._genericTestPipeline(testdata)
    
def suite():
    return KamTestCase.makeSuite(
            MessagingThroughPipelineTestCase.getTestCase()
        )
        
if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
