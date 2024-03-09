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
    user_input = input(text)
    
    if user_input[0] == 'y' or user_input[0] == 'Y':
        return True
    elif user_input[0] == 'n' or user_input[0] == 'N':
        return False
    else:
        print ('Unrecognizable input.  Please try again')
        return prompt_yesno(text)
    
def prompt_corrupt(corrupt):
    """This is really just a convenience method for prompt_yesno."""
    print ('The following files appear to be corrupted: \n', corrupt, \
        '\n There may be more corrupted files.')
    if not prompt_yesno('Would you like to continue anyway? [y/n]'):
        print ("Halting!")
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
