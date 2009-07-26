#!/usr/bin/python

from Axon.Ipc import WaitComplete
from Kamaelia.Apps.Europython09.BB.Exceptions import GotShutdownMessage
from Kamaelia.Apps.Europython09.BB.RequestResponseComponent import RequestResponseComponent

class Authenticator(RequestResponseComponent):
    users = {}
    State = {}
    def main(self):
        loggedin = False
        try:
            self.netPrint("")
            while not loggedin:
                self.send("login: ", "outbox")
                yield self.waitMsg()
                username = self.getMsg()[:-2] # strip \r\n

                self.send("password: ", "outbox")
                yield self.waitMsg()
                password= self.getMsg()[:-2] # strip \r\n

                self.netPrint("")
                if self.users.get(username.lower(), None) == password:
                    self.netPrint("Login Successful")
                    loggedin = True
                else:
                    self.netPrint("Login Failed!")

        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")

        if loggedin:
            self.State["remoteuser"] = username
