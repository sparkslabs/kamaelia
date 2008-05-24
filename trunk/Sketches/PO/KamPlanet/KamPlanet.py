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

from Kamaelia.Chassis.Pipeline    import Pipeline
from Kamaelia.Chassis.Graphline   import Graphline
from Kamaelia.Chassis.Carousel    import Carousel
from Kamaelia.Util.Splitter       import PlugSplitter,  Plug
from Kamaelia.File.Reading        import RateControlledFileReader
from Kamaelia.File.Writing        import SimpleFileWriter
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

from ConfigFileParser   import ConfigFileParser
from FeedParserFactory  import FeedParserFactory
from PostSorter         import PostSorter
from Posts2html         import Posts2html
from Posts2xml          import Posts2xml
from ForwarderComponent import Forwarder

DEFAULT_KAMPLANET_CONFIG_FILENAME = "kamaelia-config.xml"

class KamPlanet(object):
    Posts2xml_class         = Posts2xml
    Posts2html_class        = Posts2html
    PostSorter_class        = PostSorter
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
    
    def createPosts2fileManager(self, posts2file, 
                    channels_plugsplitter, feeds_plugsplitter, posts_plugsplitter, config_plugsplitter
                ):
        return Graphline(
            CHANNELS_SUBSCRIBER = self.subscribeToPlugsplitter(channels_plugsplitter), 
            FEEDS_SUBSCRIBER    = self.subscribeToPlugsplitter(feeds_plugsplitter),
            POSTS_SUBSCRIBER    = self.subscribeToPlugsplitter(posts_plugsplitter),
            CONFIG_SUBSCRIBER   = self.subscribeToPlugsplitter(config_plugsplitter), 
            POSTS2FILE          = posts2file(),
            FILE_WRITER         = Carousel(SimpleFileWriter),
            linkages = {
                ('FEEDS_SUBSCRIBER',    'outbox')        : ('POSTS2FILE',  'feeds-inbox'), 
                ('POSTS_SUBSCRIBER',    'outbox')        : ('POSTS2FILE',  'posts-inbox'), 
                ('CONFIG_SUBSCRIBER',   'outbox')        : ('POSTS2FILE',  'config-inbox'), 
                ('CHANNELS_SUBSCRIBER', 'outbox')        : ('POSTS2FILE',  'channels-inbox'), 
                ('POSTS2FILE',          'outbox')        : ('FILE_WRITER', 'inbox'), 
                ('POSTS2FILE',          'create-output') : ('FILE_WRITER', 'next'), 
                
                # Signals
                ('POSTS_SUBSCRIBER',    'signal')        : ('POSTS2FILE',  'control'), 
                ('POSTS2FILE',          'signal')        : ('FILE_WRITER', 'control'), 
            }
        )
        
    def run(self):
        channels_plugsplitter                 = PlugSplitter()
        feeds_plugsplitter                    = PlugSplitter()
        posts_plugsplitter                    = PlugSplitter()
        config_plugsplitter                   = PlugSplitter()
        config_parser_finished_plugsplitter   = PlugSplitter()
        
        self.createPosts2fileManager(
                self.Posts2xml_class,
                channels_plugsplitter, feeds_plugsplitter, posts_plugsplitter, config_plugsplitter
        ).activate()
        self.createPosts2fileManager(
                self.Posts2html_class, 
                channels_plugsplitter, feeds_plugsplitter, posts_plugsplitter, config_plugsplitter
        ).activate()
        
        graph = Graphline(
                XML_PARSER                   = self._create_xml_parser(),
                CONFIG_PARSER                = self.ConfigFileParser_class(),
                FEED_PARSER_FACTORY          = self.FeedParserFactory_class(),
                CHANNELS_SUBSCRIBER          = self.subscribeToPlugsplitter(channels_plugsplitter), 
                CHANNELS_SPLITTER            = channels_plugsplitter, 
                POST_SORTER                  = self.PostSorter_class(),
                POSTS_SUBSCRIBER             = self.subscribeToPlugsplitter(posts_plugsplitter), 
                POSTS_SPLITTER               = posts_plugsplitter,
                FEEDS_SUBSCRIBER             = self.subscribeToPlugsplitter(feeds_plugsplitter), 
                FEEDS_SPLITTER               = feeds_plugsplitter, 
                CONFIG_SUBSCRIBER            = self.subscribeToPlugsplitter(config_plugsplitter), 
                CONFIG_SPLITTER              = config_plugsplitter,
                CONFIG_PARSER_FINISHED_SUBS1 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED_SUBS2 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED_SUBS3 = self.subscribeToPlugsplitter(config_parser_finished_plugsplitter), 
                CONFIG_PARSER_FINISHED       = config_parser_finished_plugsplitter, 
                linkages = {
                    ('XML_PARSER',                   'outbox')        : ('CONFIG_PARSER',          'inbox'),
                    
                    ('CONFIG_PARSER',                'feeds-outbox')  : ('CHANNELS_SPLITTER',      'inbox'),
                    ('CONFIG_PARSER',                'config-outbox') : ('CONFIG_SPLITTER',        'inbox'),
                    
                    ('CONFIG_SUBSCRIBER',            'outbox')        : ('POST_SORTER',            'config-inbox'), 
                    
                    ('CHANNELS_SUBSCRIBER',          'outbox')        : ('FEED_PARSER_FACTORY',    'inbox'),
                    
                    ('FEED_PARSER_FACTORY',          'outbox')        : ('FEEDS_SPLITTER',         'inbox'),
                    
                    ('FEEDS_SUBSCRIBER',             'outbox')        : ('POST_SORTER',            'inbox'),
                    
                    ('POST_SORTER',                  'outbox')        : ('POSTS_SPLITTER',         'inbox'),
                    
                    # Signals
                    ('XML_PARSER',                   'signal')        : ('CONFIG_PARSER',          'control'),
                    ('CONFIG_PARSER',                'signal')        : ('CONFIG_PARSER_FINISHED', 'control'),
                    ('CONFIG_PARSER_FINISHED_SUBS1', 'signal')        : ('FEED_PARSER_FACTORY',    'control'), 
                    ('CONFIG_PARSER_FINISHED_SUBS2', 'signal')        : ('CHANNELS_SPLITTER',      'control'), 
                    ('CONFIG_PARSER_FINISHED_SUBS3', 'signal')        : ('CONFIG_SPLITTER',        'control'), 
                    ('FEED_PARSER_FACTORY',          'signal')        : ('POST_SORTER',            'control'),
                    ('POST_SORTER',                  'signal')        : ('POSTS_SPLITTER',         'control'),
                    ('POSTS_SUBSCRIBER',             'signal')        : ('FEEDS_SPLITTER',         'control'), 
                }
        )
        graph.run()

if __name__ == '__main__':
    from optparse import OptionParser
    #import introspector
    #introspector.activate()
    
    parser = OptionParser()
    parser.add_option("-c", "--config-file", 
                    dest="configFile",
                    help="kamplanet configuration file", 
                    metavar="FILE", 
                    default=DEFAULT_KAMPLANET_CONFIG_FILENAME
                )

    options, _ = parser.parse_args()
    kamPlanet = KamPlanet(options.configFile)
    kamPlanet.run()
