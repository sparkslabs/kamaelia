#!/usr/bin/python

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
   debugConfig = {}
   for tag in _tags.split("\n"):
      debugConfig[tag] = (0,"default")
   return debugConfig


if __name__=="__main__":
   import pprint
   config = defaultConfig()
   pprint.pprint(config)
