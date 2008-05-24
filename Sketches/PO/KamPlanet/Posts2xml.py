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

class Posts2xml(KamTemplateProcessor):
    def __init__(self, **argd):
        super(Posts2xml, self).__init__(**argd)

    def getTemplateFileName(self):
        return self.config.rssTemplateName

    def getOutputFileName(self):
        return self.config.rssFileName

    def fillTemplate(self,  templateProcessor):
        templateProcessor.set('name',  self.config.name)
        templateProcessor.set('link',  self.config.link)
        
        items = []
        
        for complete_entry in self.posts:
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
        item['date_822']     = entry.updated.encode(encoding)
        item['author_email'] = False
        item['author_name']  = entry.author.encode(encoding)
        return item
