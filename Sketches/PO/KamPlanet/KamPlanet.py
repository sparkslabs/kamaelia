from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

from ConfigFileParser import ConfigFileParser
from FeedParserFactory import FeedParserFactory
from FeedSorter import FeedSorter
from Feed2html import Feed2html
from Feed2xml import Feed2xml

# TODO: another backplane is needed for providing to Feed2xml and Feed2html the feeds (channels)
# 

class KamPlanet(object):
    Feed2xml_class          = Feed2xml
    Feed2html_class         = Feed2html
    FeedSorter_class        = FeedSorter
    ConfigFileParser_class  = ConfigFileParser
    FeedParserFactory_class = FeedParserFactory
    
    def __init__(self, fileName,  **argd):
        super(KamPlanet, self).__init__(self, **argd)
        self._fileName = fileName
    
    def _create_xml_parser(self):
        return Pipeline(
                RateControlledFileReader(self._fileName ),
                SimpleXMLParser()
            )
    
    def run(self):
        backplane_channels = Backplane("KAMPLANET_CHANNELS")
        backplane_channels.activate()
        
        backplane_feeds = Backplane("KAMPLANET_FEEDS")
        backplane_feeds.activate()
        
        backplane_config = Backplane("KAMPLANET_CONFIG")
        backplane_config.activate()

        configSubscriber1 = SubscribeTo("KAMPLANET_CONFIG")
        graphXml = Graphline(
            FEEDS_SUBSCRIBER  = SubscribeTo("KAMPLANET_FEEDS"),
            CONFIG_SUBSCRIBER = configSubscriber1, 
            FEED2XML          = self.Feed2xml_class(), 
            FILE_WRITER       = SimpleFileWriter("output/rss20.xml"),  #TODO: constant
            linkages = {
                ('FEEDS_SUBSCRIBER', 'outbox')  : ('FEED2XML', 'feeds-inbox'), 
                ('CONFIG_SUBSCRIBER', 'outbox') : ('FEED2XML', 'config-inbox'), 
                ('FEED2XML', 'outbox')          : ('FILE_WRITER', 'inbox'), 
                
                # Signaling
                ('FEEDS_SUBSCRIBER', 'signal')  : ('FEED2XML', 'control'), 
                ('FEED2XML', 'signal')          : ('FILE_WRITER', 'control'), 
            }
        )
        graphXml.activate()
        
        configSubscriber2 = SubscribeTo("KAMPLANET_CONFIG")
        graphHtml = Graphline(
            FEEDS_SUBSCRIBER  = SubscribeTo("KAMPLANET_FEEDS"),
            CONFIG_SUBSCRIBER = configSubscriber2, 
            FEED2HTML         = self.Feed2html_class(),
            FILE_WRITER       = SimpleFileWriter("output/index.html"),  #TODO: constant
            linkages = {
                ('FEEDS_SUBSCRIBER', 'outbox')  : ('FEED2HTML', 'feeds-inbox'), 
                ('CONFIG_SUBSCRIBER', 'outbox') : ('FEED2HTML', 'config-inbox'), 
                ('FEED2HTML', 'outbox')          : ('FILE_WRITER', 'inbox'), 
                
                # Signaling
                ('FEEDS_SUBSCRIBER', 'signal')  : ('FEED2HTML', 'control'), 
                ('FEED2HTML', 'signal')          : ('FILE_WRITER', 'control'), 
            }
        )
        graphHtml.activate()
        
        feedSorter       = self.FeedSorter_class()
        configFileParser = self.ConfigFileParser_class()
        feedsPublisher   = PublishTo("KAMPLANET_FEEDS")
        graph = Graphline(
                XML_PARSER          = self._create_xml_parser(),
                CONFIG_PARSER       = configFileParser,
                FEED_PARSER_FACTORY = self.FeedParserFactory_class(),
                CHANNELS_SUBSCRIBER = SubscribeTo("KAMPLANET_CHANNELS"), 
                CHANNELS_PUBLISHER  = PublishTo("KAMPLANET_CHANNELS"), 
                FEED_SORTER         = feedSorter,
                FEED_PUBLISHER      = feedsPublisher,
                CONFIG_PUBLISHER    = PublishTo("KAMPLANET_CONFIG"),
                linkages = {
                    ('XML_PARSER', 'outbox')            : ('CONFIG_PARSER','inbox'),
                    
                    ('CONFIG_PARSER', 'feeds-outbox')   : ('CHANNELS_PUBLISHER','inbox'),
                    ('CONFIG_PARSER', 'config-outbox')  : ('CONFIG_PUBLISHER','inbox'),
                    
                    ('CHANNELS_SUBSCRIBER', 'outbox')   : ('FEED_PARSER_FACTORY','inbox'),
                    
                    ('FEED_PARSER_FACTORY', 'outbox')   : ('FEED_SORTER','inbox'),
                    
                    ('FEED_SORTER', 'outbox')           : ('FEED_PUBLISHER','inbox'),
                    
                    # Signaling
                    ('XML_PARSER', 'signal')            : ('CONFIG_PARSER','control'),
                    ('CONFIG_PARSER', 'signal')         : ('FEED_PARSER_FACTORY','control'),
                    ('FEED_PARSER_FACTORY', 'signal')   : ('FEED_SORTER','control'),
                    ('FEED_SORTER', 'signal')           : ('CONFIG_PUBLISHER','control'),
                }
        )
        
        # TODO: both?
        configSubscriber1.link((configSubscriber1, 'signal'),  (backplane_feeds,  'control'))
        configSubscriber2.link((configSubscriber2, 'signal'),  (backplane_feeds,  'control'))
        
        graph.run()

if __name__ == '__main__':
    import introspector
    introspector.activate()
    
    kamPlanet = KamPlanet("kamaelia-config.xml")
    kamPlanet.run()
