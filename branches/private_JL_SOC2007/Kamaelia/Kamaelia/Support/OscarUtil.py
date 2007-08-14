##
## (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
##     All Rights Reserved.
##
## You may only modify and redistribute this under the terms of any of the
## following licenses(2): Mozilla Public License, V1.1, GNU General
## Public License, V2.0, GNU Lesser General Public License, V2.1
##
## (1) Kamaelia Contributors are listed in the AUTHORS file and at
##     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
##     not this notice.
## (2) Reproduced in the COPYING file, and at:
##     http://kamaelia.sourceforge.net/COPYING
## Under section 3.5 of the MPL, we are using this text since we deem the MPL
## notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
## notice is prohibited.
##
## Please contact us via: kamaelia-list-owner@lists.sourceforge.net
## to discuss alternative licensing.
## -------------------------------------------------------------------------
"""
=======================
OSCAR Utility functions
=======================
This file includes functions for packing and unpacking binary data and defines
some constants useful for dealing with OSCAR.

This is the first of two utility modules. OscarUtil2 is the other. Most AIM
code requires both this module and OscarUtil2. 

Credit goes to Alexandr Shutko for errorCodes dictionary (and for writing an
excellent guide on the OSCAR protocol). You can find the original table at
`this page <http://iserverd.khstu.ru/oscar/auth_failed.html>`_.
"""
import struct

def Single(num):
    """convenience method for "struct.pack('!B', num')" """
    return struct.pack('!B', num)

def Double(num):
    """convenience method for "struct.pack('!H, num')" """
    return struct.pack('!H', num)

def Quad(num):
    """convenience method for "struct.pack('!Q', num')" """
    return struct.pack('!i', num)

def unpackDoubles(data):
    """convenience method for "struct.unpack('!%iH' % (len(data)/2), data)" """
    fmt = '!%iH' % (len(data)/2)
    return struct.unpack(fmt, data)

def unpackSingles(data):
    """convenience method for "struct.unpack('!%iB' % len(data), data)" """
    return struct.unpack('!%iB' % len(data), data)

def printWireshark(text):
    """prints a string of binary data in Wireshark format."""
    data = unpackSingles(text)
    data = ("00 "*12 + "%02x " * len(data)) % data
    while len(data) > (3*16):
        print data[:3*8], ' ', data[3*8:3*16]
        data = data[3*16:]
    print data[:3*8],
    if len(data) > 3*8:
        print ' ',data[3*8:]
    
class selfClass(object):
    """
    selfClass() -> selfClass object.

    Calling selfClass.sendSnac(fam, sub, binaryData) causes the corresponding
    SNAC to be printed in Wireshark format. Used to debug AIM component methods.
    """
    def sendSnac(self,fam, sub, text):
        """constructs the SNAC and prints resulting binary data like a Wireshark
        packet dump."""
        snac = SNAC(fam, sub, text)
        printWireshark(snac)

errorCodes = {0x0001 :   'Invalid nick or password',
              0x0002 :	  'Service temporarily unavailable',
              0x0003 :	  'All other errors',
              0x0004 :	  'Incorrect nick or password, re-enter',
              0x0005 :	  'Mismatch nick or password, re-enter',
              0x0006 :	  'Internal client error (bad input to authorizer)',
              0x0007 :	  'Invalid account',
              0x0008 :	  'Deleted account',
              0x0009 :	  'Expired account',
              0x000A :	  'No access to database',
              0x000B :	  'No access to resolver',
              0x000C :	  'Invalid database fields',
              0x000D :	  'Bad database status',
              0x000E :	  'Bad resolver status',
              0x000F :	  'Internal error',
              0x0010 :	  'Service temporarily offline',
              0x0011 :	  'Suspended account',
              0x0012 :	  'DB send error',
              0x0013 :	  'DB link error',
              0x0014 :	  'Reservation map error',
              0x0015 :	  'Reservation link error',
              0x0016 :	  'The users num connected from this IP has reached the maximum',
              0x0017 :	  'The users num connected from this IP has reached the maximum (reservation)',
              0x0018 :	  'Rate limit exceeded (reservation). Please try to reconnect in a few minutes',
              0x0019 :	  'User too heavily warned',
              0x001A :	  'Reservation timeout',
              0x001B :	  'You are using an older version of ICQ. Upgrade required',
              0x001C :	  'You are using an older version of ICQ. Upgrade recommended',
              0x001D :	  'Rate limit exceeded. Please try to reconnect in a few minutes',
              0x001E :	  'Can\'t register on the ICQ network. Reconnect in a few minutes',
              0x0020 :	  'Invalid SecurID',
              0x0022 :	  'Account suspended because of your age (age < 13)',
              }

def readTLV08(tlvdata):
    """returns tuple ("error", error message) when given TLV 0x08"""
    code, = struct.unpack("!H", tlvdata)
    return ("error", errorCodes[code])
    
"""Lots of constants defined below"""
#How many bytes (2 ASCII chars) each variable is
RATE_ID_WIDTH = 2
RATE_WINSIZE_WIDTH = 4
RATE_CLEAR_WIDTH = 4
RATE_ALERT_WIDTH = 4
RATE_LIMIT_WIDTH = 4
RATE_DISCONNECT_WIDTH = 4
RATE_CURRENT_WIDTH = 4
RATE_MAX_WIDTH = 4
RATE_LASTTIME_WIDTH = 4
RATE_CURRENTSTATE_WIDTH = 1

#status constants
STATUS_MISC_WEBAWARE = 0x0001
STATUS_MISC_SHOWIP = 0x0002
STATUS_MISC_BIRTHDAY = 0x0008
STATUS_MISC_WEBFRONT = 0x0020
STATUS_MISC_DCDISABLED = 0x0100
STATUS_MISC_DCAUTH = 0x1000
STATUS_MISC_DCCONT = 0x2000

STATUS_ONLINE = 0x0000
STATUS_AWAY = 0x0001
STATUS_DND = 0x0002
STATUS_NA = 0x0004
STATUS_OCCUPIED = 0x0010
STATUS_FREE4CHAT = 0x0020
STATUS_INVISIBLE = 0x0100


#other OSCAR variables
AUTH_SERVER = 'login.oscar.aol.com'
AIM_PORT = 5190
AIM_MD5_STRING = "AOL Instant Messenger (SM)"

CLIENT_ID_STRING = "Kamaelia/AIM"
CHANNEL_NEWCONNECTION = 1
CHANNEL_SNAC = 2
CHANNEL_FLAPERROR = 3
CHANNEL_CLOSECONNECTION = 4
CHANNEL_KEEPALIVE = 5

#lengths
RATE_CLASS_LEN = 2 + 8*4 + 1
FLAP_HEADER_LEN = 6
