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

"""
Test case to check whether forcing supercalls to functions
affects access to class attributes

Result:
- Added methods retain usual access to class attributes
- Attribute overriding semantics maintained with shard subclassing
- Shards cannot override container attribute names: addShards raises a TypeError
- Container class can access variables of added shards
- Shard class can access variables of container class
"""

# container class: requires a(), bStr
class t1(object):
    #aStr = 't1'    # name clash; shard addition fails
    cStr = 'c:t1'
    
    def test(self):
        self.a()
        print self.bStr  # container class can access shard attributes


# shard: provides a(), aStr
class s1(object):
    aStr = 'ello'
    
    def a(self):
        print self.aStr

# subshard: provides bStr; extends a()
class s2(s1):
    #aStr = 's2'    # redefining aStr always overrides s1.aStr (shard and direct instantiation)
    bStr = 'b: s2'
    
    def a(self):
        #s1.a(self)   # identical behaviour to im_func call when s2 instantiated directly
        s1.a.im_func(self)
        print self.bStr
        print self.cStr  # shard can access container class attributes

requires('cStr')(s2)

addShards(s2)(t1)

# instantiate s2 directly to give a 'control' output for attr overriding
#s2().a()   # direct instantiation causes container variable access to fail

# indirect call of a() using shard mechanism
t1().test()
