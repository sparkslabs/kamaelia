#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
'''
Bi-directional JsonRPC Server and Client for Kamaelia.

Copyright (c) 2009 Rasjid Wilcox and CDG Computer Services.
Licensed to the BBC under a Contributor Agreement
'''
raise NotImplementedError("Slated for removal since depends on jsonrpc")

import Axon
from Axon.Handle import Handle
from Axon.background import background
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Kamaelia.Chassis.ConnectedServer import ServerCore
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Internet.TCPClient import TCPClient

from jsonrpc import JsonRpc20, RPCFault, METHOD_NOT_FOUND, INTERNAL_ERROR, ERROR_MESSAGE, REQUEST, RESPONSE, ERROR, json_split

from traceback import format_exc
from collections import defaultdict
import types, inspect, Queue

# FIXME: add protection from Denial of Service

# decorators to mark funcation args as either
# callback requests or callback notifications
def cb_request(arg_name, response_func, convert_args = False):
    def cb_request_dec(func):
        if not hasattr(func, '_callbacks_'):
            func._callbacks_ = {}
        if response_func:
            func._callbacks_[arg_name] = ResponseCallback(response_func, convert_args)
        else:
            func._callbacks_[arg_name] = None
        return func
    return cb_request_dec
    
def cb_notification(arg_name):
    return cb_request(arg_name, None)

class ResponseCallback(object):
    def __init__(self, callback_func, convert_args = False):
        '''if convert_args then convert a list, tuple or dict to args in standard jsonrpc way'''
        self.callback_func = callback_func
        self.convert_args = convert_args

class RequestOrNotification(object):
    'If response_callback is None, then this is a notification'
    def __init__(self, method, params = None, response_callback = None):
        if response_callback: assert isinstance(response_callback, ResponseCallback)
        self.method = method
        self.params = params
        self.response_callback = response_callback

