#!/usr/bin/env python
#
# (C) 2006 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: RJL

import string

from Axon.Component import component

from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
from Kamaelia.Protocol.HTTP.HTTPParser import splitUri

from Kamaelia.Util.PureTransformer import PureTransformer


def HTMLTag():
    return { "name" : "", "contents": [], "attributes": {} }

def intval(mystring):
    """Convert a string to an integer, representing errors by None"""
    try:
        retval = int(mystring)
    except ValueError:
        retval = None
    return retval
    
class HTMLProcess(component):
    def stateStart(self, c):
        if c == "<":
            contents = "".join(self.temp)
            self.temp = []
            if contents:
                self.tagstack[-1]["contents"].append(contents)
            
            return self.stateTagNameRead
        else:
            self.temp.append(c)
    
    def stateCommentStartA(self, c):
        if c == "-":
            return self.stateCommentStartB
        else:
            return self.stateStart # bad HTML
    
    def stateCommentStartB(self, c):
        if c == "-":
            return self.stateInComment
        else:
            return self.stateStart # bad HTML

    def stateCommentEndA(self, c):
        if c == "-":
            return self.stateCommentEndB
        else:
            return self.stateInComment
            
    def stateCommentEndB(self, c):
        if c == " " or c == "t":
            pass
        elif c == ">":
            return self.stateStart # I'm assuming you can't do <p align=<!--abc-->"test">yo</p>
            
    def stateInComment(self, c):
        if c == "-":
            return self.stateInComment
        else:
            return self.stateStart # ba
            
    def popTag(self):
        self.tagstack.pop(-1)
    
    def stateAttributeValueReadDoubleQuoted(self, c):
        self.temp.append(c)
        if c == '"':
            return self.stateAttributeValueRead
            
    def stateAttributeValueReadSingleQuoted(self, c):
        self.temp.append(c)
        if c == "'":
            return self.stateAttributeValueRead
        
    def stateAttributeValueRead(self, c):
        if c == "'":
            self.temp.append(c)
            return self.stateAttributeValueReadSingleQuoted
            
        elif c == '"':
            self.temp.append(c)
            return self.stateAttributeValueReadDoubleQuoted            
            
        elif c == " " or c == ">" or  c == "/":
            attributevalue = "".join(self.temp)
            self.temp = []
            if attributevalue[:1] == '"' and attributevalue[-1:] == '"':
                attributevalue = attributevalue[1:-1]
            elif attributevalue[:1] == "'" and attributevalue[-1:] == "'":
                attributevalue = attributevalue[1:-1]
            else:
                intattributevalue = intval(attributevalue)
                if intattributevalue:
                    attributevalue = intattributevalue
            
            self.tagstack[-1]["attributes"][self.attributename] = attributevalue
            
            if c == " ":
                return self.stateAttributeNameRead
            elif c == ">":
                return self.stateStart
            elif c == "/":
                return self.stateSelfClosingTag
        else:
            self.temp.append(c)

    def stateSelfClosingTag(self, c):
        if c == ">":
            self.popTag()
            return self.stateStart
        
    def stateAttributeNameRead(self, c):
    
        if c == "=":
            self.attributename = "".join(self.temp).lower()
            self.temp = []
            return self.stateAttributeValueRead
            
        elif c == " " or c == ">" or c == "/": #valueless attribute
            attributename = "".join(self.temp).lower()
            self.temp = []
            if attributename:
                self.tagstack[-1]["attributes"][attributename] = True
            if c == ">":
                return self.stateStart
            elif c == "/":
                return self.stateSelfClosingTag
        else:
            self.temp.append(c)
        
    def stateTerminatorTagNameRead(self, c):
        if c == ">":
            tagname = "".join(self.temp).lower()
            self.temp = []

            while (self.tagstack[-1]["name"] != tagname):
                 # we cannot allow broken pages to pop the root tag
                if len(self.tagstack) == 1:
                    break
                # to cope with badly formatted pages, e.g. those that
                # contain <p>xyz<p>abc when they mean <p>xyz</p><p>abc</p>
                # we pop tags that are implictly closed (by a parent closing)
                self.popTag()

            if len(self.tagstack) > 1:
                self.popTag()
            
            return self.stateStart
        else:
            self.temp.append(c)
    
    def stateTagNameRead(self, c):
        if c == "!" and len(self.temp) == 0:
            return self.stateCommentStartA
        elif (c == " " or c == "/" or c == ">") and self.temp:
            tag = HTMLTag()
            tag["name"] = "".join(self.temp).lower()
            self.temp = []
            self.tagstack[-1]["contents"].append(tag)            
            self.tagstack.append(tag)

            if c == " ":
                return self.stateAttributeNameRead
                
            elif c == "/":
                return self.stateSelfClosingTag
            
            elif c == ">":
                return self.stateStart
        
        elif c == "/": #i.e. at the start
            return self.stateTerminatorTagNameRead
        else:
            self.temp.append(c)
        
    def main(self):
        # could easily be converted to 'streaming' HTML rather than 1 msg per page
        while 1:
            yield 1
            while self.dataReady("inbox"):
                state = self.stateStart
                self.tagstack = [ { "name": "", "contents": [], "attributes":{} } ] # the root tag
                self.temp = [] # not a very efficient way (asmytotically fine but large constant factors) but a simple way
                msg = self.recv("inbox")
                for c in msg:
                    newstate = state(c)
                    if newstate: state = newstate
                self.send(self.tagstack[0], "outbox") # the new HTML tree structure
            self.pause()

