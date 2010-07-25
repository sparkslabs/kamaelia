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

"""Mail IPC messages"""
from Kamaelia.Community.RJL.Kamaelia.IPC.BaseIPC import IPC

# =================== Messages for sending an e-mail as a stream ====================
class MIPCNewMessageFrom(IPC):
    "Start of a new e-mail message from %{from}s"
    Parameters = ["fromemail"]
    
    #Parameters:
    #  fromemail - the e-mail address specified in MAIL FROM
    
class MIPCNewRecipient(IPC):
    Parameters = ["recipientemail"]
    
    #Parameters:
    #  recipientemail - the e-mail address of another recipient
    
class MIPCMessageBodyChunk(IPC):
    Parameters = ["data"]

    #Parameters:
    #  data - some bytes of the msg data
    
class MIPCCancelLastUnfinishedMessage(IPC):
    Parameters = []

class MIPCMessageComplete(IPC):
    Parameters = []