class JsonRpcProtocol(object):
    'Protocol Factory for JsonRpc over TCP'
    def __init__(self, task_runner, id_prefix = 'server', debug = 0):
        self.task_runner = task_runner
        self.id_prefix = id_prefix
        self.debug = debug

        self.dispatch_table = {}
        self.callback_table = defaultdict(dict)  # try key on actual function
        self.requests_on_connect = []
        self.requests_on_connect_wait = None  # id of request to wait for before sending next
        self.requests_sent = {}
        self._request_id_num = 1
        self.connections = []
    def get_request_id(self, request):
        req_num = self._request_id_num
        if self.id_prefix:
            request_id = '%s-%s' % (self.id_prefix, req_num)
        else:
            request_id = req_num
        assert isinstance(request, RequestOrNotification)
        self.requests_sent[request_id] = request.response_callback
        if request.response_callback:
            self.add_callbacks(request.response_callback)
        self._request_id_num += 1
        return request_id
    def add_callbacks(self, function):
        if function in self.callback_table:
            # already in callback table, so just return
            return
        if hasattr(function, '_callbacks_'): # 'response_callback'):
            for arg_name, response_callback  in function._callbacks_.items():
                name = function.__name__
                self.callback_table[function][arg_name] = response_callback
                print ('Added callback for method %s, argument %s' % (name, arg_name))
                try:
                    # args by position - offset needed for instance methods etc
                    offset = 1 if (hasattr(function, 'im_self') and function.im_self) else 0                    
                    arg_num = inspect.getargspec(function)[0].index(arg_name) - offset
                    self.callback_table[function][arg_num] = response_callback
                    print ('Added callback for method %s, arg_num %s' % (name, arg_num))
                except ValueError:
                    print ('WARNING: unable to determine argument position for callback on method %s, argument %s.\n' \
                          'Automatic callback conversion will not occur if called by position.' % (name, arg_name) )
    def add_function(self, function, name = None):
        if name is None:
            name = function.__name__
        if name in self.dispatch_table:
            raise ValueError('rpc method %s already exists!' % name)
        self.dispatch_table[name] = function
        print ('Added rpc method %s' % name)
        self.add_callbacks(function)
    def add_instance(self, instance, prefix = None):
        '''Add all callable attributes of an instance not starting with '_'.
        If prefix is none, then the rpc name is just <method_name>,
        otherwise it is '<prefix>.<method_name>
        '''
        for name in dir(instance):
            if name[0] != '_':
                func = getattr(instance, name, None)
                if type(func) == types.MethodType:
                    if prefix:
                        rpcname = '%s.%s' % (prefix, func.__name__)
                    else:
                        rpcname = func.__name__
                    self.add_function(func, name = rpcname)
    def add_request_on_connect(self, req_or_notification, wait = True):
        self.requests_on_connect.append( (req_or_notification, wait) )
    def __call__(self, **kwargs):
        if self.debug >= 1:
            print ('Creating new Protocol Factory: ', str(kwargs))
        connection = Graphline( SPLITTER = JsonSplitter(debug = self.debug, factory = self, **kwargs), 
                          DESERIALIZER = Deserializer(debug = self.debug, factory = self, **kwargs),
                          DISPATCHER = Dispatcher(debug = self.debug, factory = self, **kwargs),
                          RESPONSESERIALIZER = ResponseSerializer(debug = self.debug, factory = self, **kwargs),
                          REQUESTSERIALIZER = RequestSerializer(debug = self.debug, factory = self, **kwargs),
                          FINALIZER = Finalizer(debug = self.debug, factory = self, **kwargs),
                          TASKRUNNER = self.task_runner,
                          linkages = { ('self', 'inbox') : ('SPLITTER', 'inbox'),
                                       ('self', 'request') : ('REQUESTSERIALIZER', 'request'),
                                       ('SPLITTER', 'outbox') : ('DESERIALIZER', 'inbox'),
                                       ('DESERIALIZER', 'outbox'): ('DISPATCHER', 'inbox'),
                                       ('DESERIALIZER', 'error'): ('RESPONSESERIALIZER', 'inbox'),                                        
                                       ('DISPATCHER', 'outbox') : ('TASKRUNNER', 'inbox'),
                                       ('DISPATCHER', 'result_out') : ('RESPONSESERIALIZER', 'inbox'),
                                       ('DISPATCHER', 'request_out') : ('REQUESTSERIALIZER', 'request'),
                                       ('RESPONSESERIALIZER', 'outbox') : ('self', 'outbox'),
                                       ('REQUESTSERIALIZER', 'outbox'): ('self', 'outbox'),
                                        
                                       ('self', 'control') : ('SPLITTER', 'control'),
                                       ('SPLITTER', 'signal') : ('DESERIALIZER', 'control'),
                                       ('DESERIALIZER', 'signal'): ('DISPATCHER', 'control'),
                                       ('DISPATCHER', 'signal') : ('RESPONSESERIALIZER', 'control'),
                                       ('RESPONSESERIALIZER', 'signal') : ('REQUESTSERIALIZER', 'control'),                                        
                                       ('REQUESTSERIALIZER', 'signal') : ('FINALIZER', 'control'),
                                       ('FINALIZER', 'signal') : ('self', 'signal'),
                                        
                                       ('DISPATCHER', 'wake_requester') : ('REQUESTSERIALIZER', 'control'),
                                    } )
        self.connections.append(connection)
        return connection
    
class JsonSplitter(Axon.Component.component):
    Inboxes = { 'inbox': 'accepts arbitrary (sequential) pieces of json stings',
                'control': 'incoming shutdown requests' }
    Outboxes = { 'outbox': 'a single complete json string',
                 'signal': 'outgoing shutdown requests' }
    def __init__(self, **kwargs):
        super(JsonSplitter, self).__init__(**kwargs)
        self.partial_data = ''
        if self.debug >= 3: print ('Created %s' % repr(self))
    def main(self):
        while not self.shutdown():
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                if self.debug >= 4: print ('Got data: <<%s>>' % data)
                Json_strings, self.partial_data = json_split(self.partial_data + data)
                yield 1
                # send to dispatch
                for message in Json_strings:
                    if self.debug >= 3: print ('Sent to deserializer: %s' % message)
                    self.send(message, 'outbox')
                    yield 1
            if not self.anyReady():
                self.pause()
            yield 1
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                self.send(msg, 'signal')
                return True
            return False
        
