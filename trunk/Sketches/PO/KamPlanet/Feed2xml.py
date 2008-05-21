#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

from KamTemplateProcessor import KamTemplateProcessor

class Feed2xml(KamTemplateProcessor):
    def __init__(self, **argd):
        super(Feed2xml, self).__init__(**argd)

    def getTemplateFileName(self):
        return self.config.rssTemplateName

    def fillTemplate(self,  templateProcessor):
        templateProcessor.set('name',  self.config.name)
        templateProcessor.set('link',  self.config.link)
        
        items = []
        
        for complete_entry in self.feeds:
            feed     = complete_entry['feed']
            entry    = complete_entry['entry']
            encoding = complete_entry['encoding']
            
            item = self.createItem(feed, entry, encoding)
            
            items.append(item)
            
        templateProcessor.set('Items',  items)

    def createItem(self, feed, entry, encoding):
        item = {}
        item['channel_name'] = feed.title.encode(encoding)
        item['title']        = True
        item['title_plain']  = feed.title.encode(encoding)
        item['id']           = entry.link.encode(encoding)
        item['link']         = entry.link.encode(encoding)
        item['content']      = entry.summary.encode(encoding)
        item['date_822']     = entry.updated.encode(encoding)
        item['author_email'] = False
        item['author_name']  = entry.author.encode(encoding)
        return item
