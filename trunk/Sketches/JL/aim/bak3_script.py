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

def printHex(number):
    stri = "%x" % number
    space = False
    for char in stri:
        if space:
            print char + ' ',
        else:
            print char,
        space = not space
    print '\n'

def getseqnum():
    seqnum = 0x00
    while True:
        seqnum = (seqnum+1) % 0xffff
        yield chr(seqnum >> 2) + chr(seqnum % 0xff)
    
channel1 = '\x01'
channel2 = '\x02'
channel3 = '\x03'
channel4 = '\x04'
channel5 = '\x05'
seq = getseqnum()

sock.connect((auth, port))
flap = '*' + channel1 + seq.next() + '\x00\x04' + '\x00\x00\x00\x01'
sock.send(data)
print sock.recv(1000)
sock.close()
