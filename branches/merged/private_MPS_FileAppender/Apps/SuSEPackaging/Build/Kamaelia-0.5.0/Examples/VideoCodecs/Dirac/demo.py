#!/usr/bin/env python

#
# Generated with Kamaelia: Compose
#

from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.RateFilter import MessageRateLimit
from Kamaelia.Codec.Dirac import DiracDecoder
from Kamaelia.Internet.SingleServer import SingleServer
from Kamaelia.Chassis.Graphline import Graphline
Graphline(RFA1 = ReadFileAdaptor( filename = "/home/michaels/Development/Projects/Kamaelia/Code/Python/Kamaelia/Examples/VideoCodecs/Dirac/snowboard-jum-352x288x75.dirac.drc", bitrate = 400000 ),
          TCPC3 = TCPClient( host = "127.0.0.1", port = 1500 ),
          SS2 = SingleServer( port = 1500 ),
          MRL5 = MessageRateLimit( messages_per_second = 15, buffer = 15 ),
          DD4 = DiracDecoder(  ),
          VO6 = VideoOverlay(  ),
           linkages = {('RFA1', 'outbox') : ('SS2', 'inbox'),
                       ('TCPC3', 'outbox') : ('DD4', 'inbox'),
                       ('DD4', 'outbox') : ('MRL5', 'inbox'),
                       ('MRL5', 'outbox') : ('VO6', 'inbox'),
          }
).run()
