#!/usr/bin/env python2.5
# -------------------------------------------------------------------------
"""\
=================
SimpleTranslator
=================

A simple example to use kamaelia framework to implement
component-based concurrency systems.

Class FileReader reads data from text.txt, then send the data to
SimpleTranslator for translation and finally the translated result
is sent to ConsoleEchoer for display in the console. Pipeline is used
to connect these components.

"""


import Axon

# A component to read data from text.txt
class FileReader(Axon.Component.component):
    def __init__(self, filename):
        super(FileReader, self).__init__()
        self.file = open(filename, "r",0)
    def main(self):
        #yield 1
        try:
            for line in self.file:
                self.send(line, "outbox")
                yield 1
        finally:
            self.file.close()
  
# A very simple and very silly translator from British English
#to American English (only "tre" - "ter", "our" - "or")
#though I could add more rules or user-definable given enough time.
class SimpleTranslator(Axon.Component.component):
    def __init__(self):
        super(SimpleTranslator, self).__init__()        
    def main(self):
        count = 0
        #yield 1
        while 1:
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                data = data.replace("\r\n", "") # Windows
                data = data.replace("\n", "") # Unix
                result = data
                if data.find("tre"):
                    result = result.replace("tre", "ter")
                if data.find("our"):
                    result = result.replace("our", "or")               
                count += 1
                newData = str(count) + ' ' + data + ' - ' + result + '\n'
                self.send(newData, "outbox")
            yield 1

        
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer

# A connector to link all components used
Pipeline( FileReader("text.txt"),
          SimpleTranslator(),
          ConsoleEchoer() # A component to display the result
          ).run()
