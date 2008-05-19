#!/usr/bin/python
import random
#import string

from Axon.Component import component
import time

class Source(component):
   def __init__(self,  size=100):
      super(Source, self).__init__()
      self.size = size
   def main(self):
      i = 0
      t = time.time()
      while 1:
         yield 1
         if time.time() - t > 0.01:
            i = i + 1
            self.send(str(i), "outbox")
            t = time.time()

class Annotator(component):
   def main(self):
      n=1
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            self.send((n, item), "outbox")
            n = n + 1

class Duplicate(component):
   def main(self):
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            if random.randrange(0,10) == 0:
               self.send(item, "outbox")
               self.send(item, "outbox")
            else:
               self.send(item, "outbox")

class Throwaway(component):
   def main(self):
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            if random.randrange(0,10) != 0:
               self.send(item, "outbox")

class Reorder(component):
    def main(self):
        newlist = []
        while 1:
            yield 1
            if self.dataReady("inbox"):
                item = self.recv("inbox")
                newlist.append(item)
                if len(newlist) == 8:
                    temp = random.randrange(0,7)
                    self.send(newlist[temp], "outbox")
                    newlist.remove(newlist[temp])

class RecoverOrder(component):
   def main(self):
      bufsize = 30
      datasource = []
      while 1:
         yield 1
         if self.dataReady("inbox"):
            item = self.recv("inbox")
            datasource.append(item)
      
            if len(datasource) == bufsize:
               datasource.sort()
               try:
                  if datasource[0] != datasource[1]:
                     self.send(datasource[0], "outbox")
               except IndexError:
                   self.send(datasource[0], "outbox")
               del datasource[0]

      need_clean_shutdown_make_this_true_and_fix = False
      if need_clean_shutdown_make_this_true_and_fix:
         while datasource != []:
            try:
               if datasource[0] != datasource[1]:
                     self.send(datasource[0], "outbox")
            except IndexError:
                     self.send(datasource[0], "outbox")
            del datasource[0]

from Kamaelia.Util.PipelineComponent import pipeline
from Kamaelia.Util.ConsoleEcho import consoleEchoer

class Tuple2string(component):
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                item = self.recv("inbox")
                data_id = str(item[0])
                data_length = str(len(str(item[1])))
                data = str(item[1])
                item = "%s %s %s" % (data_id, data_length, data)
                self.send(item, "outbox")

class String2tuple(component):
    def main(self):
        while 1:
            yield 1
            if self.dataReady("inbox"):
                item = self.recv("inbox")
                temp_list = str.split(item)
                data_id = int(temp_list[0])
                data = temp_list[2]
                item = (data_id, data)
                self.send(item, "outbox")


pipeline(Source(),
         Annotator(),
         Tuple2string(),
         Duplicate(),
         Throwaway(),
         Reorder(),
         String2tuple(),
         RecoverOrder(),
         consoleEchoer()
).run()
