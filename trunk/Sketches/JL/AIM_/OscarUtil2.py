# -*- coding: utf-8 -*-

# Copyright (c) 2001-2005 Twisted Matrix Laboratories.
# TWISTED LIBRARY
# See LICENSE for details.
#
# Copyright (c) 2001-2006
# Allen Short
# Andrew Bennetts
# Apple Computer, Inc.
# Benjamin Bruheim
# Bob Ippolito
# Canonical Limited
# Christopher Armstrong
# David Reid
# Donovan Preston
# Eric Mangold
# Itamar Shtull-Trauring
# James Knight
# Jason A. Mobarak
# Jonathan Lange
# Jonathan D. Simms
# Jp Calderone
# Jürgen Hermann
# Kevin Turner
# Mary Gardiner
# Matthew Lefkowitz
# Massachusetts Institute of Technology
# Moshe Zadka
# Paul Swartz
# Pavel Pergamenshchik
# Ralph Meijer
# Sean Riley
# Travis B. Hartwell
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
=======================
OSCAR Utility functions
=======================
This file includes functions for dealing with OSCAR datatypes and passwords.

This is the second of two utility modules. OscarUtil is the other. 


Maintainer: U{Paul Swartz<mailto:z3p@twistedmatrix.com>} for Twisted

12 Jul 2007
Modified by Jinna Lei for Kamaelia.
"""

from __future__ import nested_scopes
import struct
import md5

from OscarUtil import *

def SNAC(fam,sub,data,id=1, flags=[0,0]):
    """construct a SNAC from the given data"""
    #the reqid mostly doesn't matter, unless this is a query-response situation 
    return Double(fam) + Double(sub) + Single(flags[0]) + Single(flags[1]) + Quad(id) + data

def readSNAC(data):
    """puts a SNAC off the wire into a slightly more useable form"""
    header="!HHBBL"
    head=[list(struct.unpack(header,data[:10]))]
    return head+[data[10:]]

def TLV(type,value):
    """constructs a TLV based on given data"""
    header="!HH"
    head=struct.pack(header,type,len(value))
    return head+str(value)

def readTLVs(data,count=None):
    """
    takes a string of TLVs and returns a dictionary {TLV type: TLV value}
    Optional keywords:
    - count -- how many TLVs we want to unpack at a time. If count is less than
               the number of TLVs in our string, then we return the dictionary
               plus the remaining TLV string. 
    """
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
    """returns a password hash"""
    m=md5.new()
    m.update(key)
    m.update(md5.new(password).digest())
    m.update("AOL Instant Messenger (SM)")
    return m.digest()

def encryptPasswordICQ(password):
    """
    encrypts passwords the old way, relatively insecure way. Not used very often
    """
    key=[0xF3,0x26,0x81,0xC4,0x39,0x86,0xDB,0x92,0x71,0xA3,0xB9,0xE6,0x53,0x7A,0x95,0x7C]
    bytes=map(ord,password)
    r=""
    for i in range(len(bytes)):
        r=r+chr(bytes[i]^key[i%len(key)])
    return r

