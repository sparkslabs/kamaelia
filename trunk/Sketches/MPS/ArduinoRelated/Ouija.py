#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Axon
import Axon
import time

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Console import *
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.UI.Pygame.Ticker import Ticker
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.Chassis.ConnectedServer import ServerCore

import socket





class Pinger(Axon.ThreadedComponent.threadedcomponent):
    sleep = 5
    def main(self):
        t = time.time()
        self.send("ping", "outbox")
        while True:
            time.sleep(0.01)
            if time.time() - t >= self.sleep:
                t = time.time()
                self.send("ping", "outbox")
            if self.dataReady("inbox"):
                self.recv("inbox")
                t = time.time()
                self.send("ping", "outbox")

class Schedule(Axon.Component.component):
    def main(self):
        i = 0
        self.send(schedule[i],"outbox")
        while not self.dataReady("control"):
            if self.dataReady("inbox"):                
                self.recv("inbox")
                i += 1
                try:
                    self.send(schedule[i],"outbox")
                except IndexError:
                    i = 0
                    self.send(schedule[i],"outbox")
            yield 1
        if self.dataReady("control"):
            self.send(self.recv("control"),"signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

class OpenCVAnalyser(Axon.Component.component):
    debounce = 1
    def main(self):
        t = time.time()
        newvote = False
        while not self.dataReady("control"):
            for rawvotes in self.Inbox("inbox"):
                try:
                    votes = rawvotes.split()
                    skip = int(votes[1])
                    love = int(votes[3])
                    ban = int(votes[5])
                    t = time.time()
                    newvote = True
                    print "LOVE %d SKIP %d BAN %d" % (love, skip, ban)
                except:
                    print "----------------"
                    print "ERROR"
                    print repr(rawvotes)
                    print repr(votes)
                    print "----------------"

            if newvote:
#                if True:
                if time.time() - t > self.debounce:
                    if ban > skip and ban > love:
                        print "BANZAI SAYS BAN!"
                        self.send("ban\n", "outbox")

                    if skip > ban and skip > love:
                        print "BANZAI SAYS SKIP!"
                        self.send("skip\n", "outbox")

                    if love > ban and love > skip:
                        print "BANZAI SAYS KEEP!"
                    newvote = False

            yield 1
        
        if self.dataReady("control"):
            self.send(self.recv("control"),"signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

class Ouija(Axon.Component.component):
    Inboxes= ["inbox", "user", "control"]
    Outboxes = ["outbox", "signal", "text", "image",
                "schedulecontrol", "pingcontrol"]
    def Print(self, arg):
        self.send(arg+"\n", "text")
    def main(self):
        banned = []
        while not self.dataReady("control"):
            for message in self.Inbox("inbox"):
                print message
                hrs, mins, name, synopsis, content = message
                if name not in banned:
                    self.Print("----------------")
                    self.Print("%s is starting now" % (name))
                    self.Print("")
                    self.Print(synopsis)
                    self.Print("")
                    self.Print("Remember to love/ban/skip!")
                    self.send(content, "image")
                else:
                    self.send("now", "pingcontrol")
            for message in self.Inbox("user"):
                self.Print("OK, you want to do this?")
                self.Print(message)
                if "skip" in message:
                    self.Print("")
                    self.Print("SKIPPING " + name)
                    self.Print("")
                    self.send("now", "pingcontrol")
                if "ban" in message:
                    self.Print("")
                    self.Print(name + " is BANNED SKIPPING")
                    self.Print("")
                    banned.append(name)
                    self.send("now", "pingcontrol")
            yield 1

        if self.dataReady("control"):
            self.send(self.recv("control"),"signal")
        else:
            self.send(Axon.Ipc.producerFinished(), "signal")

user_database = {
   "cube1" : [
                [21,00, "The Apprentice"],
                [15,30, "News"],
                [22,00, "Match of the Day"],
                [11,00, "Something for the Weekend"],
                [19,00, "Heroes"],
             ],
   "cube2" : [
                [21,00, "The Apprentice"],
                [18,00, "Dr Who"],
                [20,00, "Ashes to Ashes"],
                [22,00, "Torchwood"],
                [17,00, "Hitchhikers Guide to the Galaxy"],
                [19,00, "Heroes"],
             ],
   "cube3" : [
                [20,00, "The Culture Show"],
                [22,00, "BBC Proms"],
                [17,30, "Asian Network"],
                [19,30, "A History of 100 objects"],
                [23,00, "South Bank Show"],
                [19,00, "Heroes"],
             ],
}

user_hates = { }
user_skips = { }
user_loves = {
   "cube1" : ["The Apprentice", "News", "Match of the Day",
              "Something for the Weekend", "Heroes"],
   "cube2" : ["The Apprentice", "Dr Who", "Ashes to Ashes", "Torchwood",
              "Hitchhikers Guide to the Galaxy", "Heroes"],
   "cube3" : ["The Culture Show", "BBC Proms", "Asian Network",
              "A History of 100 objects", "South Bank Show", "Heroes"],
}
user_bans = {  # No, never again
   "cube1" : [ ],
   "cube2" : [ ],
   "cube3" : [ ],
}
user_skips = { # No, but maybe next time
   "cube1" : [ ],
   "cube2" : [ ],
   "cube3" : [ ],
}

schedule = [
    [11,00, "Something for the Weekend",
    """\
Tim Lovejoy and Louise Redknapp present a serving of chat with celebrity guests and classic TV archive moments. With mouthwatering recipes from Ainsley Harriott. They are joined by boyband JLS and American pop star Kesha.""",
    "Content/image/Something_for_the_weekend.jpg",
    ],
    [15,30, "News",
     """\
The latest national and international news, with reports from BBC correspondents worldwide.""",
    "Content/image/News.jpg",
    ],
    [17,00, "Hitchhikers Guide to the Galaxy",
     """\
The Hitchhiker's Guide to the Galaxy is a science fiction comedy series created by English writer, dramatist and musician Douglas Adams.""",
    "Content/image/Hitchhikers_Guide_to_the_Galaxy.jpg",
    ],
    [17,30, "Asian Network",
       """\
Digital and analogue radio station site with news, entertainment and broadcast information for the UK Asian community""",
    "Content/image/Asian_Network.jpg",
    ],
    [18,00, "Dr Who",
       """\
Watch the Doctor's latest amazing regeneration and see some of his earlier transformations.""",
    "Content/image/Dr_Who.jpg",
    ],
    [19,00, "Heroes",
       """\
Drama series in which people deal with their newly discovered superpowers. A trip into the past may give Hiro another chance to save the love of his life.""",
    "Content/image/Heroes.jpg",
    ],
    [19,30, "A History of 100 objects",
       """\
Neil MacGregor's history of the world recounted through objects at the British Museum arrives in Northern Europe 2,500 years ago.""",
    "Content/image/A_History_of_100_objects.jpg",
    ],
    [20,00, "The Culture Show",
      """\
Andrew Graham-Dixon presents the latest edition of The Culture Show and meets two-time Man Booker prize winner Peter Carey to discuss his latest novel, Parrot and Olivier in America.""",
    "Content/image/The_Culture_Show.jpg",
    ],
    [20,00, "Ashes to Ashes",
    """\
A wedge develops between Alex and Gene that threatens to rip the whole team apart, and their relationship is put to its toughest test yet in a heart-stopping showdown.""",
    "Content/image/Ashes_to_Ashes.jpg",
    ],
    [21,00, "The Apprentice",
    """\
The 12-week competition sets the candidates through a gruelling series of tasks and the first prize is the job of Sir Alan Sugar's apprentice, with a six figure salary.""",
    "Content/image/The_Apprentice.jpg",
    ],
    [22,00, "Match of the Day",
    """\
Gabby Logan presents live Championship football from Ashton Gate as automatic promotion chasers West Brom meet play-off contenders Bristol City, who will look for their first victory over the Baggies in 15 years.""",
    "Content/image/Match_of_the_Day.jpg",
    ],
    [22,00, "BBC Proms",
    """\
The Last Night of the Proms is one of the most popular classical music concerts in the world.""",
    "Content/image/BBC_Proms.jpg",
    ],
    [22,00, "Torchwood",
    """\
Captain Jack Harkness, Gwen Cooper and Ianto Jones return for a brand-new adventure in Torchwood: Children Of Earth, a five-part series for BBC One.""",
    "Content/image/Torchwood.jpg",
    ],
    [23,00, "South Bank Show",
 """\
Melvyn Bragg will host the final South Bank Show Awards in front of a star-studded audience at The Dorchester, London.""",
    "Content/image/South_Bank_Show.jpg",
    ],
]

def OpenCVPublisher(*args, **argd):
    return PublishTo("OPENCV_VOTES")

Backplane("OPENCV_VOTES").activate()
Backplane("PROGRAMME").activate()
Backplane("OUIJAOUT").activate()
Backplane("OUIJAIN").activate()
Backplane("USERRESPONSE").activate()
Backplane("SCHEDULECONTROL").activate()
Backplane("PINGERCONTROL").activate()

Pipeline(
    ConsoleReader(">> "),
    PureTransformer(lambda x: x[:-1]),
    PublishTo("PROGRAMME"),
).activate()

testing = False
template = "skip N love N ban N"

if testing:
    Backplane("DEBUGIN").activate()
    Pipeline(
        SubscribeTo("DEBUGIN"),
        PublishTo("USERRESPONSE"),
    ).activate()
    Pipeline(
        Textbox(position=(250,48), size=(500,150)),
        PublishTo("DEBUGIN"),
    ).activate()

    Pipeline(
        SubscribeTo("OUIJAOUT"),
        PureTransformer(lambda x: str(x)+"\n"),
        TextDisplayer(position=(250,220), size=(500,150)),
    ).activate()
else:
    Pipeline(
        SubscribeTo("OUIJAOUT"),
        TextDisplayer(position=(250,48),
                      size=(500,322),
                      text_height=20),
    ).activate()

ServerCore(protocol = OpenCVPublisher, port=1500,
           socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
           ).activate()

Pipeline(
    SubscribeTo("OPENCV_VOTES"),
    ConsoleEchoer(forwarder=True),
    OpenCVAnalyser(),
    ConsoleEchoer(forwarder=True),
    PublishTo("USERRESPONSE"),
#    PureTransformer(lambda x: repr(x)+"\n"),
).activate()

Pipeline(
    SubscribeTo("PINGERCONTROL"),
    Pinger(sleep=5),
    PublishTo("SCHEDULECONTROL"),
).activate()

Pipeline(
    SubscribeTo("SCHEDULECONTROL"),
    Schedule(),
    ConsoleEchoer(forwarder=True),
    PublishTo("OUIJAIN"),
).activate()

Graphline(
    SOURCE = SubscribeTo("OUIJAIN"),
    USER = SubscribeTo("USERRESPONSE"),
    LOGIC = Ouija(),
    TEXTBOX = PublishTo("OUIJAOUT"),
    IMAGE = PublishTo("PROGRAMME"),
    PING = PublishTo("PINGERCONTROL"),
    SCHED = PublishTo("SCHEDULECONTROL"),
    linkages = {
        ("SOURCE","outbox") : ("LOGIC","inbox"),
        ("USER","outbox") : ("LOGIC","user"),
        ("LOGIC","text") : ("TEXTBOX","inbox"),
        ("LOGIC","image") : ("IMAGE","inbox"),
#        ("LOGIC","schedulecontrol") : ("","inbox"),
        ("LOGIC","pingcontrol") : ("PING","inbox"),
    },
).activate()

Pipeline(
    SubscribeTo("PROGRAMME"),
    Image(size=(500,300), position=(250,400)),
).run()

