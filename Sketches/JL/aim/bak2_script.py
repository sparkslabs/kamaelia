#!/usr/bin/env python

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

auth = 'login.oscar.aol.com'
port = 5190


#* 1
#channelid 1
#seqnum 2
#dataFieldLength 2
#protocolVersion 4

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
print sock.recv(1000)
sock.close()
