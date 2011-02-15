#!/usr/bin/python

import time
import Axon
from Axon.STM import Store
import random

def all(aList, value):
    for i in aList:
        if value != i:
            return False
    return True
    
class Philosopher(Axon.ThreadedComponent.threadedcomponent):
    forks = ["fork.1", "fork.2"] # default for testing :-)
    def getforks(self):
        gotforks = False
        while not gotforks:
            try:
                X = self.store.using(*self.forks)
                if all([ X[fork].value for fork in self.forks], None):
                    for fork in self.forks:
                        X[fork].value = self.name
                    X.commit()
                    gotforks = True
                else:
                    time.sleep(random.random())
            except Axon.STM.ConcurrentUpdate:
                time.sleep(random.random())
            except Axon.STM.BusyRetry:
                time.sleep(random.random())
        print ("Got forks!", self.name, self.forks)
        return X

    def releaseforks(self,X):
        print ("releasing forks", self.name)
        for fork in self.forks:
            X[fork].value = None
        X.commit()

    def main(self):
        while 1:
            X = self.getforks()
            time.sleep(0.2)
            self.releaseforks(X)
            time.sleep(0.3+random.random())

S = Store()
N = 5
for i in range(1,N):
    Philosopher(store=S,forks=["fork.%d" % i ,"fork.%d" % (i+1)]).activate()

Philosopher(store=S,forks=["fork.%d" % N ,"fork.%d" % 1]).run()
