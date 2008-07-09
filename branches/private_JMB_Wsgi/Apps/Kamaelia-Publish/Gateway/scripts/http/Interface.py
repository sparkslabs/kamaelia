#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: JMB

from Axon.Component import component
from Axon.Ipc import producerFinished
from jabber.Interface import BoxBundle

from pprint import pformat

class HTTPInterface(component):
    Inboxes = {'inbox' : 'Receive body chunks from the HTTPServer',
               'control' : 'Receive producerFinished messages from the HTTPServer',
               'xmpp_inbox' : 'Receive input from the XMPPInterface',
               'xmpp_control' : 'Receive signals from XMPPInterface'}
    Outboxes = {'outbox' : 'Send output to the HTTPServer',
                'signal' : 'Send shutdownMicroprocess and producerFinished messages to HTTPServer',
                'xmpp_outbox' : 'Send data to XMPPInterface',
                'xmpp_signal' : 'Send producerFinished to XMPPInterface'}
    def __init__(self, request, **argd):
        self.request = request
        super(HTTPInterface, self).__init__(**argd)
        
    def main(self):       
        text = self.reconstructHTTPHeaders(self.request)        
        
        for i in self.waitForBody():
            yield i
        text += self.body
        
        resource = {
            'headers' : [('content-type', 'text/plain')],
            'statuscode' : 200,
            'data' : text,
        }
        self.send(resource, 'outbox')
        yield 1
        self.send(producerFinished(self), 'signal')
        self.send(producerFinished(self), 'xmpp_signal')
        
    def reconstructHTTPHeaders(self, request):
        request_line = "%s %s %s/%s" % (
            request['method'],
            request['raw-uri'],
            request['protocol'],
            request['version']
        )
        
        line_buffer = [request_line]
        
        for key, value in request['headers'].iteritems():
            line_buffer.append('%s: %s' % (key, value))
            
        line_buffer.extend(['', ''])
            
        return '\r\n'.join(line_buffer)
        
    def waitForBody(self):
        """
        This internal method is used to make the WSGI Handler wait for the body
        of an HTTP request before proceeding.

        FIXME:  We should really begin executing the Application and pull the
        body as needed rather than pulling it all up front.
        """
        buffer = []     #Wait on the body to be sent to us
        not_done = True
        while not_done:
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished):
                    not_done = False

            while self.dataReady('inbox'):
                buffer.append(self.recv('inbox'))

            if not_done and not self.anyReady():
                self.pause()
                
            yield 1
        self.body = ''.join(buffer) + '\r\n\r\n'
        
class getHTTPInterfaceFactory(object):
    def __init__(self, xmpp_interface):
        self.bundle_sender = component()
        self.bundle_sender.link((self.bundle_sender, 'outbox'), (xmpp_interface, 'inbox'))
        
    def __call__(self, request):
        bundle = BoxBundle()
        httpi = HTTPInterface(request)
        
        bundle.link((bundle, 'outbox'), (httpi, 'xmpp_inbox'))
        bundle.link((bundle, 'signal'), (httpi, 'xmpp_control'))
        bundle.link((httpi, 'xmpp_outbox'), (bundle, 'inbox'))
        bundle.link((httpi, 'xmpp_signal'), (bundle, 'control'))
        
        self.bundle_sender.send(bundle, 'outbox')
        
        return httpi
