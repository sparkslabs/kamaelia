#!/usr/bin/env python

from IRCClient import SimpleIRCClientPrefab
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer
           

def makeformatter(nick, channel): #the nick argument is useless
    def format(data):
        msgtype, sender, recipient, body = data
        end = '\n'
        if msgtype == 'PRIVMSG':
            if body[0:5] == '[off]': #we don't want to log lines prefixed by "[off]"
                return
            text = '<%s> %s' % (sender, body)
        elif msgtype == 'JOIN' :
            text = '*** %s has joined %s' % (sender, recipient)
        elif msgtype == 'PART' :
            text = '*** %s has parted %s' % (sender, recipient)
        elif msgtype == 'NICK':
            text = '*** %s is now known as %s' % (sender, recipient)
        elif msgtype == 'ACTION':
            text = '*** %s %s' % (sender, body)
        elif msgtype == 'TOPIC':
            text = '*** %s changed the topic to %s' % (sender, body)
        elif msgtype > '000' and msgtype < '400':
            text = 'Reply %s from %s to %s: %s' % data
        elif msgtype >= '400' and msgtype < '600':
            text = 'Error! %s %s %s %s' % data
        elif msgtype >= '600' and msgtype < '1000':
            text = 'Unknown numeric reply: %s %s %s %s' % data
        else:
            text = '%s from %s: %s' % (msgtype, sender, body)

        if recipient != channel:
            text = "Private message - %s" % text
        return text + end
    return format

Pipeline(
    ConsoleReader(),
    SimpleIRCClientPrefab(host="irc.freenode.net", nick="jinnaslogbot", defaultChannel="#kamtest"),
    PureTransformer(makeformatter("jinnaslogbot", "#kamtest")),
    SimpleFileWriter("/home/jlei/irc/kamtest.log"),
).run()
