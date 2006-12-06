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
====================================
KPI Server that transmits text data
====================================

How does it work?
-----------------
The KPITextServer listens on a TCP port, authenticates users and upon
successful authenticates encrypts and streams the text data provided
MyDataSink
"""

import Axon
from Kamaelia.Util.Graphline import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Server.KPIServer import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Client.KPIClient import KPIClient
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI


from Kamaelia.SimpleServerComponent import SimpleServer as _SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
from Axon.Scheduler import scheduler as _scheduler

class MyDataSource(Axon.Component.component):
    """ A text streaming source that generates sequence
    of numbered hello strings
    """    
    def main(self):
        index = 0
        while 1:
            yield 1
            if index % 1000 == 0:
                data = str(index) + "-helloknr"
                self.send(data, "outbox")
                print "data source sent", data
            else:
                yield 1
            index = index + 1


import sys
if __name__=="__main__":
    if len(sys.argv) != 3:
        print "Usage:", sys.argv[0], "dbfile port"
        print "default values used: dbfile=mytree and port=1256"
        dbfile = "mytree"
        tcpport = 1256
    else:
        dbfile = sys.argv[1]
        tcpport = int(sys.argv[2])
        

    kpidb = KPIDBI.getDB(dbfile)
    KPIServer(MyDataSource(), kpidb.getKPIKeys())    
    server=_SimpleServer(protocol=clientconnector, port=tcpport).activate()
    _scheduler.run.runThreads(slowmo=0)
