#!/usr/bin/env python
        
# test functions
from time import sleep
import sys
from Kamaelia.Apps.JsonRPC.BDJsonRPC import cb_notification, cb_request, JsonRpcTCPClient, RequestOrNotification, ResponseCallback
from Axon.Handle import Handle

def ho_hum():
    return 'twiddle dumb'

def request_result(x):
    print '*** Request result: ', x
    
def progress_callback(progress):
    print '*** Progress: ', progress

if __name__=='__main__':
    HOSTNAME = 'localhost'
    PORTNUMBER = 12345
    
    client = JsonRpcTCPClient(host = HOSTNAME, portnumber = PORTNUMBER, debug = 1)
    client.add_function(progress_callback)
    
    # requests on connect
    ##req = RequestOrNotification('long_calc', params = (100, 'progress_callback'), response_callback = ResponseCallback(callback_func = request_result))
    ##client.add_request_on_connect(req, wait=False)
    ##req = RequestOrNotification('double', params = (50,), response_callback = ResponseCallback(callback_func = request_result))
    ##client.add_request_on_connect(req, wait = True)
    ##req = RequestOrNotification('foo', params = {'callback': 'progress_callback' },  response_callback = ResponseCallback(callback_func = request_result))
    ##client.add_request_on_connect(req, wait = False)
    ##req = RequestOrNotification('bar', params = (3, ), response_callback = ResponseCallback(callback_func = request_result))    
    ##client.add_request_on_connect(req)
    
    client.start()
    connection = None
    counter = 0
    while 1:
        counter += 1
        if len(client.jsonprotocol.connections) > 0 and not connection:
            print 'Got connection'
            connection = client.jsonprotocol.connections[0]
            repr(connection)
        sys.stdout.write('.' + str(counter))
        sys.stdout.flush()
        sleep(1)
        if counter == 2:
            print 'Sending request'
            req = RequestOrNotification('double', params = (3.142,), response_callback = ResponseCallback(callback_func = request_result))            
            h = Handle(connection)
            #h.activate()
            h.put(req, 'request')

