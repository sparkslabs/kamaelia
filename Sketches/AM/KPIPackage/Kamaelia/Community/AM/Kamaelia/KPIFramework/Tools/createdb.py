#!/usr/bin/env python
#
# (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
#

"""
A commandline tool that creates the Logical key hierachy DB
"""

from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import LKH
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage:", sys.argv[0], "dbfile keylength numusers"
        sys.exit(1)
    dbfile = sys.argv[1]
    keylen = long(sys.argv[2])
    numusers = long(sys.argv[3])
    if numusers < 1 :
        print "numusers", sys.argv[3], "is invalid\n"
        sys.exit(1)
    LKH.createDB(dbfile, keylen, numusers)
