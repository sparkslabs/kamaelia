#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
"""
This module contains the functionality for autoinstall of necessary config files.

FIXME:  Allow user to override the default install location.
"""
import sys, zipfile, os, tarfile

from io import StringIO as cStringIO

import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Apps.JMB.Common.Console import prompt_yesno, info

_logger_suffix = '.web_common.autoinstall'

def autoinstall(zip, dir, app_name):
    """
    This function essentially just takes a tar file from the data file within a
    zip executable and expands it into the users home directory.
    """
    prompt_text = 'It does not appear that %s has been installed.  Would you like to do so now? [y/n]' % \
                  (app_name)
    if not prompt_yesno(prompt_text):
        print ('%s must be installed to continue.  Halting.' % (app_name))
        sys.exit(1)
    
    tar_mem = cStringIO.StringIO( zip.read('data/kpuser.tar') )
    kpuser_file = tarfile.open(name="-", fileobj=tar_mem, mode='r')
    kpuser_file.extractall(path=dir)
    
    kpuser_file.close()
    tar_mem.close()
    
    info('%s is now done installing.' % (app_name), _logger_suffix)
