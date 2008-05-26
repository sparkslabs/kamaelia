import pypm
import Axon
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.UI.Pygame.Button import Button

class MidiTest(Axon.Component.component):
    def __init__(self, port_number):
        super(MidiTest, self).__init__()
        pypm.Initialize()
        self.output = pypm.Output(port_number, 0)

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                #Note on (with note num from inbox) if we get data
                self.output.WriteShort(0x90, self.recv("inbox"), 127)
            yield 1

if __name__ == "__main__":
    Graphline(bd = Button(caption="BD", msg=36, position=(0, 0)),
              sd = Button(caption="SD", msg=38, position = (50, 0)),
              hh = Button(caption="HH", msg=46, position = (100, 0)),
              midi_out = MidiTest(0),
              linkages = {
                  ("bd", "outbox") : ("midi_out", "inbox"),
                  ("hh", "outbox") : ("midi_out", "inbox"),
                  ("sd", "outbox") : ("midi_out", "inbox"),
              }
    ).run()