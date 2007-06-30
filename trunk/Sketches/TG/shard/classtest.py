from shard import *
from inspect import *

"""
rebinding tests - superclass calls must be routed through
function object rather than method
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