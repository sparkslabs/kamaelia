#!/usr/bin/python

print "You probably want to copy and paste this from the console"

class microprocess(object):
    def __init__(self):
        super(microprocess, self).__init__()
    def main(self):
        yield 1

class printer(microprocess):
    def __init__(self, tag):
        super(printer, self).__init__()
        self.tag = tag
    def main(self):
        while 1:
            yield 1
            print self.tag

X = printer("Something")
G = X.main()
X,G
G.next()
G.next()
X.tag = "Something else"
G.next()
G.next()








