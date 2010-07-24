#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
