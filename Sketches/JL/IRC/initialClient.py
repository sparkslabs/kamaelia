#! /usr/bin/env python

#initial client
import time
import socket

def commandify(head, *body):
    for token in body:
        head += ' ' + token
    return head + ' \r\n'

def attachColon(*aTuple):
    result = list()
    for entry in aTuple:
        if ' ' in entry:
            result.append(':'+entry)
        else:
            result.append(entry)
    return tuple(result)

class ircClient:
    
    def __init__(self, nick,
                 uname = 'anonymous',
                 host='none',
                 server='none',
                 realname='Python IRC Client',
                 ircNetwork='irc.freenode.net',
                 bufsize = 8000,
                 port=6667):
        self.nick = nick
        self.uname = uname
        self.host = host
        self.server = server
        self.realname = realname
        self.ircNetwork = ircNetwork
        self.bufsize = bufsize
        self.port = port
        self.sock = self.connect()
        self.connectToNetwork()
        
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((self.ircNetwork, self.port))
        return sock

    def connectToNetwork(self):
        sock = self.sock
        sock.send(commandify('NICK', self.nick))
        uname_, host_, server_, realname_ = attachColon(self.uname, self.host, self.server, self.realname)
        sock.send(commandify('USER', uname_, host_, server_, realname_))
        time.sleep(1.0)
        self.flushOutput()
        
##    def mainLoop(self):
##        print
##        eval(read()))
##        self.mainLoop()
        
    def say(self, chan, text):
        self.sock.send(commandify('PRIVMSG', chan, text))

    def flushOutput(self): #new
        print self.sock.recv(self.bufsize)

    def join(self, chan):
        self.sock.send(commandify('JOIN', chan))

if __name__ == '__main__':
    nick = 'jollyolst'
    cli = ircClient(nick, realname='user', bufsize = 4000)
    channel = '#kamtest'
    cli.join(channel)
    cli.say(channel, 'hello, I am a python client')
    cli.sock.close()
