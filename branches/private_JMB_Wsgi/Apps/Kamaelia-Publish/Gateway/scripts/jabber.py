# -*- coding: utf-8 -*-
"""
This module is a simple XMPP chat client demonstrating the use of headstock.
Many Kamaelia components are created to manage different XMPP kind of stanzas.

* RosterHandler:
  * querying the server for the roster list
  * if supported by server, asking for the last activity of each contact

* DummyMessageHandler:
  * sending a message typed into the console window
  * printing to the console any received messages

* DiscoHandler: 
  * querying for the supported features by the server
  * dispatching the result of the previous query to components interested in that event

* ActivityHandler:
  * dispatching to the RosterHandler the fact the server supports the feature

* RegisterHandler:
  * registring a new user using in-band registration if supported

The actual XMPP client is the Client component that sets up the different
dispatchers and handlers involved by liking each inbox to the expected outbox and
vcie versa.

"""
import re

from Axon.Component import component
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Backplane import Backplane
from Kamaelia.Util.Backplane import PublishTo, SubscribeTo
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleReader
from Axon.Ipc import shutdownMicroprocess, producerFinished

from Kamaelia.Util.NullSink import nullSinkComponent
from interface import Interface
    
from headstock.protocol.core.stream import ClientStream, StreamError, SaslError
from headstock.protocol.core.presence import PresenceDispatcher
from headstock.protocol.core.roster import RosterDispatcher, RosterNull
from headstock.protocol.core.message import MessageDispatcher, MessageEchoer
from headstock.protocol.extension.register import RegisterDispatcher
from headstock.protocol.extension.activity import ActivityDispatcher
from headstock.protocol.extension.discovery import DiscoveryDispatcher
from headstock.protocol.extension.discovery import FeaturesDiscovery
from headstock.api.jid import JID
from headstock.api.im import Message, Body, Event
from headstock.api.contact import Presence, Roster, Item
from headstock.api import Entity
from headstock.api.activity import Activity
from headstock.api.registration import Registration
from headstock.lib.parser import XMLIncrParser
from headstock.lib.logger import Logger
from headstock.lib.utils import generate_unique

from bridge import Element as E
from bridge.common import XMPP_CLIENT_NS, XMPP_ROSTER_NS, \
    XMPP_LAST_NS, XMPP_DISCO_INFO_NS, XMPP_IBR_NS

__all__ = ['Client']

class RosterHandler(component):    
    Inboxes = {"inbox"        : "headstock.api.contact.Roster instance",
               "control"      : "stops the component",
               "pushed"       : "roster stanzas pushed by the server",
               "jid"          : "headstock.api.jid.JID instance received from the server",
               "ask-activity" : "request activity status to the server for each roster contact"}
    
    Outboxes = {"outbox"      : "UNUSED",
                "signal"      : "Shutdown signal",
                "message"     : "Message to send",
                "result"      : "", 
                "activity"    : "headstock.api.activity.Activity instance to send to the server"}

    def __init__(self, from_jid):
        super(RosterHandler, self).__init__() 
        self.from_jid = from_jid
        self.roster = None

    def initComponents(self):
        # We subscribe to the JID backplane component
        # that will inform us when the server has
        # returned the per-session jid
        sub = SubscribeTo("JID")
        self.link((sub, 'outbox'), (self, 'jid'))
        self.addChildren(sub)
        sub.activate()

        return 1

    def main(self):
        yield self.initComponents()

        while 1:
            while self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            while self.dataReady("jid"):
                self.from_jid = self.recv('jid')
            
            while self.dataReady("pushed"):
                roster = self.recv('pushed')
                for nodeid in roster.items:
                    self.send(Roster(from_jid=self.from_jid, to_jid=nodeid,
                                     type=u'result', stanza_id=generate_unique()), 'result')
                
            while self.dataReady("inbox"):
                roster = self.recv("inbox")
                self.roster = roster
                print "Your contacts:"
                for nodeid in roster.items:
                    contact = roster.items[nodeid]
                    print "  ", contact.jid
                    
            while self.dataReady('ask-activity'):
                self.recv('ask-activity')
                if self.roster:
                    for nodeid in self.roster.items:
                        contact = roster.items[nodeid]
                        a = Activity(unicode(self.from_jid), unicode(contact.jid))
                        self.send(a, 'activity')

            if not self.anyReady():
                self.pause()
  
            yield 1

