#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
import time
from htmltmpl import TemplateManager, TemplateProcessor

class Feed2html(Axon.Component.component):
    # TODO: another inbox like "channels-inbox" is needed
    Inboxes = {
            'control'      : 'From component', 
            'inbox'        : 'Not used', 
            'feeds-inbox'  : 'Not used', 
            'config-inbox' : 'Not used', 
        }
        
    def __init__(self, **argd):
        super(Feed2html, self).__init__(**argd)
        self.feeds = []
        self.config = None

    def main(self):
        while True:
            while self.dataReady("control"):
                # TODO
                data = self.recv("control")
                print "%s: %s" % (type(self), data)
                self.send(data, "signal")
                return

            while self.dataReady("feeds-inbox"):
                data = self.recv("feeds-inbox")
                self.feeds.append(data)
                print "html",data['entry'].updated
                yield 1

            while self.dataReady("config-inbox"):
                data = self.recv("config-inbox")
                self.config = data
                print "html-config", data.name, data.link

            if self.config is not None and len(self.feeds) == 10: #TODO: 10
                # TODO: first approach: 
                # * no use of sanitize.py (although feedparser seems to scape HTML)
                # * it generages and writes the file "in a single shot" (some filewriter should be used)
                # 
                tproc = TemplateProcessor()
                tproc.set('generator',  "KamPlanet 0.1")
                tproc.set('feedtype',   "rss")
                tproc.set('feed',   "rss20.xml")
                tproc.set('name',  self.config.name)
                tproc.set('channel_title_plain',  self.config.name)
                tproc.set('link',  self.config.link)
                tproc.set('date',  time.asctime())
                
                items    = []
                
                for complete_entry in self.feeds:
                    feed     = complete_entry['feed']
                    entry    = complete_entry['entry']
                    encoding = complete_entry['encoding']
                    
                    item = self.createItem(feed, entry, encoding)
                    items.append(item)
                    
                tproc.set('Items',  items)
                yield 1
                
                template = TemplateManager().prepare("index.html.tmpl") #TODO: constant
                result = tproc.process(template)
                file_name = 'output/index.html' #TODO: constant
                open(file_name, 'w').write(result)
                print "Check", file_name
                yield 1

            if not self.anyReady():
                self.pause()

            yield 1

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
        item['date']           = entry.updated.encode(encoding)
        item['author_email']       = False
        item['author_name']        = entry.author.encode(encoding)
        item['author']        = entry.author.encode(encoding)
        return item
