from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Backplane import Backplane, PublishTo, SubscribeTo
from Kamaelia.Util.Splitter import PlugSplitter,  Plug
from Kamaelia.File.Reading import RateControlledFileReader
from Kamaelia.File.Writing import SimpleFileWriter
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

from ConfigFileParser import ConfigFileParser
from FeedParserFactory import FeedParserFactory
from FeedSorter import FeedSorter
from Feed2html import Feed2html
from Feed2xml import Feed2xml
from ForwarderComponent import Forwarder

# TODO: change names: publisher vs splitters, post vs feed, etc.
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
            
    def subscribeToPlugsplitter(self,  plugsplitter):
        forwarder        = Forwarder()
        plug             = Plug(plugsplitter,  forwarder)
        plug.activate()
        outsideForwarder = Forwarder()
        plug.link((plug, 'outbox'), (outsideForwarder, 'secondary-inbox'))
        plug.link((plug, 'signal'), (outsideForwarder, 'secondary-control'))
        return outsideForwarder
    
    def run(self):
        channels_plugsplitter                 = PlugSplitter()
        feeds_plugsplitter                    = PlugSplitter()
        config_plugsplitter                   = PlugSplitter()
        config_parser_finished_plugsplitter   = PlugSplitter()
        
        channelSubscriberXml = self.subscribeToPlugsplitter(channels_plugsplitter)
        configSubscriberXml  = self.subscribeToPlugsplitter(config_plugsplitter)
        feedSubscriberXml    = self.subscribeToPlugsplitter(feeds_plugsplitter)
        feed2xml             = self.Feed2xml_class()
        #TODO: a carrousel might allow to retrieve this constant from the configuration file
        fileWriterXml        = SimpleFileWriter("output/rss20.xml")
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
                
                # Signals
                ('FEED2XML', 'signal')           : ('FILE_WRITER', 'control'), 
            }
        )
        graphXml.activate()
        
        configSubscriberHtml  = self.subscribeToPlugsplitter(config_plugsplitter)
        channelSubscriberHtml = self.subscribeToPlugsplitter(channels_plugsplitter)
        feedSubscriberHtml    = self.subscribeToPlugsplitter(feeds_plugsplitter)
        feed2html             = self.Feed2html_class()
        #TODO: a carrousel might allow to retrieve this constant from the configuration file
        fileWriterHtml        = SimpleFileWriter("output/index.html")
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
                
                # Signals
                ('FEED2HTML', 'signal')           : ('FILE_WRITER', 'control'), 
            }
        )
        graphHtml.activate()
        
        feedSorter         = self.FeedSorter_class()
        configFileParser   = self.ConfigFileParser_class()
        feedsPublisher     = feeds_plugsplitter
        feedParserFactory  = self.FeedParserFactory_class()
        channelsSubscriber = self.subscribeToPlugsplitter(channels_plugsplitter)
        channelsPublisher  = channels_plugsplitter
        configPublisher    = config_plugsplitter
        graph = Graphline(
                XML_PARSER             = self._create_xml_parser(),
                CONFIG_PARSER          = configFileParser,
                FEED_PARSER_FACTORY    = feedParserFactory,
                CHANNELS_SUBSCRIBER    = channelsSubscriber, 
                CHANNELS_PUBLISHER     = channelsPublisher, 
                FEED_SORTER            = feedSorter,
                FEED_PUBLISHER         = feedsPublisher,
                CONFIG_PUBLISHER       = configPublisher,
                CONFIG_PARSER_FINISHED_SUBS1 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED_SUBS2 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED_SUBS3 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED      = config_parser_finished_plugsplitter, 
                linkages = {
                    ('XML_PARSER', 'outbox')             : ('CONFIG_PARSER','inbox'),
                    
                    ('CONFIG_PARSER', 'feeds-outbox')    : ('CHANNELS_PUBLISHER','inbox'),
                    ('CONFIG_PARSER', 'config-outbox')   : ('CONFIG_PUBLISHER','inbox'),
                    
                    ('CHANNELS_SUBSCRIBER', 'outbox')    : ('FEED_PARSER_FACTORY','inbox'),
                    
                    ('FEED_PARSER_FACTORY', 'outbox')    : ('FEED_SORTER','inbox'),
                    
                    ('FEED_SORTER', 'outbox')            : ('FEED_PUBLISHER','inbox'),
                    
                    # Signals
                    ('XML_PARSER', 'signal')                   : ('CONFIG_PARSER','control'),
                    ('CONFIG_PARSER', 'signal')                : ('CONFIG_PARSER_FINISHED','control'),
                    ('CONFIG_PARSER_FINISHED_SUBS1', 'signal') : ('FEED_PARSER_FACTORY', 'control'), 
                    ('CONFIG_PARSER_FINISHED_SUBS2', 'signal') : ('CHANNELS_PUBLISHER', 'control'), 
                    ('CONFIG_PARSER_FINISHED_SUBS3', 'signal') : ('CONFIG_PUBLISHER', 'control'), 
                    ('FEED_PARSER_FACTORY', 'signal')          : ('FEED_SORTER','control'),
                    ('FEED_SORTER', 'signal')                  : ('FEED_PUBLISHER', 'control'), 
                }
        )
        
        graph.run()

if __name__ == '__main__':
    #import introspector
    #introspector.activate()
    
    kamPlanet = KamPlanet("kamaelia-config.xml")
    kamPlanet.run()
