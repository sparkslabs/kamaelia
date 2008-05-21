#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

from KamTemplateProcessor import KamTemplateProcessor
import time

class Feed2html(KamTemplateProcessor):
    def __init__(self, **argd):
        super(Feed2html, self).__init__(**argd)

    def getTemplateFileName(self):
        return self.config.htmlTemplateName

    def fillTemplate(self,  templateProcessor):
        templateProcessor.set('generator',            "KamPlanet 0.1")
        templateProcessor.set('feedtype',             "rss")
        templateProcessor.set('feed',                 "rss20.xml")
        templateProcessor.set('name',                 self.config.name)
        templateProcessor.set('channel_title_plain',  self.config.name)
        templateProcessor.set('link',                 self.config.link)
        templateProcessor.set('date',                 time.asctime())
        
        items    = []
        for complete_entry in self.feeds:
            feed     = complete_entry['feed']
            entry    = complete_entry['entry']
            encoding = complete_entry['encoding']
            
            item = self.createItem(feed, entry, encoding)
            items.append(item)
        templateProcessor.set('Items',  items)
        
        channels = []
        for channel in self.channels:
            chan = self.createChannel(channel)
            channels.append(chan)
        templateProcessor.set('Channels',  channels)

    def createChannel(self, channel):
        chan = {}
        chan['url']      = channel.url
        chan['name']     = channel.name
        # TODO: well, {link, message} can't be 
        # parsed with current design (they are retrieved from the address)
        # and since the blog's server could be down, there should be a
        # cache as in planetplanet
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
        item['content']            = entry.summary.encode(encoding)
        item['date_822']           = entry.updated.encode(encoding)
        item['date']               = entry.updated.encode(encoding)
        item['author_email']       = False
        item['author_name']        = entry.author.encode(encoding)
        item['author']             = entry.author.encode(encoding)
        return item
