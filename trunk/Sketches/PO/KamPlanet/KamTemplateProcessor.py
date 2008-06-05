#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: PO

import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

import time
import sanitize
from htmltmpl import TemplateManager, TemplateProcessor

class KamTemplateProcessor(Axon.Component.component):
    """
    KamTemplateProcessor() -> KamTemplateProcessor object
    
    It receives information about posts, feeds, configuration and channels and 
    sends the information translated to other format specified.
    
    The received information is posts (in feedparser.FeedParserDict entry format), 
    feeds (in feedparser.FeedParserDict feed format), config (in GeneralObjectParser
    format, see ConfigFileParser), and channels (in GeneralObjectParser format, see
    ConfigFileParser). This information is not redundant:
    - "channels" provides the feeds as they are defined in the configuration file. 
      This information is provided even if the server hosting the channel is down.
    - "feeds" provides all the information of a feed and its posts, but it does not 
      return the information gathered in the configuration file.
    - "posts" provides only the posts that actually need to be written into the file.
      Even the post information is available in "feeds", but not the information 
      about if these feeds should appear on the file or not.
    - "config" provides the general configuration.
    
    The content returned in the "outbox" outbox should be directly redirected to a 
    file or other output stream. The "create-output" outbox will be called before
    sending any data, and it will provide a string gathered in the configuration
    file such as the file name.
    """
    Inboxes = {
            'control'        : 'From component',
            'inbox'          : 'Not used', 
            'posts-inbox'    : 'Posts that must appear on the planet, in feedparser.FeedParserDict format', 
            'feeds-inbox'    : 'Feeds -information retrieved from the server-, in feedparser.FeedParserDict format', 
            'config-inbox'   : 'General KamPlanet configuration, in GeneralObjectParser format', 
            'channels-inbox' : 'Feeds -information retrieved from the conf file-, in GeneralObjectParser format', 
        }
    Outboxes = {
            'outbox'         : 'The output to be written to a file (or output stream in general)', 
            'create-output'  : 'It will be called before sending any data, to initialize the output stream', 
            'signal'         : 'From component', 
        }
    def __init__(self, templateField, outputFileField, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(KamTemplateProcessor, self).__init__(**argd)
        self.templateField    = templateField
        self.outputFileField  = outputFileField
        self.posts            = []
        self.feeds            = []
        self.channels         = []
        self.providerFinished = None
        self.mustStop         = None
        self.config           = None
        
    def fillTemplate(self,  templateProcessor):
        templateProcessor.set('name',                 self.config.name)
        templateProcessor.set('link',                 self.config.link)
        templateProcessor.set('generator',            "KamPlanet 0.1") # TODO
        templateProcessor.set('feedtype',             "rss") # TODO
        templateProcessor.set('feed',                 "rss20.xml") # TODO
        templateProcessor.set('channel_title_plain',  self.config.name)
        templateProcessor.set('date',                 time.asctime())
        
        items = []
        
        for complete_entry in self.posts:
            feed     = complete_entry['feed']
            entry    = complete_entry['entry']
            encoding = complete_entry['encoding']
            
            item = self.createItem(feed, entry, encoding)
            items.append(item)
            
        templateProcessor.set('Items',  items)
        
        channels = []
        channels_info = {}
        for feedUrl, feedInfo in [ (x.href, x) for x in self.feeds ]:
            channels_info[feedUrl] = feedInfo
            
        for channel in self.channels:
            chan = self.createChannel(channel, channels_info)
            channels.append(chan)
        templateProcessor.set('Channels',  channels)

    def createChannel(self, channel, channels_info):
        chan = {}
        chan['url']      = channel.url
        chan['name']     = channel.name
        
        if channels_info.has_key(channel.url):
            chan_info = channels_info[channel.url]
            encoding  = chan_info.encoding
            if chan_info.feed.has_key('link'):
                chan['link']    = chan_info.feed.link.encode(encoding)
            if chan_info.feed.has_key('link'):
                chan['message'] = chan_info.feed.title.encode(encoding)
        return chan
    
    def createItem(self, feed, entry, encoding):
        item = {}
        item['channel_name']       = feed.title.encode(encoding)
        item['title']              = feed.title.encode(encoding)
        item['title_plain']        = feed.title.encode(encoding)
        item['id']                 = entry.link.encode(encoding)
        item['link']               = entry.link.encode(encoding)
        item['channel_link']       = feed.title.encode(encoding)
        item['channel_title_name'] = feed.title.encode(encoding)
        if entry.has_key('content'):
            content = ''
            for i in entry.content:
                if i.type == 'text/html':
                    content += sanitize.HTML(i.value)
                elif i.type == 'text/plain':
                    content += cgi.escape(i.value)
        elif entry.has_key('summary'):
            content = entry.summary.encode(encoding)
        else:
            content = ''
        item['content']            = content
        if hasattr(entry, 'updated'):
            item['date_822']           = entry.updated.encode(encoding)
            item['date']               = entry.updated.encode(encoding)
        else:
            #TODO
            pass
        item['author_email']       = False
        if hasattr(entry, 'author'):
            item['author_name']        = entry.author.encode(encoding)
            item['author']             = entry.author.encode(encoding)
        else:
            #TODO
            pass
        return item
        
    def getTemplateFileName(self):
        return getattr(self.config, self.templateField)
        
    def getOutputFileName(self):
        return getattr(self.config, self.outputFileField)

    def checkControl(self):
        while self.dataReady("control"):
            msg = self.recv("control")
            if isinstance(msg,producerFinished):
                self.providerFinished = msg
            elif isinstance(msg,shutdownMicroprocess):
                self.mustStop = msg
        return self.mustStop, self.providerFinished
    
    def prepareTemplate(self):
        # tmanager tries to use a compiled (pickle) version of the
        # .tmpl file if available. The "problem" is that it internally 
        # reads the files in a "normal way". I should use the 
        # TemplateCompiler class in the following way:
        # 
        # templateCompiler = TemplateCompiler()
        # return templateCompiler.compileString(dataReceivedFromKamaeliaReader)
        # 
        # and serialize this class to a tmplc file
        # 
        tmanager = TemplateManager()
        return tmanager.prepare(self.getTemplateFileName())
    
    VERBOSE = True
    
    def main(self):
        while True:                
            while self.dataReady("channels-inbox"):
                data = self.recv("channels-inbox")
                self.channels.append(data)
                
            while self.dataReady("feeds-inbox"):
                data = self.recv("feeds-inbox")
                self.feeds.append(data)
                
            while self.dataReady("posts-inbox"):
                data = self.recv("posts-inbox")
                self.posts.append(data)
                
            while self.dataReady("config-inbox"):
                data = self.recv("config-inbox")
                self.config = data
            
            mustStop, providerFinished = self.checkControl()
            if mustStop:
                self.send(mustStop,"signal")
                return
            
            if providerFinished is not None and self.config is not None:
                tproc = TemplateProcessor(html_escape=0)
                template = self.prepareTemplate()
                yield 1
                
                self.fillTemplate(tproc)
                result = tproc.process(template)
                yield 1
                
                self.send(self.getOutputFileName(), 'create-output')
                yield 1
                
                self.send(result, "outbox")
                yield 1
                
                self.send(producerFinished(self), "signal")
                if self.VERBOSE:
                    print "File written %s" % self.getOutputFileName()
                return
                
            if not self.anyReady():
                self.pause()
                
            yield 1
