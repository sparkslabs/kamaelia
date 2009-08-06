#!/usr/bin/python
class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1

class printer(microprocess):
    def __init__(self, tag):
        super(printer, self).__init__()
        self.tag = tag
    def main(self):
        while 1:
            yield 1
            print self.tag

class scheduler(microprocess):
    def __init__(self):
        super(scheduler, self).__init__()
        self.active = []
        self.newqueue = []
    def main(self): 
        for i in xrange(100):
            for current in self.active:
                yield 1
                try:
                    result = current.next()
                    if result is not -1:
                        self.newqueue.append(current)
                except StopIteration:
                    pass
            self.active = self.newqueue
            self.newqueue = []
    def activateMicroprocess(self, someprocess):
        microthread = someprocess.main()
        self.newqueue.append(microthread)

class component(microprocess):
    Boxes = {
        "inbox" : "This is where we expect to receive messages for work",
        "outbox" : "This is where we expect to send results/messages to after doing work"
    }
    def __init__(self):
        super(component, self).__init__()
        self.boxes = {}
        for box in self.Boxes:
            self.boxes[box] = list()
    def send(self, value, outboxname):
        self.boxes[outboxname].append(value)
    def recv(self, inboxname):
        result = self.boxes[inboxname][0]
        del self.boxes[inboxname][0]
        return result
    def dataReady(self, inboxname):
        return len(self.boxes[inboxname])

class postman(microprocess):
    def __init__(self, source, sourcebox, sink, sinkbox):
        self.source = source
        self.sourcebox = sourcebox
        self.sink = sink
        self.sinkbox = sinkbox
    def main(self):
        while 1:
            yield 1
            if self.source.dataReady(self.sourcebox):
                d = self.source.recv(self.sourcebox)
                self.sink.send(d, self.sinkbox)

class FileReader(component):
    def __init__(self, filename):
        super(FileReader, self).__init__()
        self.file = open(filename, "rb",0)
    def main(self):
        yield 1
        for line in self.file.xreadlines():
          self.send(line, "outbox")
          yield 1

import socket
class Multicast_sender(component):
  def __init__(self, laddr, lport, daddr, dport):
    super(Multicast_sender, self).__init__()
    self.laddr = laddr
    self.lport = lport
    self.daddr = daddr
    self.dport = dport

  def main(self):
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM,
                         socket.IPPROTO_UDP)
    sock.bind((self.laddr,self.lport))
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_MULTICAST_TTL, 10)
    while 1:
      if self.dataReady("inbox"):
        data = self.recv("inbox")
        l = sock.sendto(data, (self.daddr,self.dport) )
        print l # to see activity 
      yield 1

R = FileReader("Ulysses")
S = Multicast_sender("0.0.0.0", 0, "224.168.2.9", 1600)
postie = postman(R, "outbox", S, "inbox")
myscheduler = scheduler()
myscheduler.activateMicroprocess(R)
myscheduler.activateMicroprocess(S)
myscheduler.activateMicroprocess(postie)
for _ in myscheduler.main():
    pass

