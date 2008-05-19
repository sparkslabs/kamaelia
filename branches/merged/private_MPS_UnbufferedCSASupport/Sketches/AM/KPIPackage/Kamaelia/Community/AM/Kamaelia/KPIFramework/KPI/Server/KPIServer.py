#!/usr/bin/env python
#
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
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
This Module consists of KPIServer and clientconnector 

How does it work ?
-------------------

There is one clientconnector per client connection. The clientconnector
is server side subsystem embeds authenticator, notifier to KeyManagement
backplane

KPIServer is server subsystems that has two back planes - keymanagement
and datamanagement. It encapsulates DataTx, SessionKeyController,
Encryptor, DataSink

Framework Description
When the client initiates a connection, 
1. The authenticatee and the authenticator perform a challenge response sequence 
2. If authentication is successful, the authenticator publishes the user-id to
   the Key Management backplane
3. On succesful authentication, the client connector also subscribes to the
   Data Management backplane and the authenticator and the authenticatee act
   as passthough components.
3. The session key controller subscribes to the Key management backplane and
   is thus aware of new client join events.
4. For each key change trigger, the session key controller generates a new
   session key and computes the common keys used to encrypt the session key
   with and sends the encrypted key packets to data transmitter.
5. The session key controller also passes the session key to the encryptor
   component so that data can be encrypted using it.
6. The encrypted data is also packetised by the data transmitter and
   published to the data management interface.
"""
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *

from Authenticator import Authenticator
from SessionKeyController import SessionKeyController
from DataTx import DataTx
from Encryptor import Encryptor
from Kamaelia.Community.AM.Kamaelia.KPIFramework.KPI.DB import KPIDBI

def clientconnector():
    """\   clientconnector() -> returns Graphline
    clientconnector is the peer to KPIClient
    Keyword arguments: None
    """ 
    return Graphline(
        authenticator = Authenticator(KPIDBI.getDB("mytree")),
        notifier = publishTo("KeyManagement"),
        linkages = {
            ("","inbox") : ("authenticator","inbox"),
            ("authenticator","outbox") : ("","outbox"),
            ("authenticator","notifyuser") : ("notifier","inbox"),
        }
    )



def KPIServer(datasource, kpidb):
    """\   KPIServer(datasource, kpidb) -> activates KPISever
    KPIServer is Session rekeying and Data transmission backend 
    Keyword arguments:
    - datasource -- any component with an outbox. the datasource
                    sends data to encryptor's inbox
    - kpidb    -- KPIDB instance for key lookup
    """    
    Backplane("DataManagement").activate()
    Backplane("KeyManagement").activate()
    Graphline(
        ds = datasource, 
        sc = SessionKeyController(kpidb),
        keyRx = subscribeTo("KeyManagement"),
        enc = Encryptor(),
        sender = publishTo("DataManagement"),
        pz = DataTx(),
        linkages = {
            ("ds","outbox") : ("enc","inbox"),
            ("keyRx","outbox") : ("sc","userevent"),        
            ("sc","notifykey") : ("enc","keyevent"),
            ("sc","outbox") : ("pz","keyIn"),   
            ("enc","outbox") : ("pz","inbox"),
            ("pz","outbox") : ("sender","inbox"),
        }
    ).activate()
