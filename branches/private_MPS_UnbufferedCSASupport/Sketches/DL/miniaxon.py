#!/usr/bin/python
# Copyright (C) 2005 British Broadcasting Corporation and Kamaelia Contributors(1)
#        All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#        http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#        not this notice.
# (2) Reproduced in the COPYING file, and at:
#        http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
#

# Following script is tested on python-2.4.3 and pycrypto-2.0.1
# It adds a new class securedComponent which is subclass of component
# All other classes are the same as explained in MiniAxon tutorial

from Crypto.Cipher import AES  

class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1

class scheduler(microprocess):

    def __init__(self):
        super(scheduler, self).__init__()
        self.active = []
        #self.queue = []
        self.newqueue = []
        
    def main(self):

        for i in range(100):
            for current in self.active:
                
                yield 1  #something ?
                try:
                    ret = current.next()
                    if ret != -1:
                        self.newqueue.append(current)
                    
                except StopIteration:
                    pass
            self.active = self.newqueue
            self.newqueue = []


    def activateMicroprocess(self, someprocess):

        ret = someprocess.main()
        self.newqueue.append(ret)


class component(microprocess):

    def __init__(self):

        super(component, self).__init__()
        self.boxes = {"inbox":[] , "outbox":[]}

    def send(self, value, boxname):

        self.boxes[boxname].append(value)

    def recv(self, boxname):

        return self.boxes[boxname].pop()

    def dataReady(self, boxname):

        return len(self.boxes[boxname])


class secureComponent(component):  # New class 

    def __init__(self):

        super(secureComponent, self).__init__()
        self.key = 'A simple testkey'
        self.crypt_obj = AES.new(self.key, AES.MODE_ECB) # Simplest mode for testing

    def send(self, value, boxname):     

        diff = len(value) % 16   # Data required in blocks of 16 bytes
        if diff is not 0:
            value = value + ( '~' * (16 - diff))  # For testing 
        
        encrypted_value = self.crypt_obj.encrypt(value)
        super(secureComponent, self).send(encrypted_value, boxname)

    def recv(self, boxname):

        encrypted_value = super(secureComponent, self).recv(boxname)
        value = self.crypt_obj.decrypt(encrypted_value)
        orig_len = value.find('~', len(value) - 16)
        value = value[0:orig_len]
        return value

class postman(microprocess):

    def __init__(self, source, sourcebox, sink, sinkbox):

        super(postman, self).__init__()
        self.source = source
        self.sourcebox = sourcebox
        self.sink = sink
        self.sinkbox = sinkbox

    def main(self):

        while 1:
            yield 1

            if self.source.dataReady(self.sourcebox):
                data = self.source.recv(self.sourcebox)
                self.sink.send(data, self.sinkbox)

#-------------------------------------------------------
# Testing

class Producer(secureComponent):

    def __init__(self, message):
        super(Producer, self).__init__()
        self.message = message

    def main(self):
        count = 0
        while 1:
            yield 1
            count += 1 
            msg = self.message + str(count)
            self.send(msg, "outbox")

class Consumer(secureComponent):

    def main(self):

        while 1:
            yield 1
            if self.dataReady("inbox"):
                data = self.recv("inbox")
                print data

p = Producer("Hello World - test ")
c = Consumer()
delivery_girl = postman(p, "outbox", c, "inbox")

myscheduler = scheduler()
myscheduler.activateMicroprocess(p)
myscheduler.activateMicroprocess(c)
myscheduler.activateMicroprocess(delivery_girl)

for _ in myscheduler.main():
    pass


## class printer(microprocess):

##     def __init__(self, string):

##         super(printer, self).__init__()
##         self.string = string  #String to be printed
        
##     def main(self):
##         while 1:
##             yield 1
##             print self.string

## X = printer("Hello World")
## Y = printer("Game Over")
## myscheduler = scheduler()
## myscheduler.activateMicroprocess(X)
## myscheduler.activateMicroprocess(Y)
## for _ in myscheduler.main():
##         pass


    
            
                
