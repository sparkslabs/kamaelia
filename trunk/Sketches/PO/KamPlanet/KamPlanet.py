#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
# 
# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: PO

import libraries

from Kamaelia.Chassis.Pipeline    import Pipeline
from Kamaelia.Chassis.Graphline   import Graphline
from Kamaelia.Chassis.Carousel    import Carousel
from Kamaelia.Util.Splitter       import PlugSplitter,  Plug
from Kamaelia.File.Reading        import RateControlledFileReader
from Kamaelia.File.Writing        import SimpleFileWriter
from Kamaelia.XML.SimpleXMLParser import SimpleXMLParser

from ConfigFileParser     import ConfigFileParser
from FeedParserFactory    import FeedParserFactory
from PostSorter           import PostSorter
from KamTemplateProcessor import KamTemplateProcessor
from ForwarderComponent   import Forwarder

DEFAULT_KAMPLANET_CONFIG_FILENAME = "kamaelia-config.xml"

class KamPlanet(object):
    def __init__(self, fileName,  **argd):
        super(KamPlanet, self).__init__(self, **argd)
        self._fileName = fileName
    
    def create_xml_parser(self):
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
    
    def createPosts2fileManager(self, 
                    channels_plugsplitter, feeds_plugsplitter, posts_plugsplitter, config_plugsplitter, 
                    templateField, outputFileField
                ):
        return Graphline(
            CHANNELS_SUBSCRIBER = self.subscribeToPlugsplitter(channels_plugsplitter), 
            FEEDS_SUBSCRIBER    = self.subscribeToPlugsplitter(feeds_plugsplitter),
            POSTS_SUBSCRIBER    = self.subscribeToPlugsplitter(posts_plugsplitter),
            CONFIG_SUBSCRIBER   = self.subscribeToPlugsplitter(config_plugsplitter), 
            POSTS2FILE          = KamTemplateProcessor(templateField, outputFileField),
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
        
    def start(self):
        channels_plugsplitter                 = PlugSplitter()
        feeds_plugsplitter                    = PlugSplitter()
        posts_plugsplitter                    = PlugSplitter()
        config_plugsplitter                   = PlugSplitter()
        config_parser_finished_plugsplitter   = PlugSplitter()
        
        self.createPosts2fileManager(
                channels_plugsplitter, feeds_plugsplitter, posts_plugsplitter, config_plugsplitter, 
                'rssTemplateName', 'rssFileName'
        ).activate()
        self.createPosts2fileManager(
                channels_plugsplitter, feeds_plugsplitter, posts_plugsplitter, config_plugsplitter,
                'htmlTemplateName', 'htmlFileName'
        ).activate()
        
        self.component = Graphline(
                XML_PARSER                   = self.create_xml_parser(),
                CONFIG_PARSER                = ConfigFileParser(),
                FEED_PARSER_FACTORY          = FeedParserFactory(),
                CHANNELS_SUBSCRIBER          = self.subscribeToPlugsplitter(channels_plugsplitter), 
                CHANNELS_SPLITTER            = channels_plugsplitter, 
                POST_SORTER                  = PostSorter(),
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

if __name__ == '__main__':
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-c", "--config-file", 
                    dest="configFile",
                    help="kamplanet configuration file", 
                    metavar="FILE", 
                    default=DEFAULT_KAMPLANET_CONFIG_FILENAME
                )
    parser.add_option("-i", "--introspector", 
                    action="store_true", 
                    dest="introspector",
                    help="activate introspector module: more information will be provided but the program will never finish", 
                    default=False
                )
    parser.add_option("-p", "--rt-debugger-port",
                    dest="debuggerPort",
                    help="real-time debugger port (only launched if provided)", 
                    metavar="PORT",
                    default=None
                )
               
    options, _ = parser.parse_args()
    if options.introspector:
        import introspector
        introspector.activate()
    if options.debuggerPort:
        try:
            port = int(options.debuggerPort)
        except ValueError, ve:
            print >> sys.stderr, "Invalid debugger port found: <%s>; skipping debugger" % options.debuggerPort
        else:
            import rt_debugger
            rt_debugger.launch_debugger(port)
            
    kamPlanet = KamPlanet(options.configFile)
    kamPlanet.start()
    kamPlanet.component.run()
