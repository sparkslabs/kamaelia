#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
