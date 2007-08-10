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

Single = (lambda num: struct.pack('!B', num))
Double = (lambda num: struct.pack('!H', num))
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

def printWireshark(text):
    data = unpackSingles(text)
    data = ("00 "*12 + "%02x " * len(data)) % data
    while len(data) > (3*16):
        print data[:3*8], ' ', data[3*8:3*16]
        data = data[3*16:]
    print data[:3*8],
    if len(data) > 3*8:
        print ' ',data[3*8:]
    
class selfClass(object):
    def sendSnac(self,fam, sub, text):
        snac = SNAC(fam, sub, text)
        printWireshark(snac)



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

CLIENT_ID_STRING = "Kamaelia/AIM"
CHANNEL_NEWCONNECTION = 1
CHANNEL_SNAC = 2
CHANNEL_FLAPERROR = 3
CHANNEL_CLOSECONNECTION = 4
CHANNEL_KEEPALIVE = 5
LEN_RATE_CLASS = 2 + 8*4 + 1
