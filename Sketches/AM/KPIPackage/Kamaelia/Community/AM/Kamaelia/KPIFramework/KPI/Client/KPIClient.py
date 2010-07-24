#!/usr/bin/env python2.3
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
