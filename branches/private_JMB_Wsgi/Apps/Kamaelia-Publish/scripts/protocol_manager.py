#!/usr/bin/env python
import re
from pprint import pprint, pformat
from xml.sax.saxutils import escape

import Axon
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline

from headstock.api.message import Message

class ProtocolManager(AdaptiveCommsComponent):
    """
    This component serves as an adapter to allow a protocol that can be used with
    ServerCore to be used with a headstock handler.
    """
    Inboxes={
        'inbox' : 'A headstock.api.contact.Message instance to process', #for HTTP, this is where the request comes in
        'control' : 'Receive shutdown messages'
    }
    Outboxes={
        'outbox' : 'A headstock.api.contact.Message instance to be sent', #for HTTP, this is the response
        'signal' : 'Send shutdown messages',
        'log' : 'Send messages to the chat log',
    }
    Protocol=None
    LineEnding='\r\n'
    def __init__(self, **argd):
        super(ProtocolManager, self).__init__(**argd)
        if not self.Protocol:
            raise BadProtocol('You must specify a protocol to use the Protocol Manager!')
        try:
            self.Protocol()
        except TypeError:
            raise BadProtocol('ProtocolManager.Protocol is not callable.')
        
        self.tracked_components = {}
        self.marked_components = set()
        
    def main(self):
        self.not_done = True
        while self.not_done:
            [self._processMainInbox(msg) for msg in self.igetInbox('inbox') if msg.bodies]
            self._processProtocols()
                        
            if not self.anyReady() and self.not_done:
                self.pause()
                
            yield 1
            [self._processMainControlBox(msg) for msg in self.igetInbox('control')]
                
    def _processMainInbox(self, msg):
        protocol_component = self.Protocol(peer=msg.from_jid)
        protocol_component.activate()
        out_boxname = self.addOutbox("out_%s" % (protocol_component.name))
        #print 'added ' + out_boxname
        sig_boxname = self.addOutbox("sig_%s" % (protocol_component.name))
        #print 'added ' + sig_boxname
        in_boxname = self.addInbox("in_%s" % (protocol_component.name))
        #print 'added ' + in_boxname
        ctl_boxname = self.addInbox("ctl_%s" % (protocol_component.name))
        #print 'added ' + ctl_boxname

        tracked_data =  {'in' : in_boxname,
                         'ctl' : ctl_boxname,
                         'out' : out_boxname,
                         'sig' : sig_boxname,
                         'msg' : msg,}

        self.tracked_components[protocol_component.name] = tracked_data

        self.link((self, out_boxname), (protocol_component, 'inbox'))
        self.link((protocol_component, 'outbox'), (self, in_boxname))
        self.link((protocol_component, 'signal'), (self, ctl_boxname))
    
        request = self.normalizeMsgBodies(msg)
        #printable_request = request.replace('\r\n', '\\r\\n\n')
        #print 'received ' + printable_request
        #
        

        self.send(request, out_boxname)
        self.send(producerFinished(self), sig_boxname)
        
    def _processMainControlBox(self, msg):
        msg = self.recv('control')
        if isinstance(msg, (producerFinished, shutdownMicroprocess)):
            self.not_done = False
            
    def _processProtocols(self):        
        for proto_name in self.tracked_components:
            proto_data = self.tracked_components[proto_name]
            #print 'processing ' + proto_data['in']
            #print 'box contents: '
            #pprint(self.inboxes[proto_data['in']])
            self._processProtoInbox(proto_data['in'], proto_data['msg'])
            #print 'processing ' + proto_data['ctl']
            #print 'box contents: '
            #pprint(self.inboxes[proto_data['ctl']])
            self._processProtoControl(proto_data['ctl'], proto_name)
            
        self._clearMarkedComponents()
            
    def _processProtoInbox(self, boxname, orig_msg):
        for msg in self.igetInbox(boxname):
            #print 'proto_inbox received "%s"' % (msg)
            #print 'boxname=' + boxname
            #print 'orig_msg=' + repr(orig_msg)
            msg = normalizeXML(msg)
            out = u'%s %s' % (orig_msg.from_jid, msg)
            self.send(out, 'outbox')
            
    def _processProtoControl(self, boxname, proto_name):
        for msg in self.igetInbox(boxname):
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                self.marked_components.add(proto_name)
                #print 'marking %s' % (repr(proto))
            
    def _clearMarkedComponents(self):
        #pprint(self.tracked_components)
        #pprint(self.marked_components)
        for proto in self.marked_components:
            #print 'clearing %s' % (repr(proto))
            data = self.tracked_components[proto]
            self.unlink(proto)
            self.deleteInbox(data['in'])
            self.deleteInbox(data['ctl'])
            self.deleteOutbox(data['out'])
            del self.tracked_components[proto]
            
        self.marked_components.clear()
    
    def igetInbox(self, name='inbox'):
        while self.dataReady(name):
            yield self.recv(name)
            
    _CRLF_re = re.compile('(?<!\r)\n')
    def normalizeMsgBodies(self, msg):
        buffer = [str(body) for body in msg.bodies]
        buffer = ''.join(buffer)
        text = self._CRLF_re.sub(self.LineEnding, buffer)
        if not text.endswith(self.LineEnding):
            text += self.LineEnding
            
        return text
                
def normalizeXML(text=''):
    text = text.encode('utf-8')
    return escape(text)

class Echoer(component):
    request = None
    def __init__(self, request, **argd):
        super(Echoer, self).__init__(**argd)
        self.request = request
        
    def main(self):                
        #response = pformat(self.request)
        response = u'Hello, world!'
        #response = 'Hello, world!'
        #print 'Processing request!'
        #print prequest
        #print type(prequest)
        #print 'response length-', str(len(response))
        resource = {
            'statuscode' : 200,
            'headers' : [('Content-Type' , 'text/plain')],
            'charset' : 'utf-8',
            'data' : response,
        }
        
        self.send(resource)
                
        yield 1
                
        self.send(producerFinished(self), 'signal')
        
    def __repr__(self):
        return '<%s>' % (self.name)
        
class BadProtocol(Exception):
    pass
