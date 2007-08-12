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

from oscarUtil import *

def SNAC(fam,sub,data,id=1, flags=[0,0]):
    #the reqid mostly doesn't matter, unless this is a query-response situation 
    return Double(fam) + Double(sub) + Single(flags[0]) + Single(flags[1]) + Quad(id) + data

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

