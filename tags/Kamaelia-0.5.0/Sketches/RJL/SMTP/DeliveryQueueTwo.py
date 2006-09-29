from Axon.Component import component
from MailShared import isLocalAddress

class DeliveryQueueTwo(component):
    # accepts msg tuple (filename, recipients)
    Outboxes = {
        "local" : "(filename, recipients) for local delivery",
        "remote" : "(filename, recipients) for remote delivery",
    }
            
    def __init__(self, localdict):
        self.localdict = localdict
        super(DeliveryQueueTwo, self).__init__()
    
    def splitRecipientsLocalRemote(self, recipients):
        localrecipients = []
        remoterecipients = []
        for recipient in recipients:
            if isLocalAddress(recipient, self.localdict):
                localrecipients.append(recipient)
            else:
                remoterecipients.append(recipient)
        return (localrecipients, remoterecipients)
        
    def main(self):
        while 1:
            yield 1
            while self.dataReady("inbox"): 
                msg = self.recv("inbox")

                filename, recipients = msg[0], msg[1]
                
                localrecipients, remoterecipients = self.splitRecipientsLocalRemote(recipients)
                
                self.send((filename, localrecipients), "local")
                self.send((filename, remoterecipients), "remote")
                
            self.pause()
