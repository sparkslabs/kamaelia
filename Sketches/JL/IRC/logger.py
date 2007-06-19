#!/usr/bin/env python

from IRCClient import SimpleIRCClientPrefab
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer
           

def format(data):
    msgtype, sender, recipient, body = data
    end = '\n'
    if msgtype == 'PRIVMSG':
        text = '<%s> %s' % (sender, body)
    elif msgtype == 'JOIN' :
        text = '%s has joined %s' % (sender, recipient)
    elif msgtype == 'PART' :
        text = '%s has parted %s' % (sender, recipient)
    elif msgtype > '000' and msgtype < '400':
        text = 'Reply %s from %s to %s: %s' % data
    elif msgtype >= '400' and msgtype < '600':
        text = 'Error! %s %s %s %s' % data
    elif msgtype >= '600' and msgtype < '1000':
        text = 'Unknown numeric reply: %s %s %s %s' % data
    else:
        text = '%s from %s to %s: %s' % data
    return text + end

Pipeline(
    ConsoleReader(),
    SimpleIRCClientPrefab(host="irc.freenode.net", nick="kamaeliabot", defaultChannel="#kamtest"),
    PureTransformer(format),
    SimpleFileWriter("/home/jlei/irc/kamtest.log"),
).run()

