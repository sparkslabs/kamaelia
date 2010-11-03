#!/usr/bin/env python
        
# test functions
from time import sleep
from Kamaelia.Apps.JsonRPC.BDJsonRPC import cb_notification, cb_request, JsonRpcTCPServer, RequestOrNotification
import threading

def double(x):
    return x*2
@cb_notification('callback')
def long_calc(x, callback = None):
    for percent in range(1, 101):
        if callback and (percent % 10) == 0:
            params = {'progress': 'Got to %s percent' % percent }
            callback(params)
        sleep(0.1)
    return x*10

def request_received(x):
    print '*** Request received: ', x
@cb_request('item_callback', request_received)
def get_items(item_callback):
    items = {1 : 'one', 2 : 'two', 3: 'three'}
    for item_num, value in items.items():
        params = (item_num, value)
        item_callback(params)
    return (200, 'All Sent')

class Foo(object):
    def __init__(self, mydata):
        self.data = mydata
    @cb_notification('callback')
    def foo(self, callback = None):
        this_thread = threading.currentThread()
        print 'Runing foo in thread %s' % this_thread.getName()
        for n in range(10):
            marker = ('foo %s' % n, )
            if callback:
                callback(marker)
            else:
                print marker[0]
            sleep(1)
        return self.data
    def bar(self, x):
        this_thread = threading.currentThread()
        print 'Runing bar in thread %s' % this_thread.getName()
        for n in range(10):
            print 'bar %s' % n
            sleep(1)        
        return self.data * x
    

if __name__=='__main__':
    PORTNUMBER = 12345
    
    server = JsonRpcTCPServer(PORTNUMBER, debug = 1)
    server.add_function(double)
    server.add_function(long_calc)
    server.add_function(get_items)
    f = Foo('abc')
    server.add_instance(f)
    
    ### requests on connect
    ##start_req = RequestOrNotification('ho_hum', response_callback=request_received)
    ##server.add_request_on_connect(start_req, wait = True)
    ##next_req = RequestOrNotification('foo_bar')
    ##server.add_request_on_connect(next_req)
    server.start()  # does not return
