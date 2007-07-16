#! /usr/bin/env python

#protocol negotiation
import pickle
import socket
from struct import pack, unpack
from aimUtil import *

fle = open("bos_auth.dat")
BOS_server, port, auth_cookie = pickle.load(fle)
fle.close()

seq = getseqnum()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((BOS_server, port))

### ================== send CLI_COOKIE ========================== ###
protocol_version = 1
protocol_version = chrs(protocol_version, 4)
flap_body = protocol_version
flap_body = appendTLV(0x06, auth_cookie, flap_body)
flap = '*' + channel1 + seq.next() + chrs(len(flap_body), 2) + flap_body

sock.send(flap)

### ============= get supported services from server ============ ###
reply = sock.recv(1000) # this should be the acknowledgement
printHex(reply)
reply = sock.recv(1000) # this should be the "server ready" message
printHex(reply)
fle = open("snac0103.dat", "wb")
pickle.dump(reply, fle)
fle.close()

snac_body = reply[flap_header_len + snac_header_len:]

unit_len = 2
codes_len = len(snac_body)/unit_len
fmt = '>%ih' % codes_len
supported_services_codes = unpack(fmt, snac_body)

snac_body = ""
for code in supported_services_codes:
    if code in desired_service_versions:
        snac_body += Double(code) + Double(desired_service_versions[code])

snac = makeSnac((0x01, 0x17), snac_body)
flap = makeFlap(0x02, seq.next(), snac)

sock.send(flap)

### ============== extract accepted services ================== ###
reply = sock.recv(1000)
printHex(reply)
fle = open("snac0118.dat", "wb")
pickle.dump(reply, fle)
fle.close()

snac_body = reply[flap_header_len + snac_header_len:]
fmt = '!%ih' % (len(snac_body)/2)
snac_body = unpack(fmt, snac_body)
services = snac_body[::2]
versions = snac_body[1::2]
accepted_services = dict(zip(services, versions))

### ============= request rate limits ========================== ###
RATE_LIMITS_REQUEST = 2
snac = makeSnac((0x01, 0x06), "", reqid = RATE_LIMITS_REQUEST)
flap = makeFlap(0x02, seq.next(), snac)
sock.send(flap)

### ================ extract rate limits ======================== ###
reply = sock.recv(1000)
fle = open("snac0107.dat", "wb")
pickle.dump(reply, fle)
fle.close()

snac_body = reply[flap_header_len + snac_header_len:]
num_rate_classes, = unpack('!h', snac_body[0:2])
snac_body = snac_body[2:]
rate_class_len = 2 + 4*8 + 1
rate_classes = snac_body[:num_rate_classes * rate_class_len]
rate_groups = snac_body[num_rate_classes * rate_class_len:]

rgcopy = rate_groups
rate_groups_hash = {}
LEN_PAIR = 4
while len(rgcopy) > 0:
    group_id, npairs = unpack('!hh', rgcopy[0:4])
    rawdata = rgcopy[4:4+npairs*LEN_PAIR]
    group_data = unpackFour(rawdata)
    group_data = zip(group_data[::2], group_data[1::2])    
    rate_groups_hash[group_id] = group_data
    rgcopy = rgcopy[4+group_data_len:]

### =============== send rate limits acknowledged =============== ###
fmt = '!%ih' % len(rate_groups_hash.keys())
snac_body = pack(fmt, *rate_groups_hash.keys())
snac = makeSnac((0x01, 0x08), snac_body)
flap = makeFlap(2, seq.next(), snac)
sock.send(flap)


### set privacy flags
#SNAC (01, 14)


## request personal info
#SNAC (01, 0e)

## service request
#SNAC (01, 04)


### ============== request rights ============================= ###
# we're goint to skip this section right now, because, with the barely
# functioning client this will be, we're not going to use any services


sock.close()
