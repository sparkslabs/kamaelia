#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Chassis.Carousel import Carousel
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
    
    def createFeed2fileManager(self, feed2fileFormatClass, 
                    channels_plugsplitter, feeds_plugsplitter, config_plugsplitter
                ):
        return Graphline(
            CHANNELS_SUBSCRIBER = self.subscribeToPlugsplitter(channels_plugsplitter), 
            FEEDS_SUBSCRIBER    = self.subscribeToPlugsplitter(feeds_plugsplitter),
            CONFIG_SUBSCRIBER   = self.subscribeToPlugsplitter(config_plugsplitter), 
            FEED2FILE_FORMAT    = feed2fileFormatClass(),
            FILE_WRITER         = Carousel(SimpleFileWriter),
            linkages = {
                ('FEEDS_SUBSCRIBER', 'outbox')        : ('FEED2FILE_FORMAT', 'feeds-inbox'), 
                ('CONFIG_SUBSCRIBER', 'outbox')       : ('FEED2FILE_FORMAT', 'config-inbox'), 
                ('CHANNELS_SUBSCRIBER', 'outbox')     : ('FEED2FILE_FORMAT', 'channels-inbox'), 
                ('FEED2FILE_FORMAT', 'outbox')        : ('FILE_WRITER', 'inbox'), 
                ('FEED2FILE_FORMAT', 'create-output') : ('FILE_WRITER', 'next'), 
                
                # Signals
                ('FEEDS_SUBSCRIBER', 'signal')        : ('FEED2FILE_FORMAT', 'control'), 
                ('FEED2FILE_FORMAT', 'signal')        : ('FILE_WRITER', 'control'), 
            }
        )
        
    def run(self):
        channels_plugsplitter                 = PlugSplitter()
        feeds_plugsplitter                    = PlugSplitter()
        config_plugsplitter                   = PlugSplitter()
        config_parser_finished_plugsplitter   = PlugSplitter()
        
        self.createFeed2fileManager(
                self.Feed2xml_class,
                channels_plugsplitter, feeds_plugsplitter, config_plugsplitter
        ).activate()
        self.createFeed2fileManager(
                self.Feed2html_class, 
                channels_plugsplitter, feeds_plugsplitter, config_plugsplitter
        ).activate()
        
        graph = Graphline(
                XML_PARSER                   = self._create_xml_parser(),
                CONFIG_PARSER                = self.ConfigFileParser_class(),
                FEED_PARSER_FACTORY          = self.FeedParserFactory_class(),
                CHANNELS_SUBSCRIBER          = self.subscribeToPlugsplitter(channels_plugsplitter), 
                CHANNELS_PUBLISHER           = channels_plugsplitter, 
                FEED_SORTER                  = self.FeedSorter_class(),
                FEED_PUBLISHER               = feeds_plugsplitter,
                CONFIG_SUBSCRIBER            = self.subscribeToPlugsplitter(config_plugsplitter), 
                CONFIG_PUBLISHER             = config_plugsplitter,
                CONFIG_PARSER_FINISHED_SUBS1 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED_SUBS2 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED_SUBS3 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED       = config_parser_finished_plugsplitter, 
                linkages = {
                    ('XML_PARSER', 'outbox')                    : ('CONFIG_PARSER','inbox'),
                    
                    ('CONFIG_PARSER', 'feeds-outbox')           : ('CHANNELS_PUBLISHER','inbox'),
                    ('CONFIG_PARSER', 'config-outbox')          : ('CONFIG_PUBLISHER','inbox'),
                    
                    ('CONFIG_SUBSCRIBER', 'outbox')             : ('FEED_SORTER', 'config-inbox'), 
                    
                    ('CHANNELS_SUBSCRIBER', 'outbox')           : ('FEED_PARSER_FACTORY','inbox'),
                    
                    ('FEED_PARSER_FACTORY', 'outbox')           : ('FEED_SORTER','inbox'),
                    
                    ('FEED_SORTER', 'outbox')                   : ('FEED_PUBLISHER','inbox'),
                    
                    # Signals
                    ('XML_PARSER', 'signal')                    : ('CONFIG_PARSER','control'),
                    ('CONFIG_PARSER', 'signal')                 : ('CONFIG_PARSER_FINISHED','control'),
                    ('CONFIG_PARSER_FINISHED_SUBS1', 'signal')  : ('FEED_PARSER_FACTORY', 'control'), 
                    ('CONFIG_PARSER_FINISHED_SUBS2', 'signal')  : ('CHANNELS_PUBLISHER', 'control'), 
                    ('CONFIG_PARSER_FINISHED_SUBS3', 'signal')  : ('CONFIG_PUBLISHER', 'control'), 
                    ('FEED_PARSER_FACTORY', 'signal')           : ('FEED_SORTER','control'),
                    ('FEED_SORTER', 'signal')                   : ('FEED_PUBLISHER', 'control'), 
                }
        )
        graph.run()

if __name__ == '__main__':
    #import introspector
    #introspector.activate()
    
    kamPlanet = KamPlanet("kamaelia-config.xml")
    kamPlanet.run()
