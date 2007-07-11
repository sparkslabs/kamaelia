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

def MOUSEBUTTONUP_handler(self):
    if event.button == 1:
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

def BINGLE(self):
    self.backgroundColour = bgcolour
    self.foregroundColour = fgcolour
    self.margin = margin
    self.oldpos = None
    self.drawing = False

    self.size = size
    self.innerRect = pygame.Rect(10, 10, self.size[0]-20, self.size[1]-20)

    if msg is None:
        msg = ("CLICK", self.id)
    self.eventMsg = msg
    if transparent:
        transparency = bgcolour
    else:
        transparency = None
    self.disprequest = { "DISPLAYREQUEST" : True,
                         "callback" : (self,"callback"),
                         "events" : (self, "inbox"),
                         "size": self.size,
                         "transparency" : transparency }

    if not position is None:
        self.disprequest["position"] = position

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
            elif event.type == pygame.MOUSEBUTTONUP:
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
