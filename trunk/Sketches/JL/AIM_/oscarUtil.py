import struct

Single = (lambda num: struct.pack('!B', num))
Double = (lambda num: struct.pack('!H', num))
Quad = (lambda num: struct.pack('!i', num))

def unpackDoubles(data):
    fmt = '!%iH' % (len(data)/2)
    return struct.unpack(fmt, data)

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

#status constants
STATUS_MISC_WEBAWARE = 0x0001
STATUS_MISC_SHOWIP = 0x0002
STATUS_MISC_BIRTHDAY = 0x0008
STATUS_MISC_WEBFRONT = 0x0020
STATUS_MISC_DCDISABLED = 0x0100
STATUS_MISC_DCAUTH = 0x1000
STATUS_MISC_DCCONT = 0x2000

STATUS_ONLINE = 0x0000
STATUS_AWAY = 0x0001
STATUS_DND = 0x0002
STATUS_NA = 0x0004
STATUS_OCCUPIED = 0x0010
STATUS_FREE4CHAT = 0x0020
STATUS_INVISIBLE = 0x0100


#other OSCAR variables
AUTH_SERVER = 'login.oscar.aol.com'
AIM_PORT = 5190
AIM_MD5_STRING = "AOL Instant Messenger (SM)"

CLIENT_ID_STRING = "Kamaelia/AIM"
CHANNEL_NEWCONNECTION = 1
CHANNEL_SNAC = 2
CHANNEL_FLAPERROR = 3
CHANNEL_CLOSECONNECTION = 4
CHANNEL_KEEPALIVE = 5

#lengths
RATE_CLASS_LEN = 2 + 8*4 + 1
FLAP_HEADER_LEN = 6