class Deserializer(Axon.Component.component):
    Inboxes = {'inbox': 'complete json strings',
               'control': 'shutdown messages',
              }
    Outboxes = {'outbox': 'the deserialized request/notification or result',
                'error':  'the exception if there was an error deserializing',
                'signal': 'shutdown messages',
               }
    def __init__(self, **kwargs):
        super(Deserializer, self).__init__(**kwargs)
        self.serializer = JsonRpc20()  # FIXME: make this a paramater
        if self.debug >= 3: print ('Created %s' % repr(self))
    def main(self):
        while not self.shutdown():
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                if self.debug >=1: print ('--> %s' % data)
                try:
                    request = self.serializer.loads_request_response(data)
                    self.send(request, 'outbox')
                except RPCFault:
                    error = sys.exc_info()[1]
                    self.send( (error, None), 'error')
            if not self.anyReady():
                self.pause()                
            yield 1
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                self.send(msg, 'signal')
                return True
            return False
    
class CallbackProxy(object):
    def __init__(self, method_name, response_callback):
        self.method_name = method_name
        self.response_callback = response_callback
        self.params = None
        self.component = None
        self.outbox_name = None
    def set_outbox(self, component, outbox_name):
        self.component = component
        self.outbox_name = outbox_name
    def __call__(self, params = None):
        if not self.component or not self.outbox_name:
            raise ValueError('component or outbox_name not set')
        req = RequestOrNotification(self.method_name, params, self.response_callback)
        self.component.send(req, self.outbox_name)                    
        
