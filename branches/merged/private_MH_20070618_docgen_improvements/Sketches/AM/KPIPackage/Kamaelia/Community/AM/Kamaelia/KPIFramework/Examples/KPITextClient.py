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
KPI Client that recieves and prints text data
====================================

How does it work?
-----------------
The KPITextClient establishes TCP connection with the
KPITextServer. Upon successful authentication,
receives session key and uses session key decrypt the
encrypted stream. The decrypted stream is printed by
MyDataSink component
"""

import Axon
from Kamaelia.Util.Graphline import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Server.KPIServer import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Client.KPIClient import KPIClient
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient

#from Kamaelia.Util.ConsoleEcho import consoleEchoer


class MyDataSink(Axon.Component.component):
    """ prints received text
    """     
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                print "datasink received:", self.recv("inbox")

import sys
if __name__=="__main__":
    if len(sys.argv) != 4:
        print "Usage:", sys.argv[0], "kpiserver port usercfg"
        print "default values used: kpiserver=localhost, port=1256 and usercfg = user3"
        server = "localhost"
        port = 1256
        usercfg = "user3"
    else:
        server = sys.argv[1]
        port = int(sys.argv[2])
        usercfg = sys.argv[3]

    Graphline(
        #c=KPIClient(usercfg, consoleEchoer()),
        c=KPIClient(usercfg, MyDataSink()),
        cc = _TCPClient(server,port),
        linkages = {
            ("c","outbox") : ("cc","inbox"),
            ("cc","outbox") : ("c","inbox"),
        }
    ).run()
