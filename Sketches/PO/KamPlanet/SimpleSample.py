import Axon

# Receives numbers and strings, and forwards them 
# converted to strings to outbox
class SimpleComponent(Axon.Component.component):
    Inboxes = {
            "inbox"   : "messages (strings)",
            "numbers" : "numbers (integers)", 
            "control"  : "signal messages are placed here", 
        }
    def main(self):
        while True:
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                self.send(data, 'outbox')
            while self.dataReady('numbers'):
                data = self.recv('numbers')
                self.send(str(data), 'outbox')
            while self.dataReady('control'):
                data = self.recv('control')
                self.send(data, 'signal')
                return
            if not self.anyReady():
                self.pause()
            yield 1
