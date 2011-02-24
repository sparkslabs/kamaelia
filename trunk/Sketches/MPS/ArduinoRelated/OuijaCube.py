#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import socket
import sys
import os
import serial

import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.UI.Pygame.Image import Image
from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
from Kamaelia.Util.PureTransformer import PureTransformer

class Pinger(Axon.ThreadedComponent.threadedcomponent):
    sleep = 10
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
    """
    Schedule
    
    Simple schedule component. This component waits for system
    pings to tell it to move onto the next item. (There's
    obviously other ways of doing this, but this approach
    was chosen because it simplified the creation of
    skip/ban-skip mechanics.
    """
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
    """
    OpenCVAnalyser
    
    Simple analyser that takes voting information from Matt's
    OpenCV system and uses it to decide whether to ban or skip
    the current programme. May choose not to do either if no
    clear win, or if programme is loved.
    
    Since the Open CV based code is jittery (due to real world
    considerations) and does stabilise, this code includes simple
    debouncing of values. Specifically it waits for the system
    to stabilise before accepting the votes.
    
    A debounce time of greater than a second seemed unnatural.
    
    Works on first past the post voting.
    
    Expects to recieve strings generateable using this template
    code:
        "skip %d love %d ban %d\n" %(skip, love, ban)
    """
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
        hrs, mins, name, synopsis, content  = "","","","",""
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

class SerialIO(Axon.ThreadedComponent.threadedcomponent):
    serialport = '/dev/ttyUSB0'
    baudrate = 9600
    def main(self):
        ser = serial.Serial(self.serialport, self.baudrate)
        input = ""
        while True:
            input += ser.read()
            while input.find("\r\n") != -1:
                chopped_line = input[:input.find("\r\n")]
                input = input[input.find("\r\n")+2:]
                self.send(chopped_line, "outbox")
            for msg in self.Inbox("inbox"):
                ser.write(str(msg))

# User information was not implemented in this version,
# but could be, and was expected to be.
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

Backplane("PROGRAMME").activate()
Backplane("OUIJAOUT").activate()
Backplane("OUIJAIN").activate()
Backplane("USERRESPONSE").activate()
Backplane("OPENCV_VOTES").activate()
Backplane("SCHEDULECONTROL").activate()
Backplane("PINGERCONTROL").activate()
Backplane("DEBUGIN").activate()

if "debug" in sys.argv:
    testing = True
else:
    testing = False

if testing:
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

Pipeline(
    ConsoleReader(">> "),
    PureTransformer(lambda x: x[:-1]),
    PublishTo("PROGRAMME"),
).activate()

else:
    Pipeline(
        SubscribeTo("OUIJAOUT"),
        TextDisplayer(position=(250,48),
                      size=(500,322),
                      text_height=25),
    ).activate()

def Publisher(*args, **argd):
    return PublishTo("OPENCV_VOTES")

# For receiving Voting information from Matt's Open CV system

ServerCore(protocol = Publisher, port=1500,
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
        ("LOGIC","pingcontrol") : ("PING","inbox"),
    },
).activate()

Pipeline(
    SubscribeTo("SCHEDULECONTROL"),
    PureTransformer(lambda x: "\n"),
    SerialIO(),
    PureTransformer(lambda x: str(x)+"\n"),
    ConsoleEchoer(),
).activate()

Pipeline(
    SubscribeTo("PROGRAMME"),
    Image(size=(500,300), position=(250,400)),
).run()
