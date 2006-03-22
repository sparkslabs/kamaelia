#!/usr/bin/env python


class nullsink(object):
    def __init__(self):
        super(nullsink,self).__init__()
    def append(self, data):
        pass
    def __len__(self):
        return 0
#    def addsource(self, postbox):
#        pass
#    def removesource(self, postbox):
#        pass        
    
    
class realsink(list):
    pass
#    def addsource(self, postbox):
#        pass
#    def removesource(self, postbox):
#        pass        


class postbox(object):
    def __init__(self, storage, notify=None):
        super(postbox,self).__init__()
        self.storage = storage
        self.sink = self.storage
        self.notify = notify
#        self.sources = []
#        self.addsource = self.sources.append
#        self.removesource = self.sources.remove
        
    def append(self, data):
        if self.notify:
            self.notify()
        return self.sink.append(data)
    
    def __len__(self):
        return len(self.sink)

    def pop(self,index):
        return self.sink.pop(index)
     
    def retarget(self, newtarget=None):
#         self.sink.removesource(self)
        if newtarget==None:
            self.sink = self.storage
        else:
            self.sink = newtarget
#            while len(self.storage):
#                self.sink.append( self.storage.pop(0) )
#         self.sink.addsource(self)



def makeInbox(notify):
    return postbox(storage=realsink(), notify=notify)

def makeOutbox():
    return postbox(storage=nullsink())
