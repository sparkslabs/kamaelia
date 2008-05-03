#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

import Axon
from htmltmpl import TemplateManager, TemplateProcessor

class Feed2xml(Axon.Component.component):
	Inboxes = {
			'control'      : 'From component', 
			'inbox'        : 'Not used', 
			'feeds-inbox'  : 'Not used', 
			'config-inbox' : 'Not used'
		}
	def __init__(self):
		super(Feed2xml, self).__init__()
		self._feeds = []
		self._config = None

	def main(self):
		while 1:
			while self.dataReady("control"):
				# TODO
				data = self.recv("control")
				print "%s: %s" % (type(self), data)
				self.send(data, "signal")
				return

			while self.dataReady("feeds-inbox"):
				data = self.recv("feeds-inbox")
				self._feeds.append(data)
				print "xml", data['entry'].updated
				yield 1

			while self.dataReady("config-inbox"):
				data = self.recv("config-inbox")
				self._config = data
				print "xml-config", data.name, data.link

			if self._config is not None and len(self._feeds) == 10: #TODO: 10
				# TODO: first approach: 
				# * no use of sanitize.py (although feedparser seems to scape HTML)
				# * it generages and writes the file "in a single shot" (some filewriter should be used)
				# 
				tproc = TemplateProcessor()
				tproc.set('name',  self._config.name)
				tproc.set('link',  self._config.link)
				
				items = []
				
				for complete_entry in self._feeds:
					feed     = complete_entry['feed']
					entry    = complete_entry['entry']
					encoding = complete_entry['encoding']
					
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
					items.append(item)
					
				tproc.set('Items',  items)
				yield 1
				
				template = TemplateManager().prepare("rss20.xml.tmpl") #TODO: constant
				result = tproc.process(template)
				file_name = '/tmp/kamplanet.output.rss20.xml.tmpl'
				open(file_name, 'w').write(result)
				print "Check", file_name
				yield 1

			if not self.anyReady():
				self.pause()

			yield 1

