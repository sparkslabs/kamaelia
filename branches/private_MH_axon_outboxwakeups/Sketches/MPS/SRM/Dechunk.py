#!/usr/bin/python
#
# Algorithm tester/experiment
#


import random

def datasource():
    r = random.randrange(50,100)
    while 1:
        yield "XXXXXXXXXXXXXXXXXXXXXXX"
        for i in xrange(r):
            yield str(i)
        r = random.randrange(50,100)
      
def consumer(datasource, divider="XXXXXXXXXXXXXXXXXXXXXXX"):
    buffer = ''
    foundFirstChunk = 0
    for i in datasource:
        buffer += i
        location = buffer.find(divider,len(divider))
        if location != -1:
            if foundFirstChunk:
                chunk = buffer[:location]
                print "CHUNK", chunk
            buffer = buffer[location:]
            foundFirstChunk = 1

consumer(datasource(), "XXXXXXXXXXXXXXXXXXXXXXX")
