import os
import shutil
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from binascii import hexlify, unhexlify
class DeliveryQueueOne(AdaptiveCommsComponent):
    def makeRecipientLink(self, filename, recipient):
        # we no longer use hard links because some backward operating systems don't support them
        codedrecipient = hexlify(recipient) # hex is filesystem safe characters only
        dst = os.path.join("pending", filename, "recipient-" + codedrecipient)
        f = open(dst, "w")
        f.close()
        # src = os.path.join("received", filename)
        # dst = os.path.join("todeliver", filename + "-" + codecrecipient)
        # if not os.path.exists(dst):
        #     os.link(src, dst)
        #     return True
        # else:
        #     return False

    def makePendingFolder(self, filename):
        foldername = os.path.join("pending", filename)
        os.mkdir(foldername)
        
    def moveMessageToPending(self, filename):
        src = os.path.join("received", filename)
        dst = os.path.join("pending", filename, "data")
        shutil.move(src, dst)
        
    def deleteOriginal(self, filename):
        os.unlink(os.path.join("received", filename))

    def getRecipientsIfComplete(self, filename):
        f = open(os.path.join("received", filename))
        
        recipients = []
        while 1:
            parttype = f.read(1)
            if parttype == "":
                break
            elif parttype == "C":
                return recipients
    
            partlength = ["0"]        
            while partlength[-1] != "=":
                partlength.append(f.read(1))
            partlength = int("".join(partlength[:-1]))
            
            if parttype == "R":
                recipient = f.read(partlength)
                recipients.append(recipient)
            else:
                f.seek(partlength, 1)
                
        return None # no complete ending ("C") message
    
    def main(self):
        # load up messages in the ./received/ folder
        for msgname in os.listdir("pending"):
            if not os.path.isfile(os.path.join("pending", msgname, "data")):
                # recipients list not created properly
                print "Removing incomplete message pending/" + msgname
                shutil.rmtree(os.path.join("pending", msgname)) 
            else:
                print "Resuming delivery of pending/" + msgname
                msgfolder = os.path.join("pending", msgname)
                contents = os.listdir(msgfolder)
                if len(contents) == 1: # message must have been delivered, no recipient files remain
                    shutil.rmtree(msgfolder)
                else:
                    recipients = []
                    recipientstart = "recipient-"
                    for entry in contents:
                        if entry[:len(recipientstart)] == recipientstart:
                            recipient = unhexlify(entry[len(recipientstart):])
                            recipients.append(recipient)
                    self.send((msgname, recipients), "outbox")
                    
                
        for msgname in os.listdir("received"):
            print "Resuming delivery of received/" + msgname        
            msgrecipients = self.getRecipientsIfComplete(msgname)
            if not msgrecipients:
                # the saved message is incomplete so delete it
                print "Removing incomplete message received/" + msgname 
                self.deleteOriginal(msgname)
                
            else:
                self.makePendingFolder(msgname)
                for recipient in msgrecipients:
                    self.makeRecipientLink(msgname, recipient)

                self.moveMessageToPending(msgname)
                self.send((msgname, msgrecipients), "outbox")
            
        while 1:
            yield 1

            while self.dataReady("inbox"):
                msgtuple = self.recv("inbox")
                filename = msgtuple[0]
                recipients = msgtuple[1]
    
                self.makePendingFolder(filename)
                for recipient in recipients:
                    self.makeRecipientLink(filename, recipient)

                self.moveMessageToPending(filename)
                self.send((filename, recipients), "outbox")
            
            self.pause()