class Dispatcher(Axon.Component.component):
    Inboxes = {'inbox': 'rpc request/notification or response objects',
               'result_in': 'the function/method result or RequestOrNotification',
               'control': 'shutdown messages',
              }
    Outboxes = {'outbox': '(return_component, method, args, id) tuple for the worker.  NOTE: return_component == (self, <boxname>)',
                'result_out': 'the result of the request (relayed from result_in)',
                'request_out': 'requests from callback functions',
                'signal': 'shutdown messages',
                'wake_requester': 'wake up RequestSerializer',
               }    
    def __init__(self, **kwargs):
        super(Dispatcher, self).__init__(**kwargs)
        if self.debug >= 3: print ('Created %s' % repr(self))
    def _do_dispatch(self, dispatch_func, args, id, notification, convert_args = True):
        'Assumes args is always a list, tuple or dict'
        kwargs = {}
        if convert_args:
            if isinstance(args, dict):
                # args by name
                args, kwargs = [], args
                # find any callback args and replace with callback proxy
                for arg_name in set(self.factory.callback_table[dispatch_func].keys()).intersection(set(kwargs.keys())):
                    kwargs[arg_name] = CallbackProxy(kwargs[arg_name], self.factory.callback_table[dispatch_func][arg_name])
            else:
                arg_nums = range(len(args))
                for arg_num in set(self.factory.callback_table[dispatch_func].keys()).intersection(set(arg_nums)):                        
                    args[arg_num] = CallbackProxy(args[arg_num], self.factory.callback_table[dispatch_func][arg_num])
        else:
            args = [args]
        return_box = (self, 'result_in')
        dispatch_info = (dispatch_func, args, kwargs)
        return_info = (id, notification)
        if self.debug >= 3: print ('Sending: %r\n%r\n%r' % (return_box, dispatch_info, return_info))
        self.send( (return_box, dispatch_info, return_info), 'outbox')                
    def _process_request(self, request):
        if self.debug >= 3: print ('Got dispatch request: %s' % repr(request))
        notification = False
        if len(request) == 2:
            notification = True
            method, args = request
            id = None
        else:
            method, args, id = request
        if not notification and method not in self.factory.dispatch_table:
            response = ( RPCFault(METHOD_NOT_FOUND, ERROR_MESSAGE[METHOD_NOT_FOUND]), id)
            self.send(response, 'result_out')
        else:
            dispatch_func = self.factory.dispatch_table[method]
            self._do_dispatch(dispatch_func, args, id, notification)
    def _process_response(self, response):
        print ('=== Response: %s ===' % repr(response))
        result, id = response
        response_callback = None
        if id == self.factory.requests_on_connect_wait:
            self.factory.requests_on_connect_wait = None  # clear waiting on this request
            if len(self.factory.requests_on_connect):
                self.send(Axon.Ipc.notify(self, id), 'wake_requester')  # wake requester so it can send pending requests
        # look up response callback
        try:
            response_callback = self.factory.requests_sent.pop(id)
            assert isinstance(response_callback, ResponseCallback)
        except KeyError:
            print ('ERROR: Invalid response id %s' % id)
        if result is None:
            return
        if response_callback.convert_args and type(result) not in (types.ListType, types.TupleType, types.DictionaryType):
            print ("ERROR: Can't convert response result to procedure argments - must be List, Tuple or Dict")
            return
        if not response_callback:
            print ('ERROR: Got result for a notification or request with no callback defined')
        else:
            self._do_dispatch(response_callback.callback_func, result, id, True, convert_args = response_callback.convert_args)  # not really a notification - but we don't return a response to a response
    def main(self):
        while not self.shutdown():
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                if data[0] == REQUEST:
                    request = data[1]
                    self._process_request(request)
                elif data[0] == RESPONSE:
                    # got a response to a request we sent
                    response = data[1]
                    self._process_response(response)
                elif data[0] == ERROR:
                    # FIXME: handle error responses
                    print ('!!! GOT ERROR RESPONSE: %s' % repr(data[1]))
                else:
                    # FIXME
                    print ('INTERNAL ERROR: Unexpected message type')
            if self.dataReady('result_in'):
                data = self.recv('result_in')
                result, (id, notification) = data
                if isinstance(result, RequestOrNotification):
                    if self.debug >= 3: print ('Got RequestOrNotification: %s' % result)
                    self.send(result, 'request_out')
                else:
                    if self.debug >= 2: print ('Got result for id %s:\n  %s' % (id, repr(result)))
                    if not notification:
                        self.send((result, id), 'result_out')
            if not self.anyReady():
                self.pause()
            yield 1                
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                self.send(msg, 'signal')
                return True
            return False
                    
class ResponseSerializer(Axon.Component.component):
    Inboxes = {'inbox': '(result, id) tuple',
               'control': 'shutdown messages',
              }
    Outboxes = {'outbox': 'the json-rpc response',
                'signal': 'shutdown messages',
               }    
    def __init__(self, **kwargs):
        super(ResponseSerializer, self).__init__(**kwargs)
        self.serializer = JsonRpc20()  # FIXME: make this a paramater
        if self.debug >= 3: print ('Created %s' % repr(self))
    def main(self):
        while not self.shutdown():
            if self.dataReady('inbox'):
                result, id = self.recv('inbox')
                if self.debug >= 3: print ('Got result. Id: %r, Value: %r' % (id, result))
                if isinstance(result, RPCFault):
                    response = self.serializer.dumps_error( result, id)
                elif isinstance(result, Exception):
                    # procedure exception - FIXME: log to logger!
                    print (format_exc())
                    response = self.serializer.dumps_error( RPCFault(INTERNAL_ERROR, ERROR_MESSAGE[INTERNAL_ERROR]), id )
                else:                    
                    try:
                        response = self.serializer.dumps_response(result, id)                                       
                    except RPCFault:
                        e = sys.exc_info()[1]
                        response = self.serializer.dumps_error( e, id)
                        # serialization error - log to logger!
                        print (format_exc())
                        response = self.serializer.dumps_error( RPCFault(INTERNAL_ERROR, ERROR_MESSAGE[INTERNAL_ERROR]), id )
                response += '\r\n'  # make things easier to read if testing with telnet or netcat
                if self.debug >= 1:
                    print ('<-- %s' % response)
                self.send(response, 'outbox')
            if not self.anyReady():
                self.pause()
            yield 1
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                self.send(msg, 'signal')
                return True
            return False

