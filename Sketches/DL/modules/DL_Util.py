# Some Utilities useful for testing purposes

from Kamaelia.Util.Chargen import Chargen

class SerialChargen(Chargen):
    """ Generates Hello World0, Hello World1, Hello World2, ....."""

    def main(self):
        """Main loop."""
        count = 0
        while 1:
            self.send("Hello World" + str(count), "outbox")
            count += 1
            yield 1
            

                                                                    
