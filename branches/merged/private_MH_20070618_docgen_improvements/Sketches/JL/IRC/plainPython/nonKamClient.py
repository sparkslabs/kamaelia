#! /usr/bin/env python
 
#short IRC client to log on, send some commands, and log off

import time
import socket

network = "irc.freenode.net"
port = 6667
nick = "excelllent"
uname = "nonKamClient"
host = "home"
server = "home1"
realname = "jlei"
channel = '#kamtest'
BUFFER = 8000 #new

##def makecommand(tag):
##    def commandify(*body):
##        head = tag
##        for token in body:
##            head += ' ' + token
##        return head + ' \r\n'
##    return commandify
##
##say = makecommand('PRIVMSG') #need stricter parameters (channel, msg)
##join = makecommand('JOIN')  
##nick = makecommand('NICK')
##
##def say(channel, words):
##    makecommand('PRIVMSG')(channel, words)
###how redundant. I can see why Ryan turned to parameter lists
##
##
##def makecommand(tag, params):
##    if len(params) is 0:
##        params = ("arg",)
##    def commandify(*body):
##        if len(params) is not len(body):
##            raise tag + ": wrong number of parameters. " + str(body) + ' vs. ' + str(params)
##        head = tag
##        for token in body:
##            head += ' ' + token
##        return head + ' \r\n'
##    return commandify
##
##say = makecommand('PRIVMSG', ('channel', 'text'))

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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((network, port))

def say(chan, text): #new
    client.send(commandify('PRIVMSG', chan, text))

def flushOutput(): #new
    print client.recv(BUFFER)

    
nick_str = commandify('NICK', nick)
client.send(nick_str)
uname, host, server, realname = attachColon(uname, host, server, realname)
client.send(commandify('USER', uname, host, server, realname)) # changed
time.sleep(0.5)
flushOutput() #new
client.send(commandify('JOIN', channel))
say(channel, 'stuff')
print client.recv(8000)
client.send(commandify('QUIT'))
print client.recv(8000)
client.close()
