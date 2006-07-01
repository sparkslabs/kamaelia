#!/usr/bin/env python

import Axon
from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.Ipc import producerFinished, shutdownMicroprocess, ipc, newComponent
from Axon import Ipc
import time
import sys
sys.path.append("../MPS")
from IRCClient import SimpleIRCClient



class demodulation(component):
    """Filters out title messages and blank lines, and tags content"""
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                text = self.recv("inbox").rstrip()
                if text:
                    # this line is not blank
                    if text == "Twelfth Night":
                        pass
                    elif text[:4] == "    ":
                        if text[4:9] == "Enter":
                            # actors walking on
                            self.send(("ENTER",text[9:].strip()), "outbox")
                        elif text[4:12] == "Re-enter":
                            # actors walking on
                            self.send(("ENTER",text[12:].strip()), "outbox")
                        elif text[4:10] == "Exeunt":
                            # actors leaving
                            if not text[10:]: text+="all"
                            self.send(("EXIT",text[10:].strip()), "outbox")
                        elif text[4:8] == "Exit":
                            # actors leaving
                            self.send(("EXIT",text[8:].strip()), "outbox")
                        else:
                            # speech
                            self.send(("SAY",text.strip()), "outbox")
                    elif text[:3] == "ACT":
                        # act change
                        self.send(("ACT",text[4:].strip()), "outbox")
                    elif text[:5] == "SCENE":
                        # scene change
                        self.send(("SCENE",text[6:].strip()), "outbox")
                    else:
                        # actor name
                        self.send(("ACTOR",text.title().strip()), "outbox")
            yield 1




class error_correction(component):
    """Notes speaker names and tags speech"""
    def main(self):
        self.currentspeaker = ""
        while 1:
            yield 1
            if self.dataReady("inbox"):
                (cmd,arg) = self.recv("inbox")

                # if a speaker's name goes by, change the current speaker
                # if speech goes by, tag it as the current speaker
                if cmd == "ACTOR":
                    self.currentspeaker = arg
                elif cmd == "SAY":
                    self.send( ("SAY", self.currentspeaker, arg), "outbox")
                else:
                    # something else is happening, just pass it on
                    self.send( (cmd,arg), "outbox")


class demultiplexing(component):
    """parses ENTER and EXIT/EXEUNT stage directions"""
    def main(self):
        self.currentActors = {}
        while 1:
            yield 1
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                cmd = msg[0]
                if cmd == "ENTER" or cmd == "EXIT":
                    actors = self.extractActors(msg[1])
                    msg = [cmd] + actors
                    self.send( msg, "outbox")
                    if cmd == "ENTER":
                        for actor in actors:
                            self.currentActors[actor] = 1
                    else: # cmd == "EXIT":
                        for actor in actors:
                            try: del self.currentActors[actor]
                            except: pass
                else:
                    self.send( msg, "outbox")

                    
    def extractActors(self, text):
        # pick out names that begin with capitals, separated by lower case or punctuation
        # stop at end of string or at except
        # detect "all" case-insensitive

        # substitute punctuation with ' and '
        for punct in [",", ":", ";", "."]:
            text = text.replace(punct," and ")

        # split into words
        words = text.split(" ")
        
        # substitute 'all' with all actors
        namewords = []
        while words:
            if words[0].lower() == "all":
                for actor in self.currentActors.keys():
                    namewords.extend([" and ",actor])
                namewords.append(" and ")
            else:
                namewords.append(words[0])
            del words[0]

        # now pass through
        doingExcepts = False
        names = []
        currentname = ""
        for word in namewords:
            flush = False
            if word:
            
                if word == "except":
                    doingExcepts = True
                    flush = True
                elif word == "and":
                    flush = True
                elif word.islower():
                    flush = True
                elif word[0].isupper():
                    currentname += word + " "
    
                if flush and currentname:
                    cleanname = currentname.title().strip()
                    if not doingExcepts:
                        names.append(cleanname)
                    elif cleanname in names:
                        names.remove(cleanname)
                    currentname=""

        if currentname:
            cleanname = currentname.title().strip()
            if not doingExcepts:
                names.append(cleanname)
            elif cleanname in names:
                names.remove(cleanname)
                
        return names    



            
