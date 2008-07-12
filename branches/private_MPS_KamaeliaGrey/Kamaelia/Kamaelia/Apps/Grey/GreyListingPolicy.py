
#
# This component focuses on the core Greylisting semantics. This is intended
# to be used as a protocol handler in a ServerCore instance.
#

import anydbm
import math
import time
from Kamaelia.Apps.Grey.ConcreteMailHandler import ConcreteMailHandler

class GreyListingPolicy(ConcreteMailHandler):
    allowed_senders = [] # List of senders
    allowed_sender_nets = [] # Only class A,B, C network style networks at present (ie IP prefixes)
    allowed_domains = [ ] # list of IPs

    def sentFromAllowedIPAddress(self):
        if self.peer in self.allowed_senders:
            return True
        return False

    def sentFromAllowedNetwork(self):
        for network_prefix in self.allowed_sender_nets:
            if self.peer[:len(network_prefix)] == network_prefix:
                return True
        return False

    def sentToADomainWeForwardFor(self):
        for recipient in self.recipients:
            recipient = recipient.replace("<", "")
            recipient = recipient.replace(">", "")
            try:
                domain = recipient[recipient.find("@")+1:]
                domain = domain.lower()
                if not (domain in self.allowed_domains):
                    return False
            except:
                raise
                return False # don't care why it fails if it fails
        return True # Only reach here if all domains in allowed_domains

    def isGreylisted(self, recipient):
        max_grey = 3000000
        too_soon = 180
        min_defer_time = 3600
        max_defer_time = 25000

        IP = self.peer
        sender = self.sender
        def _isGreylisted(greylist, seen, IP,sender,recipient):
            # If greylisted, and not been there too long, allow through
            if greylist.get(triplet,None) is not None:
                greytime = float(greylist[triplet])
                if (time.time() - greytime) > max_grey:
                    del greylist[triplet]
                    try:
                        del seen[triplet]
                    except KeyError:
                        # We don't care if it's already gone
                        pass
                    # REFUSED: grey too long
                else:
                    # ACCEPTED: already grey (have reset greytime)
                    greylist[triplet] = str(time.time())
                    return True

            # If not seen this triplet before, defer and note triplet
            if seen.get( triplet, None) is None:
                seen[triplet] = str(time.time())
                return False

            # If triplet retrying waaay too soon, reset their timer & defer
            last_tried = float(seen[triplet])
            if (time.time() - last_tried) < too_soon:
                seen[triplet] = str(time.time())
                return False

            # If triplet retrying too soon generally speaking just defer
            if (time.time() - last_tried) < min_defer_time :
                return False

            # If triplet hasn't been seen in aaaages, defer
            if (time.time() - last_tried) > max_defer_time :
                seen[triplet] = str(time.time())
                return False

            # Otherwise, allow through & greylist then
            greylist[triplet] = str(time.time())
            return True

        greylist = anydbm.open("greylisted.dbm","c")
        seen = anydbm.open("attempters.dbm","c")
        triplet = repr((IP,sender,recipient))
        result = _isGreylisted(greylist, seen, IP,sender,recipient)
        seen.close()
        greylist.close()
        return result

    def whiteListed(self, recipient):
        for (IP, sender, r) in self.whitelisted_triples:
            if self.peer == IP:
                if self.sender == sender:
                    if recipient == r:
                        return True
        for (remotename, network_prefix, r) in self.whitelisted_nonstandard_triples:
            if remotename == self.remotename:
                if self.peer[:len(network_prefix)] == network_prefix:
                    if r == recipient:
                        return True
        return False

    def shouldWeAcceptMail(self):
        if self.sentFromAllowedIPAddress():  return True # Allowed hosts can always send to anywhere through us
        if self.sentFromAllowedNetwork():    return True # People on truste networks can always do the same
        if self.sentToADomainWeForwardFor():
            try:
                for recipient in self.recipients:
                    if self.whiteListed(recipient):
                        return True
                    if not self.isGreylisted(recipient):
                        return False
            except Exception, e:
                # print "Whoops", e
                pass
            return True # Anyone can always send to hosts we own

        return False

    def logResult(self):
        def m(x, w=2):
            return "0"*(w-len(str(x)))+str(x)
        now = time.time()
        msec = int((now -math.floor(now))*1000)
        x= time.gmtime(now)
        stamp =  "".join([ str(z) for z in [ m(x.tm_year,4), m(x.tm_mon,2), m(x.tm_mday,2), m(x.tm_hour,2), m(x.tm_min,2), m(x.tm_sec,2), ".", m(msec,3) ] ])

        logline  = str(stamp) + " | "
        logline += str(self.remotename) + " | "
        logline += str(self.peer) + " | "
        logline += str(self.sender) + " | "
        logline += str(", ".join(self.recipients)) + " | "
        logline += str(self.mailStatus) + " | "

        self.noteToLog(logline)
        # print logline