class WebMessageHandler(component):
    Inboxes = {"inbox"    : "headstock.api.contact.Message instance received from a peer",
               "trans_inbox" : "Receive messages from the inbound translator",
               "jid"      : "headstock.api.jid.JID instance received from the server",
               "control"  : "stops the component",}
    
    Outboxes = {"outbox"  : "headstock.api.im.Message to send to the client",
                "trans_outbox" : "Send messages to the outbound translator",
                "signal"  : "Shutdown signal",
                "proto" : "Send messages to the protocol manager",}

    def __init__(self):
        super(WebMessageHandler, self).__init__() 
        self.from_jid = None

    def initComponents(self):
        sub = SubscribeTo("JID")
        self.link((sub, 'outbox'), (self, 'jid'))
        self.addChildren(sub)
        sub.activate()

    def main(self):
        self.initComponents()
        yield 1

        while 1:
            while self.dataReady("control"):
                mes = self.recv("control")
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            if self.dataReady("jid"):
                self.from_jid = self.recv('jid')
            
            [self.send(msg, 'trans_outbox') for msg in self.Inbox('inbox')]
            [self.send(msg, 'outbox') for msg in self.Inbox('trans_inbox')]
                    
            if not self.anyReady():
                self.pause()
  
            yield 1

class DiscoHandler(component):
    Inboxes = {"inbox"          : "UNUSED",
               "control"        : "stops the component", 
               "initiate"       : "event informing the component the client session is active",
               "jid"            : "headstock.api.jid.JID instance received from the server",
               "features.result": "headstock.api.discovery.FeaturesDiscovery instance from the server",}
    
    Outboxes = {"outbox"           : "UNUSED",
                "signal"           : "Shutdown signal",
                "features-disco"   : "headstock.api.discovery.FeaturesDiscovery query to the server",  
                "features-announce": "headstock.api.discovery.FeaturesDiscovery informs"\
                    "the other components about the features instance received from the server"}

    def __init__(self, from_jid, to_jid):
        super(DiscoHandler, self).__init__() 
        self.from_jid = from_jid
        self.to_jid = to_jid

    def initComponents(self):
        sub = SubscribeTo("JID")
        self.link((sub, 'outbox'), (self, 'jid'))
        self.addChildren(sub)
        sub.activate()

        pub = PublishTo("DISCO_FEAT")
        self.link((self, 'features-announce'), (pub, 'inbox'))
        self.addChildren(pub)
        pub.activate()

        sub = SubscribeTo("BOUND")
        self.link((sub, 'outbox'), (self, 'initiate'))
        self.addChildren(sub)
        sub.activate()

        return 1

    def main(self):
        yield self.initComponents()

        while 1:
            while self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            while self.dataReady("jid"):
                self.from_jid = self.recv('jid')
            
            # When this box has some data, it means
            # that the client is bound to the server
            # Let's ask for its supported features then.
            while self.dataReady("initiate"):
                self.recv("initiate")
                d = FeaturesDiscovery(unicode(self.from_jid), self.to_jid)
                self.send(d, "features-disco")

            # The response to our discovery query
            # is a a headstock.api.discovery.FeaturesDiscovery instance.
            # What we immediatly do is to notify all handlers
            # interested in that event about it.
            while self.dataReady('features.result'):
                disco = self.recv('features.result')
                print "Supported features:"
                for feature in disco.features:
                    print "  ", feature.var
                self.send(disco, 'features-announce')

            if not self.anyReady():
                self.pause()
  
            yield 1

class ActivityHandler(component):
    Inboxes = {"inbox"   : "headstock.api.discovery.FeaturesDiscovery instance",
               "control" : "stops the component",
               }
    
    Outboxes = {"outbox"            : "UNUSED",
                "signal"            : "Shutdown signal",
                "activity-supported": "when used this tells the RosterHandler it needs"\
                    "to request the server for each contact's activity."\
                    "This is only used when the server supports the feature",
                }

    def __init__(self):
        super(ActivityHandler, self).__init__() 

    def initComponents(self):
        sub = SubscribeTo("DISCO_FEAT")
        self.link((sub, 'outbox'), (self, 'inbox'))
        self.addChildren(sub)
        sub.activate()
        
        return 1

    def main(self):
        yield self.initComponents()

        while 1:
            while self.dataReady("control"):
                mes = self.recv("control")
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            while self.dataReady("inbox"):
                disco = self.recv("inbox")
                support = disco.has_feature(XMPP_LAST_NS)
                print "Activity support: ", support
                if support:
                    self.send('', "activity-supported")

            if not self.anyReady():
                self.pause()
  
            yield 1

