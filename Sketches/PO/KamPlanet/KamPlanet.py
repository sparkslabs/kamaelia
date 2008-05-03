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
	backplane = Backplane("FEEDS")
	backplane.activate()

	pipelineXml = Pipeline(
		SubscribeTo("FEEDS"),
		Feed2xml()
	)
	pipelineXml.activate()

	pipelineHtml = Pipeline(
		SubscribeTo("FEEDS"),
		Feed2html()
	)
	pipelineHtml.activate()

	feedSorter = FeedSorter()
	graph = Graphline(
			CONFIG_PARSER       = ConfigFileParser(),
			FEED_PARSER_FACTORY = FeedParserFactory(),
			FEED_SORTER         = feedSorter,
			PUBLISHER           = PublishTo("FEEDS"),
			linkages = {
				('CONFIG_PARSER', 'outbox')         : ('FEED_PARSER_FACTORY','inbox'),
				('CONFIG_PARSER', 'signal')         : ('FEED_PARSER_FACTORY','control'),
				('FEED_PARSER_FACTORY', 'outbox')   : ('FEED_SORTER','inbox'),
				('CONFIG_PARSER', 'counter-outbox') : ('FEED_SORTER','counter-inbox'),
				('FEED_PARSER_FACTORY', 'signal')   : ('FEED_SORTER','control'),
				('FEED_SORTER', 'outbox')           : ('PUBLISHER','inbox'),
				('FEED_SORTER', 'signal')           : ('PUBLISHER','control'),
			}
	)
	#feedSorter.link((feedSorter,'signal'),(backplane,'control'))

	import threading, time
	class Watcher(threading.Thread):
		def run(self):
			while 1:
				time.sleep(1)
				print (graph.children, 
						backplane._isStopped(), 
						pipelineXml._isStopped(),
						pipelineHtml._isStopped()
					)
	w = Watcher()
	w.setDaemon(1)
	w.start()
	graph.run()

