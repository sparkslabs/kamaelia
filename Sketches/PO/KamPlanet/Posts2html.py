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

from KamTemplateProcessor import KamTemplateProcessor
import sanitize

import time

class Posts2html(KamTemplateProcessor):
    def __init__(self, **argd):
        super(Posts2html, self).__init__(**argd)

    def getTemplateFileName(self):
        return self.config.htmlTemplateName
        
    def getOutputFileName(self):
        return self.config.htmlFileName

    def fillTemplate(self,  templateProcessor):
        templateProcessor.set('generator',            "KamPlanet 0.1")
        templateProcessor.set('feedtype',             "rss")
        templateProcessor.set('feed',                 "rss20.xml")
        templateProcessor.set('name',                 self.config.name)
        templateProcessor.set('channel_title_plain',  self.config.name)
        templateProcessor.set('link',                 self.config.link)
        templateProcessor.set('date',                 time.asctime())
        
        items    = []
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
        item['date_822']           = entry.updated.encode(encoding)
        item['date']               = entry.updated.encode(encoding)
        item['author_email']       = False
        item['author_name']        = entry.author.encode(encoding)
        item['author']             = entry.author.encode(encoding)
        return item
