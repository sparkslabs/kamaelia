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
This module contains the necessary parts to adapt the Kamaelia Config file reader
to read a Wsgi Config file as used in Kamaelia Publish.  A UrlListFormatter is included,
but you probably don't want to use it directly unless you want to make another formatter
to parse its output.

Instead, you should call the convenience function ParseUrlFile.  This will process
all of the formatting for you.

Example
----------
Suppose you had the following urls file:

[static_files]
regex: static
import_path: Kamaelia.Support.WsgiApps.Static
app_object: static_app
static_path: ~/www
index_file: index.html

[simple_app]
regex: simple
import_path: Kamaelia.Support.WsgiApps.Simple
app_object: simple_app

[error_404]
import_path: Kamaelia.Support.WsgiApps.ErrorHandler
app_object: application

A call to ParseUrlFile would produce the following output:

[
    {
        'kp.regex' : 'static',
        'kp.import_path' : 'Kamaelia.Support.WsgiApps.Static',
        'kp.app_object' : 'static_app',
        'kp.static_path' : '~/www',
        'kp.index_file' : 'index.html',
    }
    {
        'kp.regex' : 'simple',
        'kp.import_path' : 'Kamaelia.Support.WsgiApps.Simple',
        'kp.app_object' : 'simple_app',
    }
    {
        'kp.regex' : '.*',
        'kp.import_path' : 'Kamaelia.Support.WsgiApps.ErrorHandler',
        'kp.app_object' : 'application',
    }
]

Changes made
-------------

The Formatter will make the following changes:

* Each option will be prepended with 'kp.' if it does not already have an identifier
at the beginning.  Thus, 'foo.bar' will stay 'foo.bar' and will not be prepended
with 'kp.', while 'regex' will be converted to 'kp.regex'

* It will raise an exception if there is not an error_404 section or the error_404 section
contains a regex.

* It will add '.*' as the regex for error_404.
"""

from Kamaelia.File.ConfigFile import FormatterBase, ParseConfigFile, DictFormatter, ParseException
from Axon.Ipc import producerFinished, shutdownMicroprocess

class UrlListFormatter(FormatterBase):
    """
    This component expects to be linked to a DictFormatter
    """
    def __init__(self):
        super(UrlListFormatter, self).__init__()
        self.results = []
        self.error_404 = None

    def main(self):
        not_done = True
        while not_done:
            while self.dataReady('control'):
                signal = self.recv('control')
                if isinstance(signal, producerFinished):
                    not_done = False

            while self.dataReady('inbox'):
                section, data = self.recv('inbox')
                if section == 'error_404':
                    if data.has_key('regex'):
                        raise ParseException('error_404 cannot contain a regex')
                    data['regex'] = '.*'
                    self.error_404 = self.normalizeDict(data)
                elif section == 'root':
                    data['regex'] = '\|' * 4
                    self.results.append(self.normalizeDict(data))
                else:
                    self.results.append(self.normalizeDict(data))
            if not self.anyReady() and not_done:
                self.pause()

            yield 1
        if not self.error_404:
            raise ParseException('Urls list must contain an error_404 item!')
        self.results.reverse()
        self.results.append(self.error_404)

    def normalizeDict(self, dic):
        ret_val = {}
        for key, value in dic.iteritems():
            if key.find('.') == -1: #only prepend kp. if there isn't already a dot
                ret_val['kp.' + key] = value
            else:
                ret_val[key] = value
        return ret_val
    
def ParseUrlFile(location):
    return ParseConfigFile(location, [DictFormatter(), UrlListFormatter()])
