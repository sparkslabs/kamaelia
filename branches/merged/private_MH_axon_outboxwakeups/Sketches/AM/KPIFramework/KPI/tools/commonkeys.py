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

from KPI.DB import btree
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage:", sys.argv[0], "dbfile [id1] [id2].."
        sys.exit(1)
    dbfile = sys.argv[1]
    info = btree.getInfo(dbfile)

    #validate all the user ids
    ids = []
    for index in range(2, len(sys.argv)):
        userid = long(sys.argv[index])
        if((userid < info.min_user_id)  or
           (userid > info.max_user_id - 1)):
            print "userid", sys.argv[index], "is invalid"
            sys.exit(1)
        ids.append(userid)


    idkeymap = btree.getCommonKeys(dbfile, ids)
    for ID in idkeymap:
        print "ID=",ID, ",KEY=", idkeymap[ID]
