---
pagename: Sandbox/NewFile
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
\

Sandbox
=======

>     from Kamaelia.Device.DVB.Parse.ReassemblePSITables import ReassemblePSITablesService
>
>     RegisterService( \
>
>          Graphline( PSI     = ReassemblePSITablesService(),
>
>                     DEMUXER = ToService("DEMUXER"),
>
>                     linkages = {
>
>                         ("PSI", "pid_request") : ("DEMUXER", "inbox"),
>
>                         ("",    "request")     : ("PSI",     "request"),
>
>                     }
>
>                   ),
>
>          {"PSI_Tables":"request"}
>
>     ).activate()

\
