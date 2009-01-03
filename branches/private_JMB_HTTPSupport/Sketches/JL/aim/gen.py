#!/usr/bin/env python
import socket
import md5
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

auth = 'login.oscar.aol.com'
port = 5190
screenname = 'kamaelia1'
password = 'abc123'
AIM_MD5_STRING = "AOL Instant Messenger (SM)"

#* 1
#channelid 1
#seqnum 2
#dataFieldLength 2
#protocolVersion 4

def printHex(stri):
    for char in stri:
        print hex(ord(char)),
    print '\n'

def getseqnum():
    seqnum = 0x00
    while True:
        seqnum = (seqnum+1) & 0xffff
        yield chr(seqnum & 0xff00) + chr(seqnum & 0x00ff)

def chrs(num, width):
    """width is number of characters the resulting string should contain.
    Will return 0 if the num is greater than 2**width."""
    result = ""
    while len(result) < width:
        result = chr(num & 0xff) + result
        num = num >> 8
    return result

##def chrs2int(stri):
##    exponential = 1
##    result = 0
##    for i in range(len(stri)):
##        j = -(i+1)
##        result += ord(stri[j]) * exponential
##        exponential <<= 8
##    return result
        
channel1 = '\x01'
channel2 = '\x02'
channel3 = '\x03'
channel4 = '\x04'
channel5 = '\x05'
seq = getseqnum()

sock.connect((auth, port))

### ============= initial connection =====================###
flap = '*' + channel1 + seq.next() + '\x00\x04' + '\x00\x00\x00\x01'
sock.send(flap)
printHex(sock.recv(1000))

###============ send client key request =====================###
snac_fam = 0x17
snac_sub = 0x06
snac_flags = 0
snac_reqid = 1

tlv_type = 0x01
payload1 = chrs((len(screenname)), 2) + screenname 
payload1 = chrs(tlv_type, 2) + payload1

tlv_type = 0x4b
payload2 = chrs(0, 2)
payload2 = chrs(tlv_type, 2) + payload2

tlv_type = 0x5a
payload3 = chrs(0, 2)
payload3 = chrs(tlv_type, 2) + payload3

payload = payload1 + payload2 + payload3

snac = chrs(snac_fam, 2) + chrs(snac_sub, 2) + chrs(snac_flags, 2) + chrs(snac_reqid, 4) + payload

fieldLen = len(snac)
flap = '*' + channel2 + seq.next() + chrs(fieldLen, 2) + snac
sock.send(flap)

###============ get md5 key ================================###
reply = sock.recv(1000)
printHex(reply) 
md5len = reply[16:18]
md5key = reply[18:]

###=============== send encrypted password ==================###
snac_fam = 0x17
snac_sub = 0x06
snac_flags = 0
snac_reqid = 0x02
snac_body = ""

tlv_type = 0x01
payload = screenname
tlv = chrs(tlv_type, 2) + chrs(len(payload), 2) + payload
snac_body += tlv

tlv_type = 0x03
client_id_string = "KamaeliaAIM/0.01"
payload = client_id_string
tlv = chrs(tlv_type, 2) + chrs(len(payload), 2) + payload
snac_body += tlv

def appendTLV(tlv_type, payload, orig_snac):
    tlv = chrs(tlv_type, 2) + chrs(len(payload), 2) + payload
    return orig_snac + tlv

### Hash password ###
md5obj = md5.new()
md5obj.update(md5key)
md5obj.update(password)
md5obj.update(AIM_MD5_STRING)
password_hash = md5obj.digest()
snac_body = appendTLV(0x25, password_hash, snac_body)


client_id = 0x0109 #???
snac_body = appendTLV(0x16, chrs(client_id, 2), snac_body)
major_version = 0
snac_body = appendTLV(0x17, chrs(major_version, 2), snac_body)
minor_version = 0
snac_body = appendTLV(0x18, chrs(minor_version, 2), snac_body)
lesser_version = 1
snac_body = appendTLV(0x19, chrs(lesser_version, 2), snac_body)
build_num = 0
snac_body = appendTLV(0x1a, chrs(build_num, 2), snac_body)
distr_num = 0
snac_body = appendTLV(0x14, chrs(distr_num, 2), snac_body)
language = 'en'
snac_body = appendTLV(0x0f, language, snac_body)
country = 'us'
snac_body = appendTLV(0x0e, country, snac_body)
ssiflag = 1
snac_body = appendTLV(0x18, chrs(ssiflag, 1), snac_body)

print sock.recv(1000)
sock.close()
