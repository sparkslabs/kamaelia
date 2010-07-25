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
# -------------------------------------------------------------------------

import datetime
import time
import re

def parseInt(string):
    HEX = re.compile("^\s*0x[0-9a-f]+\s*$", re.I)
    DEC = re.compile("^\s*\d+\s*$", re.I)
        
    if re.match(DEC,string):
        return int(string, 10)
    elif re.match(HEX,string):
        return int(string, 16)
    else:
        return int(string)

def parseList(string):
    CAR_CDR = re.compile(r"^\s*(\S+)(\s+.*)?$")
    tail = string.strip()
    theList = []
    
    while tail:
        match = re.match(CAR_CDR, tail)
        theList.append(match.group(1))
        tail = match.group(2)
        
    return theList

def parseISOdateTime(isoDateTime):
    return datetime.datetime(*time.strptime(isoDateTime,"%Y-%m-%dT%H:%M:%S")[0:6])
