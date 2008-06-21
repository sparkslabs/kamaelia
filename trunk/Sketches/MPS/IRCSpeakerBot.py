#!/usr/bin/python

import time
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer

from Kamaelia.Support.Protocol.IRC import informat, outformat
from Kamaelia.Protocol.IRC.IRCClient import SimpleIRCClientPrefab
from Kamaelia.Util.PureTransformer import PureTransformer

from Kamaelia.File.UnixProcess import UnixProcess
from Kamaelia.Util.Backplane import *


class IRCLogin(Axon.ThreadedComponent.threadedcomponent): # lazy
    def main(self):
        time.sleep(1)

        self.send("/nick kamspeakbot", "outbox")
        time.sleep(0.2)
        self.send("/user kamspeakbot irc.freenode.net 127.0.0.1 username", "outbox")
        time.sleep(0.2)
        self.send("/join #kamtest", "outbox")
        time.sleep(1)

class spokenIRCFilter(Axon.Component.component):
    channels = ["#mashed", "#kamaelia", "#kamtest"]
    def main(self):
        last_to_speak = None
        while True:
            for comment in self.Inbox("inbox"):
                print comment
                if comment[0] != "PRIVMSG":
                    continue
                if comment[2] in self.channels:
                    speaker, said = comment[1], comment[3]
                    if speaker != last_to_speak:
                        last_to_speak = speaker
                        self.send ( "%s says %s\n" % (speaker, said) , "outbox")
                    else:
                        self.send( said +"\n", "outbox")

            if not self.anyReady():
                self.pause()

            yield 1        

Backplane("TOCHANNEL").activate()
Backplane("FROMCHANNEL").activate()

Pipeline(
    ConsoleReader(),
    PublishTo("TOCHANNEL"),
).activate()

Pipeline(
    IRCLogin(),
    PublishTo("TOCHANNEL"),
).activate()

Pipeline(
    SubscribeTo("TOCHANNEL"),
    PureTransformer(informat),
    SimpleIRCClientPrefab(host="64.161.254.20"),
    PublishTo("FROMCHANNEL"),
).activate()

Pipeline(
    SubscribeTo("FROMCHANNEL"),
    spokenIRCFilter(),
    UnixProcess("while read word; do echo $word | espeak -w foo.wav --stdin ; aplay foo.wav ; done")
).activate()    

Pipeline(
    SubscribeTo("FROMCHANNEL"),
    PureTransformer(outformat),
    ConsoleEchoer()
).run()
