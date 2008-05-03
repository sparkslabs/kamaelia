from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo

from ConfigFileParser import ConfigFileParser
from FeedParserFactory import FeedParserFactory
from FeedSorter import FeedSorter
from Feed2html import Feed2html
from Feed2xml import Feed2xml

# TODO list:
# * Process not dying:
#    - if I link FEED_SORTER signal with publisher, publisher dies but backplane is still active
#    - if I link FEED_SORTER signal with backplane, backplane dies but publisher is still active
#    * How do I resolve this?
# * Actually implement the ConfigParser reading a configuration file :-D
# * Actually implement the 2html and 2xml stuff :-D
# * Quite several doubts written at tomboy :-o

if __name__ == '__main__':
	backplane_feeds = Backplane("KAMPLANET_FEEDS")
	backplane_feeds.activate()

	backplane_config = Backplane("KAMPLANET_CONFIG")
	backplane_config.activate()

	graphXml = Graphline(
		FEEDS_SUBSCRIBER  = SubscribeTo("KAMPLANET_FEEDS"),
		CONFIG_SUBSCRIBER = SubscribeTo("KAMPLANET_CONFIG"), 
		FEED2XML          = Feed2xml(), 
		linkages = {
			('FEEDS_SUBSCRIBER', 'outbox')  : ('FEED2XML', 'feeds-inbox'), 
			('CONFIG_SUBSCRIBER', 'outbox') : ('FEED2XML', 'config-inbox'), 
		}
	)
	graphXml.activate()

	graphHtml = Graphline(
		FEEDS_SUBSCRIBER  = SubscribeTo("KAMPLANET_FEEDS"),
		CONFIG_SUBSCRIBER = SubscribeTo("KAMPLANET_CONFIG"), 
		FEED2HTML          = Feed2html(),
		linkages = {
			('FEEDS_SUBSCRIBER', 'outbox')  : ('FEED2HTML', 'feeds-inbox'), 
			('CONFIG_SUBSCRIBER', 'outbox') : ('FEED2HTML', 'config-inbox'), 
		}
	)
	graphHtml.activate()

	feedSorter = FeedSorter()
	graph = Graphline(
			CONFIG_PARSER       = ConfigFileParser(),
			FEED_PARSER_FACTORY = FeedParserFactory(),
			FEED_SORTER         = feedSorter,
			FEED_PUBLISHER      = PublishTo("KAMPLANET_FEEDS"),
			CONFIG_PUBLISHER    = PublishTo("KAMPLANET_CONFIG"),
			linkages = {
				('CONFIG_PARSER', 'feeds-outbox')   : ('FEED_PARSER_FACTORY','inbox'),
				('CONFIG_PARSER', 'signal')         : ('FEED_PARSER_FACTORY','control'),
				('FEED_PARSER_FACTORY', 'outbox')   : ('FEED_SORTER','inbox'),
				('CONFIG_PARSER', 'counter-outbox') : ('FEED_SORTER','counter-inbox'),
				('CONFIG_PARSER', 'config-outbox')  : ('CONFIG_PUBLISHER','inbox'),
				('FEED_PARSER_FACTORY', 'signal')   : ('FEED_SORTER','control'),
				('FEED_SORTER', 'outbox')           : ('FEED_PUBLISHER','inbox'),
				('FEED_SORTER', 'signal')           : ('FEED_PUBLISHER','control'),
			}
	)
	#feedSorter.link((feedSorter,'signal'),(backplane,'control'))

	import threading, time
	class Watcher(threading.Thread):
		def run(self):
			while 1:
				time.sleep(1)
				print (graph.children, 
						backplane_feeds._isStopped(), 
						backplane_config._isStopped(), 
						graphXml._isStopped(),
						graphHtml._isStopped()
					)
	w = Watcher()
	w.setDaemon(1)
	w.start()
	graph.run()
	