class ExtractLinks(PureTransformer):
    def listLinks(self, msg, linklist, norobots):
        if msg["name"] == "meta":
            #print "found a meta"
            if msg["attributes"].get("name", "").lower() == "robots":
                #print "found robots tag"
                splitcontent = msg["attributes"].get("content", "").split(",")
                #print "robots split content = "                
                #print splitcontent
                for part in splitcontent:
                    if part.lower() in ["none", "nofollow"]:
                        norobots = [True]
                        print "NOROBOTS!"
        
        if norobots == [True]:
            return
        
        if msg["name"] == "a":
            link = msg["attributes"].get("href")
            if link:
                linklist.append(link)
        
        for submsg in msg["contents"]:
            if not isinstance(submsg, str):
                self.listLinks(submsg, linklist, norobots)
        
    def processMessage(self, msg):
        norobots = [False]
        #print msg
        linklist = []
        self.listLinks(msg, linklist, norobots)
        if norobots == [False]:
            return linklist

def removeBookmarkBit(link):
    findindex = link.rfind("#")
    if findindex != -1:
        return link[:findindex]
    else:
        return link
        
def correctRelativeLink(link, sourceurl):
    splitsource = splitUri(sourceurl)
    
    link = removeBookmarkBit(link)
    protocolend = link.find("://")
    if protocolend != -1:
        protocol = link[:protocolend - 3].lower()
        if protocol in ["http"]:
            return link
        else:
            return None
    
    elif link[:1] == "/": #absolute for that server
        return "http://" + splitsource["uri-server"] + link
    else:
        endsplit = upDir(splitsource, len(splitsource["raw-uri"]))
        linkstart = 0
        while link[linkstart:linkstart + 1] == ".":
            if link[linkstart:linkstart + 2] == "./":
                linkstart += 2
            elif link[linkstart:linkstart + 3] == "../":
                linkstart += 3
                endsplit = upDir(splitsource, endsplit)
        return "http://" + splitsource["uri-server"] + splitsource["raw-uri"][:endsplit] + "/" + link[linkstart:]

def upDir(splitsource, endsplit):
    return splitsource["raw-uri"].rfind("/", 0, endsplit)
        
class CorrectRelativeLinks(component):
    Inboxes = {
        "links" : "List of URLs",
        "sourceurl" : "The URL of the page those links were extracted from",
        "control" : "Shut me down",
    }
    
    def main(self):
        while 1:
            yield 1
            while self.dataReady("links") and self.dataReady("sourceurl"):
                linkslist = self.recv("links")            
                sourceurl = self.recv("sourceurl")
                
                newlinkslist = []
                
                for link in linkslist:
                    fulllink = correctRelativeLink(link, sourceurl)
                    if fulllink:
                        newlinkslist.append(fulllink)

                self.send(newlinkslist, "outbox")
            
            self.pause()
            
if __name__ == "__main__":
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    from Kamaelia.Util.UnseenOnly import UnseenOnly    
    from Kamaelia.Util.Fanout import fanout
    
    urlprefix = raw_input("URL matching prefix: ") # e.g. "http://www.example.com/" to only download stuff from that domain
    
    def suffixMatchOnly(x):
        if x[:len(urlprefix)] == urlprefix:
            return x
    
    class ListSplit(component):
        def main(self):
            while 1:
                yield 1
                while self.dataReady("inbox"):
                    msg = self.recv("inbox")
                    for m in msg:
                        self.send(m, "outbox")
                self.pause()
    
    Graphline(
        usersuppliedurls = ConsoleReader(eol=""),
        splitter = fanout(["toHTTPClient", "toCorrectRelativeLinks"]),
        splittertwo = fanout(["toSplitterOne", "toEchoer"]),
        newlinesuffixadder = PureTransformer(lambda x : x + "\n"),
        httpclient = SimpleHTTPClient(),
        htmlprocessor = HTMLProcess(),
        linkextractor = ExtractLinks(),
        linkcorrector = CorrectRelativeLinks(),
        listsplitter = ListSplit(),
        prefixmatcher = PureTransformer(suffixMatchOnly),
        newurlechoer = ConsoleEchoer(),
        unseenonly = UnseenOnly(),
        
        linkages = {
            ("usersuppliedurls", "outbox") : ("unseenonly", "inbox"),
            ("newurlechoer", "outbox") : ("splitter", "inbox"),
            
            ("splitter", "toHTTPClient") : ("httpclient", "inbox"),
            ("splitter", "toCorrectRelativeLinks") : ("linkcorrector", "sourceurl"),
            
            ("httpclient", "outbox") : ("htmlprocessor", "inbox"),
            ("htmlprocessor", "outbox") : ("linkextractor", "inbox"),
            ("linkextractor", "outbox") : ("linkcorrector", "links"),
            
            ("linkcorrector", "outbox") : ("listsplitter", "inbox"),
            ("listsplitter", "outbox") : ("prefixmatcher", "inbox"),
            ("prefixmatcher", "outbox") : ("unseenonly", "inbox"),
            ("unseenonly", "outbox"): ("splittertwo", "inbox"),
            
            ("splittertwo", "toSplitterOne") : ("splitter", "inbox"),
            ("splittertwo", "toEchoer") : ("newlinesuffixadder", "inbox"),
            ("newlinesuffixadder", "outbox") : ("newurlechoer", "inbox"),
        }
    ).run()
    """Pipeline(
        ConsoleReader(),
        HTMLProcess(),
        ExtractLinks(),
        ConsoleEchoer()
    ).run()"""
    
    """while 1:
        sourceurl = raw_input("source url: ")
        link = raw_input("link: ")
        print correctRelativeLink(link, sourceurl)"""
