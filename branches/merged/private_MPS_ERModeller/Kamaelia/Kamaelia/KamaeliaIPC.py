#!/usr/bin/env python

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
"""\
This is a deprecation stub, due for later removal.
"""

import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.IPC import producerFinished as __producerFinished
from Kamaelia.IPC import notify as __notify
from Kamaelia.IPC import socketShutdown as __socketShutdown
from Kamaelia.IPC import newCSA as __newCSA
from Kamaelia.IPC import shutdownCSA as __shutdownCSA
from Kamaelia.IPC import newServer as __newServer
from Kamaelia.IPC import newWriter as __newWriter
from Kamaelia.IPC import newReader as __newReader
from Kamaelia.IPC import newExceptional as __newExceptional
from Kamaelia.IPC import removeReader as __removeReader
from Kamaelia.IPC import removeWriter as __removeWriter
from Kamaelia.IPC import removeExceptional as __removeExceptional

Deprecate.deprecationWarning("Use Kamaelia.IPC instead of Kamaelia.KamaeliaIPC")

producerFinished = Deprecate.makeClassStub(
    __producerFinished,
    "Use Kamaelia.IPC:producerFinished instead of KamaeliaIPC:producerFinished",
    "WARN"
    )

notify = Deprecate.makeClassStub(
    __notify,
    "Use Kamaelia.IPC:notify instead of Kamaelia.KamaeliaIPC:notify",
    "WARN"
    )

socketShutdown = Deprecate.makeClassStub(
    __socketShutdown,
    "Use Kamaelia.IPC:socketShutdown instead of Kamaelia.KamaeliaIPC:socketShutdown",
    "WARN"
    )

newCSA = Deprecate.makeClassStub(
    __newCSA,
    "Use Kamaelia.IPC: instead of Kamaelia.KamaeliaIPC:newCSA",
    "WARN"
    )

shutdownCSA = Deprecate.makeClassStub(
    __shutdownCSA,
    "Use Kamaelia.IPC:shutdownCSA instead of Kamaelia.KamaeliaIPC:shutdownCSA",
    "WARN"
    )

newServer = Deprecate.makeClassStub(
    __newServer,
    "Use Kamaelia.IPC:newServer instead of Kamaelia.KamaeliaIPC:newServer",
    "WARN"
    )
newWriter = Deprecate.makeClassStub(
    __newWriter,
    "Use Kamaelia.IPC:newWriter instead of Kamaelia.KamaeliaIPC:newWriter",
    "WARN"
    )
newReader = Deprecate.makeClassStub(
    __newReader,
    "Use Kamaelia.IPC:newReader instead of Kamaelia.KamaeliaIPC:newReader",
    "WARN"
    )
newExceptional = Deprecate.makeClassStub(
    __newExceptional,
    "Use Kamaelia.IPC:newExceptional instead of Kamaelia.KamaeliaIPC:newExceptional",
    "WARN"
    )
removeReader = Deprecate.makeClassStub(
    __removeReader,
    "Use Kamaelia.IPC:removeReader instead of Kamaelia.KamaeliaIPC:removeReader",
    "WARN"
    )

removeWriter = Deprecate.makeClassStub(
    __removeWriter,
    "Use Kamaelia.IPC:removeWriter instead of Kamaelia.KamaeliaIPC:removeWriter",
    "WARN"
    )
removeExceptional = Deprecate.makeClassStub(
    __removeExceptional,
    "Use Kamaelia.IPC:removeExceptional instead of Kamaelia.KamaeliaIPC:removeExceptional",
    "WARN"
    )

removeExceptional = Deprecate.makeClassStub(
    __removeExceptional,
    "Use Kamaelia.IPC:removeExceptional instead of Kamaelia.KamaeliaIPC:removeExceptional",
    "WARN"
    )
