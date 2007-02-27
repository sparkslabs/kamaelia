#!/usr/bin/env python

class RenderPlaintext(object):
    def __init__(self, debug=False):
        super(RenderPlaintext,self).__init__()
        self.debug=debug

    def heading(self, label, level=4):
        if level == 2: 
            u = "".join(["*" for x in label])
            return "\n"+label + "\n"+ u + "\n"
        if level == 3: return label + "\n"
        if level == 4: return label + ":" + "\n"
        if level == 5: return label + ":"

    def preformat(self, somestring):
        lines = somestring.split("\n")
        L = []
        for l in lines:
            L.append("    "+l+"\n")
        return "".join(L)
    def divider(self):
        return "\n"
    def start(self): return ""
    def stop(self): return ""