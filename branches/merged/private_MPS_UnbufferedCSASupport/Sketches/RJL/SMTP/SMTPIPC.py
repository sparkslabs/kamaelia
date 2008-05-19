#!/usr/bin/env python
#
# Copyright (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
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
