#!/usr/bin/env python
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
