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
#

from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, WaitComplete

from Kamaelia.UI.Pygame.Display import PygameDisplay

class ProperSurfaceDisplayer(component):
    Inboxes = {
        "inbox" : "",
        "control" : "",
        "callback" : "",
    }
    Outboxes = {
        "outbox" : "",
        "signal" : "",
        "display_signal" : "",
    }

    def __init__(self, **argd):
        super(ProperSurfaceDisplayer, self).__init__(**argd)
        self.disprequest = { "DISPLAYREQUEST" : True,
                           "callback" : (self,"callback"),
                           "size": self.displaysize,
                           "position" : self.position,
                           "bgcolour" : self.bgcolour}

    def shutdown(self):
       """Return 0 if a shutdown message is received, else return 1."""
       if self.dataReady("control"):
           msg=self.recv("control")
           if isinstance(msg,producerFinished) or isinstance(msg,shutdownMicroprocess):
               self.send(producerFinished(self),"signal")
               return 0
       return 1

    def pygame_display_flip(self):
        self.send({"REDRAW":True, "surface":self.display}, "display_signal")

    def getDisplay(self):
       displayservice = PygameDisplay.getDisplayService()
       self.link((self,"display_signal"), displayservice)
       self.send(self.disprequest, "display_signal")
       while not self.dataReady("callback"):
           self.pause()
           yield 1
       self.display = self.recv("callback")
       self.display.fill( (self.bgcolour) )

    def main(self):
       yield WaitComplete(self.getDisplay())

       while self.shutdown():
          if self.dataReady("inbox"):
              data = self.recv("inbox")
              if isinstance(data,list):
                  self.display.blit(data[0], data[1])
              else:
                  self.display.blit(data, (0,0))
              self.pygame_display_flip()
          self.pause()
          yield 1