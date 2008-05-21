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

        configSubscriberXml  = SubscribeTo("KAMPLANET_CONFIG")
        channelSubscriberXml = SubscribeTo("KAMPLANET_CHANNELS")
        feedSubscriberXml    = SubscribeTo("KAMPLANET_FEEDS")
        feed2xml             = self.Feed2xml_class()
        fileWriterXml        = SimpleFileWriter("output/rss20.xml") #TODO: constant
        graphXml = Graphline(
            CHANNELS_SUBSCRIBER = channelSubscriberXml, 
            FEEDS_SUBSCRIBER    = feedSubscriberXml,
            CONFIG_SUBSCRIBER   = configSubscriberXml, 
            FEED2XML            = feed2xml,
            FILE_WRITER         = fileWriterXml,
            linkages = {
                ('FEEDS_SUBSCRIBER', 'outbox')  : ('FEED2XML', 'feeds-inbox'), 
                ('CONFIG_SUBSCRIBER', 'outbox') : ('FEED2XML', 'config-inbox'), 
                ('CHANNELS_SUBSCRIBER', 'outbox') : ('FEED2HTML', 'channels-inbox'), 
                ('FEED2XML', 'outbox')          : ('FILE_WRITER', 'inbox'), 
            }
        )
        graphXml.activate()
        
        configSubscriberHtml  = SubscribeTo("KAMPLANET_CONFIG")
        channelSubscriberHtml = SubscribeTo("KAMPLANET_CHANNELS")
        feedSubscriberHtml    = SubscribeTo("KAMPLANET_FEEDS")
        feed2html             = self.Feed2html_class()
        fileWriterHtml        = SimpleFileWriter("output/index.html")   #TODO: constant
        graphHtml = Graphline(
            CHANNELS_SUBSCRIBER = channelSubscriberHtml, 
            FEEDS_SUBSCRIBER  = feedSubscriberHtml,
            CONFIG_SUBSCRIBER = configSubscriberHtml, 
            FEED2HTML         = feed2html,
            FILE_WRITER       = fileWriterHtml,
            linkages = {
                ('FEEDS_SUBSCRIBER', 'outbox')    : ('FEED2HTML', 'feeds-inbox'), 
                ('CONFIG_SUBSCRIBER', 'outbox')   : ('FEED2HTML', 'config-inbox'), 
                ('CHANNELS_SUBSCRIBER', 'outbox') : ('FEED2HTML', 'channels-inbox'), 
                ('FEED2HTML', 'outbox')           : ('FILE_WRITER', 'inbox'),                 
            }
        )
        graphHtml.activate()
        
        feedSorter         = self.FeedSorter_class()
        configFileParser   = self.ConfigFileParser_class()
        feedsPublisher     = PublishTo("KAMPLANET_FEEDS")
        feedParserFactory  = self.FeedParserFactory_class()
        channelsSubscriber = SubscribeTo("KAMPLANET_CHANNELS")
        channelsPublisher  = PublishTo("KAMPLANET_CHANNELS")
        configPublisher    = PublishTo("KAMPLANET_CONFIG")
        graph = Graphline(
                XML_PARSER          = self._create_xml_parser(),
                CONFIG_PARSER       = configFileParser,
                FEED_PARSER_FACTORY = feedParserFactory,
                CHANNELS_SUBSCRIBER = channelsSubscriber, 
                CHANNELS_PUBLISHER  = channelsPublisher, 
                FEED_SORTER         = feedSorter,
                FEED_PUBLISHER      = feedsPublisher,
                CONFIG_PUBLISHER    = configPublisher,
                linkages = {
                    ('XML_PARSER', 'outbox')            : ('CONFIG_PARSER','inbox'),
                    
                    ('CONFIG_PARSER', 'feeds-outbox')   : ('CHANNELS_PUBLISHER','inbox'),
                    ('CONFIG_PARSER', 'config-outbox')  : ('CONFIG_PUBLISHER','inbox'),
                    
                    ('CHANNELS_SUBSCRIBER', 'outbox')   : ('FEED_PARSER_FACTORY','inbox'),
                    
                    ('FEED_PARSER_FACTORY', 'outbox')   : ('FEED_SORTER','inbox'),
                    
                    ('FEED_SORTER', 'outbox')           : ('FEED_PUBLISHER','inbox'),
                    
                    # Signals
                    ('XML_PARSER', 'signal')            : ('CONFIG_PARSER','control'),
                    ('CONFIG_PARSER', 'signal')         : ('FEED_PARSER_FACTORY','control'),
                    ('FEED_PARSER_FACTORY', 'signal')   : ('FEED_SORTER','control'),
                }
        )
        
        # At this point, I haven't found any way to multiplex a signal outbox
        # to multiple control inboxes, which becomes a problem when dealing with
        # backplanes. This way, I draw a line through all the components that, in 
        # the end, are not called by anyone. You can easily see this line in the
        # documentation (basic_design.odg)
        
        # <Signal linkages (following the line drawed in the documentation)>
        feedSorter.link((feedSorter, 'signal'),                       (backplane_feeds, 'control'))
        backplane_feeds.link((backplane_feeds, 'signal'),             (feedSubscriberHtml, 'control'))
        feedSubscriberHtml.link((feedSubscriberHtml, 'signal'),       (feedsPublisher, 'control'))
        feedsPublisher.link((feedsPublisher, 'signal'),               (feedSubscriberXml, 'control'))
        feedSubscriberXml.link((feedSubscriberXml, 'signal'),         (backplane_channels, 'control'))
        backplane_channels.link((backplane_channels, 'signal'),       (channelsPublisher, 'control'))
        channelsPublisher.link((channelsPublisher, 'signal'),         (channelsSubscriber, 'control'))
        channelsSubscriber.link((channelsSubscriber, 'signal'),       (channelSubscriberHtml, 'control'))
        channelSubscriberHtml.link((channelSubscriberHtml, 'signal'), (channelSubscriberXml, 'control'))
        channelSubscriberXml.link((channelSubscriberXml, 'signal'),   (backplane_config, 'control'))
        backplane_config.link((backplane_config, 'signal'),           (configPublisher, 'control'))
        configPublisher.link((configPublisher, 'signal'),             (configSubscriberXml, 'control'))
        configSubscriberXml.link((configSubscriberXml, 'signal'),     (configSubscriberHtml, 'control'))
        configSubscriberHtml.link((configSubscriberHtml, 'signal'),   (feed2html, 'control'))
        feed2html.link((feed2html, 'signal'),                         (fileWriterHtml, 'control'))
        fileWriterHtml.link((fileWriterHtml, 'signal'),               (feed2xml, 'control'))
        feed2xml.link((feed2xml, 'signal'),                           (fileWriterXml, 'control'))
        fileWriterXml.link((fileWriterXml, 'signal'),                 (graph, 'control'))
        graph.link((graph, 'signal'),                                 (graphXml, 'control'))
        graphXml.link((graphXml, 'signal'),                           (graphHtml, 'control'))
        # </Signal linkages>
        
        graph.run()

if __name__ == '__main__':
    #import introspector
    #introspector.activate()
    
    kamPlanet = KamPlanet("kamaelia-config.xml")
    kamPlanet.run()