class RequestSerializer(Axon.Component.component):
    Inboxes = {'inbox': 'not used',
               'request' : 'incoming RequestOrNotification objects',
               'control': 'wakeup & shutdown messages',
              }
    Outboxes = {'outbox': 'the json-rpc request / notification',
                'signal': 'shutdown messages',
               }    
    def __init__(self, **kwargs):
        super(RequestSerializer, self).__init__(**kwargs)
        self.serializer = JsonRpc20()  # FIXME: make this a paramater
        if self.debug >= 3: print ('Created %s' % repr(self))
    def _send_req_or_notification(self, req, wait = False):
        assert isinstance(req, RequestOrNotification)
        if req.response_callback:
            id = self.factory.get_request_id(req)  # this adds the id to self.requests_sent
            if wait:
                self.factory.requests_on_connect_wait = id
            output = self.serializer.dumps_request(req.method, req.params, id) if req.params \
                    else self.serializer.dumps_request(req.method, id = id)
        else:                    
            output = self.serializer.dumps_notification(req.method, req.params) if req.params \
                else self.serializer.dumps_notification(req.method)
        output += '\r\n'  # make things easier to read if testing with telnet or netcat
        if self.debug >= 1: print ('<-- %s' % output)
        self.send(output, 'outbox')        
    def main(self):
        while not self.shutdown():
            if len(self.factory.requests_on_connect) and not self.factory.requests_on_connect_wait:
                request, wait = self.factory.requests_on_connect.pop(0)
                self._send_req_or_notification(request, wait)
            if self.dataReady('request'):
                req = self.recv('request')
                self._send_req_or_notification(req)
            if not self.anyReady() and (len(self.factory.requests_on_connect) == 0 or self.factory.requests_on_connect_wait) :
                self.pause()
            yield 1
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                self.send(msg, 'signal')
                return True
            return False

class Finalizer(Axon.Component.component):
    Inboxes = {'inbox': 'not used',
               'control': 'shutdown messages',
              }
    Outboxes = {'outbox': 'not used',
                'signal': 'shutdown messages',
               }    
    def __init__(self, **kwargs):
        super(Finalizer, self).__init__(**kwargs)
        if self.debug >= 3: print ('Created %s' % repr(self))
    def main(self):
        while not self.shutdown():
            if not self.anyReady():
                self.pause()
            yield 1
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                # FIXME: Log any outstanding request reponses missing
                print ('Connection is being closed')
                for req_id in self.factory.requests_sent:
                    print ('WARNING: No response seen to request %s' % req_id)
                self.send(msg, 'signal')
                return True
            return False
        
        
# -------------------------------------------        
        
def ThreadedTaskRunner(num_workers = 5, debug = 0):
    worker_list = []
    for dummy in range(num_workers):
        worker = ThreadedWorker(debug = debug)
        worker.activate()
        worker_list.append(worker)
    manager = TaskManager(worker_list, debug = debug)
    return manager

