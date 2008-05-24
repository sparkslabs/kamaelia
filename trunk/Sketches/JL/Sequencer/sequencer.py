#! /usr/bin/env python
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished

class sequencer(component):
#Inboxes: inbox, control
#Outboxes: outbox, signal
    def __init__(self):
        super(sequencer, self).__init__()
        self.running = True
        
    def findNext(self):
        return 0
    
    def main(self):
        while self.running:
##            self.send('message', 'outbox')
            if self.dataReady("control"):
                msg = self.recv("control")
                print "received control message: ", msg
                if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                    self.shutdown()
                    break
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                print "received inbox message: ", msg
                if msg == "NEXT":
                    self.send(self.findNext(), 'outbox')
            yield 1

    def shutdown(self):
        self.running = False
        self.send(producerFinished(), "signal")

                
class fibonacciSequencer(sequencer):
    def __init__(self):
        super(fibonacciSequencer, self).__init__()
        self.n = 0
        self.n_1 = 1
        
    def findNext(self):
        val = self.n
        self.n = self.n_1
        self.n_1 = val + self.n_1
        return val
    
    def main(self):
        i = 0
        while i < 20:
            yield 1
            self.printNext()
            i = i+1
        self._closeDownMicroprocess()
            
                
        
class naturals(sequencer):
    def __init__(self):
        super(naturals, self).__init__()
        self.n = 0
        
    def findNext(self):
        self.n = self.n + 1
        return self.n

class mrsequencer(component):
#quicker to use
    def __init__(self, seed=0, length=-1, findNext=(lambda x: x)):
        super(mrsequencer, self).__init__()
        self.findNext = findNext
        self.seed = seed
        self.length = length
        self.current = self.seed
        self.counter = 0
            
    def main(self):
        while self.shouldGo():
            if self.dataReady("inbox"):
                msg = self.recv("inbox")
                self.send(self.current, 'outbox')
                self.current = self.findNext(self.current)
                self.counter = self.counter + 1                
            yield 1

    def shouldGo(self):
        if self.counter == self.length+1:
            return False
        if self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                print "mrsequencer received control message: ", msg
                return False
        return True

if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
    #Pipeline(ConsoleReader(),mrsequencer(seed = (0,1), findNext = (lambda (n, fact): (n+1, fact * (n+1))), length = 10),ConsoleEchoer()).run()
    Pipeline(ConsoleReader(), mrsequencer(seed = (0, 0,1), findNext = (lambda (n, x,y): (n+1, y,x+y)), length = 20), ConsoleEchoer()).run() #fibonacci
    #Pipeline(ConsoleReader(), mrsequencer(seed = (0,0), findNext = (lambda (n, sigma): (n+1, sigma + n + 1))), ConsoleEchoer()).run() #triangular numbers

    def looksay(num):
            str_rep = str(num)
            str_result = ''
            count = 0
            digit = ''
            while str_rep:
                    if str_rep[0] is digit: count = count + 1
                    else: 
                            str_result = str_result + str(count) + digit
                            count = 1
                            digit = str_rep[0]
                    str_rep = str_rep[1:]
            str_result = str_result + str(count) + digit
            return int(str_result)

    #Pipeline(ConsoleReader(), mrsequencer(seed = 1, findNext = looksay), ConsoleEchoer()).run() #Look and Say # 1, 11, 21, 1211, 111221, 312211, 13112221, 1113213211


