from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Graphline import *

from KPI.Server.Authenticator import Authenticator
from KPI.Server.SessionKeyController import SessionKeyController
from KPI.Server.DataTx import DataTx
from KPI.Server.Encryptor import Encryptor

#server side client connector
def clientconnector(kpidb):
    authenticator = Authenticator(kpidb)
    Graphline(
        author = authenticator,
        notifier = publishTo("KeyManagement"),
        linkages = {
            ("author","notifyuser") : ("notifier","inbox"),
        }
    ).activate()
    return authenticator    


#KPI Session management and streaming backend
def KPIServer(datasource, kpidb):
    Backplane("DataManagement").activate()
    Backplane("KeyManagement").activate()
    Graphline(
        ds = datasource, 
        sc = SessionKeyController(kpidb),
        keyRx = subscribeTo("KeyManagement"),
        enc = Encryptor(),
        sender = publishTo("DataManagement"),
        pz = DataTx(),
        linkages = {
            ("ds","outbox") : ("enc","inbox"),
            ("keyRx","outbox") : ("sc","userevent"),        
            ("sc","notifykey") : ("enc","keyevent"),
            ("sc","outbox") : ("pz","keyIn"),   
            ("enc","outbox") : ("pz","inbox"),
            ("pz","outbox") : ("sender","inbox"),
        }
    ).activate()
