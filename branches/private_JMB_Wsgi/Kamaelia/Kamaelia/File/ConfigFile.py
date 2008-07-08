#!/usr/bin/env python
#
# Copyright (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
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
# Licensed to the BBC under a Contributor Agreement: JMB
"""
This module is used for reading config files.  A config file is a standard .ini file
that looks something like this:

[section]
option1:  blah
option2:  blahblah
option3:  blahblahblah

ConfigFileReader
-----------------

The base of the set is the ConfigFileReader component, which will read the config
file and then send each individual section of it out on its outbox as a tuple consisting
of the section name, and a list of tuples that represents the options.

Thus, for the example given above, the ConfigFileReader will output something like:

('section',
 [
    ('option1', 'blah'),
    ('option2', 'blahblah'),
    ('option3', 'blahblahblah')
 ]
)

The formatters
---------------

The ConfigFileReader was designed to use a set of formatters to format the results
into a usable piece of data.  FormatterBase defines how these formatters should work.

Using this method, each formatter may be a link in the chain or they may also be
the producer of the end result.  You may get the end result out of the last component
by calling its getResults method.  This will simply return self.results (which is
where the results should be stored by the formatter).

==================
DictFormatter
==================

This formatter is used to format the results into a dictionary.  Please note that
the value stored into self.results will be different from the compiled results of
listening to its outbox.  Reading self.results will give a dictionary of dictionaries
while the results passed on the outbox will be a tuple containing the section name
and a dictionary that contains the options.  For example, if a DictFormatter was
connected to a ConfigFileReader that read the example config file posted above,
you would get the following if you read self.results:

{'section' : {
    'option1' : 'blah',
    'option2' : 'blahblah',
    'option3' : 'blahblahblah',
}}

However, if you were to read the DictFormatter's outbox, you would get:

('section', {
    'option1' : 'blah',
    'option2' : 'blahblah',
    'option3' : 'blahblahblah',
})

This is done in case any listening formatters depend upon the order of the sections.
"""

from Axon.Component import component
from Axon.Ipc import producerFinished
from Kamaelia.Chassis.Pipeline import Pipeline
from ConfigParser import SafeConfigParser
from pprint import pprint
import os


##################################
#The config file reader
##################################
class ConfigFileReader(component):
    def __init__(self, filename, defaults=None, vars=None):
        super(ConfigFileReader, self).__init__()
        self.config_parser = SafeConfigParser(defaults)
        filename = os.path.expanduser(filename)
#        print 'filename = %s' % (filename)
        self.config_parser.read(filename)
        sections = self.config_parser.sections()
        #print sections
        self.isections = iter(sections)
        self.vars = None

    def main(self):
        while 1:
            try:
                section = self.isections.next()
#                print 'section ='
#                pprint(section)
            except StopIteration:
                break

            self.send((section, self.config_parser.items(section, vars=self.vars)))
            yield 1

        self.send(producerFinished(self), 'signal')

##################################
#The config file formatters
##################################

class FormatterBase(component):
    Inboxes = {'inbox' : 'used to receive input from the ConfigFileReader',
               'control' : 'used to receive producerFinished'}
    Outboxes = {'outbox' : 'Used to forward results piece by piece for formatter chaining',
                'signal' : 'used to send producerFinished'}

    def __init__(self, **argd):
        super(FormatterBase, self).__init__(argd)
        self.results = None
    def getResults(self):
        """
        This method is used to pull results once processing is finished.
        """
        return self.results

class DictFormatter(FormatterBase):
    def __init__(self):
        super(DictFormatter, self).__init__()
        self.results = {}

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                signal = self.recv('control')
                if isinstance(signal, producerFinished):
                    not_done = False

            while self.dataReady('inbox'):
                section, options = self.recv('inbox')
                self.results[section] = dict(options)
                self.send((section, dict(options)))

            if not self.anyReady() and not_done:
                self.pause()

            yield 1

        self.send(producerFinished(self), 'signal')

##################################
#Support functions
##################################

def ParseConfigFile(filename, formatters, defaults=None, vars=None):
    if isinstance(formatters, FormatterBase):
        Pipeline(
            ConfigFileReader(filename),
            formatters
        ).run()
        return formatters.getResults()
    else:
        try:
            components = [ConfigFileReader(filename)] + formatters
        except TypeError:
            raise ParseException('Unknown argument passed to ParseConfigFile')
        [x.activate() for x in formatters]
        RecursiveLink(iter(components)).run()
    return formatters[-1].getResults()

def RecursiveLink(iterable, current=None):
    """
    This will link up components just as a pipeline does but in a recursive
    fashion and over an iterator.  You should always leave out current when
    calling this function.

    This function will return the first component in the iterable
    """
    if current is None:
        try:
            comp1 = iterable.next()
            comp2 = iterable.next()
        except StopIteration:
            return comp1
    else:
        try:
            comp1 = current
            comp2 = iterable.next()
        except StopIteration:
            return comp1

    comp1.link((comp1, 'outbox'), (comp2, 'inbox'))
    comp1.link((comp1, 'signal'), (comp2, 'control'))

    RecursiveLink(iterable, comp2)
    return comp1
##################################
#Exceptions
##################################

class ParseException(Exception):
    pass


##################################
#Example
##################################
if __name__ == '__main__':
    from pprint import pprint
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = '~/urls'

    pprint(ParseConfigFile(filename, [DictFormatter(), UrlListFormatter()]))
