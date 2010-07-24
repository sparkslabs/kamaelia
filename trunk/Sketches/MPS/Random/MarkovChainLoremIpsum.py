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

import pprint
import random

f = open("pandp12.txt","r")
lines = []
for line in f:
    lines.append(line)

f.close()

s = "".join(lines)
s.lower()    

s = s.replace("\r","")
s = s.replace("\n"," ")

followset = {

}

chain = 1

current = [x for x in " "+s[:chain]]
# print current

for i in s[chain:]:
    try:
        followset[tuple(current)].append(i)
    except KeyError:
        followset[tuple(current)] = [ i ]
    current = current[1:]
    current.append(i)

word_starts = [ x for x in followset.keys() if x[0] == " "]

X = list(random.choice(word_starts))

R = []
spaces = 0
lines = 0
linelen = 0
while lines<100:
    linelen += 1
    R.append(X[0])
    try:
        FS = followset[tuple(X)]
    except KeyError:
        Y = [x for x in "".join(X).replace("\n"," ")]
        FS = followset[tuple(Y)]
        
    next = random.choice(FS)
    if next == " ":
        spaces +=1
        if spaces > 14:
            if linelen > 60:
#                print ">>>>>>>>>>>>>>", linelen
                next = "\n"
                lines +=1
                spaces = 0
                linelen = 0
    X = X[1:]+[next]

#    X = (X[1], X[2], X[3], next)
    

print "".join(R[1:])

# print repr("".join(R[1:]))

