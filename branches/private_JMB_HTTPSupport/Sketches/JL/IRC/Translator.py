from Axon.Component import component

class Translator(component):
    Inboxes = {"inbox" : " standard inbox",
               "control": "shutdown messages"}

    Outboxes = {"outbox": "",
                "signal" : ""}

    def __init__(self, nick):
        super(Translator, self).__init__()
        self.nick = nick

    def main(self):
        while 1:
            if not self.anyReady():
                self.pause()
            yield 1
            data = ""
            if self.dataReady('privmsg'):
                formatted = self.formatPrivmsg(self.recv('privmsg'))
                self.send(formatted)
            if self.dataReady('channel'):
                formatted = self.formatChannelMsg(self.recv('channel'))
                self.send(formatted)
            if self.dataReady('nonPrivmsg'):
                formatted = self.formatMisc(self.recv('channel'))
                self.send(formatted)
            if self.dataReady('notice'):
                formatted = self.formatNotice(self.recv('notice'))
                self.send(formatted)
            if self.dataReady('ERR'):
                formatted = self.formatError(self.recv('ERR'))
                self.send(formatted)
            if self.dataReady('RPL'):
                formatted = self.formatNumReply(self.recv('RPL'))
                self.send(formatted)

    def formatPrivmsg(self, msg):
        temp, sender, recipient, body = msg
        if body[0] == 'ACTION':
            send = "*** %s %s" % (sender, body[body.find('ACTION') + 7])
        else:
            send = "%s: %s" % (sender, body)
        return send
    
    def formatChannelMsg(self, msg):
        return msg

    def formatMisc(self, msg):
        return msg

    def formatNotice(self, msg):
        return msg

    def formatError(self, msg):
        return msg

    def formatNumReply(self, msg):
        return msg

if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Prefab import ComplexIRCClientPrefab
    
    client = Graphline(
        prefab = ComplexIRCClientPrefab(host="irc.freenode.net", nick="kamaeliabot", defaultChannel="#kamtest"),
        formatter = Translator("kamaeliabot"),
        linkages = {("prefab", "outbox") : ("formatter", "privmsg")}
        )
    
    Pipeline(ConsoleReader(), client, ConsoleEchoer()).run()
    
