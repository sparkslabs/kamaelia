#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
"""\
=============================
Pygame keypress event handler
=============================

A component that registers with a Pygame Display service component to receive
key-up and key-down events from Pygame. You can set up this component to send
out different messages from different outboxes depending on what key is pressed.



Example Usage
-------------

Capture keypresses in pygame for numbers 1,2,3 and letters a,b,c::

    import pygame
  
    Graphline( output = ConsoleEchoer(),
               keys = KeyEvent( key_events={ pygame.K_1 : (1,"numbers"),
                                             pygame.K_2 : (2,"numbers"),
                                             pygame.K_3 : (3,"numbers"),
                                             pygame.K_a : ("A", "letters"),
                                             pygame.K_b : ("B", "letters"),
                                             pygame.K_c : ("C", "letters"),
                                           },
                                outboxes={ "numbers" : "numbers between 1 and 3",
                                           "letters" : "letters between A and C",
                                         }
                              ),
               linkages = { ("keys","numbers"):("output","inbox"),
                            ("keys","letters"):("output","inbox")
                          }
             ).run()

How does it work?
-----------------

This component requests a zero sized display surface from the Pygame Display
service component and registers to receive events from pygame.

Whenever a KEYDOWN event is received, the pygame keycode is looked up in the
mapping you specified. If it is there, then the specified message is sent
out of the specified outbox.

In addition, if the allKeys flag was set to True during initialisation, then
any KEYDOWN or KEYUP event will result in a ("DOWN",keycode) or ("UP",keycode)
message being sent to the "allkeys" outbox.

If you have specified a message to send for a particular key, then both that
message and the 'all-keys' message will be sent when the KEYDOWN event occurs.

If this component receives a shutdownMicroprocess or producerFinished message on
its "control" inbox, then this will be forwarded out of its "signal" outbox and
the component will then terminate.
"""

import pygame
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class KeyEvent(Axon.Component.component):
   """\
   KeyEvent([allkeys][,key_events][,outboxes]) -> new KeyEvent component.

   Component that sends out messages in response to pygame keypress events.

   Keyword arguments:
   
   - allkeys     -- if True, all keystrokes send messages out of "allkeys" outbox (default=False)
   - key_events  -- dict mapping pygame keycodes to (msg,"outboxname") pairs (default=None)
   - outboxes    -- dict of "outboxname":"description" key:value pairs (default={})
   """

   Inboxes = { "inbox"    : "Receive events from Pygame Display",
               "control"  : "Shutdown messages: shutdownMicroprocess or producerFinished",
               "callback" : "Receive callbacks from Pygame Display"
             }
   Outboxes = { "outbox"         : "NOT USED",
                "allkeys"        : "Outbox that receives *every* keystroke if enabled",
                "signal"         : "Shutdown signalling: shutdownMicroprocess or producerFinished",
                "display_signal" : "Outbox used for communicating to the display surface" }

   def __init__(self, allkeys=False, key_events=None, key_up_events=None, outboxes = {}):
      """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
      self.Outboxes = self.__class__.Outboxes
      self.Outboxes.update(outboxes)
      super(KeyEvent,self).__init__()

      self.allkeys = allkeys
      self.key_events = key_events
      self.key_up_events = key_up_events
      if self.key_events is None: self.key_events = {}
      if self.key_up_events is None: self.key_up_events = {}

      self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "events" : (self, "inbox"),
                           "size": (0,0) }

   def waitBox(self,boxname):
      """Generator. yields 1 until data is ready on the named inbox."""
      waiting = True
      while waiting:
        if self.dataReady(boxname): return
        else: yield 1

   def main(self):
      """Main loop."""
      displayservice = PygameDisplay.getDisplayService()
      self.link((self,"display_signal"), displayservice)

      self.send( self.disprequest,
                  "display_signal")

      for _ in self.waitBox("callback"): yield 1
      self.display = self.recv("callback")

      self.send({ "ADDLISTENEVENT" : pygame.MOUSEBUTTONDOWN,
                  "surface" : self.display},
                  "display_signal")
      if (self.key_events is not None) or self.allkeys or (self.key_up_events is not None):
         message = { "ADDLISTENEVENT" : pygame.KEYDOWN,
                     "surface" : self.display,
                     "TRACE" : "ME"}
         self.send(message, "display_signal")

      if self.allkeys or (self.key_up_events is not None):
         message = { "ADDLISTENEVENT" : pygame.KEYUP,
                     "surface" : self.display,
                     "TRACE" : "METO"}
         self.send(message, "display_signal")

      done = False
      while not done:
         if self.dataReady("control"):
            cmsg = self.recv("control")
            if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
               done = True

         while self.dataReady("inbox"):
            for event in self.recv("inbox"):
                if event.type == pygame.KEYDOWN:
                   if event.key in self.key_events:
                      self.send( self.key_events[event.key][0] , self.key_events[event.key][1] )
                   if self.allkeys:
                      self.send(("DOWN", event.key), "allkeys")
                if event.type == pygame.KEYUP:
                   if event.key in self.key_up_events:
                      self.send( self.key_up_events[event.key][0] , self.key_up_events[event.key][1] )
                   if self.allkeys:
                      self.send(("UP", event.key), "allkeys")
         yield 1

      self.send(Axon.Ipc.producerFinished(message=self.display), "display_signal")
      yield 1


__kamaelia_components__  = ( KeyEvent, )
