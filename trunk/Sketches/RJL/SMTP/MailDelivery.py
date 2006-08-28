from Axon.Component import component
import os
import shutil

def determineDeliveryMethod(dest):
    
class Delivery(component):
    def __init__(self, deliveryqueuedir, localmaildir):
        self.deliveryqueuedir = deliveryqueuedir
        self.localmaildir = localmaildir
        super(Delivery, self).__init__()
        
    def deliverLocal(self, msgid, deliverto):
        src = self.deliveryqueuedir + "/" + msgid
        dst = self.localmaildir + "/" + deliverto + "/" + msgid
        try:
            os.link(src, dst) # we use hard links so if a message has several recipients it only gets stored once
        except OSError:
            shutil.copy2(src, dst) # hard link failed, we'll copy it (e.g. if it's on a different partition)
    
    def deleteDeliverQueueCopy(self, msgid):
        os.unlink(self.deliveryqueuedir + "/" + msgid)
        
    def localUserExists(self, user):
        if os.isdir(self.localmaildir + "/")
        
    def isAlphaNumeric(s):
        for c in s:
            if "a" <= c and c <= "z":
                pass
            elif "A" <= c and c <= "Z":
                pass
            elif "0" <= c and c <= "9":
                pass
            else
                return False
        return True
    
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msg = self.recv("inbox")
                for recipient in msg["recipients"]:
                    # local only
                    username = recipient.split("@", 1)[0]
                    if self.isAlphaNumeric(username) and self.localUserExists(username):
                        self.deliverLocal(msg["id"], username)
                    else:
                        print "warning: user not found"
                    self.deleteDeliveryQueueCopy(username)
