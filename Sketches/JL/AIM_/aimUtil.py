import struct

auth_server = 'login.oscar.aol.com'
port = 5190
AIM_MD5_STRING = "AOL Instant Messenger (SM)"
flap_header_len = 1+1+2+2
#* + channel + seqnum + datafieldlen
snac_header_len = 2+2+2+4
#family + subtype + flags + snacid

def printHex(stri):
    for char in stri:
        print hex(ord(char)),
    print '\n'

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

def unpackFour(stri):
    fmt = '!%ih' % (len(stri)/2)
    return struct.unpack(fmt, stri)

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
