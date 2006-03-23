#!/usr/bin/env python


class nullsink(object):
    def __init__(self):
        super(nullsink,self).__init__()
    def append(self, data):
        pass
    def __len__(self):
        return 0
    
    
class realsink(list):
    def __init__(self, notify):
        super(realsink,self).__init__()
        self.notify = notify
    def append(self,data):
        list.append(self,data)
        self.notify()


class postbox(object):
    def __init__(self, storage):
        super(postbox,self).__init__()
        self.storage = storage
        self.sources = []
        self.sink = self.storage
        
    def append(self, data):
        return self.sink.append(data)
    
    def __len__(self):
        return len(self.sink)

    def pop(self,index):
        return self.sink.pop(index)
     
    def addsource(self,newsource):
        self.sources.append(newsource)       # XXX assuming not already linked from that source
        newsource.retarget(self.sink)
        
    def removesource(self,oldsource):
        self.sources.remove(oldsource)
        oldsource.retarget(newtarget=None)
        
    def retarget(self, newtarget=None):
        if newtarget==None:
            self.sink = self.storage
        else:
            self.sink = newtarget
        # propagate the change back up the chain
        for source in self.sources:
            source.retarget(newtarget=self.sink)



def makeInbox(notify):
    return postbox(storage=realsink(notify=notify))

def makeOutbox():
    return postbox(storage=nullsink())