class director(AdaptiveCommsComponent):
    """Directs the action in the play"""
    def __init__(self, host, channel):
        super(director,self).__init__()
        self.host = host
        self.channel = channel

    def main(self):
        self.actors = {}

        try:
            # start the performance
            yield self.enter("NARRATOR")
            
            waitUntil = self.say("NARRATOR", "Welcome to our performance of Shakespeare's 'Twelfth Night'")
            while self.scheduler.time < waitUntil:
                yield 1
                if self.shutdown(): raise "DONE"

            waitUntil = self.say("NARRATOR", "Brought to you by http://kamaelia.sf.net/")
            while self.scheduler.time < waitUntil:
                yield 1
                if self.shutdown(): raise "DONE"

            while 1:
                
                yield 1
                if self.shutdown(): raise "DONE"

                if self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    cmd = msg[0].upper().strip()
                    args = msg[1:]
                    if cmd == "SAY":
                        # speak dialog
                        waitUntil = self.say( actor=args[0], words=args[1] )
                        while self.scheduler.time < waitUntil:
                            yield 1
                            if self.shutdown(): raise "DONE"
                    elif cmd == "ENTER":
                        # make actors, get them to walk on
                        for actor in args:
                            yield self.enter(actor)
                    elif cmd == "EXIT":
                        # get actors to leave
                        if args:
                            for actor in args:
                                for retval in self.exeunt(actor):
                                    yield retval
                        else:
                            self.exeuntAll()
                    elif cmd == "ACT":
                        # act change
                        for retval in self.exeuntAll():
                            yield retval
                        self.say( actor="NARRATOR", words="Act "+args[0])
                    elif cmd == "SCENE":
                        # scene change
                        for retval in self.exeuntAll():
                            yield retval
                        self.setChange("Scene "+args[0])


            waitUntil = time.time() + 5
            while self.scheduler.time < waitUntil:
                yield 1
                if self.shutdown(): raise "DONE"
            self.say("NARRATOR", "That concludes our performance. We hope you enjoyed it. Goodbye!")
            waitUntil = time.time() + 5
            while self.scheduler.time < waitUntil:
                yield 1
                if self.shutdown(): raise "DONE"
                        
        except "DONE":
            for retval in self.exeuntAll(includingNarrator=True):
                yield retval


    def closeDownComponent(self):
        pass

    def shutdown(self):
        """\
        Returns True if a shutdownMicroprocess or producerFinished message is received.

        Also passes the message on out of the "signal" outbox.
        """
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                self.send(msg, "signal")
                return True
        return False


    def makeActor(self,name):
        name = name.replace(" ","")  # spaces not possible in nicks
        return SimpleIRCClient(host=self.host, nick=name, defaultChannel=self.channel)

    
    def say(self, actor, words):
        self.send(actor+": "+words+"\n", "outbox")
        outbox = self.actors[actor][1]["outbox"]
        words = words.strip()
        if words[0]=="[" and words[-1]=="]":
            words = "\1ACTION "+words[1:-1]+"\1"
        self.send( words, outbox)
        return self.scheduler.time + 0.07*len(words)


    def setChange(self, newLocation):
        self.send( "NEW SCENE: "+newLocation+"\n", "outbox")
        outbox = self.actors["NARRATOR"][1]["topic"]
        self.send( newLocation, outbox)
        self.waitUntil = self.scheduler.time + 4.0


    def enter(self, actorName):
        self.send("ENTER: "+actorName+"\n", "outbox")
        if actorName not in self.actors:
            actor = self.makeActor(actorName)

            outboxes = dict()
            linkages = dict()

            for (o,i) in [("outbox","inbox"),("signal","control"),("topic","topic")]:
                outboxes[o] = self.addOutbox(o)
                linkages[o] = self.link( (self, outboxes[o]), (actor,i) )

            self.actors[actorName] = (actor, outboxes, linkages)
            
            self.addChildren(actor)
            return newComponent(actor)
        else:
            return 1



    def exeunt(self, actorName):
        self.send("EXIT: "+actorName+"\n", "outbox")
        if actorName in self.actors:
            (actor, outboxes, linkages) = self.actors[actorName]
            self.send(shutdownMicroprocess(self), outboxes['signal'])
            yield 1

            for box in outboxes.keys():
                self.postoffice.deregisterlinkage(thelinkage = linkages[box])
                self.deleteOutbox(outboxes[box])

            del self.actors[actorName]


    def exeuntAll(self, includingNarrator=False):
        self.send("EXIT ALL...\n","outbox")
        for actor in self.actors.keys():
            if includingNarrator or actor != "NARRATOR":
                for retval in self.exeunt(actor):
                    yield retval






if __name__ == "__main__":
    from Kamaelia.Util.PipelineComponent import pipeline
    from Kamaelia.File.Reading import RateControlledFileReader
    from Kamaelia.Util.ConsoleEcho import consoleEchoer

    pipeline( RateControlledFileReader("../CE/twelfthnight.txt", readmode="lines", rate=50, chunksize=1),
              demodulation(),
              error_correction(),
              demultiplexing(),
              director("127.0.0.1", "#theglobe"),
              consoleEchoer(),
            ).run()
            