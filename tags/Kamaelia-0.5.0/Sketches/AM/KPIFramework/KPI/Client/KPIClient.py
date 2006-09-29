from Kamaelia.Util.Graphline import *
from KPI.Client.Authenticatee import Authenticatee
from KPI.Client.Decryptor import Decryptor
from KPI.DB.KPIUser import KPIUser

#client side
def KPIClient(config, datasink):
    authenticatee = Authenticatee(KPIUser(configfile=config))
    Graphline(
        authee = authenticatee,
        dec = Decryptor(),
        ds = datasink,
        linkages = {
            ("authee","encout") : ("dec","inbox"),
            ("authee","notifykey") : ("dec","keyevent"),
            ("dec", "outbox") : ("ds","inbox"),
        }
    ).activate()
    return authenticatee
