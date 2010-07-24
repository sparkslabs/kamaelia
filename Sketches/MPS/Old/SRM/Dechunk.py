#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Algorithm tester/experiment
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


import random

def datasource():
    r = random.randrange(50,100)
    while 1:
        yield "XXXXXXXXXXXXXXXXXXXXXXX"
        for i in xrange(r):
            yield str(i)
        r = random.randrange(50,100)
      
def consumer(datasource, divider="XXXXXXXXXXXXXXXXXXXXXXX"):
    buffer = ''
    foundFirstChunk = 0
    for i in datasource:
        buffer += i
        location = buffer.find(divider,len(divider))
        if location != -1:
            if foundFirstChunk:
                chunk = buffer[:location]
                print "CHUNK", chunk
            buffer = buffer[location:]
            foundFirstChunk = 1

consumer(datasource(), "XXXXXXXXXXXXXXXXXXXXXXX")
