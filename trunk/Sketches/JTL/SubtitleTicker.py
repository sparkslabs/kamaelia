#!/usr/bin/python

from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.PipelineComponent import pipeline
from Ticker import Ticker
from TagFilterComponent import TagFilterComponent

tickerIP = "132.185.133.22"
tickerPort = 1500

pipeline(TCPClient(tickerIP,tickerPort),
         TagFilterComponent(),
                Ticker()
        ).run()
