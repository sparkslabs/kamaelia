import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

authorize_addr = 'login.oscar.aol.com'
port = 5190

### ======== Login Stage I: Authorization ======= ###

def connectAuth():
"client connects to authorizer server"
    pass

def sndLogin():
    "client sends login request"
    pass

def getBOS():
    "server replies via BOS address/cookie"
    pass

def disconnect():
    "client disconnects from authorizer
    pass

connectAuth()
sndLogin()
getBOS()
disconnect()


###============ Login Stage 2: Protocol Negotiation ========== ###

def extractCookie():
    "client extracts BOS server/auth cookie from reply packet"
    return None

def connectBOS():
    "client connects to BOS"
    pass

def sndCookie():
    "client sends cookie via special FLAP channel 0x10 packet named cli_cookie"
    pass

def getServiceList():
    "server returns list of supported services via SNAC(01,03)
    return serviceList

def askServicesVersion():
    "client asks for services verion numbers via SNAC(01,17)"
    pass

def getServicesVersion():
    "server returns services version numbers via SNAC(01,18)"
    return servicesVersion

cookie = extractCookie()
connectBOS()
sndCookie()
serviceList = getServiceList()
askServicesVersion()
servicesVersion = getServicesVersion()


### ============ Services setup ================ ###
def askLocationServiceLimitations():
    "client asks for location service limitations"
    pass

def getLocationServiceLimitations():
    "get reply from server"
    return locationServiceLimitations

def sndCapabilities():
    "client sends capabilities/profile to server"
    pass

def askBLMServiceLimitations():
    "ask server"
    pass

def getBLMServiceLimitations():
    "server reply"
    return BLMServiceLimitations()

def askICBMServiceParameters():
    "ask server"
    pass

def getICBMServiceParameters():
    "server reply"
    return ICBMServiceParameters

def changeICBMParameters():
    "change default ICBM parameters"
    pass

def askPRMServiceLimitations():
    "ask server"
    pass

def getPRMServiceLimitations():
    "server reply"
    return PRMServiceLimitations

def askSSIServiceLimitations():
    "ask server"
    pass

def getSSIServiceLimitations():
    "server reply"
    return SSIServiceLimitations

def askSSIuptodate():
    "Client checks if its local SSI copy is up-to-date"
    pass

def getSSIuptodate():
    "Server tells client if its local copy up-to-date"
    return SSIuptodate

def activateSSIData():
    "Client activates server SSI data"
    pass

askLocationServiceLimitations()
getLocationServiceLimitations()
sndCapabilities()
askBLMServiceLimitations()
getBLMServiceLimitations()
askICBMServiceParameters()
getICBMServiceParameters()
changeICBMParameters()
askPRMServiceLimitations()
getPRMServiceLimitations()
askSSIServiceLimitations()
getSSIServiceLimitations()
askSSIuptodate()
getSSIuptodate()
activateSSIData()


### ================ Final Actions ================ ###
def sndDC():
    "set its DC information and status on main connection via SNAC(01,1E)"
    pass

def sndClientReady():
    "Login sequence finishes by client ready SNAC(01,02) which contain version/build numbers for protocol dlls."
    pass

sndDC()
sndClientReady()

