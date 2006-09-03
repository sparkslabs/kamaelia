from Axon.Component import component
import os
import shutil

from MailShared import isLocalAddress, isPlain
from binascii import hexlify, unhexlify

class RemoteDelivery(component):
    def main(self):
        while 1:
            yield 1
            self.pause()

class LocalDelivery(component):
    def __init__(self, deliveryqueuedir, localmaildir):
        self.deliveryqueuedir = deliveryqueuedir
        self.localmaildir = localmaildir
        
        if not os.path.isdir(self.localmaildir + "/"):
            os.mkdir(self.localmaildir + "/")
            
        super(LocalDelivery, self).__init__()
        
    def deliverLocal(self, msgid, server, user):
        print "Delivering " + msgid + " locally to " + user + "@" + server
        src = os.path.join("pending", msgid, "data")
        dst = os.path.join("local", server, user, msgid)
        if os.path.lexists(dst):
            os.unlink(dst) # already copied/partly copied
            
        try:
            os.link(src, dst) # we use hard links so if a message has several recipients it only gets stored once
        except OSError:
            shutil.copy2(src, dst) # hard link failed, we'll copy it (e.g. if it's on a different partition)
    
    def deletePendingMessageIfFullyDelivered(self, msgid):
        try:
            if len(os.listdir(os.path.join("pending", msgid))) == 1:
                shutil.rmtree(os.path.join("pending", msgid))
        except OSError:
            pass
            
    def deleteRecipientFile(self, msgid, recipient):
        os.unlink(os.path.join("pending", msgid, "recipient-" + hexlify(recipient)))
        
    def localUserExists(self, server, user):
        if os.path.isdir(os.path.join("local", server)) and os.path.isdir(os.path.join("local", server, user)):
            return True
        else:
            return False
    
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"):
                msgname, recipients = self.recv("inbox")
                for recipient in recipients:
                    # local only
                    splitbyat = recipient.rsplit("@", 1)
                    username = splitbyat[0]                    
                    server = splitbyat[1]
                    if isPlain(username) and isPlain(server) and self.localUserExists(server, username):
                        self.deliverLocal(msgname, server, username)
                    else:
                        print "warning: user " + recipient + "not found"
                    self.deleteRecipientFile(msgname, recipient) # probably don't want to do this for messages with some local some remote recipients
                self.deletePendingMessageIfFullyDelivered(msgname)
            self.pause()
