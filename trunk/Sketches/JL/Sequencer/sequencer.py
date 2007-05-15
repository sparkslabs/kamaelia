from Axon.Component import component

class sequencer(component):
    def __init__(self):
        super(sequencer, self).__init__()
        
    def findNext(self):
        return 1
    
    def printNext(self):
        print self.findNext()
        
    def main(self):
        while True:
            yield 1
            self.printNext()
        
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