#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: JMB

from Kamaelia.Chassis.Graphline import Graphline

from jabber.Interface import BoxBundle, XMPPInterface
from translator import messageToResponseTranslator, requestToMessageTranslator

def MasterInterface(DebugMemory=False):
    return Graphline(
        xmppi=XMPPInterface(DebugMemory=DebugMemory),
        mtr=messageToResponseTranslator(),
        rtm=requestToMessageTranslator(),
        
        linkages={
            #internal linkages
            ('xmppi', 'outbox') : ('rtm', 'inbox'),
            ('mtr', 'outbox') : ('xmppi', 'response'),
            
            #external linkages
            ('self', 'to_http') : ('mtr', 'inbox'),
            ('self', 'to_xmpp') : ('rtm', 'inbox'),
            ('self', 'receptor') : ('xmppi', 'inbox'),
                
            #signal/control
            ('self', 'control') : ('xmppi', 'control'),
            ('xmppi', 'signal') : ('mtr', 'control'),
            ('mtr', 'signal') : ('rtm', 'control'),
            ('rtm', 'signal') : ('self', 'signal'),
        }
    )
