#!/usr/bin/env python

# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""\
Date and time parsing for DVB PSI tables
"""

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
