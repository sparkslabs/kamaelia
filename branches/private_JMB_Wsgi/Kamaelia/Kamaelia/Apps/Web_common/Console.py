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
"""This is just a source file for miscellaneous console IO functions.  There is also
an interface for using python's logging system for console IO."""

import logging

_console_name = 'kamaelia'

def setConsoleName(name):
    """
    This sets the name of the python logger that represents the console.
    """
    _console_name = name

def prompt_yesno(text):
    """
    Just a generic function to determine if the user wants to continue or not.
    Will repeat if input is unrecognizable.
    """
    user_input = raw_input(text)
    
    if user_input[0] == 'y' or user_input[0] == 'Y':
        return True
    elif user_input[0] == 'n' or user_input[0] == 'N':
        return False
    else:
        print 'Unrecognizable input.  Please try again'
        return prompt_yesno(text)
    
def prompt_corrupt(corrupt):
    """This is really just a convenience method for prompt_yesno."""
    print 'The following files appear to be corrupted: \n', corrupt, \
        '\n There may be more corrupted files.'
    if not prompt_yesno('Would you like to continue anyway? [y/n]'):
        print "Halting!"
        sys.exit(1)
        
def debug(msg, suffix='', *args, **argd):
    """Print a debug message to the screen"""
    logging.getLogger(_console_name + suffix).debug(msg, *args, **argd)
    
def info(msg, suffix='', *args, **argd):
    """Print info to the screen"""
    logging.getLogger(_console_name+suffix).info(msg, *args, **argd)
    
def warning(msg, suffix='', *args, **argd):
    """Print a warning to the screen"""
    logging.getLogger(_console_name+suffix).warning(msg, *args, **argd)
    
def error(msg, suffix='', *args, **argd):
    """Print an error to the screen"""
    logging.getLogger(_console_name+suffix).error(msg, *args, **argd)
    
def critical(msg, suffix='', *args, **argd):
    """Print a critical message to the screen."""
    logging.getLogger(_console_name+suffix).critical(msg, *args, **argd)
