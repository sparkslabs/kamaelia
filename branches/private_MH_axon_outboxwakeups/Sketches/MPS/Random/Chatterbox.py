#!/usr/bin/python

import Axon, random
from Kamaelia.Chassis.ConnectedServer import SimpleServer
nlnl = '\n', '\n'
key = nlnl

def new_key(key, word):
   if word == '\n': return nlnl
   else: return (key[1], word)
      
class Chatty(Axon.Component.component):
   data = {}
   def updateChain(self, message):
       key = nlnl
       for word in message.split():
           self.__class__.data.setdefault(key, []).append(word)
           key = new_key(key, word)
   def response(self):
       key, result, word = nlnl, [], None
       while word != "\n":
           word = random.choice(self.__class__.data.get(key, nlnl))
           key = new_key(key, word)
           result.append(word)
       return " ".join(result)
   def main(self):
       while 1:
           if self.dataReady("inbox"):
               message = self.recv("inbox")
               self.updateChain(message)
               self.send(self.response(), "outbox")
           yield 1

SimpleServer(protocol=Chatty, port=1500).run() 
