#!/usr/bin/env python


class nullbox(object):
    def __init__(self):
        super(nullbox,self).__init__()
        self.sources = []
    def append(self, data):
        pass
    def __len__(self):
        return 0
    def retarget(self, target):
        pass

class realbox(list):
    def __init__(self, owner):
        super(realbox,self).__init__()
        self.owner = owner
        self.sources = []
    def append(self,object):
        self.owner._unpause()
        return super(realbox,self).append(object)
    def retarget(self, target):
        for box in self.sources:
            box.retarget(target)

class proxybox(object):
    def __init__(self, target):
        super(proxybox,self).__init__()
        self.target = target
        self.target.sources.append(self)
        self.sources = []
    def append(self, data):
        return self.target.append(data)
    def __len__(self):
        return len(self.target)
    def retarget(self, target):
        self.target.sources.remove(self)
        self.target = target
        self.target.sources.append(self)
        for box in self.sources:
            box.retarget(target)
        
