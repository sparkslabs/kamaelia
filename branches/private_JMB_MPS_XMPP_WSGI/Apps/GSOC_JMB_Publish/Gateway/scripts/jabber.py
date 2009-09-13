# -*- coding: utf-8 -*-
#
# JMB_PUBLISH_GATEWAY
#
"""
This is an adapted version of Sylvain Hellegouarch's simplechat example.  It is used
as the basis for Kamaelia Publish's XMPP code.  The original documentation is reproduced
below.

The majority of the code that needs to be read to understand this is in the Client
component.

Original documentation
------------------------

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

FIXME
---------
This code desperately needs to be refactored and needs to have uneccessary functionality
removed.  The code is good for an example, but not a production system.
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

class RosterHandler(component):    # Now identical to headstock's simple chat example
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

            if self.dataReady("jid"):
                self.from_jid = self.recv('jid')
            
            if self.dataReady("pushed"):
                roster = self.recv('pushed')
                for nodeid in roster.items:
                    self.send(Roster(from_jid=self.from_jid, to_jid=nodeid,
                                     type=u'result', stanza_id=generate_unique()), 'result')
                
            if self.dataReady("inbox"):
                roster = self.recv("inbox")
                self.roster = roster
                print "Your contacts:"
                for nodeid in roster.items:
                    contact = roster.items[nodeid]
                    print "  ", contact.jid
                    
            if self.dataReady('ask-activity'):
                self.recv('ask-activity')
                if self.roster:
                    for nodeid in self.roster.items:
                        contact = roster.items[nodeid]
                        a = Activity(unicode(self.from_jid), unicode(contact.jid))
                        self.send(a, 'activity')

            if not self.anyReady():
                self.pause()
  
            yield 1

class WebMessageHandler(component): # NOT USED - REPLACED BY 'Interface' -- from interface import Interface
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

            # Assumes that messages to/from translator are already fully formed headstock messages. (maybe valid)
            for msg in self.Inbox('inbox'):       self.send(msg, 'trans_outbox')
            for msg in self.Inbox('trans_inbox'): self.send(msg, 'outbox')

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
            if self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            if  self.dataReady("jid"):
                self.from_jid = self.recv('jid')
            
            # When this box has some data, it means
            # that the client is bound to the server
            # Let's ask for its supported features then.
            if self.dataReady("initiate"):
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
            if self.dataReady("control"):
                mes = self.recv("control")
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            if self.dataReady("inbox"):
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
'unavailable' : 'Receive notifications when another client becomes unavailable', #notinheadstock
'available': 'Receive notifications when another client becomes available'}      #notinheadstock
    
    Outboxes = {"outbox" : "headstock.api.contact.Presence instance to return to the server",
                "signal" : "Shutdown signal",
                "roster" : "",
                "log"    : "log",}
    
    def __init__(self):
        super(PresenceHandler, self).__init__()

    def main(self):
        while 1:
            if self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            if self.dataReady("subscribe"):
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
                
            if self.dataReady("unsubscribe"):
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
            if self.dataReady('available'): # Changed to match logic of rest, but #notinheadstock
                #print 'Presence handler received:'                               #notinheadstock
                self.recv('available             ')                               #notinheadstock
            if self.dataReady('unavailable'):                                     #notinheadstock
                #print 'Presence handler received:'                               #notinheadstock
                self.recv('unavailable')                                          #notinheadstock
                
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
            if self.dataReady("control"):
                mes = self.recv("control")
                
                if isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(producerFinished(), "signal")
                    break

            if self.dataReady("inbox"):
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
                
            if self.dataReady("error"):
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
               "http-inbox" : "Receive messages to an HTTP Server",                #notinheadstock
               "output" : "Forward messages to the WebMessageHandler"}             #notinheadstock
    
    Outboxes = {"outbox"  : "",
                "forward" : "",
                "log"     : "",
                "doauth"  : "",
                "signal"  : "Shutdown signal",
                "lw-signal" : "Shutdown signal for WsgiLogWritable",             #notinheadstock
                "doregistration" : ""}

    def __init__(self, Config):                 #notinheadstock, perhaps more logical
        super(Client, self).__init__() 
        self.cfg = Config              # notinheadstock
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
        self.register = False         #notinheadstock - differnet logic-prevents register message
        self.use_std_out = Config.options.xmpp_verbose    #notinheadstock

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
        
        if self.use_std_out:                             #notinheadstock - unlikely to be an issue
            log = Logger(stdout=True, name='XmppLogger') #notinheadstock
        else:                                            #notinheadstock
            log = nullSinkComponent()                    #notinheadstock
        
        # We pipe everything typed into the console
        # directly to the console backplane so that
        # every components subscribed to the console
        # backplane inbox will get the typed data and
        # will decide it it's of concern or not.
        Pipeline(ConsoleReader(), PublishTo('CONSOLE')).activate()

        #FIXME: This actually looks potentially a bust (changes class for all new instances)
        #FIXME: That said, it's in headstock's example, so it shouldn't be a major issue...
        # Add two outboxes ro the ClientSteam to support specific extensions.
        ClientStream.Outboxes["%s.query" % XMPP_IBR_NS] = "Registration"
        ClientStream.Outboxes["%s.query" % XMPP_LAST_NS] = "Activity"
        ClientStream.Outboxes["%s.query" % XMPP_DISCO_INFO_NS] = "Discovery"

        self.client = ClientStream(self.jid, self.passwordLookup, use_tls=self.usetls)

        self.graph = Graphline(client = self,                                    # SAME
                               console = SubscribeTo('CONSOLE'),                 # SAME
                               logger = log,                                     # SAME*
                               tcp = TCPClient(self.server, self.port),          # SAME
                               xmlparser = XMLIncrParser(),                      # SAME
                               xmpp = self.client,                               # SAME
                               streamerr = StreamError(),                        # SAME
                               saslerr = SaslError(),                            # SAME
                               discohandler = DiscoHandler(self.jid, self.domain),# SAME
                               activityhandler = ActivityHandler(),              # SAME
                               rosterhandler = RosterHandler(self.jid),          # SAME
                               registerhandler = RegistrationHandler(self.username, self.password),              # SAME
                               # CHANGE (was DummyMessageHander)
                               presencehandler = PresenceHandler(),              # SAME
                               presencedisp = PresenceDispatcher(),              # SAME
                               rosterdisp = RosterDispatcher(),                  # SAME
                               msgdisp = MessageDispatcher(),                    # SAME
                               discodisp = DiscoveryDispatcher(),                # SAME
                               activitydisp = ActivityDispatcher(),              # SAME
                               registerdisp = RegisterDispatcher(),              # SAME
                               pjid = PublishTo("JID"),                          # SAME
                               pbound = PublishTo("BOUND"),                      # SAME
                               webhandler=Interface(ThisJID=self.jid), # EXTRA (replaces dummy)

                               linkages = {('xmpp', 'terminated'): ('client', 'inbox'),                       # SAME
                                           ('console', 'outbox'): ('client', 'control'),                      # SAME
                                           ('client', 'forward'): ('xmpp', 'forward'),                        # SAME
                                           ('client', 'outbox'): ('tcp', 'inbox'),                            # SAME
                                           ('client', 'signal'): ('tcp', 'control'),                          # SAME
                                           ("tcp", "outbox") : ("xmlparser", "inbox"),                        # SAME
                                           ("xmpp", "starttls") : ("tcp", "makessl"),                         # SAME
                                           ("tcp", "sslready") : ("xmpp", "tlssuccess"),                      # SAME
                                           ("xmlparser", "outbox") : ("xmpp" , "inbox"),                      # SAME
                                           ("xmpp", "outbox") : ("tcp" , "inbox"),                            # SAME
                                           ("xmpp", "reset"): ("xmlparser", "reset"),                         # SAME
                                           ("client", "log"): ("logger", "inbox"),                            # SAME
                                           ("xmpp", "log"): ("logger", "inbox"),                              # SAME
                                           ("xmpp", "jid"): ("pjid", "inbox"),                                # SAME
                                           ("xmpp", "bound"): ("pbound", "inbox"),                            # SAME
                                           ("xmpp", "features"): ("client", "streamfeat"),                    # SAME
                                           ("client", "doauth"): ("xmpp", "auth"),                            # SAME
                                           
                                           # Registration
                                           ("xmpp", "%s.query" % XMPP_IBR_NS): ("registerdisp", "inbox"),   # SAME
                                           ("registerdisp", "log"): ('logger', "inbox"),                    # SAME
                                           ("registerdisp", "xmpp.error"): ("registerhandler", "error"),    # SAME
                                           ("registerdisp", "xmpp.result"): ("registerhandler", "inbox"),   # SAME
                                           ("registerhandler", "outbox"): ("registerdisp", "forward"),      # SAME
                                           ("client", "doregistration"): ("registerdisp", "forward"),       # SAME
                                           ("registerdisp", "outbox"): ("xmpp", "forward"),                 # SAME
                                           
                                           # Presence 
                                           ("xmpp", "%s.presence" % XMPP_CLIENT_NS): ("presencedisp", "inbox"),       # SAME
                                           ("presencedisp", "log"): ('logger', "inbox"),                              # SAME
                                           ("presencedisp", "xmpp.subscribe"): ("presencehandler", "subscribe"),      # SAME
                                           ("presencedisp", "xmpp.unsubscribe"): ("presencehandler", "unsubscribe"),  # SAME
                                           ("presencehandler", "outbox"): ("presencedisp", "forward"),                # SAME
                                           ("presencehandler", "roster"): ("rosterdisp", "forward"),                  # SAME
                                           ("presencedisp", "outbox"): ("xmpp", "forward"),                           # SAME
                                           ("presencedisp", "xmpp.available") : ('webhandler', 'xmpp.available'),#DIFFERENT
                                           ("presencedisp", 'xmpp.unavailable') : ('webhandler', 'xmpp.unavailable'),#DIFFERENT

                                           # Roster
                                           ("xmpp", "%s.query" % XMPP_ROSTER_NS): ("rosterdisp", "inbox"), # SAME
                                           ("rosterdisp", "log"): ('logger', "inbox"),                     # SAME
                                           ('rosterdisp', 'xmpp.set'): ('rosterhandler', 'pushed'),        # SAME
                                           ('rosterdisp', 'xmpp.result'): ('rosterhandler', 'inbox'),      # SAME
                                           ('rosterhandler', 'result'): ('rosterdisp', 'forward'),         # SAME
                                           ("rosterdisp", "outbox"): ("xmpp", "forward"),                  # SAME

                                           # Discovery
                                           ("xmpp", "%s.query" % XMPP_DISCO_INFO_NS): ("discodisp", "features.inbox"),# SAME
                                           ("discodisp", "log"): ('logger', "inbox"),                                 # SAME
                                           ("discohandler", "features-disco"): ('discodisp', "features.forward"),     # SAME
                                           ("discodisp", "out.features.result"): ('discohandler', "features.result"), # SAME
                                           ("discodisp", "outbox"): ("xmpp", "forward"),                              # SAME

                                           # Message
                                           ("xmpp", "%s.message" % XMPP_CLIENT_NS): ("msgdisp", "inbox"),   # SAME
                                           ("msgdisp", "log"): ('logger', "inbox"),                         # SAME
                                           ("msgdisp", "xmpp.chat"): ('webhandler', 'xmpp.inbox'),          # DIFFERENT
                                           ("webhandler", "xmpp.outbox"): ('msgdisp', 'forward'),           # DIFFERENT
                                           ("msgdisp", "outbox"): ("xmpp", "forward"),                      # SAME

                                           # Activity
                                           ("xmpp", "%s.query" % XMPP_LAST_NS): ("activitydisp", "inbox"),   # SAME
                                           ("activitydisp", "log"): ('logger', "inbox"),                     # SAME
                                           ("activitydisp", "outbox"): ("xmpp", "forward"),                  # SAME
                                           ("activityhandler", 'activity-supported'): ('rosterhandler', 'ask-activity'),# SAME
                                           ("rosterhandler", 'activity'): ('activitydisp', 'forward'),       # SAME
                                           }
                               )
        self.addChildren(self.graph)
        self.graph.activate()

        return 1

    def main(self):
        yield self.setup()

        while 1:
            if self.dataReady("control"):
                mes = self.recv("control")

                if isinstance(mes, str):
                    if mes.strip() == 'quit':
                        self.shutdown()
                elif isinstance(mes, shutdownMicroprocess) or isinstance(mes, producerFinished):
                    self.send(mes, "signal")
                    break

            if self.dataReady("inbox"):
                msg = self.recv('inbox')
                if msg == "quit":
                    self.send(shutdownMicroprocess(), "signal")
                    yield 1
                    break

            if self.dataReady("streamfeat"):
                feat = self.recv('streamfeat')
                if feat.register and self.register:
                    self.send(Registration(), 'doregistration')
                elif self.register and not feat.register:
                    print "The server does not support in-band registration. Closing connection."
                    self.abort()
                else:
                    self.send(feat, 'doauth')
                
            if self.dataReady("jid"):
                self.jid = self.recv('jid')
                
            if not self.anyReady():
                self.pause()
  
            yield 1

        yield 1
        self.stop()
        print "You can hit Ctrl-C to shutdown all processes now." 

def constructXMPPClient(Config): #FIXME: Irrelevant factory function
    return Client(Config)

print __name__

if __name__ == '__main__':
    main()
