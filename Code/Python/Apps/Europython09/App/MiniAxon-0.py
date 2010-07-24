#!/usr/bin/python
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
print "0. Generators"
print "You're expected to manually copy and paste the contents"
print "of this file into a python console, so you can see what"
print "it does"

def fib(a,b):
    while 1:
        yield a
        a, b = b, b + a

g = fib(1,1)
g
g.next()
g.next()
g.next()
g.next()
g.next()
g.next()

GS = [ fib(x,x) for x in range(10) ]
GS
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]

def fib(a,b):
    while 1:
        yield 1 # Just to say "keep running me"
        print a
        a, b = b, b + a

g = fib(1,1)
g
for i in range(15):
    r = g.next()

def printer(tag):
    while 1:
        yield 1 # Makes it a generator
        print tag

PS = [ printer(str(x)) for x in range(10) ]
PS
for i in range(10):
    r = [ p.next() for p in PS ]

print
print
print "0. Generators"
print "You're expected to manually copy and paste the contents"
print "of this file into a python console, so you can see what"
print "it does"
