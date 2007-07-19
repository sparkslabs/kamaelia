# Copyright (c) 2001-2005 Twisted Matrix Laboratories.
# TWISTED LIBRARY
# See LICENSE for details.


"""An implementation of the OSCAR protocol, which AIM and ICQ use to communcate.

This module is unstable.

Maintainer: U{Paul Swartz<mailto:z3p@twistedmatrix.com>} for Twisted

12 Jul 2007
Modified by Jinna Lei for Kamaelia.
"""

from __future__ import nested_scopes
import struct
import md5
import string
import socket
import random
import time
import types
import re

# Twisted
def SNAC(fam,sub,data,id=1, flags=[0,0]):
    header="!HHBBL"
    head=struct.pack(header,fam,sub,
                     flags[0],flags[1],
                     id)
    return head+str(data)

def readSNAC(data):
    header="!HHBBL"
    head=[list(struct.unpack(header,data[:10]))]
    return head+[data[10:]]

def TLV(type,value):
    header="!HH"
    head=struct.pack(header,type,len(value))
    return head+str(value)

def readTLVs(data,count=None):
    header="!HH"
    dict={}
    while data and len(dict)!=count:
        head=struct.unpack(header,data[:4])
        dict[head[0]]=data[4:4+head[1]]
        data=data[4+head[1]:]
    if not count:
        return dict
    return dict,data

def encryptPasswordMD5(password,key):
    m=md5.new()
    m.update(key)
    m.update(md5.new(password).digest())
    m.update("AOL Instant Messenger (SM)")
    return m.digest()

def encryptPasswordICQ(password):
    key=[0xF3,0x26,0x81,0xC4,0x39,0x86,0xDB,0x92,0x71,0xA3,0xB9,0xE6,0x53,0x7A,0x95,0x7C]
    bytes=map(ord,password)
    r=""
    for i in range(len(bytes)):
        r=r+chr(bytes[i]^key[i%len(key)])
    return r

def FLAP(channel, seqnum, data):
    header="!cBHH"
    head=struct.pack(header,'*', channel, seqnum, len(data))
    return head + data

def readFlap(self, flap):
    header="!cBHH"
    head=struct.unpack(header,flap[:6])
    if len(flap) < (6+head[3]):
        print "flap delivered less than specified length"
        return
    data = flap[6:]
    return (head, data) #return a tuple in the same form they were passed in


def getseqnum():
    seqnum = 0x00
    while True:
        seqnum = (seqnum+1) & 0xffff
        yield chr(seqnum & 0xff00) + chr(seqnum & 0x00ff)

def appendTLV(tlv_type, payload, orig_snac):
    tlv = chrs(tlv_type, 2) + chrs(len(payload), 2) + payload
    return orig_snac + tlv

def chrs(num, width):
    """width is number of characters the resulting string should contain.
    Will return 0 if the num is greater than 2**width."""
    result = ""
    while len(result) < width:
        result = chr(num & 0xff) + result
        num = num >> 8
    return result

channel1 = '\x01'
channel2 = '\x02'
channel3 = '\x03'
channel4 = '\x04'
channel5 = '\x05'

def parseTLVstring(tlvs):
    result = {}
    while len(tlvs) > 0:
        try:
            tlv_type = tlvs[0:2]
            tlv_type = ord(tlv_type[0])*256 + ord(tlv_type[1])
            tlv_len = tlvs[2:4]
            tlv_len = ord(tlv_len[0])*256 + ord(tlv_len[1])
            tlvs = tlvs[4:]
            tlv_body = tlvs[:tlv_len]
            tlvs = tlvs[tlv_len:]
            result[tlv_type] = tlv_body
        except IndexError:
            raise "IndexError! \nresult=%s \ntlvs=%s" % (str(result), tlvs)
    return result

snac_families =  {0x01 : "Generic",
                  0x02 : "Location",
                  0x03 : "Buddy list",
                  0x04 : "Messaging",
                  0x05 : "Advertisements",
                  0x06 : "Invitation",
                  0x07 : "Administrative",
                  0x08 : "Popup",
                  0x09 : "BOS",
                  0x0a : "User lookup",
                  0x0b : "Stats",
                  0x0c : "Translate",
                  0x0d : "Chat navigation",
                  0x0e : "Chat",
                  0x0f : "Directory user search",
                  0x10 : "Server-stored buddy icons",
                  0x13 : "Server-stored information",
                  0x15 : "ICQ",
                  0x17 : "Authorization",
                  0x85 : "Broadcast",
                  }

desired_service_versions = {
    0x01 : 3,
    0x02 : 1,
    0x03 : 1,
    0x04 : 1,
    0x08 : 1,
    0x09 : 1,
    0x0a : 1,
    0x0b : 1,
    0x13 : 4,
    0x15 : 1,
    }

single = '!b'
double = '!h'
quad = '!i'

Single = (lambda num: struct.pack('!b', num))
Double = (lambda num: struct.pack('!h', num))
Quad = (lambda num: struct.pack('!i', num))

def makeSnac((snac_fam, snac_sub), snac_body, flags=0, reqid=1):
    #the reqid mostly doesn't matter, unless this is a query-response situation 
    return Double(snac_fam) + Double(snac_sub) + Double(flags) + Quad(reqid) + snac_body

def makeFlap(channel, seqchars, flap_body):
    return '*' + Single(channel) + seqchars + Double(len(flap_body)) + flap_body

def unpackDoubles(data):
    fmt = '!%iH' % (len(data)/2)
    return struct.unpack(fmt, data)

unpackFour = unpackDoubles
def unpackSingles(data):
    return struct.unpack('!%iB' % len(data), data)

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

#other OSCAR variables
AUTH_SERVER = 'login.oscar.aol.com'
AIM_PORT = 5190
AIM_MD5_STRING = "AOL Instant Messenger (SM)"
FLAP_HEADER_LEN = 1+1+2+2
#* + channel + seqnum + datafieldlen
SNAC_HEADER_LEN = 2+2+2+4
#family + subtype + flags + snacid

CHANNEL1 = 1
CHANNEL2 = 2
CHANNEL3 = 3
CHANNEL4 = 4
CHANNEL5 = 5

