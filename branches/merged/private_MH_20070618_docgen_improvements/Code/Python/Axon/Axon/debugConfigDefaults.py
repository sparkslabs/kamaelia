#!/usr/bin/env python2.3
#
# (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
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
===============================
Default debugging configuration
===============================

This file defines default configuration used by Axon.debug.debug when it cannot
find a configuration file to load.

The defaultConfig() method returns the default configuration.
"""

_tags = """debugTestClass.even
debugTestClass.triple
debugTestClass.run
debugTestClass.__init__
debugTestClass.randomChange
microprocess.microprocess
microprocess.__str__
microprocess.__init__
microprocess.setthread
microprocess._isStopped
microprocess._isRunnable
microprocess.stop
microprocess.pause
microprocess._unpause
microprocess.activate
microprocess.main
microprocess._unpause
scheduler.scheduler
scheduler.__init__
scheduler._addThread
scheduler.main
scheduler.main.threads
scheduler.objecttrack
scheduler.runThreads
microthread.microthread
microthread.__init__
microthread.activate
postman.postman
postman.main
postman.__init__
postman.__str__
postman.register
postman.registerlinkage
postman.deregister
postman.deregisterlinkage
postman.showqueuelengths
postman.findrecipient
postman.domessagedelivery.linkages
postman.domessagedelivery
postman.specificTransits
postman.messagedelivery.fail
component.component
component.Component
component.__init__
component.__str__
component.dataReady
component.link
component.recv
component.send
component.doSomething
component.mainBody
component.main
component.addChildren
component.removeChild
component.childComponents
component.initialiseComponent
component.closeDownComponent
component._collect
component._deliver
component.__addChild
linkage.linkage
idGen.idGen
idGen.numId
idGen.strId
idGen.tupleId
ReadFileAdapter.main
AudioCookieProtocol.initialiseComponent
FortuneCookieProtocol.main
SimpleServer.checkOOBInfo
SimpleServer.handleClosedCSA
SimpleServer.handleNewCSA
SimpleServerTestProtocol.__init__
SimpleServerTestProtocol.mainBody
SimpleServerTestProtocol.closeDownComponent
HTTPServer.initialiseComponent
MimeRequestComponent.mainBody
PrimaryListenSocket.makeTCPServerPort
ConnectedSocketAdapter.handleDataReady
ConnectedSocketAdapter.handleDataSend
ConnectedSocketAdapter.mainBody
"""

def defaultConfig():
   """\
   Returns a default debugging configuration - a dictionary mapping section
   names to (level, location) tuples
   """
   debugConfig = {}
   for tag in _tags.split("\n"):
      debugConfig[tag] = (0,"default")
   return debugConfig


if __name__=="__main__":
   import pprint
   config = defaultConfig()
   pprint.pprint(config)
