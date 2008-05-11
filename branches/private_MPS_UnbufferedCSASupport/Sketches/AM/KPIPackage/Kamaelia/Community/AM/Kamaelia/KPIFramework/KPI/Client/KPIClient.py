#!/usr/bin/env python2.3
#
# Copyright (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
"""
====================
KPIClient
====================

KPIClient is client subsystem that encapsulates Authenticatee, Decryptor
and DataSink into a graphline component
"""

from Kamaelia.Util.Graphline import *
from Authenticatee import Authenticatee
from Decryptor import Decryptor
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB.KPIUser import KPIUser

def KPIClient(config, datasink):
    """\   KPIClient(config, datasink) -> returns a Graphline
    KPIClient handles authentication and decryption
    Keyword arguments:
    - config    -- uses KPIUser instance for looking up user
                    key from client config file
    - datasink    -- any component with an inbox. the KPIClient sends
        decrypted data to datasink's inbox
    """      
    return Graphline(
        authenticatee = Authenticatee(KPIUser(configfile=config)),
        dec = Decryptor(),
        ds = datasink,
        linkages = {
            ("","inbox") : ("authenticatee","inbox"),
            ("authenticatee","outbox") : ("","outbox"),
            ("authenticatee","encout") : ("dec","inbox"),
            ("authenticatee","notifykey") : ("dec","keyevent"),
            ("dec", "outbox") : ("ds","inbox"),
        }
    )
