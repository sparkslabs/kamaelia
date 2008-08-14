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
"""
This module contains the functionality for autoinstall of necessary config files.

FIXME:  Allow user to override the default install location.
"""
import sys, zipfile, os, tarfile, cStringIO

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Apps.Web_common.Console import prompt_yesno, info

_logger_suffix = '.web_common.autoinstall'

def autoinstall(zip, dir, app_name):
    """
    This function essentially just takes a tar file from the data file within a
    zip executable and expands it into the users home directory.
    """
    prompt_text = 'It does not appear that %s has been installed.  Would you like to do so now? [y/n]' % \
                  (app_name)
    if not prompt_yesno(prompt_text):
        print '%s must be installed to continue.  Halting.' % (app_name)
        sys.exit(1)
    
    tar_mem = cStringIO.StringIO( zip.read('data/kpuser.tar') )
    kpuser_file = tarfile.open(fileobj=tar_mem, mode='r')
    kpuser_file.extractall(path=dir)
    
    kpuser_file.close()
    tar_mem.close()
    
    info('%s is now done installing.' % (app_name), _logger_suffix)