class ThreadedWorker(Axon.ThreadedComponent.threadedcomponent):
    Inboxes = {'inbox': '(function, args, kwargs) tuple',
               'control': 'shutdown messages',
              }
    Outboxes = {'outbox': 'the result or exception or callback request',
                'signal': 'shutdown messages',
               }
    def __init__(self, **kwargs):
        super(ThreadedWorker, self).__init__(**kwargs)
        if self.debug >= 3: print ('Created %s' % repr(self))
    def main(self):
        while not self.shutdown():
            if self.dataReady('inbox'):
                func, args, kwargs = self.recv('inbox')
                for arg in args:
                    if isinstance(arg, CallbackProxy):
                        arg.set_outbox(self, 'outbox')
                for arg_name in kwargs:
                    if isinstance(kwargs[arg_name], CallbackProxy):
                        kwargs[arg_name].set_outbox(self, 'outbox')
                if self.debug >= 3: print ('Worker %s got data: %r, %r, %r' % (id(self), func, args, kwargs))
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    error = sys.exc_info()[1]
                    result = error
                if self.debug >= 3: print ('Worker %s got result: %r' % (id(self), result))
                self.send(result, 'outbox')
            if not self.anyReady():
                self.pause()
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                self.send(msg, 'signal')
                return True
            return False

        
class TaskManager(Axon.AdaptiveCommsComponent.AdaptiveCommsComponent):
    Inboxes = {'inbox': '(return_box, dispatch_info, return_info) tuple',
               'control': 'shutdown messages',
              }
    Outboxes = {'outbox': 'not used',
                'signal': 'shutdown messages',
               }
    '''    
    return_box = (<sending_component>, <return_box_name>)
    dispatch_info = (self.factory.dispatch_table[method], args, kwargs)
    return_info = (id, notification)
    '''
    def __init__(self, workers, debug = 0):
        super(TaskManager, self).__init__()
        self.debug = debug
        self.workers = workers  # a list of worker components
        self.task_data = [ None for x in range(len(workers)) ]  # an available worker has None here
        self.work_queue = []
        self.worker_box_names = []
        self.links = []
        # make connections to the workers
        for worker_num in range(len(self.workers)):
            outbox_name = self.addOutbox('to_worker_%s' % worker_num)
            inbox_name = self.addInbox('from_worker_%s' % worker_num)
            signal_name = self.addOutbox('signal_worker_%s' % worker_num)
            boxnames = {'to': outbox_name, 'from': inbox_name, 'signal': signal_name}
            self.worker_box_names.append(boxnames)
            outlink = self.link((self, outbox_name), (self.workers[worker_num], 'inbox'))
            control_link = self.link((self, signal_name), (self.workers[worker_num], 'control'))
            inlink = self.link((self.workers[worker_num], 'outbox'), (self, inbox_name))
            self.links.append((outlink, control_link, inlink))
        if self.debug >= 3: print ('Created %s' % repr(self))
    def main(self):
        while not self.shutdown():
            if self.dataReady('inbox'):
                data = self.recv('inbox')
                if self.debug >= 3: print ('Task Manager got data: %s' % repr(data))
                self.work_queue.append(data)
            if len(self.work_queue) != 0 and None in self.task_data:
                return_box, dispatch_info, return_info = self.work_queue.pop(0)
                result_box_name = self.addOutbox('%s-%s-%s' % (id(return_box), id(dispatch_info), id(return_info)))
                self.link((self, result_box_name), return_box)
                worker_num = self.task_data.index(None) # pick the first free worker
                self.task_data[worker_num] = (result_box_name, return_box, return_info)
                if self.debug >= 3:
                    print ('Sending task data to worker %s (box %s)' % (worker_num, self.worker_box_names[worker_num]['to']))
                    print ('Dispatch:', dispatch_info)
                self.send(dispatch_info, self.worker_box_names[worker_num]['to'])
            if self.anyReady():
                for worker_num in range(len(self.workers)):
                    boxname = self.worker_box_names[worker_num]['from']
                    if self.dataReady(boxname):
                        data = self.recv(boxname)
                        if self.debug >= 3: print ('TaskManager got data %r on boxname %s' % (data, boxname))
                        result_box_name, return_box, return_info = self.task_data[worker_num]
                        self.send( (data, return_info), result_box_name)  # post the result
                        if not isinstance(data, RequestOrNotification):
                            if self.debug >= 3: print ('** Doing unlink ** on %s' % result_box_name)
                            self.unlink( (self, result_box_name), return_box) 
                            self.deleteOutbox(result_box_name)
                            self.task_data[worker_num] = None  # mark that worker as done
                    yield 1
            if not self.anyReady():
                self.pause()
            yield 1
        if self.debug >= 3:
            print ('End of main for %s' % self.__class__.__name__)
    def shutdown(self):
        if self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                if self.debug >= 3: print ('%s got shutdown msg: %r' % (self.__class__.__name__, msg))
                for boxnames in self.worker_box_names:
                    self.send(msg, boxnames['signal'])
                self.send(msg, 'signal')
                return True
            return False
    
