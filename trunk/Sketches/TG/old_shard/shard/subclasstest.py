# -*- coding: utf-8 -*-

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
from shard import *
from inspect import *

"""
Test case to work out why superclass calls were causing
TypeErrors on first arguments

Solution:
- superclass calls must be routed through
  function object rather than method
- superclasses must be named in upcall as opposed
  to using super()
"""

class A(object):  #md
    def testA(self):
        print 'a!'
        
class B(object):  #mh
    def testB(self):
        print 'b!'
        
class C(B):  #cp
    def testC(self):
        print 'c!'
        
    def testB(self):
        B.testB.im_func(self)
        print 'and c!'

addShards(C)(A)

dicta = dict(inspect.getmembers(A))
print dicta['testA']
print dicta['testB']
print dicta['testC']

try:
    A().testB()
except TypeError, m:
    print 'TypeError:', m
"""
if addShards doesn't convert methods to functions, prints give:
<unbound method A.testA>
<unbound method C.testB>
<unbound method C.testC>
TypeError: unbound method testB() must be called with C instance as first argument (got nothing instead)

as called, prints give:
<unbound method A.testA>
<unbound method A.testB>
<unbound method A.testC>
TypeError: unbound method testB() must be called with B instance as first argument (got A instance instead)
"""

#~ try:
#~     class D: pass
#~     B.testB(D())
#~ except TypeError, m:
#~     print 'TypeError:', m

#~ try:
#~     class D(B): pass
#~     B.testB(D())
#~ except TypeError, m:
#~     print 'TypeError:', m

#~ try:
#~     class D(B): pass
#~     B.testB.im_func(D())
#~ except TypeError, m:
#~     print 'TypeError:', m

# ok
A.testA.im_func('')