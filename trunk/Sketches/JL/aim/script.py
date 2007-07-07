#!/usr/bin/env python
# -*- coding: ascii -*-
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

auth = 'login.oscar.aol.com'
port = 5190
protocolVersion = 1
screenname = 'kamaelia1'

def getOrdinals(bstring):
    num = 0
    exponential = 1
    for i in range(len(bstring)):
        j = -(i+1)
        char = bstring[j]
        num = num + ord(char)*exponential
        exponential *= 256
    return num

channel1 = '\x01'
channel2 = '\x02'
channel3 = '\x03'
channel4 = '\x04'
channel5 = '\x05'

sock.connect((auth, port))
seqnum = '\x00\x01'
fieldLen = '\x00\x04'
data = '\x00\x00\x00\x01'
flap = '*' + channel1 + seqnum + fieldLen + data
sock.send(flap)
reply = sock.recv(1000)
print reply
asterisk = reply[0]
serv_channel = reply[1]
serv_seqnum = reply[2:4]
serv_seqnum = getOrdinals(serv_seqnum)
serv_fieldLen = reply[4:6]
serv_fieldLen = getOrdinals(serv_fieldLen)
serv_msg = getOrdinals(reply[6:])
print asterisk, serv_channel, serv_seqnum, serv_fieldLen, serv_msg

flap_header = '*' + '\x02' + '\x00\x02' + '\x00\x23'
fnac = '\x00\x17' + '\x00\x06' + '\x00\x00\x00\x00\x00\x01'
signon = '\x00\x01' + '\x00\x09' + 'kamaelia1'
sock.close()
