
import time
logfile = "message_log"

print "loading responders" # :-)

def Always(*args, **argd):
    return True

def Never(*args, **argd):
    return False

def SendNotHere(self, who, message):
    sendmessage = False
    seen = self.stash.get("seen", {})
#    print "seen", seen, self.stash
    if seen.get(who):
        (first, last, count) = seen[who]
    else:
        (first, last, count) = time.time(),time.time(), 0
    now = time.time()
    if count == 0:
        sendmessage = True
        x = list(self.NotHere)
    if (count % 11) == 3:
        sendmessage = True
        x = ["Just a reminder" ] + list(self.NotHere)
    if (count % 11) == 9:
        sendmessage = True
        x = ["You know, he's not there!" ] + list(self.NotHere)
    if (now - last) > 3600:
        sendmessage = True
        x = ["Nope, still not back!"]  + list(self.NotHere)
    if sendmessage:
        last = now
        while len(x) > 0:
            time.sleep(0.5)
            self.send( ("message", who, x.pop(0)) , "outbox")

    count += 1
    seen[who] = (first, last, count)
    self.stash["seen"] = seen

def noteToLog(self, who, message):
    try:
        x = open(logfile, "a")
    except IOError:
        x = open(logfile, "w")
    x.write( " | ".join([ time.ctime(), who, repr(message) ]) +"\n")
    x.flush()
    x.close()

def debug(self, who, message):
    print self.stash

def Otherdebug(self, who, message):
#    self.__class__.stash = {}
    self.__class__.NotHere = [ "Sorry, I'm not here right now. I'm in Geneva and back on Wednesday!",
                "Please leave a message and Michael'll get back to you ASAP",
                "(This is an automated response)"]

message_handlers = [
#    (Always, Otherdebug),
    (Always, SendNotHere),
    (Always, noteToLog),
#    (Always, debug),
]

