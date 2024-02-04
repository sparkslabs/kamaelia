---
pagename: Docs/BaseModules
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Base Modules]{style="font-size: 24pt; font-weight: 600;"}
==========================================================

[Kamaelia.Exceptions](/Components/pydoc/Kamaelia.Exceptions) contains a
number of exceptions covering different potential failure points in the
modules. These exceptions generally inherit from
[Axon.AxonExceptions.AxonException](/Docs/Axon/Axon.AxonExceptions.AxonException)

[Kamaelia.BaseIPC](/Components/pydoc/Kamaelia.BaseIPC) however defines
some specific payloads for intercomponent communication. These are
generally control messages used by various Internet Adaption components
for signalling various events - normally relating to new or closed
socket events. The IPC messages inherit from [Axon.IPC]{style=""}, and
are mainly notify events. Currently the only [producerFinished
]{style=""}class is [socketShutdown ]{style=""}- issued by Internet
Abstraction Modules.

\-- Michael, December 2004, updated by Matt, April 2007\
