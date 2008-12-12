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

from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Support.Protocol.HTTP import HTTPProtocol
from Kamaelia.Support.Protocol.HTTP import ReqTranslatorFactory
from Kamaelia.Support.Protocol.HTTP import WSGILikeTranslator
from Kamaelia.Protocol.HTTP.Handlers.Minimal import Minimal

from Kamaelia.Apps.Publish.Gateway.translator import Translator

import socket

def constructHTTPServer(Config):
    class StaticServer(Minimal):
        indexfilename=Config.static.index
        homedirectory=Config.static.homedirectory
        def __init__(self, request):
            super(StaticServer, self).__init__(request)
    
    routing = [[Config.static.url, StaticServer],
               #FIXME:one of the translators will have to change its name
               ['/', ReqTranslatorFactory(Translator, WSGILikeTranslator)]]
    return ServerCore(
        protocol=HTTPProtocol(routing),
        port = 8080,
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
    )
