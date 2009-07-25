#!/usr/bin/python
'''
This file contains an example of using Kamaelia.Apps.SA.DSL.DataSink
'''

from Kamaelia.Util.DataSource import DataSource
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Apps.SA.DSL import DataSink

class mylist(list):
    def append(self, item):
        print "Appending", item
        super(mylist, self).append(item)

R = mylist()
Pipeline(
    DataSource([1,2,3,4]),
    DataSink(R)
).run()

print R
