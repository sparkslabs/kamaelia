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
"""\
Date and time parsing for DVB PSI tables
"""
raise NotImplementedError("Due to drift/bit rot, DVB libraries need updating")

def parseMJD(MJD):
    """Parse 16 bit unsigned int containing Modified Julian Date, as per DVB-SI spec
    returning year,month,day"""
    YY = int( (MJD - 15078.2) / 365.25 )
    MM = int( (MJD - 14956.1 - int(YY*365.25) ) / 30.6001 )
    D  = MJD - 14956 - int(YY*365.25) - int(MM * 30.6001)
    
    K=0
    if MM == 14 or MM == 15:
        K=1
    
    return (1900 + YY+K), (MM-1-K*12), D


def unBCD(byte):
    return (byte>>4)*10 + (byte & 0xf)
