#!/usr/bin/env python
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

# C2 merge algorithm for establishing method resolution order of classes

def mro(klass):
    order = [klass]
    bases = list(klass.__bases__)
    mergedBases = [mro(base) for base in bases]
    mergedBases.extend([[base] for base in bases])
    while len(mergedBases) > 0:
        for baselist in mergedBases:
            head = baselist[0]
            foundElsewhere = [True for merged in mergedBases if (head in merged[1:])]
            if foundElsewhere == []:
                order.append(head)
                for baselist in mergedBases:
                    if baselist[0]==head:
                        del baselist[0]
                mergedBases = [baselist for baselist in mergedBases if baselist != []]
                break
        if foundElsewhere:
            raise "Failed. Unable to resolve method resolution order."
    return order


if __name__=="__main__":
    O = object
    class F(O): pass
    class E(O): pass
    class D(O): pass
    class C(D,F): pass
    class B(D,E): pass
    class A(B,C): pass
    print
    print mro(A)
    print mro(A) == [A,B,C,D,E,F,O]  # check this is the correct method resolution order

    
    O = object
    class F(O): pass
    class E(O): pass
    class D(O): pass
    class C(D,F): pass
    class B(E,D): pass
    class A(B,C): pass
    print
    print mro(A)
    print mro(A) == [A,B,E,C,D,F,O]  # check this is the correct method resolution order

    
    class A(object): pass
    class B(object): pass
    class C(object): pass
    class D(object): pass
    class E(object): pass
    class K1(A,B,C): pass
    class K2(D,B,E): pass
    class K3(D,A):   pass
    class Z(K1,K2,K3): pass
    print
    print mro(Z)
    print mro(Z) == [Z,K1,K2,K3,D,A,B,C,E,object]  # check this is the correct method resolution order
    
