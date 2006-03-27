#!/usr/bin/env python


class nullsink(object):
    def __init__(self):
        super(nullsink,self).__init__()
    def append(self, data):
        pass
    def __len__(self):
        return 0
    def pop(self,index):
        raise IndexError("nullsink: You can't pop from an empty piece of storage!")
    
    
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
        self.retarget()
    
    def __len__(self):
        return self.__len__()

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
            # if i'm storing stuff, pass it on
            while len(self.storage):
                self.sink.append(self.storage.pop(0))
        # make calling these methods go direct to the sink
        self.append  = self.sink.append
        self.pop     = self.sink.pop
        self.__len__ = self.sink.__len__
        # propagate the change back up the chain
        for source in self.sources:
            source.retarget(newtarget=self.sink)



def makeInbox(notify):
    return postbox(storage=realsink(notify=notify))


thenullsink = nullsink()

def makeOutbox():
    return postbox(storage=thenullsink)
