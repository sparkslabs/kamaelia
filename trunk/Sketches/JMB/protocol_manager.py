#!/usr/bin/env python
import Axon
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Kamaelia.Chassis.Graphline import Graphline

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
    def __init__(self, **argd):
        super(ProtocolManager, self).__init__(**argd)
        if not self.Protocol:
            raise BadProtocol('You must specify a protocol to use the Protocol Manager!')
        try:
            Protocol
        except TypeError:
            raise BadProtocol('ProtocolManager.Protocol is not callable.')
        
        self.message_store = {} #to be indexed by the outbox associated with the protocol
        
    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    not_done = False
                    
            while self.dataReady('inbox'):
                msg = self.recv('inbox')


                
                
                
    def _processMainInbox(self, msg):
        buffer = [str(body) for body in msg.bodies]
        request = ''.join(buffer)
                
        protocol_component = self.Protocol(peer=msg.sender)
        out_boxname = self.addOutbox("out_%s" % (protocol_component.name))
        in_boxname = self.addInbox("in_%s" % (protocol_component.name))
        ctl_boxname = self.addInbox("ctl_%s" % (protocol_component.name))
        
        inboxes = {'in' : in_boxname,
                   'ctl' : ctl_boxname}
        
        Graphline(
            this=self,
            proto=protocol_component,
            linkages={
                ('this', out_boxname) : ('proto', 'inbox'),
                ('proto', 'signal') : ('this', ctl_boxname),
                ('proto', 'outbox') : ('this', in_boxname)
            }
        ).activate()
        
        self.trackResourceInformation(protocol_component, inboxes, out_boxname, msg)
    
    def getInbox(self, name='inbox'):
        while self.dataReady(name):
            yield self.recv(name)
                
        
class BadProtocol(Exception): pass
