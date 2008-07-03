#!/usr/bin/env python
import Axon
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent

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
            self.Protocol()
        except TypeError:
            raise BadProtocol('ProtocolManager.Protocol is not callable.')
        
    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    not_done = False
                    
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                
        
class BadProtocol(Exception): pass
