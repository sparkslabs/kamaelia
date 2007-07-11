import inspect
import re
#
# This is where we will put shards that come from *inside* the main method.
#
def MOUSEBUTTONDOWN_handler(self):
    if  event.button == 1:
        self.drawing = True
    elif event.button == 3:
        self.oldpos = None
        self.drawBG()
        self.blitToSurface()

def MOUSEBUTTONUP_conditional_handler(self):
    self.drawing = False
    self.oldpos = None

def MOUSEMOTION_handler(self):
    if self.drawing and self.innerRect.collidepoint(*event.pos):
        if self.oldpos == None:
            self.oldpos = event.pos
        else:
            pygame.draw.line(self.display, (0,0,0), self.oldpos, event.pos, 3)
            self.oldpos = event.pos
        self.blitToSurface()

def SetEventOptions(self):
    self.addListenEvent("MOUSEBUTTONDOWN")
    self.addListenEvent("MOUSEBUTTONUP")
    self.addListenEvent("MOUSEMOTION")

#
# Reusaable IShards
#

def ShutdownHandler(self):
    while self.dataReady("control"):
        cmsg = self.recv("control")
        if isinstance(cmsg, producerFinished) or isinstance(cmsg, shutdownMicroprocess):
            self.send(cmsg, "signal")
            done = True

def LoopOverPygameEvents(self):
    while self.dataReady("inbox"):
        for event in self.recv("inbox"):
            if event.type == pygame.MOUSEBUTTONDOWN:
                exec self.getIShard("MOUSEBUTTONDOWN")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                exec self.getIShard("MOUSEBUTTONUP_conditional")
            elif event.type == pygame.MOUSEMOTION:
                exec self.getIShard("MOUSEMOTION")

def RequestDisplay(self):
    displayservice = PygameDisplay.getDisplayService()
    self.link((self,"display_signal"), displayservice)
    self.send( self.disprequest, "display_signal")

def GrabDisplay(self):
    self.display = self.recv("callback")

#def getIShard(code_object):
    #IShard = inspect.getsource(code_object)
    #IShard = IShard[re.search(":.*\n",IShard).end():] # strip def.*
    #lines = []
    #indent = -1
    #for line in IShard.split("\n"):
        #if indent == -1:
            #r = line.strip()
            #indent = len(line) - len(r)
            #lines.append(r)
        #else:
            #lines.append(line[indent:])
    #IShard = "\n".join(lines)
    #return IShard
##    exec IShard