class PresenceHandler(component):
    Inboxes = {"inbox"       : "headstock.api.contact.Presence instance",
               "control"     : "Shutdown the client stream",
               "subscribe"   : "",
               "unsubscribe" : "",
               'unavailable' : 'Receive notifications when another client becomes unavailable',
               'available': 'Receive notifications when another client becomes available'}
    
    Outboxes = {"outbox" : "headstock.api.contact.Presence instance to return to the server",
                "signal" : "Shutdown signal",
                "roster" : "",
                "log"    : "log",}
    
    def __init__(self):
        super(PresenceHandler, self).__init__()

    def main(self):
        while 1:
            print 'loop!'
            while self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            while self.dataReady("subscribe"):
                p = self.recv("subscribe")
                p.swap_jids()

                # Automatically accept any subscription requests
                p = Presence(from_jid=p.from_jid, to_jid=unicode(p.to_jid),
                             type=u'subscribed')
                self.send(p, "outbox")
                
                # Automatically subscribe in return as well
                p = Presence(from_jid=p.from_jid, to_jid=unicode(p.to_jid),
                             type=u'subscribe')
                self.send(p, "outbox")
                
            while self.dataReady("unsubscribe"):
                p = self.recv("unsubscribe")
                p.swap_jids()
                
                # We stop our subscription to the other user
                p = Presence(from_jid=p.from_jid, to_jid=unicode(p.to_jid),
                             type=u'unsubscribed')
                self.send(p, "outbox")
                
                # We stop the other user's subscription
                p = Presence(from_jid=p.from_jid, to_jid=unicode(p.to_jid),
                             type=u'unsubscribe')
                self.send(p, "outbox")

                # We remove this user from our roster list
                r = Roster(from_jid=p.from_jid, type=u'set')
                i = Item(p.to_jid)
                i.subscription = u'remove'
                r.items[unicode(p.to_jid)] = i
                self.send(r, 'roster')

                # We tell the other user we're not available anymore
                p = Presence(from_jid=p.from_jid, to_jid=unicode(p.to_jid),
                             type=u'unavailable')
                self.send(p, "outbox")
            while self.dataReady('available'):
                #print 'Presence handler received:'
                self.recv('available')
            while self.dataReady('unavailable'):
                #print 'Presence handler received:'
                self.recv('unavailable')
                
            if not self.anyReady():
                self.pause()
  
            yield 1
    

class RegistrationHandler(component):
    Inboxes = {"inbox"   : "headstock.api.registration.Registration",
               "error"   : "headstock.api.registration.Registration",
               "control" : "Shutdown the client stream",}
    
    Outboxes = {"outbox" : "headstock.api.registration.Registration",
                "signal" : "Shutdown signal",
                "log"    : "log",}
    
    def __init__(self, username, password):
        super(RegistrationHandler, self).__init__()
        self.username = username
        self.password = password
        self.registration_id = None

    def main(self):
        while 1:
            while self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            while self.dataReady("inbox"):
                r = self.recv('inbox')
                if r.registered:
                    print "'%s' is already a registered username." % self.username
                elif self.registration_id == r.stanza_id:
                    print "'%s' is now a registered user."\
                        "Please restart the client without the register flag." % self.username
                else:
                    if 'username' in r.infos and 'password' in r.infos:
                        self.registration_id = generate_unique()
                        r = Registration(type=u'set', stanza_id=self.registration_id)
                        r.infos[u'username'] = self.username
                        r.infos[u'password'] = self.password
                        self.send(r, 'outbox')
                
            while self.dataReady("error"):
                r = self.recv('error')
                print r.error

            if not self.anyReady():
                self.pause()
  
            yield 1

