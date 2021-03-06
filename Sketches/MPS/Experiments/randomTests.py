#!/usr/local/bin/python
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
"""Program to test the idea of a rotating rand range.
ie overall generally increasing, but loops much quicker
than would otherwise. 
"""
def normrand(range):
	import random
	a=random.Random()
	while 1:
		yield a.randint(0,range)

def myrand(range):
	import random
	A=random.Random().randint
	seq = lambda : A(1,range)
	c=0
	while 1:
		c = (c+seq()) % range
		yield c

def myrand2(range,factor):
	import random
	incr = range / factor
	A=random.Random().randint
	seq = lambda : A(1,incr)
	c=0
	while 1:
		c = (c+seq()) % range
		yield c


def dupfind(range,randgen):
	count=0
	seen={}
	rnd=randgen(range).next
	while 1:
		c = rnd()
		if str(c) in seen: break
		seen[str(c)]=1
		count = count + 1
	return count,seen

def dostats(range,randfunc,count=10):
	hit={}
	for i in xrange(count):
		count,seen = dupfind(range,randfunc)
		try:             hit[str(count)] = hit[str(count)]+1
		except KeyError: hit[str(count)] = 1
	for key in hit.keys():
		print "repetition after",key," hits : ", hit[str(key)]

# dostats(2147483647,2)

for func in [normrand,myrand,
             lambda x: myrand2(x,3),
		   lambda x: myrand2(x,10),
		   lambda x: myrand2(x,30),
		   lambda x: myrand2(x,100) ]:
	print "===Doing stats for ", func.__name__
	print
	dostats(10000,func,1000)
	print
