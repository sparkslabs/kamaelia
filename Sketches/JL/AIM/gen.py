#!/usr/bin/env python

import md5
import struct
import pickle
from aimUtil import *
from Axon.ThreadedComponent import threadedcomponent
from Kamaelia.Internet.TCPClient import TCPClient

screenname = 'kamaelia1'
password = 'abc123'
seq = getseqnum()

class AuthCookieGetter(threadedcomponent):
    def main(self):
    ### ============= initial connection =====================###
        flap = '*' + channel1 + seq.next() + '\x00\x04' + '\x00\x00\x00\x01'
        self.send(flap)
        printHex(self.recv())
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
        self.send(flap)
    ###============ get md5 key ================================###
        reply = self.recv()
        printHex(reply) 
        md5len = reply[16:18]
        md5key = reply[18:]
    ###=============== send encrypted password ==================###
        snac_fam = 0x17
        snac_sub = 0x02
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

        ### Hash password ###
        md5obj = md5.new()
        md5obj.update(md5key)
        md5obj.update(password)
        md5obj.update(AIM_MD5_STRING)
        password_hash = md5obj.digest()
        snac_body = appendTLV(0x25, password_hash, snac_body)


        client_id = 0x0109 #this value seems to work
        snac_body = appendTLV(0x16, chrs(client_id, 2), snac_body)

        major_version = 0
        snac_body = appendTLV(0x17, chrs(major_version, 2), snac_body)

        minor_version = 0
        snac_body = appendTLV(0x18, chrs(minor_version, 2), snac_body)

        lesser_version = 1
        snac_body = appendTLV(0x19, chrs(lesser_version, 2), snac_body)

        build_num = 3036
        snac_body = appendTLV(0x1a, chrs(build_num, 2), snac_body)

        distr_num = 0
        snac_body = appendTLV(0x14, chrs(distr_num, 4), snac_body)

        language = 'en'
        snac_body = appendTLV(0x0f, language, snac_body)

        country = 'us'
        snac_body = appendTLV(0x0e, country, snac_body)

        ssiflag = 1
        snac_body = appendTLV(0x4a, chrs(ssiflag, 1), snac_body)

        snac = chrs(snac_fam, 2) + chrs(snac_sub, 2) + chrs(snac_flags, 2) + chrs(snac_reqid, 4) + snac_body
        flap = '*' + channel2 + seq.next() + chrs(len(snac), 2) + snac
        self.send(flap)
        reply = self.recv()
        
        #save data, in case we need it for debugging later
        fle = open("snac1703.dat", "wb")
        pickle.dump(reply, fle)
        fle.close()
    ###================= extract BOS server and auth cookie ========================= ###
        snac_body = reply[flap_header_len+snac_header_len:]
        #parse a string of TLV's, returns a dictionary. tlv_type: tlv_data

        parsed = parseTLVstring(snac_body)
        for p in parsed:
            print p,
            printHex(parsed[p])
            
        BOS_server = parsed[0x05]
        BOS_server, port = BOS_server.split(':')
        port = int(port)
        auth_cookie = parsed[0x06]

        #save for future reference
        fle = open("bos_auth.dat", "wb")
        pickle.dump((BOS_server, port, auth_cookie), fle)
        fle.close()



from Kamaelia.Chassis.Graphline import Graphline

server = auth_server
port = port
Graphline(auth = AuthCookieGetter(),
          tcp = TCPClient(server, port),
          linkages = {("auth", "outbox") : ("tcp", "inbox"),
                      ("tcp", "outbox") : ("auth", "inbox"),
                      }
          ).run()
          
