"""
Pseudocode

One module per service
each module has a __version__, __dllversion__
At startup, when client is negotiating service versions:
    for module in services:
        snac.append(module.__version__)

Each module asks for its own limitations.
self.askRights()
self.getRights()
Each handles the SNACs coming to itself.

Will need a router to route messages coming from OSCARClient.
Will need a router to route incoming messages from the user.
"""
services = [1, 4, 0x17]
modules = []
for service in services:
    modname = "family%02x" % service
    exec("import " + modname)
    modules.append(sys.modules.get(modname))
    
class ControlTower(adaptivecommscomponent):
    def main(self):
        for goal in self.getCookie(): yield goal
        for rates in self.getRates(goal): yield rates
        self.initServices(rates): yield 1
        yield WaitComplete(self.activateConnection())
        
        while not self.shutdown():
            while self.dataReady():
                data = self.recv()
                if data[0] == 1:
                    self.sendComponent(data[1], self.family01)
                elif data[0] == 2:
                    self.routeSnacs(data[1])
                elif data[0] == 3:
                    raise "uh oh, FLAP error " + str(data)
                elif data[0] == 4:
                    print "Terminated!"
                elif data[0] == 5:
                    print "Are we supposed to be RECEIVING keepalives?"

    def getCookie(self):
        self.connect('login.oscar.aol.com', 5190)
        family17 = Family17.Service().activate()
        self.linkUp(family17)
        for goal in self.waitComponent(family17): yield goal
        self.disconnect()
        self.destroy(family17)

    def getRates(self, (server, port, cookie)):
        self.connect(server, port)
        self.family01 = Family01.Service().activate()
        self.linkUp(self.family01)
        for rates in self.waitComponent(family01): yield 1

    def initServices(self, rates):
        partitionRates()
        for mod in modules:
            if mod.__name__[-2:] not in ('01', '17'):
                self.activeServices[mod.__name__] = mod.Service().activate()
                
    def activateConnection(self):
        self.wait_for_all_services_to_say_ready()
        self.sendComponent("send ready", self.family01)
        
    def routeSnacs(self, data):
        header, body = readSNAC(data)
        self.sendFamily(data, header[0])

