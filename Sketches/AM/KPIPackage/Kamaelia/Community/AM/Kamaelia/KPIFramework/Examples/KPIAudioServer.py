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
import Axon
from Kamaelia.Util.Graphline import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Server.KPIServer import *
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.Client.KPIClient import KPIClient
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI

from AudioLib import *


def MyAudioSource():
    return Graphline(
            src = AudioSource(100000),
            enc = AudioEncoder('mp3'),
            linkages = {
                ("src","outbox") : ("enc","inbox"),
                ("src","signal") : ("enc","control"),
                ("enc","outbox") : ("","outbox"),
                ("enc","signal") : ("","control")
            }
        )
 

kpidb = KPIDBI.getDB("mytree")
KPIServer(MyAudioSource(), kpidb.getKPIKeys())

import random
from Kamaelia.SimpleServerComponent import SimpleServer as _SimpleServer
from Kamaelia.Internet.TCPClient import TCPClient as _TCPClient
clientServerTestPort=1256
server=_SimpleServer(protocol=clientconnector, port=clientServerTestPort).activate()

from Axon.Scheduler import scheduler as _scheduler
_scheduler.run.runThreads(slowmo=0)

