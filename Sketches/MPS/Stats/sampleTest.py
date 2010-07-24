#!/usr/bin/env python
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
#

from random import random
import time
targetSample = 22
target = targetSample/100.

def likelihood(numSamples, targetSample, numRequests=1): # This can return > 1.0
   try:
      currentRate= numSamples/float(numRequests)
      result = 100*   ((target-currentRate)/target)
      return result
   except ZeroDivisionError:
      return 1

def test_sampler():
   numRequests = 0
   numSamples = 0
   while 1:
      numRequests += 1
      l = likelihood(numSamples, targetSample, numRequests)
      if random() <= l:
         numSamples += 1
      if 1:
         if int((numSamples/float(numRequests))*100)<=targetSample:
            break
      else:
         print "reqs", numRequests,
         print "samples", numSamples,
         print "size",((numSamples/float(numRequests))*100),
         print "likelyhood", l
   return numRequests, int((numSamples/float(numRequests))*100)


sampleSize=1000
p5 = int(sampleSize*.05)
p25 = int(sampleSize*.25)
p50 = int(sampleSize*.50)
p75 = int(sampleSize*.75)
p95 = int(sampleSize*.95)
p97 = int(sampleSize*.97)
p99 = int(sampleSize*.99)
print p5,p25,p50,p75,p97,p99
for skew in xrange(1,20):
   results=[]
   rates=[]
   for i in xrange(sampleSize):
      x,y=test_sampler()
      results.append(x)
      rates.append(y)

   results.sort()
   print "5,25,50,75,95,97,99 : ", results[p5],results[p25],results[p50],results[p75],results[p95],results[p97],results[p99]
   print "5,25,50,75,95,97,99 : ", rates[p5],rates[p25],rates[p50],rates[p75],rates[p95],rates[p97],rates[p99]