class JsonRPCBase(object):
    'Base class for JsonRPC clients and servers'
    def __init__(self, workers, debug):
        self.workers = workers
        self.debug = debug
        taskrunner = ThreadedTaskRunner(num_workers = self.workers, debug = self.debug)
        self.jsonprotocol = JsonRpcProtocol(taskrunner, debug = self.debug)
    def add_function(self, func):
        self.jsonprotocol.add_function(func)
    def add_instance(self, instance):
        self.jsonprotocol.add_instance(instance)
    def add_request_on_connect(self, req_or_notification, wait = True):
        self.jsonprotocol.add_request_on_connect(req_or_notification, wait)
        
class JsonRpcTCPServer(JsonRPCBase):
    def __init__(self, portnumber, workers = 5, debug = 1):
        JsonRPCBase.__init__(self, workers = workers, debug = debug)
        self.portnumber = portnumber
        self.server = None
    def start(self):
        if self.debug: print ('Starting JSON-RPC server on port %s' % self.portnumber)
        self.server = ServerCore( protocol = self.jsonprotocol, port = self.portnumber )
        self.server.run()
    #FIXME: some way to stop!        
    
        
class JsonRpcTCPClient(JsonRPCBase):
    def __init__(self, host, portnumber, delay = 0, workers = 5, debug = 1):
        JsonRPCBase.__init__(self, workers = workers, debug = debug)
        self.host = host
        self.portnumber = portnumber
        self.delay = delay
        self.client = Graphline(
            TCPCLIENT = TCPClient(self.host, self.portnumber, self.delay),
            PROTOCOL = self.jsonprotocol(),
            linkages = { ('TCPCLIENT', 'outbox') : ('PROTOCOL', 'inbox'),
                         ('PROTOCOL', 'outbox') : ('TCPCLIENT', 'inbox'),                          
                         ('TCPCLIENT', 'signal') : ('PROTOCOL', 'control'),
                         ('PROTOCOL', 'signal') : ('TCPCLIENT', 'control'), 
                        } )
        self.handle = Handle(self.client)
    def start(self):
        if self.debug: print ('Starting TCP Client - connecting to %s on port %s' % (self.host, self.portnumber))
        ##self.client.run()
        try:
            background().start()
        except:
            pass  # assume already running
        self.client.activate()
        
class Proxy(object):
    def __init__(self, host, portnumber, delay = 0, threaded = True, workers = 5, debug = 1):
        self.host = host
        self.portnumber = portnumber
        self.delay = delay
        self.threaded = threaded
        self.workers = workers
        self.debug = debug
        self.client = JsonRpcTCPClient(host = host, portnumber = portnumber, delay = delay, threaded = True, workers = workers,
                                                        debug = debug)
        self.request = RequestProxy(self.client, True)
        self.notification = RequestProxy(self.client, False)
        
class RequestProxy(object):
    def __init__(self, client, request = True):
        self.client = client
        self.request = request
    def _remote_call(self, name, params):
        client = self.client
    
