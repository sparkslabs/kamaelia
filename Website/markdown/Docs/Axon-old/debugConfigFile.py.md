---
pagename: Docs/Axon-old/debugConfigFile.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[debugConfigFile.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

Reads and parses the debugging config file. Exports 1 function which is
expected to be used as follows:

<div>

[config = readConfig(\"debug.conf\")\
\
]{style="font-family:Courier 10 Pitch"}[for
]{style="font-family:Courier 10 Pitch;font-weight:600"}[tag
]{style="font-family:Courier 10 Pitch"}[in
]{style="font-family:Courier 10 Pitch;font-weight:600"}[config.keys():]{style="font-family:Courier 10 Pitch"}

</div>

Snippet from the debug.conf config file:

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

[FUNCTIONS]{style="font-weight:600"}

readConfig(filename)

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[TODO: ]{style="font-weight:600"}Implement test suite for Axon.debug.py
(We did mention that tests were added late in the project?)

[Sample Config file]{style="font-size:14pt;font-weight:600"}

[\#\
\# Component System Debug Configuration File\
\#\
\# Format is:\
\# Section level where\
\#\
\# The following tags are for debugging the debug system\
debugTestClass.even 0 default\
debugTestClass.triple 0 default\
debugTestClass.run 0 default\
debugTestClass.\_\_init\_\_ 0 default\
debugTestClass.randomChange 0 default\
\
\#\
\# Tags for debugging the microprocess underlying code\
\#\
microprocess.microprocess 0 default\
microprocess.\_\_str\_\_ 0 default\
microprocess.\_\_init\_\_ 0 default\
microprocess.setthread 0 default\
microprocess.\_isStopped 0 default\
microprocess.\_isRunnable 0 default\
microprocess.stop 0 default\
microprocess.pause 0 default\
microprocess.\_unpause 0 default\
microprocess.activate 0 default\
microprocess.main 0 default\
microprocess.\_unpause 0 default\
\
\#\
\# Tags for debugging the scheduler\
\#\
scheduler.scheduler 0 default\
scheduler.\_\_init\_\_ 0 default\
scheduler.\_addThread 0 default\
scheduler.main 0 default\
scheduler.main.threads 0 default\
scheduler.objecttrack 0 default\
scheduler.runThreads 0 default\
\
\#\
\# Tags for debugging the microthreading - not really relevant\
\#\
microthread.microthread 0 default\
microthread.\_\_init\_\_ 0 default\
microthread.activate 0 default\
\
\#\
\# Tags for debugging the postman\
\#\
postman.postman 0 default\
postman.main 0 default\
postman.\_\_init\_\_ 0 default\
postman.\_\_str\_\_ 0 default\
postman.register 0 default\
postman.registerlinkage 0 default\
postman.deregister 0 default\
postman.deregisterlinkage 0 default\
postman.showqueuelengths 0 default\
postman.findrecipient 0 default\
postman.domessagedelivery.linkages 0 default\
postman.domessagedelivery 0 default\
postman.specificTransits 0 default\
postman.messagedelivery.fail 0 default\
\
\#\
\# Tags for debugging the component subsystem\
\#\
component.component 0 default\
component.Component 0 default\
component.\_\_init\_\_ 0 default\
component.\_\_str\_\_ 0 default\
component.dataReady 0 default\
component.link 0 default\
component.recv 0 default\
component.send 0 default\
component.doSomething 0 default\
component.mainBody 0 default\
component.main 0 default\
component.addChildren 0 default\
component.removeChild 0 default\
component.childComponents 0 default\
component.initialiseComponent 0 default\
component.closeDownComponent 0 default\
component.\_collect 0 default\
component.\_deliver 0 default\
component.\_\_addChild 0 default]{style="font-family:Courier 10 Pitch"}

[\#\
\# Tags for debugging linkages\
\#\
linkage.linkage 0 default\
\#\
\#\
\#\
idGen.idGen 0 default\
idGen.numId 0 default\
idGen.strId 0 default\
idGen.tupleId 0 default\
\#\
\# ReadFileAdaptor debug tags\
\#\
ReadFileAdapter.main 0 default\
\#\
\# AudioCookieProtocol\
\#\
AudioCookieProtocol.initialiseComponent 0 default\
\#\
\# FortuneCookieProtocol\
\#\
FortuneCookieProtocol.main 0 default\
\#\
SimpleServer.checkOOBInfo 0 default\
SimpleServer.handleClosedCSA 0 default\
SimpleServer.handleNewCSA 0 default\
\#\
SimpleServerTestProtocol.\_\_init\_\_ 0 default\
SimpleServerTestProtocol.mainBody 0 default\
SimpleServerTestProtocol.closeDownComponent 0
default]{style="font-family:Courier 10 Pitch"}

[HTTPServer.initialiseComponent 0 default\
MimeRequestComponent.mainBody 0
default]{style="font-family:Courier 10 Pitch"}

[PrimaryListenSocket.makeTCPServerPort 0
default]{style="font-family:Courier 10 Pitch"}

[ConnectedSocketAdapter.handleDataReady 0 default\
ConnectedSocketAdapter.handleDataSend 0 default\
ConnectedSocketAdapter.mainBody 0
default]{style="font-family:Courier 10 Pitch"}

Michael, December 2004
