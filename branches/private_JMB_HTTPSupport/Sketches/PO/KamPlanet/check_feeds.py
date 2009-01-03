#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-

FILENAME='feeds-control.tmp'

import pickle
d = pickle.load(open(FILENAME))

not_stopped = [ url for url in d if d[url] == 'started' ]
stopped     = [ url for url in d if d[url] == 'stopped' ]
print 
print "Stopped"
for url in stopped:
	print "\t",url
print 
print "Not stopped"
for url in not_stopped:
	print "\t",url
print 
print "Not Stopped:",len(not_stopped)
print "Stopped:",len(stopped)
print "Total:",len(d.keys())