class Client(component):
    Inboxes = {"inbox"      : "",
               "jid"        : "",
               "streamfeat" : "",
               "control"    : "Shutdown the client stream",
               "http-inbox" : "Receive messages to an HTTP Server",
               "output" : "Forward messages to the WebMessageHandler"}
    
    Outboxes = {"outbox"  : "",
                "forward" : "",
                "log"     : "",
                "doauth"  : "",
                "signal"  : "Shutdown signal",
                "lw-signal" : "Shutdown signal for WsgiLogWritable",
                "doregistration" : ""}

    def __init__(self, Config):
        super(Client, self).__init__() 
        self.cfg = Config
        self.jid = JID(
            Config.xmpp.username,
            Config.xmpp.domain,
            Config.xmpp.resource)
        self.username = Config.xmpp.username
        self.password = Config.xmpp.password
        self.server = Config.xmpp.server
        self.port = Config.xmpp.port
        self.client = None
        self.graph = None
        self.domain = Config.xmpp.domain
        self.usetls = Config.xmpp.usetls
        self.register = False
        self.use_std_out = Config.options.xmpp_verbose

    def passwordLookup(self, jid):
        return self.password

    def shutdown(self):
        self.send(Presence.to_element(Presence(self.jid, type=u'unavailable')), 'forward')
        self.send('OUTGOING : </stream:stream>', 'log')
        self.send('</stream:stream>', 'outbox') 

    def abort(self):
        self.send('OUTGOING : </stream:stream>', 'log')
        self.send('</stream:stream>', 'outbox')

    def setup(self):
        # Backplanes are like a global entry points that
        # can be accessible both for publishing and
        # recieving data. 
        # In other words, a component interested
        # in advertising to many other components that
        # something happened may link one of its outbox
        # to a PublishTo component's inbox.
        # A component wishing to receive that piece of
        # information will link one of its inbox
        # to the SubscribeTo component's outbox.
        # This helps greatly to make components more
        # loosely connected but also allows for some data
        # to be dispatched at once to many (such as when
        # the server returns the per-session JID that
        # is of interest for most other components).
        Backplane("CONSOLE").activate()
        Backplane("JID").activate()
        # Used to inform components that the session is now active
        Backplane("BOUND").activate()
        # Used to inform components of the supported features
        Backplane("DISCO_FEAT").activate()
        

        sub = SubscribeTo("JID")
        self.link((sub, 'outbox'), (self, 'jid'))
        self.addChildren(sub)
        sub.activate()
        
        if self.use_std_out:
            log = Logger(stdout=True, name='XmppLogger')
        else:
            log = nullSinkComponent()
        
        # We pipe everything typed into the console
        # directly to the console backplane so that
        # every components subscribed to the console
        # backplane inbox will get the typed data and
        # will decide it it's of concern or not.
        Pipeline(ConsoleReader(), PublishTo('CONSOLE')).activate()

        # Add two outboxes ro the ClientSteam to support specific extensions.
        ClientStream.Outboxes["%s.query" % XMPP_IBR_NS] = "Registration"
        ClientStream.Outboxes["%s.query" % XMPP_LAST_NS] = "Activity"
        ClientStream.Outboxes["%s.query" % XMPP_DISCO_INFO_NS] = "Discovery"

        self.client = ClientStream(self.jid, self.passwordLookup, use_tls=self.usetls)

        self.graph = Graphline(client = self,
                               console = SubscribeTo('CONSOLE'),
                               logger = log,
                               tcp = TCPClient(self.server, self.port),
                               xmlparser = XMLIncrParser(),
                               xmpp = self.client,
                               streamerr = StreamError(),
                               saslerr = SaslError(),
                               discohandler = DiscoHandler(self.jid, self.domain),
                               activityhandler = ActivityHandler(),
                               rosterhandler = RosterHandler(self.jid),
                               registerhandler = RegistrationHandler(self.username, self.password),
                               presencehandler = PresenceHandler(),
                               presencedisp = PresenceDispatcher(),
                               rosterdisp = RosterDispatcher(),
                               msgdisp = MessageDispatcher(),
                               discodisp = DiscoveryDispatcher(),
                               activitydisp = ActivityDispatcher(),
                               registerdisp = RegisterDispatcher(),
                               pjid = PublishTo("JID"),
                               pbound = PublishTo("BOUND"),
                               webhandler=Interface(ThisJID=self.jid),

                               linkages = {('xmpp', 'terminated'): ('client', 'inbox'),
                                           ('console', 'outbox'): ('client', 'control'),
                                           ('client', 'forward'): ('xmpp', 'forward'),
                                           ('client', 'outbox'): ('tcp', 'inbox'),
                                           ('client', 'signal'): ('tcp', 'control'),
                                           ("tcp", "outbox") : ("xmlparser", "inbox"),
                                           ("xmpp", "starttls") : ("tcp", "makessl"),
                                           ("tcp", "sslready") : ("xmpp", "tlssuccess"), 
                                           ("xmlparser", "outbox") : ("xmpp" , "inbox"),
                                           ("xmpp", "outbox") : ("tcp" , "inbox"),
                                           ("xmpp", "reset"): ("xmlparser", "reset"),
                                           ("client", "log"): ("logger", "inbox"),
                                           ("xmpp", "log"): ("logger", "inbox"),
                                           ("xmpp", "jid"): ("pjid", "inbox"),
                                           ("xmpp", "bound"): ("pbound", "inbox"),
                                           ("xmpp", "features"): ("client", "streamfeat"),
                                           ("client", "doauth"): ("xmpp", "auth"),
                                           
                                           # Registration
                                           ("xmpp", "%s.query" % XMPP_IBR_NS): ("registerdisp", "inbox"),
                                           ("registerdisp", "log"): ('logger', "inbox"),
                                           ("registerdisp", "xmpp.error"): ("registerhandler", "error"),
                                           ("registerdisp", "xmpp.result"): ("registerhandler", "inbox"),
                                           ("registerhandler", "outbox"): ("registerdisp", "forward"),
                                           ("client", "doregistration"): ("registerdisp", "forward"),
                                           ("registerdisp", "outbox"): ("xmpp", "forward"),
                                           
                                           # Presence 
                                           ("xmpp", "%s.presence" % XMPP_CLIENT_NS): ("presencedisp", "inbox"),
                                           ("presencedisp", "log"): ('logger', "inbox"),
                                           ("presencedisp", "xmpp.subscribe"): ("presencehandler", "subscribe"),
                                           ("presencedisp", "xmpp.unsubscribe"): ("presencehandler", "unsubscribe"),
                                           ("presencehandler", "outbox"): ("presencedisp", "forward"),
                                           ("presencehandler", "roster"): ("rosterdisp", "forward"),
                                           ("presencedisp", "outbox"): ("xmpp", "forward"),
                                           ("presencedisp", "xmpp.available") : ('webhandler', 'xmpp.available'),
                                           ("presencedisp", 'xmpp.unavailable') : ('webhandler', 'xmpp.unavailable'),

                                           # Roster
                                           ("xmpp", "%s.query" % XMPP_ROSTER_NS): ("rosterdisp", "inbox"),
                                           ("rosterdisp", "log"): ('logger', "inbox"),
                                           ('rosterdisp', 'xmpp.set'): ('rosterhandler', 'pushed'),
                                           ('rosterdisp', 'xmpp.result'): ('rosterhandler', 'inbox'),
                                           ('rosterhandler', 'result'): ('rosterdisp', 'forward'),
                                           ("rosterdisp", "outbox"): ("xmpp", "forward"),

                                           # Discovery
                                           ("xmpp", "%s.query" % XMPP_DISCO_INFO_NS): ("discodisp", "features.inbox"),
                                           ("discodisp", "log"): ('logger', "inbox"),
                                           ("discohandler", "features-disco"): ('discodisp', "features.forward"),
                                           ("discodisp", "out.features.result"): ('discohandler', "features.result"),
                                           ("discodisp", "outbox"): ("xmpp", "forward"),

                                           # Message
                                           ("xmpp", "%s.message" % XMPP_CLIENT_NS): ("msgdisp", "inbox"),
                                           ("msgdisp", "log"): ('logger', "inbox"),
                                           ("webhandler", "xmpp.outbox"): ('msgdisp', 'forward'),
                                           ("msgdisp", "xmpp.chat"): ('webhandler', 'xmpp.inbox'),
                                           ("msgdisp", "outbox"): ("xmpp", "forward"),

                                           # Activity
                                           ("xmpp", "%s.query" % XMPP_LAST_NS): ("activitydisp", "inbox"),
                                           ("activitydisp", "log"): ('logger', "inbox"),
                                           ("activitydisp", "outbox"): ("xmpp", "forward"),
                                           ("activityhandler", 'activity-supported'): ('rosterhandler', 'ask-activity'),
                                           ("rosterhandler", 'activity'): ('activitydisp', 'forward'),
                                           }
                               )
        self.addChildren(self.graph)
        self.graph.activate()

        return 1

    def main(self):
        yield self.setup()

        while 1:
            while self.dataReady("control"):
                mes = self.recv("control")

                if isinstance(mes, str):
                    if mes.strip() == 'quit':
                        self.shutdown()
                elif isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(mes, "signal")
                    break

            while self.dataReady("inbox"):
                msg = self.recv('inbox')
                if msg == "quit":
                    self.send(shutdownMicroprocess(), "signal")
                    yield 1
                    break

            while self.dataReady("streamfeat"):
                feat = self.recv('streamfeat')
                if feat.register and self.register:
                    self.send(Registration(), 'doregistration')
                elif self.register and not feat.register:
                    print "The server does not support in-band registration. Closing connection."
                    self.abort()
                else:
                    self.send(feat, 'doauth')
                
            while self.dataReady("jid"):
                self.jid = self.recv('jid')
                
            if not self.anyReady():
                self.pause()
  
            yield 1

        yield 1
        self.stop()
        print "You can hit Ctrl-C to shutdown all processes now." 

def constructXMPPClient(Config):
    return Client(Config)

print __name__

if __name__ == '__main__':
    main()
