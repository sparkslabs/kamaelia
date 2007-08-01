
from IRCIPC import *
from Axon.Component import component

class Interface(component):
    #standard inboxes and outboxes
    def __init__(self):
        super(Interface, self).__init__()
        self.defaultChannel = '#kamtest'

    def main(self):
        while 1:
            yield 1
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                tokens = data.split()
                head = tokens[0].lower()
                
                if head == '/nick':
                    toSend = IRCIPCChangeNick(nick = tokens[1])
                elif head == '/quit':
                    toSend = IRCIPCDisconnect()
                #IRCIPCConnect
                #IRCIPCLogin
                elif head == '/join':
                    toSend = IRCIPCJoinChannel(channel = tokens[1])
                elif head == '/part':
                    toSend = IRCIPCLeaveChannel(channel = tokens[1])
                elif head == '/topic':
                    toSend = IRCIPCSetChannelTopic(channel = tokens[1], topic = tokens[2])
                else:
                    toSend = IRCIPCSendMessage(recipient = self.defaultChannel, msg = data)
                self.send(toSend)


if __name__ == '__main__':
    print "running"
    from ryans_irc_client import *
    from Kamaelia.Internet.TCPClient import TCPClient
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    host = 'irc.freenode.net'
    port = 6667
    nick = 'ryans_irc_client'
    pwd = ''
    user = 'jinna'

    Graphline(irc = IRCClient(host, port, nick, pwd, user),
              tcp = TCPClient(host, port),
              interface = Interface(),
              inputter = ConsoleReader(),
              out = ConsoleEchoer(),
              linkages = {
                  ("inputter", "outbox") : ("interface", "inbox"),
                  ("inputter", "signal") : ("interface", "control"),
                  ("interface", "outbox") : ("irc", "ipcObjects"),
                  ("interface", "signal") : ("irc", "control"),
                  ("irc", "outbox") : ("tcp", "inbox"),
                  ("irc", "signal") : ("tcp", "control"),
                  ("tcp", "outbox") : ("irc", "inbox"),
                  ("tcp", "signal") : ("irc", "control"),
                  ("irc", "heard") : ("out", "inbox")
                  }
              ).run()
