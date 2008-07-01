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
        print "Starting SimpleComponent..."
        while True:
            print "yet another iteration..."
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                self.send(data, 'outbox')
                print "SimpleComponent::inbox...", data
            while self.dataReady('numbers'):
                data = self.recv('numbers')
                self.send(str(data), 'outbox')
                print "SimpleComponent::numbers...", data
            while self.dataReady('control'):
                data = self.recv('control')
                self.send(data, 'signal')
                print "SimpleComponent::control...", data
                return
            if not self.anyReady():
                print "SimpleComponent::pausing..."
                self.pause()
            yield 1
