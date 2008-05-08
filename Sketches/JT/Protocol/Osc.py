import OSC
import Axon

class Osc(Axon.Component.component):
    def __init__(self, addressPrefix = None):
        super(Osc, self).__init__()
        self.addressPrefix = addressPrefix
    
    def main(self):
        while 1:
            while self.dataReady("inbox"):
                address, arguments = self.recv("inbox")
                # Prepend forward slash to address
                if address[0] != "/":
                    address = "/" + address
                if self.addressPrefix:
                    address = self.addressPrefix + address
                message = OSC.OSCMessage(address)
                message.append(arguments)
                self.send(message.getBinary(), "outbox")
            self.pause()
            yield 1

if __name__ == "__main__":
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Internet.UDP import SimplePeer
    Pipeline(Osc("/OscTest"), SimplePeer(receiver_addr="127.0.0.1", receiver_port=2000)).run()
