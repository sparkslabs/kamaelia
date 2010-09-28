#!/usr/bin/python

import simplejson
import time

from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.DataSource import DataSource

def TimeService(**argd):
    return Pipeline(
              DataSource([time.time()]),
              PureTransformer(lambda x: time.localtime(x)),
              PureTransformer(lambda x: [y for y in x]),
              PureTransformer(lambda x: simplejson.dumps(x)),
           )

FastRestartServer(protocol=TimeService, port=1500).run()
