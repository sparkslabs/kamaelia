#!/usr/bin/env python


class nullbox(object):
    def append(self, data):
        pass
    def __len__(self):
        return 0
    def box_interface(self):
        return self.append, self.__len__

class realbox(list):
    def __init__(self, owner):
        super(realbox,self).__init__()
        self.owner = owner
    def append(self,object):
        self.owner._unpause()
        return super(realbox,self).append(object)
    def box_interface(self):
        return self.append, self.__len__

class proxybox(object):
    def __init__(self, append, len):
        super(proxybox,self).__init__()
        self.append = append
        self.__len__ = len
    def box_interface(self):
        return self.append, self.__len__
        
