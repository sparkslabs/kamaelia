#!/usr/bin/env python
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""Direct python translation of the ffmpeg copies of the reference MPEG DCT
transform. Accepts & leaves results as floats not ints.
It's not fast, it's not big, and it's not clever.
"""

import math
sqrt = math.sqrt
cos = math.cos
sin = math.sin
floor = math.floor

class SimpleDCT:
	""" This class provides Simple DCT facilities to client classes. It does
	not attempt to do anything interesting or even attempt to limit itself to
	integers or anything sensible.
	"""
	M_PI = 3.14159265358979323846
	PI = M_PI
	coefficients = [[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0], 
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0], 
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0]]

	def __init__(self):
		i, j=(0,0)
		s = 0.0
		for i in range(0,8):
			if i==0:
				s = sqrt(0.125)
			else:
				s = 0.5
			for j in range(0,8):
				self.coefficients[i][j] = s * cos((self.PI/8.0)*i*(j+0.5))

	def fdct2(self,block):
		i, j = (0,0)
		s=0.0
		tmp = []
		for t in range(0,64):
			tmp.append(0.0)
		for i in range(0,8):
			for j in range(0,8):
				s = 0.0
				for k in range(0,8):
					s = s + (self.coefficients[j][k] * block[8 * i + k])
				tmp[8 * i + j] = s
		for j in range(0,8):
			for i in range(0,8):
				s = 0.0;
				for k in range(0,8):
					s = s + (self.coefficients[i][k] * tmp[8 * k + j] )
				block[8 * i + j] = s

	def idct2(self, block):
		"""perform IDCT matrix multiply for 8x8 coefficient block"""
		i, j, k, v = (0,0,0,0)
		partial_product = 0.0
		tmp = []
		for t in range(0,64): tmp.append(0.0)
		#
		for i in range(0,8):
			for j in range(0,8):
				partial_product = 0.0
				for k in range(0,8):
					partial_product = partial_product + (self.coefficients[k][j]*block[8*i+k])
				tmp[8*i+j] = partial_product

		"""Transpose operation is integrated into address mapping by switching
		"loop order of i and j"""
		for j in range(0,8):
			for i in range(0,8):
				partial_product = 0.0
				for k in range(0,8):
					partial_product = partial_product + (self.coefficients[k][i]*tmp[8*k+j])
				v = floor(partial_product+0.5)
				block[8*i+j] = partial_product

if __name__ =="__main__":
	import math

	def sine(freq=5,steps=64):
		l=[]
		pi=math.pi
		for i in range(0,steps):
			Q = math.floor((math.sin((2*pi) * (i*freq/float(steps))))*10000)/10000
			l.append(Q)
		return l

	def bar(arg,amplitude=30, delay=50000):
		for i in arg:
			print " "*(int(i * amplitude + amplitude + 3)),"=*###*="
			for j in range(0,delay): pass

	def quantise(block, start=0, end=0):
		"Highly Crappy quantisation"
		result = []
		l=len(block)
		s=(1.0-end)/(l-start)
		for i in range(0,start):
			result = result + [1]
		for i in range(start,len(block)):
			block[i] = block[i]*(1-(s*(i-start)))
			result = result + [1-(s*(i-start))]
		return result


"""
Sample usage:

quantise(W); quantise(W,end=0.5)

bar(foo(1),80); bar(foo(2),40); bar(foo(4),20); bar(foo(8),10); bar(foo(16),5)
W=foo(2) ; fdct2(W) ; quantise(W,start=8,end=0.1) ; idct2(W) ; bar(W,20)

#define M_PI 3.14159265358979323846
long b,k
double arg
for (bin = 0; bin < transformLength; bin ++) :
   transformData[bin] = 0.;
   for (k = 0; k < transformLength; k++) : 
      arg = (float) bin * M_PI * (float) k  / transformLength;
      transformData[bin] += inputData[k] * cos(arg);

"""
